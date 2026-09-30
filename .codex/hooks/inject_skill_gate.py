"""Inject the repository skill preflight policy into Codex turns and subagents."""

from __future__ import annotations

import sys


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
    sys.stdin.read()
    sys.stdout.write(POLICY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
