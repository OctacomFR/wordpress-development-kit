"""Inject the repository skill preflight policy into Codex turns and subagents."""

from __future__ import annotations

import sys


POLICY = """SKILL PREFLIGHT REQUIRED
Before the next observable execution unit, use the available `skill-gate` skill. Select the minimum applicable domain skills from the real catalog, read every selected SKILL.md and its mandatory references, then verify scope, target, permissions, ownership, blockers, rollback needs, and expected evidence. If no domain skill applies, keep `skill-gate` alone. Re-run the preflight when objective, target, action class, permissions, owner, or applicable skills change. A subagent must perform its own preflight; a parent's suggested skills do not grant permission. Skill selection never expands user authorization. Missing required information blocks dependent writes. Hooks inject context only and are not a complete security boundary.
"""


def main() -> int:
    # Codex provides hook metadata on stdin. The policy is deliberately static so
    # user-controlled prompt text is never copied into privileged instructions.
    sys.stdin.read()
    sys.stdout.write(POLICY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
