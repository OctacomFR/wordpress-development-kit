"""Check mission identity, scope and observed snapshot before covered Oxygen writes."""

from __future__ import annotations

import json
import re
import sqlite3
import sys
import time
from pathlib import Path

from mission_guard import action_digest, digest, epoch, invalidate, load_mission, mutation_check, pending_overlap, response_data, site_identity, state


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
READS = frozenset({
    "oxygen_site_info", "oxygen_get_breakpoints", "oxygen_get_component_editable_properties",
    "oxygen_get_css_selectors", "oxygen_get_css_variables", "oxygen_get_dropdown_options",
    "oxygen_get_dynamic_data_categories", "oxygen_get_dynamic_fields", "oxygen_get_ecommerce_instructions",
    "oxygen_get_element_conditions", "oxygen_get_element_css", "oxygen_get_element_schemas",
    "oxygen_get_element_slugs", "oxygen_get_form_submission", "oxygen_get_form_submissions",
    "oxygen_get_global_settings", "oxygen_get_instructions", "oxygen_get_media_sizes",
    "oxygen_get_post_css_files", "oxygen_get_post_details", "oxygen_get_post_tree",
    "oxygen_get_template_conditions", "oxygen_preview_element", "oxygen_preview_global_settings_css",
    "oxygen_preview_post", "oxygen_search_posts",
})

SNAPSHOT_READS = {
    "oxygen_get_post_tree": "post", "oxygen_get_global_settings": "global:settings",
    "oxygen_get_css_variables": "global:variables", "oxygen_get_css_selectors": "global:selectors",
}

GLOBAL_OPERATIONS = {
    "oxygen_delete_css_selectors": "global:selectors", "oxygen_delete_css_variables": "global:variables",
    "oxygen_insert_css_variables": "global:variables", "oxygen_insert_stylesheet": "global:stylesheets",
    "oxygen_set_global_settings": "global:settings", "oxygen_set_home_page": "global:site",
    "oxygen_set_modern_normalize": "global:site", "oxygen_import_design_library_dependencies": "global:library",
    "oxygen_import_design_library_site": "global:library", "oxygen_insert_design_library_item": "global:library",
    "oxygen_create_post": "create:post", "oxygen_create_template": "create:template",
    "oxygen_create_reusable_component": "create:component",
}


def classify(tool_name: object) -> tuple[str, str] | None:
    if not isinstance(tool_name, str) or not tool_name.startswith("mcp__"):
        return None
    match = re.fullmatch(r"(mcp__[A-Za-z0-9_]+_)(oxygen_[A-Za-z0-9_]+)", tool_name)
    return (match[1], match[2]) if match else None


def site_info_succeeded(response: object) -> bool:
    try:
        data = response_data(response)
        site_identity(data.get("site_url", ""))
        return bool(re.fullmatch(r"6\.[0-9]+(?:\.[0-9]+)?(?:[-+][A-Za-z0-9.-]+)?", data.get("builder_version", "")))
    except (ValueError, TypeError):
        return False


def deny(reason: str) -> dict:
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}


def resource_for(operation: str, arguments: dict) -> str:
    if operation in GLOBAL_OPERATIONS:
        return GLOBAL_OPERATIONS[operation]
    post_id = arguments.get("post_id")
    if type(post_id) is int and post_id > 0:
        return f"post:{post_id}"
    raise ValueError("Contrat d'objet/révision non pris en charge pour cette opération")


def validate_snapshot(operation: str, arguments: dict, data: dict):
    if operation == "oxygen_get_post_tree":
        if "post_id" in data and (type(data["post_id"]) is not int or data["post_id"] != arguments["post_id"]):
            raise ValueError("Identité du post retourné différente de la demande")
        tree = data.get("tree", data)
        if not isinstance(tree, dict) or type(tree.get("id")) is not int or not isinstance(tree.get("children"), list):
            raise ValueError("Schéma d'arbre Oxygen non reconnu : adaptateur requis")
    elif operation == "oxygen_get_global_settings":
        if not isinstance(data.get("settings"), dict):
            raise ValueError("Schéma de settings globaux non reconnu : adaptateur requis")
    else:
        if any(arguments.get(key) for key in ("ids", "names", "search", "collections", "types")):
            raise ValueError("Lecture globale complète sans filtres requise avant écriture")
        field = "variables" if operation == "oxygen_get_css_variables" else "selectors"
        if not isinstance(data.get(field), list) or any(not isinstance(item, dict) for item in data[field]):
            raise ValueError(f"Schéma global {field} non reconnu : adaptateur requis")
        if field == "selectors" and arguments.get("include_properties") is not True:
            raise ValueError("Toutes les propriétés des sélecteurs requises dans le snapshot")


