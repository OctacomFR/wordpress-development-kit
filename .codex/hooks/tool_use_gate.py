"""Ask Codex to continue an action turn if no local tool ran."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import sys
import tempfile
import unicodedata
from pathlib import Path

from mission_guard import finish_unobserved_attempts


ACTION = re.compile(
    r"\b(?:fais|faites|modifie|modifiez|corrige|corrigez|cree|creez|construis|"
    r"construisez|implemente|implementez|audite|auditez|analyse|analysez|"
    r"inspecte|inspectez|verifie|verifiez|teste|testez|deploie|deploiez|"
    r"installe|installez|configure|configurez|utilise|utilisez|"
    r"build|edit|fix|create|implement|audit|analyze|inspect|verify|test|"
    r"deploy|install|configure|use)\b"
)
QUESTION = re.compile(r"^\s*(?:comment|pourquoi|how|why|what|explique|explain|decris|describe)\b")
STATE_ROOT = Path(tempfile.gettempdir()) / "octacom-codex-tool-gate"


def needs_tools(prompt: str) -> bool:
    plain = "".join(
        char for char in unicodedata.normalize("NFKD", prompt.casefold())
        if not unicodedata.combining(char)
    )
    return not QUESTION.search(plain) and bool(ACTION.search(plain))


def state_paths(event: dict, root: Path) -> tuple[Path, Path] | None:
    session_id = event.get("session_id")
    turn_id = event.get("turn_id")
    cwd = event.get("cwd")
    if not all(isinstance(value, str) and value for value in (session_id, turn_id, cwd)):
        return None
    digest = hashlib.sha256(
        json.dumps([cwd, session_id, turn_id], separators=(",", ":")).encode()
    ).hexdigest()
    return root / f"{digest}.required", root / f"{digest}.used"


def handle(event: dict, root: Path = STATE_ROOT) -> dict:
    finish_unobserved_attempts(event)
    paths = state_paths(event, root)
    if paths is None:
        return {}
    required, used = paths
    kind = event.get("hook_event_name")

    if kind == "UserPromptSubmit":
        prompt = event.get("prompt")
        if isinstance(prompt, str) and needs_tools(prompt):
            root.mkdir(parents=True, exist_ok=True)
            required.touch()
        return {}

    if kind == "PostToolUse":
        tool = event.get("tool_name")
        if required.exists() and isinstance(tool, str) and tool not in {"Agent", "update_plan"}:
            used.touch()
        return {}

    if kind == "Stop" and required.exists():
        if used.exists():
            required.unlink(missing_ok=True)
            used.unlink(missing_ok=True)
        elif not event.get("stop_hook_active", False):
            return {
                "decision": "block",
                "reason": (
                    "Cette demande exige une action ou une vérification. Utilise l'outil Codex ou MCP "
                    "pertinent, et lis les skills applicables avant de conclure. Si la capacité manque, "
                    "indique précisément le blocage sans prétendre avoir vérifié."
                ),
            }
        else:
            required.unlink(missing_ok=True)
            return {"systemMessage": "Aucun appel d'outil local observé après la relance."}
    return {}


def main() -> int:
    try:
        event = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        result = handle(event)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, sqlite3.Error) as exc:
        result = {"systemMessage": f"Contrôle d'usage des outils indisponible : {type(exc).__name__}"}
    sys.stdout.buffer.write(json.dumps(result, ensure_ascii=True).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
