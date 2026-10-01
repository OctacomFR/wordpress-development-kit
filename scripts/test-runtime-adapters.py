"""Exercise real adapters with mock runtime APIs and Python subprocess fixtures."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).absolute().parents[1]
CLAUDE = REPO / ".claude/hooks/octacom_bridge.py"
NODE = shutil.which("node")
CORE_FIXTURE = '''import json, sys
from pathlib import Path
event = json.load(sys.stdin)
Path("observed.json").write_text(json.dumps(event), encoding="utf-8")
mode = event.get("tool_input", {}).get("fixture")
if mode == "exit": raise SystemExit(3)
if mode == "invalid": print("broken")
elif mode == "deny":
 print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "fixture denied"}}))
elif mode == "warning": print(json.dumps({"systemMessage": "fixture warning"}))
else: print("{}")
'''
NODE_FIXTURE = r'''
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";
const { OctacomControls } = await import(pathToFileURL(process.argv[2]));
const directory = process.argv[3];
const hooks = await OctacomControls({ directory });
const input = { tool: "site_oxygen_edit_post", sessionID: "native-session", callID: "call-7", args: {} };
await hooks["tool.execute.before"](input, { args: { fixture: "pass", post_id: 17 } });
let event = JSON.parse(await readFile(directory + "/observed.json", "utf8"));
assert.equal(event.tool_name, "mcp__site__oxygen_edit_post");
assert.equal(event.session_id, "native-session");
assert.equal(event.tool_use_id, "call-7");
assert.equal(event.tool_input.post_id, 17);
await assert.rejects(hooks["tool.execute.before"](input, { args: { fixture: "deny" } }), /fixture denied/);
await assert.rejects(hooks["tool.execute.before"](input, { args: { fixture: "invalid" } }));
await assert.rejects(hooks["tool.execute.before"](input, { args: { fixture: "exit" } }), /control failed/);
await assert.rejects(hooks["tool.execute.before"]({ ...input, tool: "other_oxygen_edit_post" }, { args: {} }), /Register the exact/);
await assert.rejects(hooks["tool.execute.before"]({ ...input, sessionID: "" }, { args: {} }), /session identity/);
await hooks["tool.execute.after"](input, { output: JSON.stringify({ isError: true, content: [] }), metadata: {} });
event = JSON.parse(await readFile(directory + "/observed.json", "utf8"));
assert.equal(event.hook_event_name, "PostToolUse");
assert.equal(event.tool_response.isError, true);
await hooks["tool.execute.after"](input, { output: "plain result", metadata: {} });
event = JSON.parse(await readFile(directory + "/observed.json", "utf8"));
assert.equal(event.tool_response.content[0].text, "plain result");
assert.equal(event.tool_response.isError, undefined);
await assert.rejects(hooks["tool.execute.before"](input, { args: { fixture: "warning" } }), /reported an error/);
const warning = { output: "inventory result", metadata: {} };
await hooks["tool.execute.after"]({ ...input, args: { fixture: "warning" } }, warning);
assert.equal(warning.output, "inventory result\n\nfixture warning");
await assert.rejects(hooks["tool.execute.after"]({ ...input, args: { fixture: "deny" } }, { output: "inventory" }), /fixture denied/);
const output = { system: [] };
await hooks["experimental.chat.system.transform"]({}, output);
await hooks["experimental.chat.system.transform"]({}, output);
assert.deepEqual(output.system, ["STATIC PREFLIGHT"]);
const compact = { context: [] };
await hooks["experimental.session.compacting"]({}, compact);
assert.deepEqual(compact.context, ["STATIC PREFLIGHT"]);
process.env.OCTACOM_PYTHON = directory + "/missing-python";
await assert.rejects(hooks["tool.execute.before"](input, { args: {} }), /could not start/);
console.log("OpenCode native callbacks: passed");
'''

NODE_CORE = r'''
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { pathToFileURL } from "node:url";
const { OctacomControls } = await import(pathToFileURL(process.argv[2]));
const root = process.argv[3];
const hooks = await OctacomControls({ directory: root });
function cli(...args) {
  return JSON.parse(execFileSync(process.env.OCTACOM_PYTHON,
    ["-B", root + "/.codex/hooks/mission_guard.py", "--workspace", root, ...args], { encoding: "utf8" }));
}
function input(tool, callID, args = {}) { return { tool, callID, args, sessionID: "opencode-real-core" }; }
const mutation = input("site_oxygen_edit_post", "mutation-1", { post_id: 17, operations: [] });
await assert.rejects(hooks["tool.execute.before"](mutation, { args: mutation.args }), /oxygen_site_info/);
cli("bind-session", "--session", mutation.sessionID, "--owner", "page-owner");
const site = input("site_oxygen_site_info", "site-1");
await hooks["tool.execute.before"](site, { args: {} });
await hooks["tool.execute.after"](site, { output: JSON.stringify({ site_url: "https://fixture.invalid", builder_version: "6.1.0" }) });
const tree = input("site_oxygen_get_post_tree", "tree-1", { post_id: 17 });
await hooks["tool.execute.before"](tree, { args: tree.args });
await hooks["tool.execute.after"](tree, { output: JSON.stringify({ post_id: 17, tree: { id: 1, children: [] } }) });
const revision = cli("status").snapshots[0].revision;
cli("accept-snapshot", "--resource", "post:17", "--revision", revision);
await hooks["tool.execute.before"](mutation, { args: mutation.args });
await hooks["tool.execute.after"](mutation, { output: JSON.stringify({ success: true }) });
assert.deepEqual(cli("status").snapshots, []);
await assert.rejects(hooks["tool.execute.before"]({ ...mutation, callID: "mutation-2" }, { args: mutation.args }), /Révision/);
await assert.rejects(hooks["tool.execute.before"](input("site_oxygen_future_operation", "future-1"), { args: {} }), /inconnue/);
console.log("OpenCode shared-core path: passed");
'''

NODE_INVENTORY = r'''
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { pathToFileURL } from "node:url";
const { OctacomControls } = await import(pathToFileURL(process.argv[2]));
const root = process.argv[3];
const hooks = await OctacomControls({ directory: root });
function cli(...args) {
  return JSON.parse(execFileSync(process.env.OCTACOM_PYTHON,
    ["-B", root + "/.codex/hooks/mission_guard.py", "--workspace", root, ...args], { encoding: "utf8" }));
}
function input(tool, callID, args = {}) { return { tool, callID, args, sessionID: "opencode-inventory" }; }
cli("bind-session", "--session", "opencode-inventory", "--owner", "page-owner");
const site = input("mcp__site__oxygen_site_info", "site");
await hooks["tool.execute.before"](site, { args: site.args });
await hooks["tool.execute.after"](site, { output: JSON.stringify({ site_url: "https://fixture.invalid", builder_version: "6.1.0" }) });
const full = input("mcp__site__oxygen_get_css_selectors", "complete", { include_properties: true });
await hooks["tool.execute.before"](full, { args: full.args });
await hooks["tool.execute.after"](full, { output: JSON.stringify({ selectors: [{ name: ".fixture", properties: {} }] }) });
const revision = cli("status").snapshots[0].revision;
cli("accept-snapshot", "--resource", "global:selectors", "--revision", revision);
for (const [callID, args, data] of [
  ["filtered", { search: "fixture", include_properties: true }, { selectors: [{ name: ".fixture" }] }],
  ["unknown-schema", { include_properties: true }, { inventory: [".fixture"] }],
  ["tool-failed", { include_properties: true }, { isError: true, content: [] }],
]) {
  const read = input("mcp__site__oxygen_get_css_selectors", callID, args);
  await hooks["tool.execute.before"](read, { args });
  const original = JSON.stringify(data);
  const output = { output: original, metadata: {} };
  await hooks["tool.execute.after"](read, output);
  assert.ok(output.output.startsWith(original + "\n\n"), callID);
  assert.match(output.output, /Snapshot refusé/, callID);
  assert.deepEqual(cli("status").snapshots, [], callID);
  const mutation = input("mcp__site__oxygen_delete_css_selectors", "write-" + callID, { names: [".fixture"] });
  await assert.rejects(hooks["tool.execute.before"](mutation, { args: mutation.args }), /Révision/, callID);
}
console.log("OpenCode inventory warnings: passed");
'''


class RuntimeAdapters(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="octacom-adapters-")
        self.root = Path(self.temp.name)
        (self.root / ".codex/hooks").mkdir(parents=True)
        (self.root / ".octacom").mkdir()
        (self.root / "AGENTS.md").write_text("fixture", encoding="utf-8")
        (self.root / ".codex/hooks/oxygen_site_gate.py").write_text(CORE_FIXTURE, encoding="utf-8")
        (self.root / ".codex/hooks/inject_skill_gate.py").write_text('print("STATIC PREFLIGHT")', encoding="utf-8")
        (self.root / ".octacom/runtime-tool-map.json").write_text(json.dumps({"opencode": {
            "site_oxygen_edit_post": "mcp__site__oxygen_edit_post"}}), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def claude(self, event):
        result = subprocess.run([sys.executable, str(CLAUDE)], input=json.dumps(event),
                                text=True, encoding="utf-8", capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def event(self, kind="PreToolUse", fixture="pass"):
        return {"hook_event_name": kind, "cwd": str(self.root), "session_id": "claude-session",
                "tool_name": "mcp__site__oxygen_edit_post", "tool_input": {"fixture": fixture},
                "tool_use_id": "call-8"}

    def real_core(self):
        for name in ("oxygen_site_gate.py", "mission_guard.py", "inject_skill_gate.py"):
            shutil.copyfile(REPO / ".codex/hooks" / name, self.root / ".codex/hooks" / name)
        mission = {"format": 1, "mission_id": "adapter-fixture", "authorization_source": "local test",
                   "scope": "fixture post", "completion_criteria": ["no external effect"],
                   "target": {"site_url": "https://fixture.invalid", "final_domain": "fixture.invalid",
                              "connector": "mcp__site__", "builder_version": "6.1.0", "consistency": "serial_observed"},
                   "max_observation_age_seconds": 300,
                   "sources": [{"id": "fixture", "reference": "local-test", "version": "1"}],
                   "resources": {"post:17": {"owner": "page-owner", "operations": ["oxygen_edit_post"]}},
                   "figma": {"required": False, "references": []}}
        (self.root / ".octacom/mission.json").write_text(json.dumps(mission), encoding="utf-8")
        (self.root / ".octacom/runtime-tool-map.json").write_text(json.dumps({"opencode": {
            f"site_{name}": f"mcp__site__{name}" for name in
            ("oxygen_site_info", "oxygen_get_post_tree", "oxygen_edit_post", "oxygen_future_operation")}}), encoding="utf-8")

    def core_cli(self, *args):
        result = subprocess.run([sys.executable, "-B", str(self.root / ".codex/hooks/mission_guard.py"),
                                "--workspace", str(self.root), *args], text=True, encoding="utf-8",
                                capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_claude_native_denial_and_envelope(self):
        result = self.claude(self.event(fixture="deny"))
        self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")
        observed = json.loads((self.root / "observed.json").read_text())
        self.assertEqual(observed["session_id"], "claude-session")
        self.assertEqual(observed["tool_use_id"], "call-8")
        self.assertEqual(observed["runtime"], "claude-code")

    def test_claude_errors_deny_before_execution(self):
        for fixture in ("invalid", "exit"):
            with self.subTest(fixture=fixture):
                self.assertEqual(self.claude(self.event(fixture=fixture))["hookSpecificOutput"]["permissionDecision"], "deny")
        (self.root / ".codex/hooks/oxygen_site_gate.py").unlink()
        self.assertEqual(self.claude(self.event())["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_claude_failed_tool_is_not_success_evidence(self):
        self.claude(self.event("PostToolUseFailure"))
        observed = json.loads((self.root / "observed.json").read_text())
        self.assertEqual(observed["hook_event_name"], "PostToolUseFailure")
        self.assertEqual(observed["tool_response"], {"isError": True})

    def test_claude_static_policy_at_each_boundary(self):
        for kind in ("SessionStart", "UserPromptSubmit", "SubagentStart"):
            event = self.event(kind)
            event["prompt"] = "UNTRUSTED PROMPT"
            result = self.claude(event)["hookSpecificOutput"]
            self.assertEqual(result["hookEventName"], kind)
            self.assertEqual(result["additionalContext"], "STATIC PREFLIGHT")

    def test_claude_subdirectory_keeps_workspace_identity(self):
        nested = self.root / "nested"
        nested.mkdir()
        event = self.event()
        event["cwd"] = str(nested)
        self.claude(event)
        self.assertEqual(json.loads((self.root / "observed.json").read_text())["cwd"], str(self.root))

    def test_claude_configuration_uses_exec_form(self):
        settings = json.loads((REPO / ".claude/settings.json").read_text())
        self.assertEqual(set(settings["hooks"]), {"SessionStart", "UserPromptSubmit", "SubagentStart",
                                                "PreToolUse", "PostToolUse", "PostToolUseFailure"})
        for groups in settings["hooks"].values():
            for group in groups:
                hook = group["hooks"][0]
                self.assertEqual(hook["command"], "python")
                self.assertEqual(hook["args"], ["-B", "${CLAUDE_PROJECT_DIR}/.claude/hooks/octacom_bridge.py"])

    def test_claude_real_shared_core_allows_then_invalidates(self):
        self.real_core()
        event = self.event()
        event["tool_input"] = {"post_id": 17, "operations": []}
        self.assertEqual(self.claude(event)["hookSpecificOutput"]["permissionDecision"], "deny")
        self.core_cli("bind-session", "--session", event["session_id"], "--owner", "page-owner")
        for operation, arguments, data in (
            ("oxygen_site_info", {}, {"site_url": "https://fixture.invalid", "builder_version": "6.1.0"}),
            ("oxygen_get_post_tree", {"post_id": 17}, {"post_id": 17, "tree": {"id": 1, "children": []}}),
        ):
            read = dict(event, tool_name=f"mcp__site__{operation}", tool_input=arguments)
            self.assertEqual(self.claude(read), {})
            self.claude(dict(read, hook_event_name="PostToolUse", tool_response={"isError": False, "structuredContent": data}))
        revision = self.core_cli("status")["snapshots"][0]["revision"]
        self.core_cli("accept-snapshot", "--resource", "post:17", "--revision", revision)
        self.assertEqual(self.claude(event), {})
        self.claude(dict(event, hook_event_name="PostToolUse", tool_response={"isError": False, "structuredContent": {"success": True}}))
        self.assertEqual(self.core_cli("status")["snapshots"], [])
        self.assertEqual(self.claude(dict(event, tool_use_id="call-9"))["hookSpecificOutput"]["permissionDecision"], "deny")

    @unittest.skipUnless(NODE, "Node runtime absent")
    def test_opencode_real_plugin_and_python_bridge(self):
        runner = self.root / "runner.mjs"
        runner.write_text(NODE_FIXTURE, encoding="utf-8")
        env = dict(os.environ, OCTACOM_PYTHON=sys.executable)
        result = subprocess.run([NODE, str(runner), str(REPO / ".opencode/plugins/octacom-controls.js"), str(self.root)],
                                env=env, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("native callbacks: passed", result.stdout)

    @unittest.skipUnless(NODE, "Node runtime absent")
    def test_opencode_real_shared_core_allows_then_invalidates(self):
        self.real_core()
        runner = self.root / "core-runner.mjs"
        runner.write_text(NODE_CORE, encoding="utf-8")
        result = subprocess.run([NODE, str(runner), str(REPO / ".opencode/plugins/octacom-controls.js"), str(self.root)],
                                env=dict(os.environ, OCTACOM_PYTHON=sys.executable), capture_output=True,
                                text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("shared-core path: passed", result.stdout)

    @unittest.skipUnless(NODE, "Node runtime absent")
    def test_opencode_inventory_warning_keeps_result_without_write_base(self):
        self.real_core()
        mission_file = self.root / ".octacom/mission.json"
        mission = json.loads(mission_file.read_text())
        mission["resources"]["global:selectors"] = {"owner": "page-owner", "operations": ["oxygen_delete_css_selectors"]}
        mission_file.write_text(json.dumps(mission), encoding="utf-8")
        runner = self.root / "inventory-runner.mjs"
        runner.write_text(NODE_INVENTORY, encoding="utf-8")
        result = subprocess.run([NODE, str(runner), str(REPO / ".opencode/plugins/octacom-controls.js"), str(self.root)],
                                env=dict(os.environ, OCTACOM_PYTHON=sys.executable), capture_output=True,
                                text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("inventory warnings: passed", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
