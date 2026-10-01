"""Translate Claude Code hook envelopes to the shared repository controls."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


INJECTION_EVENTS = {"SessionStart", "UserPromptSubmit", "SubagentStart"}
TOOL_EVENTS = {"PreToolUse", "PostToolUse", "PostToolUseFailure"}


def deny(reason: str) -> dict:
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
            "permissionDecision": "deny", "permissionDecisionReason": reason}}


def workspace(cwd: str) -> Path:
    # Keep the workspace path, even when .codex is a junction to the kit.
    current = Path(cwd).absolute()
    for candidate in (current, *current.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / ".codex/hooks").is_dir():
            return candidate
    raise ValueError("workspace not found")


def bridge(event: dict) -> dict:
    kind = event.get("hook_event_name")
    if kind not in INJECTION_EVENTS | TOOL_EVENTS:
        return {}
    if not isinstance(event.get("cwd"), str) or not event["cwd"]:
        raise ValueError("missing cwd")
    root = workspace(event["cwd"])
    normalized = {key: event[key] for key in (
        "hook_event_name", "session_id", "tool_name", "tool_input", "tool_response",
        "tool_use_id", "agent_id", "prompt") if key in event}
    normalized["cwd"] = str(root)
    normalized["runtime"] = "claude-code"
    if kind == "PostToolUseFailure":
        normalized["tool_response"] = {"isError": True}
    script = "inject_skill_gate.py" if kind in INJECTION_EVENTS else "oxygen_site_gate.py"
    result = subprocess.run([sys.executable, "-B", str(root / ".codex/hooks" / script)],
                            input=json.dumps(normalized), capture_output=True,
                            text=True, encoding="utf-8", timeout=8, cwd=root)
    if result.returncode != 0:
        raise RuntimeError("control subprocess failed")
    if kind in INJECTION_EVENTS:
        return {"hookSpecificOutput": {"hookEventName": kind,
                "additionalContext": result.stdout.strip()}}
    decision = json.loads(result.stdout)
    if not isinstance(decision, dict):
        raise ValueError("control output must be an object")
    if kind == "PreToolUse" and decision.get("decision") == "block":
        return deny(decision.get("reason", "Octacom control blocked the call"))
    if kind == "PreToolUse" and decision.get("systemMessage"):
        raise RuntimeError("control reported an error")
    return decision


def main() -> int:
    event = {}
    try:
        event = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        if not isinstance(event, dict):
            event = {}
            raise ValueError("event must be an object")
        result = bridge(event)
    except (OSError, ValueError, TypeError, RuntimeError, subprocess.TimeoutExpired) as exc:
        reason = f"Octacom control unavailable ({type(exc).__name__}); retry after repair."
        result = deny(reason) if event.get("hook_event_name") == "PreToolUse" or not event else {"systemMessage": reason}
    sys.stdout.buffer.write(json.dumps(result, ensure_ascii=True).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
