"""Inject the repository skill preflight policy into Codex turns and subagents."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


POLICY = (
    "SKILL PREFLIGHT REQUIRED: read skill-gate and only the applicable skills and "
    "mandatory references before this work unit. Confirm scope, permissions, blockers "
    "and evidence; recheck when the unit changes. Use Codex/MCP tools when the task "
    "needs real state. Missing required information blocks dependent writes. "
    "A subagent performs its own preflight. Hooks are reminders, not proof.\n"
)


def main() -> int:
    # Codex provides hook metadata on stdin. The policy is deliberately static so
    # user-controlled prompt text is never copied into privileged instructions.
    raw = sys.stdin.read()
    observed = ""
    try:
        event = json.loads(raw)
        cwd = Path(event.get("cwd", ""))
        session = event.get("session_id")
        if cwd.is_absolute() and isinstance(session, str) and session:
            sys.path.insert(0, str(Path(__file__).parent))
            from mission_guard import finish_unobserved_attempts, local_root
            if event.get("hook_event_name") == "SessionStart":
                finish_unobserved_attempts(event)
            source_files = [cwd / "AGENTS.md", cwd / ".agents/skills/skill-gate/SKILL.md", cwd / ".codex/hooks.json"]
            hashes = {str(p.relative_to(cwd)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}
            kit_digest = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
            folder = local_root(cwd) / "runtime"
            folder.mkdir(exist_ok=True)
            receipt = folder / (hashlib.sha256(session.encode()).hexdigest() + ".json")
            data = {"session_id": session, "hook_event": event.get("hook_event_name"), "observed_at_utc": datetime.now(timezone.utc).isoformat(), "kit_digest": kit_digest, "file_hashes": hashes}
            receipt.write_text(json.dumps(data, indent=2), encoding="utf-8")
            observed = f"KIT FILES OBSERVED: {kit_digest}. Runtime receipt: .octacom/runtime/. This proves this injection ran, not that every instruction was understood.\n"
    except (OSError, ValueError, TypeError, KeyError):
        pass
    sys.stdout.write(POLICY)
    sys.stdout.write(observed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
