"""Validate the repository skill catalog and Codex preflight configuration."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path


FRONTMATTER = re.compile(r"\A---\s*\n(?P<header>.*?)\n---\s*\n", re.DOTALL)
FIELD = re.compile(r"^(?P<key>[a-zA-Z0-9_-]+):\s*(?P<value>.*)$")
REFERENCE = re.compile(r"(?P<target>(?:\.\./)*references/[A-Za-z0-9._/-]+\.md)")
EXPECTED_HOOK_EVENTS = {"SessionStart", "UserPromptSubmit", "SubagentStart"}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[4]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(text)
    if not match:
        raise ValueError("frontmatter YAML manquant ou non fermé")

    fields: dict[str, str] = {}
    for raw_line in match.group("header").splitlines():
        field = FIELD.match(raw_line)
        if not field:
            continue
        value = field.group("value").strip().strip("\"'")
        fields[field.group("key")] = value
    return fields


def validate_skill_references(skill_file: Path, repo: Path) -> list[str]:
    errors: list[str] = []
    skill_root = skill_file.parent.resolve()
    shared_references_root = (repo / ".agents" / "references").resolve()
    label = skill_file.relative_to(repo)

    if skill_file.is_symlink():
        return [f"{label}: SKILL.md ne doit pas être un symlink"]

    text = skill_file.read_text(encoding="utf-8")
    for target in sorted({match.group("target") for match in REFERENCE.finditer(text)}):
        raw_path = skill_file.parent / Path(target)
        try:
            resolved = raw_path.resolve(strict=True)
        except OSError:
            errors.append(f"{label}: référence absente {target}")
            continue

        if not (
            resolved.is_relative_to(skill_root)
            or resolved.is_relative_to(shared_references_root)
        ):
            errors.append(f"{label}: référence hors du skill ou des références partagées {target}")
        elif not resolved.is_file():
            errors.append(f"{label}: référence non fichier {target}")

    return errors


def validate(repo: Path) -> list[str]:
    errors: list[str] = []
    skills_root = repo / ".agents" / "skills"
    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    names: dict[str, Path] = {}

    if not skill_files:
        errors.append("aucun skill repo-scoped trouvé")

    for skill_file in skill_files:
        try:
            fields = parse_frontmatter(skill_file)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"{skill_file.relative_to(repo)}: {exc}")
            continue

        name = fields.get("name", "")
        description = fields.get("description", "")
        if not name:
            errors.append(f"{skill_file.relative_to(repo)}: champ name manquant")
        elif name != skill_file.parent.name:
            errors.append(
                f"{skill_file.relative_to(repo)}: name={name!r} différent du dossier"
            )
        elif name in names:
            errors.append(
                f"nom de skill dupliqué {name!r}: "
                f"{names[name].relative_to(repo)} et {skill_file.relative_to(repo)}"
            )
        else:
            names[name] = skill_file
        if not description:
            errors.append(f"{skill_file.relative_to(repo)}: description manquante")
        try:
            errors.extend(validate_skill_references(skill_file, repo))
        except (OSError, UnicodeError) as exc:
            errors.append(f"{skill_file.relative_to(repo)}: références illisibles: {exc}")

    if "skill-gate" not in names:
        errors.append("skill-gate absent du catalogue local")

    agents_file = repo / "AGENTS.md"
    config_file = repo / ".codex" / "config.toml"
    hooks_file = repo / ".codex" / "hooks.json"
    injector_file = repo / ".codex" / "hooks" / "inject_skill_gate.py"
    manifest_file = skills_root / "skill-gate" / "agents" / "openai.yaml"

    try:
        config = tomllib.loads(config_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        errors.append(f".codex/config.toml invalide: {exc}")
        config = {}

    max_bytes = config.get("project_doc_max_bytes")
    if not isinstance(max_bytes, int) or max_bytes <= 0:
        errors.append("project_doc_max_bytes doit être un entier positif")
    elif agents_file.exists() and agents_file.stat().st_size > max_bytes:
        errors.append(
            f"AGENTS.md dépasse project_doc_max_bytes: "
            f"{agents_file.stat().st_size} > {max_bytes}"
        )

    features = config.get("features", {})
    skills_config = config.get("skills", {})
    if not isinstance(features, dict) or features.get("hooks") is not True:
        errors.append("features.hooks doit être true")
    if not isinstance(skills_config, dict) or skills_config.get("max_context_tokens") != 10000:
        errors.append("skills.max_context_tokens doit valoir 10000")

    try:
        hooks = json.loads(hooks_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f".codex/hooks.json invalide: {exc}")
        hooks = {}

    hook_map = hooks.get("hooks", {}) if isinstance(hooks, dict) else {}
    if not isinstance(hook_map, dict):
        errors.append(".codex/hooks.json: hooks doit être un objet")
        hook_map = {}

    configured_events = set(hook_map)
    missing_events = EXPECTED_HOOK_EVENTS - configured_events
    if missing_events:
        errors.append(f"hooks obligatoires absents: {sorted(missing_events)}")

    for event in EXPECTED_HOOK_EVENTS & configured_events:
        groups = hook_map.get(event)
        if not isinstance(groups, list) or not groups:
            errors.append(f"hook {event}: aucun groupe configuré")
            continue
        handlers = [
            handler
            for group in groups
            if isinstance(group, dict)
            for handler in group.get("hooks", [])
            if isinstance(handler, dict)
        ]
        if not any("inject_skill_gate.py" in str(item.get("command", "")) for item in handlers):
            errors.append(f"hook {event}: inject_skill_gate.py non appelé")
        if not any(
            "inject_skill_gate.py" in str(item.get("commandWindows", ""))
            for item in handlers
        ):
            errors.append(f"hook {event}: commande Windows absente")

    for required in (injector_file, manifest_file):
        if not required.is_file():
            errors.append(f"fichier requis absent: {required.relative_to(repo)}")

    if manifest_file.is_file():
        try:
            manifest = manifest_file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"manifest skill-gate illisible: {exc}")
        else:
            if not re.search(r"^\s*allow_implicit_invocation:\s*true\s*$", manifest, re.MULTILINE):
                errors.append("manifest skill-gate: invocation implicite non activée")
            if not re.search(r"^\s*-\s*CODEX\s*$", manifest, re.MULTILINE):
                errors.append("manifest skill-gate: produit CODEX absent")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=repository_root())
    args = parser.parse_args()
    repo = args.repo.resolve()
    errors = validate(repo)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    skill_count = len(list((repo / ".agents" / "skills").glob("*/SKILL.md")))
    print(f"OK: {skill_count} skills, configuration statique et injections validées")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
