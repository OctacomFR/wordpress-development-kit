"""Validate the repository skill catalog and Codex preflight configuration."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote, urlsplit


FRONTMATTER = re.compile(r"\A---\s*\n(?P<header>.*?)\n---\s*\n", re.DOTALL)
FIELD = re.compile(r"^(?P<key>[a-zA-Z0-9_-]+):\s*(?P<value>.*)$")
REFERENCE = re.compile(r"(?<![A-Za-z0-9_./\\-])(?P<target>(?:\.\./)*references/[A-Za-z0-9._/-]+\.md)")
MARKDOWN_LINK = re.compile(r"\[[^\]\n]*\]\(<?(?P<target>[^\s)<>]+)>?[^)]*\)")
UNIX_HOOK_COMMAND = re.compile(
    r'python3?\s+"\$\(git rev-parse --show-toplevel\)/\.codex/hooks/(?P<script>[a-zA-Z0-9_-]+\.py)"'
)
WINDOWS_HOOK_COMMAND = re.compile(
    r'''powershell\.exe -NoProfile -ExecutionPolicy Bypass -Command "python '''
    r'''\(Join-Path \(git rev-parse --show-toplevel\) '\.codex/hooks/(?P<script>[a-zA-Z0-9_-]+\.py)'\)"'''
)
INJECTION_EVENTS = {"SessionStart", "UserPromptSubmit", "SubagentStart"}
TOOL_GATE_EVENTS = {"UserPromptSubmit", "PostToolUse", "Stop"}
OXYGEN_GATE_EVENTS = {"PreToolUse", "PostToolUse"}
EXPECTED_HOOK_EVENTS = INJECTION_EVENTS | TOOL_GATE_EVENTS | OXYGEN_GATE_EVENTS


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

    pending = [skill_file]
    visited: set[Path] = set()
    while pending:
        source = pending.pop()
        if source.resolve() in visited:
            continue
        visited.add(source.resolve())
        text = source.read_text(encoding="utf-8")
        targets = {match.group("target") for match in REFERENCE.finditer(text)}
        targets.update(match.group("target") for match in MARKDOWN_LINK.finditer(text))
        for target in sorted(targets):
            url = urlsplit(target)
            if url.netloc or url.scheme in {"http", "https", "mailto"}:
                continue
            if url.scheme:
                errors.append(f"{source.relative_to(repo)}: référence hors du skill ou des références partagées {target}")
                continue
            path = unquote(url.path)
            if not path.endswith(".md"):
                continue
            raw_path = source.parent / path
            resolved = raw_path.resolve()
            source_label = source.relative_to(repo)
            if not (
                resolved.is_relative_to(skill_root)
                or resolved.is_relative_to(shared_references_root)
            ):
                errors.append(f"{source_label}: référence hors du skill ou des références partagées {target}")
            elif not resolved.is_file():
                errors.append(f"{source_label}: référence absente {target}")
            else:
                pending.append(raw_path)

    return errors


def oxygen_mutations(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "MUTATIONS" for target in node.targets
        ):
            value = node.value
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "frozenset":
                mutations = ast.literal_eval(value.args[0])
                if isinstance(mutations, set) and all(isinstance(item, str) for item in mutations):
                    return mutations
    raise ValueError("liste MUTATIONS littérale absente du contrôle Oxygen")


def validate_hooks(hook_map: dict, repo: Path, mutations: set[str]) -> list[str]:
    errors: list[str] = []
    configured: dict[str, list[tuple[str | None, str]]] = {}
    for event, groups in hook_map.items():
        if not isinstance(groups, list) or not groups:
            errors.append(f"hook {event}: aucun groupe configuré")
            continue
        for group in groups:
            if not isinstance(group, dict):
                errors.append(f"hook {event}: groupe invalide")
                continue
            matcher = group.get("matcher")
            if matcher is not None:
                try:
                    if not isinstance(matcher, str):
                        raise TypeError
                    re.compile(matcher)
                except (TypeError, re.error):
                    errors.append(f"hook {event}: matcher invalide")
                    continue
            if event in {"UserPromptSubmit", "SubagentStart", "Stop"} and matcher not in {None, "", ".*"}:
                errors.append(f"hook {event}: matcher global restrictif")
            handlers = group.get("hooks")
            if not isinstance(handlers, list) or not handlers:
                errors.append(f"hook {event}: aucun handler configuré")
                continue
            for handler in handlers:
                if not isinstance(handler, dict):
                    errors.append(f"hook {event}: handler invalide")
                    continue
                if handler.get("type") != "command":
                    errors.append(f"hook {event}: type doit être command")
                timeout = handler.get("timeout")
                if type(timeout) is not int or not 1 <= timeout <= 60:
                    errors.append(f"hook {event}: timeout doit être un entier de 1 à 60 secondes")
                scripts = []
                for field, pattern in (("command", UNIX_HOOK_COMMAND), ("commandWindows", WINDOWS_HOOK_COMMAND)):
                    command = handler.get(field)
                    match = pattern.fullmatch(command) if isinstance(command, str) else None
                    if match is None:
                        errors.append(f"hook {event}: {field} doit appeler directement un script Python de .codex/hooks")
                    else:
                        scripts.append(match["script"])
                        if not (repo / ".codex" / "hooks" / match["script"]).is_file():
                            errors.append(f"hook {event}: script absent {match['script']}")
                if len(scripts) == 2:
                    if scripts[0] != scripts[1]:
                        errors.append(f"hook {event}: commandes Unix et Windows ciblent des scripts différents")
                    else:
                        configured.setdefault(event, []).append((matcher, scripts[0]))

    for event in EXPECTED_HOOK_EVENTS:
        required: dict[str, list[str]] = {}
        if event in INJECTION_EVENTS:
            required["inject_skill_gate.py"] = (
                ["startup", "resume", "clear", "compact"] if event == "SessionStart" else [""]
            )
        if event in TOOL_GATE_EVENTS:
            required["tool_use_gate.py"] = [""]
        if event in OXYGEN_GATE_EVENTS:
            operations = mutations if event == "PreToolUse" else {"oxygen_site_info"}
            required["oxygen_site_gate.py"] = [f"mcp__site__{operation}" for operation in sorted(operations)]
        for script, samples in required.items():
            handlers = [(matcher, name) for matcher, name in configured.get(event, []) if name == script]
            if script == "tool_use_gate.py" and event == "PostToolUse":
                covered = any(matcher in {None, "", ".*"} for matcher, _ in handlers)
            else:
                covered = all(any(matcher in {None, ""} or re.search(matcher, sample)
                                  for matcher, _ in handlers) for sample in samples)
            if not covered:
                errors.append(f"hook {event}: commande ou couverture requise absente pour {script}")
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
    tool_gate_file = repo / ".codex" / "hooks" / "tool_use_gate.py"
    oxygen_gate_file = repo / ".codex" / "hooks" / "oxygen_site_gate.py"
    manifest_file = skills_root / "skill-gate" / "agents" / "openai.yaml"

    if not agents_file.is_file():
        errors.append("fichier requis absent: AGENTS.md")

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

    try:
        mutations = oxygen_mutations(oxygen_gate_file)
    except (OSError, UnicodeError, ValueError, SyntaxError, IndexError) as exc:
        errors.append(f"contrôle Oxygen invalide: {exc}")
        mutations = set()
    errors.extend(validate_hooks(hook_map, repo, mutations))

    for required in (injector_file, tool_gate_file, oxygen_gate_file, manifest_file):
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
