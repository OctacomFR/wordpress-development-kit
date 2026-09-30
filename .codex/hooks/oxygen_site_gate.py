"""Require an Oxygen site identity read before a recognized Oxygen mutation."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path


SITE_INFO = "oxygen_site_info"
MUTATIONS = frozenset(
    {
        "oxygen_change_post_status",
        "oxygen_create_post",
        "oxygen_create_reusable_component",
        "oxygen_create_template",
        "oxygen_delete_css_selectors",
        "oxygen_delete_css_variables",
        "oxygen_edit_post",
        "oxygen_html_to_page",
        "oxygen_import_design_library_dependencies",
        "oxygen_import_design_library_site",
        "oxygen_insert_css_variables",
        "oxygen_insert_design_library_item",
        "oxygen_insert_stylesheet",
        "oxygen_mark_submission_read",
        "oxygen_set_component_editable_properties",
        "oxygen_set_component_instance_properties",
        "oxygen_set_element_animations",
        "oxygen_set_element_conditions",
        "oxygen_set_element_form",
        "oxygen_set_element_interactions",
        "oxygen_set_element_variable_overrides",
        "oxygen_set_global_settings",
        "oxygen_set_home_page",
        "oxygen_set_modern_normalize",
        "oxygen_set_template_conditions",
    }
)
STATE_ROOT = Path(tempfile.gettempdir()) / "octacom-codex-oxygen-site-gate"


def classify(tool_name: object) -> tuple[str, str] | None:
    if not isinstance(tool_name, str) or not tool_name.startswith("mcp__"):
        return None
    for suffix in (SITE_INFO, *sorted(MUTATIONS)):
        if tool_name.endswith(suffix):
            return tool_name[: -len(suffix)], suffix
    return None


def marker(event: dict, site_prefix: str, root: Path) -> Path | None:
    identity = (event.get("cwd"), event.get("session_id"), site_prefix)
    if not all(isinstance(part, str) and part for part in identity):
        return None
    digest = hashlib.sha256(json.dumps(identity, separators=(",", ":")).encode()).hexdigest()
    return root / f"{digest}.seen"


def site_info_succeeded(response: object) -> bool:
    return (
        isinstance(response, dict)
        and response.get("isError") is not True
        and (bool(response.get("content")) or bool(response.get("structuredContent")))
    )


def handle(event: dict, root: Path = STATE_ROOT) -> dict:
    classification = classify(event.get("tool_name"))
    if classification is None:
        return {}
    site_prefix, operation = classification
    path = marker(event, site_prefix, root)
    kind = event.get("hook_event_name")

    if kind == "PostToolUse" and operation == SITE_INFO and path is not None:
        if site_info_succeeded(event.get("tool_response")):
            root.mkdir(parents=True, exist_ok=True)
            path.touch()
        return {}

    if kind == "PreToolUse" and operation in MUTATIONS and (path is None or not path.exists()):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    "Lis d'abord oxygen_site_info sur ce même connecteur MCP, puis vérifie "
                    "que le site et la version Oxygen correspondent à la tâche avant de modifier."
                ),
            }
        }
    return {}


def main() -> int:
    try:
        event = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        result = handle(event)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        result = {"systemMessage": f"Contrôle Oxygen indisponible : {type(exc).__name__}"}
    sys.stdout.buffer.write(json.dumps(result, ensure_ascii=True).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