def handle(event: dict, root: Path | None = None) -> dict:
    classification = classify(event.get("tool_name"))
    if classification is None:
        return {}
    connector, operation = classification
    kind = event.get("hook_event_name")
    if kind == "PreToolUse" and operation not in READS and operation not in MUTATIONS:
        return deny("Opération Oxygen inconnue : examiner son contrat avant activation")
    workspace = Path(event.get("cwd", ""))
    session = event.get("session_id")
    if not isinstance(session, str) or not session or not workspace.is_absolute():
        return deny("Identité runtime/cwd absente") if kind == "PreToolUse" and operation not in READS else {}
    try:
        mission, mission_digest = load_mission(workspace)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return deny(f"Mission confirmée requise avant écriture : {exc}") if kind == "PreToolUse" and operation not in READS else {}
    arguments = event.get("tool_input", {})
    if not isinstance(arguments, dict):
        return deny("Arguments JSON objet requis") if kind == "PreToolUse" else {}
    call = event.get("tool_use_id", "")
    with state(workspace, mission_digest) as db:
        if operation == SITE_INFO:
            db.execute("DELETE FROM sites WHERE session=?", (session,))
            if kind == "PostToolUse":
                try:
                    data = response_data(event.get("tool_response"))
                    url = site_identity(data.get("site_url", ""))
                    version = data.get("builder_version")
                    target = mission["target"]
                    if connector != target["connector"] or url != target["site_url"] or version != target["builder_version"]:
                        raise ValueError("Mauvais site/version Oxygen")
                    db.execute("INSERT INTO sites VALUES (?,?,?,?,?)", (session, connector, url, version, time.time()))
                except (ValueError, TypeError) as exc:
                    return {"systemMessage": f"Observation site refusée : {exc}"}
            return {}
        if operation in SNAPSHOT_READS:
            resource = resource_for(operation, arguments) if SNAPSHOT_READS[operation] == "post" else SNAPSHOT_READS[operation]
            if connector != mission["target"]["connector"] or resource not in mission["resources"]:
                return {}
            db.execute("DELETE FROM snapshots WHERE resource=?", (resource,))
            if kind == "PostToolUse":
                try:
                    if pending_overlap(db, resource):
                        raise ValueError("Lecture pendant mutation en cours : aucune base valide avant clôture et relecture")
                    data = response_data(event.get("tool_response"))
                    validate_snapshot(operation, arguments, data)
                    revision = digest(data)
                    expected = db.execute("SELECT revision FROM expected WHERE resource=?", (resource,)).fetchone()
                    if expected and expected[0] != revision:
                        invalidate(db, resource)
                    db.execute("INSERT INTO snapshots VALUES (?,?,?,?)", (resource, revision, session, time.time()))
                    db.execute("INSERT OR IGNORE INTO epochs VALUES (?,0)", (resource,))
                    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": f"Session {session}; snapshot observé {resource}: {revision}; epoch {epoch(db, resource)}. Accepter cette base explicitement via mission_guard accept-snapshot avant écriture."}}
                except (ValueError, TypeError) as exc:
                    invalidate(db, resource)
                    return {"systemMessage": f"Snapshot refusé : {exc}"}
            return {}
        if operation in MUTATIONS:
            try:
                resource = resource_for(operation, arguments)
                if kind == "PreToolUse":
                    mutation_check(db, mission, session, connector, operation, resource, call, arguments)
                elif kind in {"PostToolUse", "PostToolUseFailure"}:
                    attempt = db.execute("SELECT * FROM attempts WHERE call=?", (call,)).fetchone()
                    if not attempt:
                        invalidate(db, resource)
                        return {"systemMessage": "Effet Oxygen observé sans contrôle préalable : preuves invalidées, couverture à vérifier"}
                    if attempt["resource"] != resource or attempt["argument_digest"] != action_digest(session, connector, operation, resource, arguments):
                        invalidate(db, attempt["resource"])
                        invalidate(db, resource)
                        db.execute("UPDATE attempts SET status='unknown' WHERE call=?", (call,))
                        return {"systemMessage": "Résultat différent de l'action contrôlée : preuves des objets concernés invalidées, réconcilier"}
                    if attempt["status"] != "completed":
                        invalidate(db, resource)
                    status = "unknown"
                    try:
                        data = response_data(event.get("tool_response"))
                        if data.get("success") is True:
                            status = "completed"
                    except (ValueError, TypeError):
                        pass
                    db.execute("UPDATE attempts SET status=? WHERE call=?", (status, call))
            except (ValueError, TypeError) as exc:
                return deny(str(exc)) if kind == "PreToolUse" else {"systemMessage": str(exc)}
    return {}


def main() -> int:
    try:
        event = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        result = handle(event)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, sqlite3.Error) as exc:
        result = {"decision": "block", "reason": f"Contrôle Oxygen indisponible : {type(exc).__name__}"}
    sys.stdout.buffer.write(json.dumps(result, ensure_ascii=True).encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
