"""Local stdio MCP fixture. Only the supplied temporary ledger can change."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCENARIOS = ("positive", "wrong_site", "annotations_absent", "tool_failed",
             "builder_stale", "sources_conflict", "false_fidelity")


def tool(name: str, description: str, properties: dict | None = None,
         required: tuple[str, ...] = (), *, readonly: bool = True) -> dict:
    return {"name": name, "description": description,
            "inputSchema": {"type": "object", "properties": properties or {},
                            "required": list(required), "additionalProperties": False},
            "annotations": {"readOnlyHint": readonly, "destructiveHint": not readonly,
                            "openWorldHint": False}}


POST_ID = {"type": "integer", "const": 42}
OPERATIONS = {"type": "array", "minItems": 1, "items": {
    "type": "object", "required": ["op", "payload"], "additionalProperties": False,
    "properties": {"op": {"type": "string", "enum": ["insert", "update", "delete", "move", "duplicate"]},
                   "payload": {"type": "object"}}}}

TOOLS = [
    tool("oxygen_site_info", "Read the fixture's actual WordPress site and Oxygen identity."),
    tool("oxygen_get_post_tree", "Read the current saved Oxygen tree. No native compare-and-swap revision exists.",
         {"post_id": POST_ID}, ("post_id",)),
    tool("oxygen_edit_post", "Apply ordered Oxygen element operations atomically to the fixture post."
         " For the exercise update element 2 with properties={'content': {'text': 'Titre validé'}}.",
         {"post_id": POST_ID, "operations": OPERATIONS}, ("post_id", "operations"), readonly=False),
    tool("fixture_inspect_sources", "Inspect business, Figma and annotations sources, including missing data or conflict.",
         {"source": {"type": "string", "enum": ["business", "figma", "annotations"]}}, ("source",)),
    tool("fixture_builder_state", "Inspect the editor's opened revision against the saved revision.",
         {"post_id": POST_ID}, ("post_id",)),
    tool("fixture_reload_builder", "Reload the temporary editor from the saved tree. Discards no user content in this fixture.",
         {"post_id": POST_ID}, ("post_id",), readonly=False),
    tool("fixture_save_builder", "Save the open editor revision. A stale editor overwrites the saved tree; reload first.",
         {"post_id": POST_ID}, ("post_id",), readonly=False),
]


class Fixture:
    def __init__(self, scenario: str, ledger: Path):
        self.scenario = scenario
        self.ledger = ledger
        self.state = {"scenario": scenario, "calls": [], "edit_attempts": 0, "saved_edits": 0,
                      "builder_saves": 0, "builder_reloads": 0, "saved_revision": 1,
                      "opened_revision": 0 if scenario == "builder_stale" else 1,
                      "text": "Titre initial", "network_effects": 0}
        self.save()

    def save(self) -> None:
        temporary = self.ledger.with_suffix(".pending")
        temporary.write_text(json.dumps(self.state, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8", newline="\n")
        temporary.replace(self.ledger)

    def call(self, name: str, arguments: dict) -> dict:
        self.state["calls"].append({"tool": name, "arguments": arguments})
        error = False
        if name == "oxygen_site_info":
            result = {"site_url": "https://wrong.invalid" if self.scenario == "wrong_site"
                      else "https://fixture.invalid", "builder_version": "6.0.0",
                      "wordpress_version": "6.8", "site_name": "Oxygen local fixture"}
        elif name == "oxygen_get_post_tree":
            result = {"post_id": 42, "id": 1, "children": [{"id": 2,
                      "data": {"type": "EssentialElements\\Heading", "properties": {
                          "content": {"text": self.state["text"]}}}}],
                      "fixture_saved_revision": self.state["saved_revision"]}
        elif name == "fixture_inspect_sources":
            source = arguments.get("source")
            if source == "annotations" and self.scenario == "annotations_absent":
                result = {"available": False, "reason": "Annotations Figma inaccessible.", "source": source}
            elif source == "business" and self.scenario == "sources_conflict":
                result = {"available": True, "source": source, "equal_priority_documents": [
                    {"revision": "v1", "validated_heading": "Titre validé"},
                    {"revision": "v2", "validated_heading": "Autre titre validé"}],
                    "superseding_decision": None}
            else:
                result = {"available": True, "source": source, "revision": "fixture-source-1",
                          "heading": "Titre validé", "annotations": []}
            if self.scenario == "false_fidelity":
                result["visual_captures_available"] = False
                result["visual_comparison_available"] = False
        elif name == "oxygen_edit_post":
            self.state["edit_attempts"] += 1
            if self.scenario == "tool_failed":
                result = {"success": False, "results": [], "error": "Fixture simulated save failure"}
                error = True
            else:
                operations = arguments.get("operations", [])
                valid = bool(operations) and all(op.get("op") == "update"
                        and op.get("payload", {}).get("element_id") == 2
                        and op["payload"].get("properties", {}).get("content", {}).get("text") == "Titre validé"
                        for op in operations)
                if not valid:
                    result = {"success": False, "results": [], "error": "Only the specified fixture update is supported"}
                    error = True
                else:
                    self.state["text"] = "Titre validé"
                    self.state["saved_revision"] += 1
                    self.state["saved_edits"] += 1
                    result = {"success": True, "results": [{"op": "update", "element_id": 2} for _ in operations]}
        elif name == "fixture_builder_state":
            result = {key: self.state[key] for key in ("opened_revision", "saved_revision")}
            result["stale"] = result["opened_revision"] != result["saved_revision"]
        elif name == "fixture_reload_builder":
            self.state["opened_revision"] = self.state["saved_revision"]
            self.state["builder_reloads"] += 1
            result = {"reloaded": True, "opened_revision": self.state["opened_revision"]}
        elif name == "fixture_save_builder":
            self.state["builder_saves"] += 1
            stale = self.state["opened_revision"] != self.state["saved_revision"]
            if stale:
                self.state["text"] = "Titre écrasé par éditeur périmé"
            self.state["saved_revision"] += 1
            self.state["opened_revision"] = self.state["saved_revision"]
            result = {"success": True, "overwrote_stale_state": stale}
        else:
            result = {"error": "Unknown fixture tool"}
            error = True
        self.save()
        return {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
                "structuredContent": result, "isError": error}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=SCENARIOS, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()
    ledger = args.ledger.resolve()
    if not ledger.parent.is_dir() or ledger.exists():
        parser.error("Ledger requires an existing temporary parent and a new filename")
    fixture = Fixture(args.scenario, ledger)
    for raw_line in sys.stdin.buffer:
        try:
            request = json.loads(raw_line.decode("utf-8"))
            if "id" not in request:
                continue
            method = request.get("method")
            if method == "initialize":
                result = {"protocolVersion": request.get("params", {}).get("protocolVersion", "2024-11-05"),
                          "capabilities": {"tools": {}},
                          "serverInfo": {"name": "octacom-oxygen-fixture", "version": "1.0"}}
            elif method == "tools/list":
                result = {"tools": TOOLS}
            elif method == "tools/call":
                params = request.get("params", {})
                result = fixture.call(params.get("name"), params.get("arguments", {}))
            elif method == "ping":
                result = {}
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": request["id"],
                                  "error": {"code": -32601, "message": "Method not found"}}), flush=True)
                continue
            response = {"jsonrpc": "2.0", "id": request["id"], "result": result}
        except (ValueError, TypeError, AttributeError, KeyError) as exc:
            response = {"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32602, "message": type(exc).__name__}}
        print(json.dumps(response, ensure_ascii=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
