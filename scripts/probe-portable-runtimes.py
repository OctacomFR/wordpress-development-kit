"""Probe pinned portable clients against local protocol fixtures, never a live site."""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.server
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import urllib.request
import urllib.error


REPO = Path(__file__).absolute().parents[1]
PINS = {"opencode-windows-x64": "1.18.34", "@anthropic-ai/claude-code-win32-x64": "2.1.286",
        "@t3code/t3-win32-x64": "0.0.44"}
MCP = r'''
import json,sys
from pathlib import Path
for line in sys.stdin:
 try: request=json.loads(line)
 except ValueError: continue
 if "id" not in request: continue
 method=request.get("method")
 if method=="initialize": result={"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"octacom-fixture","version":"1"}}
 elif method=="tools/list": result={"tools":[{"name":"oxygen_edit_post","description":"Local no-effect hook fixture","inputSchema":{"type":"object","properties":{"post_id":{"type":"integer"},"operations":{"type":"array"}},"required":["post_id","operations"]}}]}
 elif method=="tools/call":
  Path("unexpected-effect.txt").write_text("fixture tool executed")
  result={"isError":False,"content":[{"type":"text","text":"{\"success\":true}"}]}
 elif method in {"resources/list","prompts/list"}: result={method.split('/')[0]:[]}
 else: result={}
 print(json.dumps({"jsonrpc":"2.0","id":request["id"],"result":result}),flush=True)
'''


def install(root: Path) -> list[dict]:
    installed = []
    for name, version in PINS.items():
        folder = root / name.replace("@", "").replace("/", "_")
        receipt = folder / "registry.json"
        if receipt.exists():
            meta = json.loads(receipt.read_text())
            archive = folder / "package.tgz"
            integrity = "sha512-" + base64.b64encode(hashlib.sha512(archive.read_bytes()).digest()).decode()
            if meta.get("name") != name or meta.get("version") != version or integrity != meta["dist"]["integrity"]:
                raise ValueError("cached package identity or integrity mismatch")
        else:
            with urllib.request.urlopen(f"https://registry.npmjs.org/{name}/{version}", timeout=30) as response:
                meta = json.load(response)
            with urllib.request.urlopen(meta["dist"]["tarball"], timeout=60) as response:
                data = response.read()
            integrity = "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode()
            if integrity != meta["dist"]["integrity"]:
                raise ValueError("registry integrity mismatch")
            folder.mkdir()
            archive = folder / "package.tgz"
            archive.write_bytes(data)
            with tarfile.open(archive) as tar:
                tar.extractall(folder, filter="data")
            receipt.write_text(json.dumps(meta), encoding="utf-8")
        executable = folder / "package" / {"opencode-windows-x64": "bin/opencode.exe",
                      "@anthropic-ai/claude-code-win32-x64": "claude.exe",
                      "@t3code/t3-win32-x64": "t3.exe"}[name]
        installed.append({"name": name, "version": version, "integrity": meta["dist"]["integrity"],
                          "executable": str(executable)})
    return installed


def environment(root: Path) -> dict:
    env = dict(os.environ)
    for name in ("SSLKEYLOGFILE", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "OPENAI_API_KEY",
                 "ANTHROPIC_BASE_URL", "CODEX_HOME", "CLAUDE_CONFIG_DIR", "OPENCODE_CONFIG"):
        env.pop(name, None)
    for name, folder in (("USERPROFILE", "home"), ("HOME", "home"), ("XDG_CONFIG_HOME", "xdg-config"),
                         ("XDG_DATA_HOME", "xdg-data"), ("XDG_CACHE_HOME", "xdg-cache"),
                         ("CLAUDE_CONFIG_DIR", "claude-home"), ("T3CODE_HOME", "t3-home")):
        destination = root / folder
        destination.mkdir(exist_ok=True)
        env[name] = str(destination)
    env["OCTACOM_PYTHON"] = sys.executable
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    return env


def fixture(root: Path) -> Path:
    workspace = root / "workspace"
    workspace.mkdir(exist_ok=True)
    (workspace / "AGENTS.md").write_text("Use repository controls. This is a local protocol test without a site.\n", encoding="utf-8")
    for folder in (".codex", ".claude", ".opencode/plugins"):
        shutil.copytree(REPO / folder, workspace / folder, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "skills"))
    (workspace / ".octacom").mkdir(exist_ok=True)
    (workspace / ".octacom/runtime-tool-map.json").write_text(json.dumps({"opencode": {
        "site_oxygen_edit_post": "mcp__site__oxygen_edit_post"}}), encoding="utf-8")
    (workspace / "fixture-mcp.py").write_text(MCP, encoding="utf-8")
    (workspace / ".mcp.json").write_text(json.dumps({"mcpServers": {"site": {"command": sys.executable,
        "args": ["-B", str(workspace / "fixture-mcp.py")]}}}), encoding="utf-8")
    return workspace


T3_RPC = r'''
let raw = "";
for await (const chunk of process.stdin) raw += chunk;
const { base, token, workspace, provider, model } = JSON.parse(raw);
const response = await fetch(base + "/api/auth/websocket-ticket", { method: "POST", headers: { Authorization: "Bearer " + token } });
if (!response.ok) throw new Error("temporary T3 ticket rejected: " + response.status);
const ticket = await response.json();
const ws = new WebSocket(base.replace("http:", "ws:") + "/ws?wsTicket=" + encodeURIComponent(ticket.ticket));
const timer = setTimeout(() => { ws.close(); process.exitCode = 2; console.log(JSON.stringify({ timeout: true })); }, 35000);
ws.onopen = () => ws.send(JSON.stringify({ _tag: "Request", id: "1", tag: "server.getConfig", payload: {}, headers: [] }));
const summary = {};
ws.onmessage = (event) => {
 const parsed = JSON.parse(event.data);
 for (const message of Array.isArray(parsed) ? parsed : [parsed]) {
  if (message._tag === "Chunk") {
   summary.stream_kinds = [...new Set([...(summary.stream_kinds || []), ...message.values.map((item) => item.type || item.kind || item._tag || "object")])];
   summary.event_types = [...new Set([...(summary.event_types || []), ...message.values.map((item) => item.event?.type).filter(Boolean)])];
   ws.send(JSON.stringify({ _tag: "Ack", requestId: message.requestId }));
   continue;
  }
  if (message._tag !== "Exit") continue;
  const value = message.exit?.value;
  if (String(message.requestId) === "1" && message.exit?._tag === "Success") {
   summary.initial_settings = value?.settings?.providers?.[provider];
   ws.send(JSON.stringify({ _tag: "Request", id: "2", tag: "server.refreshProviders",
    payload: { instanceId: provider, cwd: workspace, fresh: true, refreshModels: false }, headers: [] }));
   continue;
  }
  if (String(message.requestId) === "2") {
   summary.refresh_exit = message.exit?._tag;
   ws.send(JSON.stringify({ _tag: "Request", id: "3", tag: "server.getConfig", payload: {}, headers: [] }));
   continue;
  }
  if (String(message.requestId) === "3") {
   summary.config = { cwd: value?.cwd, selected_settings: value?.settings?.providers?.[provider],
    providers: value?.providers?.map((provider) => ({ id: provider.instanceId, version: provider.version,
      status: provider.status, installed: provider.installed, auth_status: provider.auth?.status })) };
   const now = new Date().toISOString();
   summary.project = crypto.randomUUID(); summary.thread = crypto.randomUUID();
   ws.send(JSON.stringify({ _tag: "Request", id: "4", tag: "orchestration.dispatchCommand", payload: {
    type: "project.create", commandId: crypto.randomUUID(), projectId: summary.project, title: "Local hook fixture",
    workspaceRoot: workspace, createdAt: now }, headers: [] }));
   continue;
  }
  if (String(message.requestId) === "4" && message.exit?._tag === "Success") {
   ws.send(JSON.stringify({ _tag: "Request", id: "5", tag: "orchestration.dispatchCommand", payload: {
    type: "thread.create", commandId: crypto.randomUUID(), threadId: summary.thread, projectId: summary.project,
    title: "Local hook fixture", modelSelection: { instanceId: provider, model }, runtimeMode: "full-access",
    interactionMode: "default", branch: null, worktreePath: null, createdAt: new Date().toISOString() }, headers: [] }));
   continue;
  }
  if (String(message.requestId) === "5" && message.exit?._tag === "Success") {
   ws.send(JSON.stringify({ _tag: "Request", id: "stream", tag: "orchestration.subscribeThread", payload: { threadId: summary.thread }, headers: [] }));
   ws.send(JSON.stringify({ _tag: "Request", id: "6", tag: "orchestration.dispatchCommand", payload: {
    type: "thread.turn.start", commandId: crypto.randomUUID(), threadId: summary.thread,
    message: { messageId: crypto.randomUUID(), role: "user", text: "Call the local fixture oxygen_edit_post once.", attachments: [] },
    modelSelection: { instanceId: provider, model }, runtimeMode: "full-access", interactionMode: "default",
    createdAt: new Date().toISOString() }, headers: [] }));
   continue;
  }
  if (String(message.requestId) === "6" && message.exit?._tag === "Success") {
   summary.turn_dispatch = "Success";
   setTimeout(() => { clearTimeout(timer); console.log(JSON.stringify(summary)); ws.close(); }, 7000);
   continue;
  }
  clearTimeout(timer);
  console.log(JSON.stringify({ ...summary, tag: message._tag, exit: message.exit?._tag,
   cwd: value?.cwd, keys: value ? Object.keys(value) : [],
   codex_settings: value?.settings?.providers?.codex,
   providers: value?.providers?.map((provider) => ({ id: provider.instanceId, driver: provider.driver, version: provider.version,
    status: provider.status, installed: provider.installed, enabled: provider.enabled,
    runtime_paths: provider.runtimePaths, auth_status: provider.auth?.status })) }));
  ws.close();
 }
};
ws.onerror = () => { clearTimeout(timer); console.log(JSON.stringify({ websocket_error: true })); process.exitCode = 1; };
'''


def trust_fixture_hooks(codex: str, provider_home: Path, workspace: Path, env: dict) -> dict:
    source = importlib.util.spec_from_file_location("codex_runtime_probe", REPO / "scripts/probe-codex-runtime.py")
    module = importlib.util.module_from_spec(source)
    source.loader.exec_module(module)
    previous = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(env, CODEX_HOME=str(provider_home))
        runtime = module.Runtime(workspace, [codex, "app-server", "--stdio"])
    finally:
        os.environ.clear()
        os.environ.update(previous)
    try:
        listing = runtime.request("hooks/list", {"cwds": [str(workspace)]})
    finally:
        runtime.close()
    entries = [hook for item in listing.get("data", []) for hook in item.get("hooks", [])]
    with (provider_home / "config.toml").open("a", encoding="utf-8") as config:
        for hook in entries:
            config.write(f"\n[hooks.state.'{hook['key']}']\ntrusted_hash = '{hook['currentHash']}'\n")
    return {"scope": "reviewed kit definitions, isolated TEMP home only", "count": len(entries),
            "keys_and_hashes": [{"key": hook["key"], "hash": hook["currentHash"]} for hook in entries]}


def t3_probe(root: Path, workspace: Path, installed: list[dict], env: dict, model_base: str, provider="codex") -> dict:
    base_dir = root / f"t3-native-probe-{time.time_ns()}"
    state = base_dir / "userdata"
    state.mkdir(parents=True, exist_ok=True)
    codex = shutil.which("codex")
    provider_home = root / "t3-codex-home"
    provider_home.mkdir(exist_ok=True)
    (provider_home / "config.toml").write_text(
        'model = "fixture-model"\nmodel_provider = "fixture"\n[features]\nhooks = true\n'
        '[model_providers.fixture]\nname = "Local protocol fixture"\nwire_api = "responses"\n'
        f'base_url = "{model_base}/v1"\nrequires_openai_auth = false\nenv_key = "OCTACOM_FIXTURE_API_KEY"\n'
        f'[projects.{json.dumps(str(workspace))}]\ntrust_level = "trusted"\n'
        '[mcp_servers.site]\ncommand = ' + json.dumps(sys.executable) + '\nargs = ["-B", ' +
        json.dumps(str(workspace / "fixture-mcp.py")) + ']\n', encoding="utf-8")
    env = dict(env, OCTACOM_FIXTURE_API_KEY="local-protocol-fixture")
    subprocess.run(["git", "init", "--quiet", str(workspace)], capture_output=True, check=True)
    trust = trust_fixture_hooks(codex, provider_home, workspace, env)
    settings = {"providers": {"codex": {"binaryPath": codex or "codex", "homePath": str(provider_home)},
                              "claudeAgent": {"enabled": False}, "opencode": {"enabled": False}}}
    if provider == "claudeAgent":
        settings["providers"]["codex"]["enabled"] = False
        settings["providers"]["claudeAgent"] = {"enabled": True, "binaryPath": installed[1]["executable"],
                                                  "homePath": env["CLAUDE_CONFIG_DIR"]}
        env = dict(env, ANTHROPIC_BASE_URL=model_base, ANTHROPIC_API_KEY="local-protocol-fixture")
        fixture_settings = json.loads((workspace / ".claude/settings.json").read_text(encoding="utf-8-sig"))
        fixture_settings["enableAllProjectMcpServers"] = True
        fixture_settings["permissions"] = {"allow": ["mcp__site__oxygen_edit_post"]}
        (workspace / ".claude/settings.json").write_text(json.dumps(fixture_settings), encoding="utf-8")
    (state / "settings.json").write_text(json.dumps(settings), encoding="utf-8")
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    exe = installed[2]["executable"]
    process = subprocess.Popen([exe, "serve", "--mode", "desktop", "--host", "127.0.0.1", "--port", str(port),
                                "--base-dir", str(base_dir), str(workspace)], cwd=workspace, env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    result = {"provider": provider, "provider_binary": settings["providers"][provider]["binaryPath"],
              "provider_home": settings["providers"][provider]["homePath"], "workspace": str(workspace),
              "provider_home_scope": "isolated TEMP, no credentials copied; global home is read-only in this sandbox",
              "conversation_hooks_observed": False}
    if provider == "codex":
        result["fixture_hook_trust"] = trust
    try:
        base = f"http://127.0.0.1:{port}"
        for _ in range(50):
            try:
                with urllib.request.urlopen(base + "/.well-known/t3/environment", timeout=1) as response:
                    descriptor = json.load(response)
                    result.update(http_status=response.status, server_version=descriptor.get("serverVersion"))
                    break
            except (urllib.error.URLError, TimeoutError):
                if process.poll() is not None:
                    result["startup_exit"] = process.returncode
                    return result
                time.sleep(0.2)
        issued = subprocess.run([exe, "auth", "session", "issue", "--base-dir", str(base_dir), "--ttl", "5m", "--token-only"],
                                cwd=workspace, env=env, capture_output=True, text=True, encoding="utf-8", timeout=15)
        if issued.returncode != 0:
            result["temporary_session_issue_exit"] = issued.returncode
            return result
        # Generated temporary bearer token stays in memory and is never written to logs or evidence.
        runner = root / "t3-rpc.mjs"
        runner.write_text(T3_RPC, encoding="utf-8")
        rpc = subprocess.run([shutil.which("node"), str(runner)], input=json.dumps({"base": base, "token": issued.stdout.strip(), "workspace": str(workspace),
                             "provider": provider, "model": "fixture-model" if provider == "codex" else "claude-sonnet-4-5"}),
                             env=env, capture_output=True, text=True, encoding="utf-8", timeout=45)
        result["rpc_exit"] = rpc.returncode
        try:
            result["config_rpc"] = json.loads(rpc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            result["config_rpc"] = {"failed": True}
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        result["error_type"] = type(exc).__name__
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    return result


class Protocol(http.server.BaseHTTPRequestHandler):
    calls = []

    def log_message(self, *_args):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
        tools = body.get("tools", [])
        names = [tool.get("name", tool.get("function", {}).get("name", "")) for tool in tools]
        tool_name = next((name for name in names if name.endswith("oxygen_edit_post")), "")
        if "responses" in self.path:
            return self.respond_codex(body, tool_name)
        anthropic = "messages" in self.path
        already_called = any(message.get("role") == "tool" or any(part.get("type") == "tool_result" for part in message.get("content", []) if isinstance(part, dict))
                             for message in body.get("messages", []))
        call_tool = bool(tool_name) and not already_called
        self.calls.append({"protocol": "anthropic" if anthropic else "openai", "tool_requested": tool_name if call_tool else None,
                           "static_preflight_observed": "SKILL PREFLIGHT" in json.dumps(body),
                           "guard_denial_in_input": "Mission confirm" in json.dumps(body)})
        if "count_tokens" in self.path:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"input_tokens":100}')
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        arguments = {"post_id": 17, "operations": []}
        if anthropic:
            events = [("message_start", {"type": "message_start", "message": {"id": "msg_fixture", "type": "message", "role": "assistant", "model": body.get("model"), "content": [], "stop_reason": None, "stop_sequence": None, "usage": {"input_tokens": 100, "output_tokens": 1}}})]
            if call_tool:
                events += [("content_block_start", {"type": "content_block_start", "index": 0, "content_block": {"type": "tool_use", "id": "tool_fixture_1", "name": tool_name, "input": {}}}),
                           ("content_block_delta", {"type": "content_block_delta", "index": 0, "delta": {"type": "input_json_delta", "partial_json": json.dumps(arguments)}})]
            else:
                events += [("content_block_start", {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}),
                           ("content_block_delta", {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Fixture complete."}})]
            events += [("content_block_stop", {"type": "content_block_stop", "index": 0}),
                       ("message_delta", {"type": "message_delta", "delta": {"stop_reason": "tool_use" if call_tool else "end_turn", "stop_sequence": None}, "usage": {"output_tokens": 10}}),
                       ("message_stop", {"type": "message_stop"})]
            for name, payload in events:
                self.wfile.write(f"event: {name}\ndata: {json.dumps(payload)}\n\n".encode())
        else:
            delta = {"role": "assistant"}
            if call_tool:
                delta["tool_calls"] = [{"index": 0, "id": "tool_fixture_1", "type": "function", "function": {"name": tool_name, "arguments": json.dumps(arguments)}}]
            else:
                delta["content"] = "Fixture complete."
            for choice in ({"index": 0, "delta": delta, "finish_reason": None},
                           {"index": 0, "delta": {}, "finish_reason": "tool_calls" if call_tool else "stop"}):
                chunk = {"id": "chat_fixture", "object": "chat.completion.chunk", "created": 1, "model": body.get("model"), "choices": [choice]}
                self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
            self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()

    def respond_codex(self, body, tool_name):
        namespace = None
        if not tool_name:
            for tool in body.get("tools", []):
                for member in tool.get("tools", []):
                    if member.get("name") == "oxygen_edit_post":
                        tool_name, namespace = member["name"], tool["name"]
        already_called = any(item.get("type") == "function_call_output" for item in body.get("input", []) if isinstance(item, dict))
        call_tool = bool(tool_name) and not already_called
        self.calls.append({"protocol": "responses", "tool_requested": tool_name if call_tool else None,
                           "mcp_namespace": namespace,
                           "static_preflight_observed": "SKILL PREFLIGHT" in json.dumps(body),
                           "guard_denial_in_input": "Mission confirm" in json.dumps(body)})
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        arguments = json.dumps({"post_id": 17, "operations": []})
        item = {"type": "function_call", "id": "fc_fixture", "call_id": "call_fixture", "name": tool_name, "arguments": arguments, "status": "completed"} if call_tool else {
            "type": "message", "id": "msg_fixture", "role": "assistant", "status": "completed",
            "content": [{"type": "output_text", "text": "Fixture complete.", "annotations": []}]}
        if call_tool and namespace:
            item["namespace"] = namespace
        response = {"id": "resp_fixture", "object": "response", "created_at": 1, "status": "in_progress", "model": body.get("model"), "output": []}
        events = [{"type": "response.created", "response": response},
                  {"type": "response.output_item.added", "output_index": 0, "item": item},
                  {"type": "response.output_item.done", "output_index": 0, "item": item},
                  {"type": "response.completed", "response": {**response, "status": "completed", "output": [item],
                    "usage": {"input_tokens": 100, "output_tokens": 10, "total_tokens": 110, "input_tokens_details": {"cached_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 0}}}}]
        for index, event in enumerate(events):
            event["sequence_number"] = index
            self.wfile.write(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n".encode())
        self.wfile.flush()


def run(executable, args, workspace, env, log: Path, timeout=60) -> dict:
    try:
        result = subprocess.run([executable, *args], cwd=workspace, env=env, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=timeout,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        output = result.stdout + "\n" + result.stderr
        log.write_text(output, encoding="utf-8")
        return {"exit_code": result.returncode, "log": str(log), "output": output}
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or b"") + (exc.stderr or b"")
        log.write_bytes(output)
        return {"exit_code": None, "timeout": True, "log": str(log), "output": output.decode("utf-8", "replace")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--output", type=Path, default=REPO / "docs/verification/portable-runtimes.json")
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("these pinned binary packages target Windows x64")
    os.environ.pop("SSLKEYLOGFILE", None)
    root = args.root.absolute() if args.root else Path(tempfile.mkdtemp(prefix="octacom-native-runtimes-"))
    root.mkdir(exist_ok=True)
    installed = install(root)
    env = environment(root)
    workspace = fixture(root)
    evidence = {"format": 1, "scope": "native clients, deterministic local model and MCP fixtures, no real model or site", "packages": installed, "workspace": str(workspace), "checks": {}}
    for item in installed:
        result = run(item["executable"], ["--version"], workspace, env, root / (item["name"].replace("/", "_").replace("@", "") + "-version.log"))
        evidence["checks"][item["name"]] = {"version_output": result["output"].strip(), "version_exit": result["exit_code"]}
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Protocol)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    config = {"model": "fixture/test", "provider": {"fixture": {"npm": "@ai-sdk/openai-compatible", "options": {"baseURL": base + "/v1"}, "models": {"test": {"name": "local deterministic fixture", "limit": {"context": 32000, "output": 1024}}}}},
              "mcp": {"site": {"type": "local", "command": [sys.executable, "-B", str(workspace / "fixture-mcp.py")], "enabled": True}}}
    (workspace / "opencode.json").write_text(json.dumps(config), encoding="utf-8")
    result = run(installed[0]["executable"], ["run", "--format", "json", "--model", "fixture/test", "Call the local fixture oxygen_edit_post once."], workspace, env, root / "opencode-native.log", timeout=90)
    evidence["checks"]["opencode-native"] = {"exit_code": result["exit_code"], "timeout": result.get("timeout", False),
        "guard_denial_observed": "Mission confirm" in result["output"], "fixture_effect_observed": (workspace / "unexpected-effect.txt").exists(), "requests": list(Protocol.calls)}
    Protocol.calls.clear()
    claude_env = dict(env, ANTHROPIC_BASE_URL=base, ANTHROPIC_API_KEY="local-protocol-fixture")
    result = run(installed[1]["executable"], ["--print", "--verbose", "--include-hook-events", "--output-format", "stream-json", "--model", "claude-sonnet-4-5", "--no-session-persistence", "--settings", str(workspace / ".claude/settings.json"), "--strict-mcp-config", "--mcp-config", str(workspace / ".mcp.json"), "--allowedTools", "mcp__site__oxygen_edit_post", "--", "Call the local fixture oxygen_edit_post once."], workspace, claude_env, root / "claude-native.log", timeout=90)
    evidence["checks"]["claude-native"] = {"exit_code": result["exit_code"], "timeout": result.get("timeout", False),
        "guard_denial_observed": "Mission confirm" in result["output"], "hook_events_observed": "hook_" in result["output"], "fixture_effect_observed": (workspace / "unexpected-effect.txt").exists(), "requests": list(Protocol.calls), "settings_source": "explicit --settings points to project file; project trust discovery not claimed"}
    Protocol.calls.clear()
    evidence["checks"]["t3-native"] = t3_probe(root, workspace, installed, env, base)
    evidence["checks"]["t3-native"]["requests"] = list(Protocol.calls)
    evidence["checks"]["t3-native"]["fixture_effect_observed"] = (workspace / "unexpected-effect.txt").exists()
    evidence["checks"]["t3-native"]["guard_denial_observed"] = any(item.get("guard_denial_in_input") for item in Protocol.calls)
    evidence["checks"]["t3-native"]["conversation_hooks_observed"] = evidence["checks"]["t3-native"]["guard_denial_observed"]
    Protocol.calls.clear()
    evidence["checks"]["t3-claude-native"] = t3_probe(root, workspace, installed, env, base, "claudeAgent")
    evidence["checks"]["t3-claude-native"]["requests"] = list(Protocol.calls)
    evidence["checks"]["t3-claude-native"]["fixture_effect_observed"] = (workspace / "unexpected-effect.txt").exists()
    evidence["checks"]["t3-claude-native"]["guard_denial_observed"] = any(item.get("guard_denial_in_input") for item in Protocol.calls)
    evidence["checks"]["t3-claude-native"]["conversation_hooks_observed"] = evidence["checks"]["t3-claude-native"]["guard_denial_observed"]
    server.shutdown()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, ensure_ascii=True), encoding="utf-8")
    print(json.dumps({"evidence": str(args.output), "checks": {name: {key: value for key, value in check.items()
                      if key not in ("fixture_hook_trust", "requests", "config_rpc")} for name, check in evidence["checks"].items()}}, indent=2))
    return 0 if all(evidence["checks"][name]["guard_denial_observed"] and
                    not evidence["checks"][name]["fixture_effect_observed"]
                    for name in ("opencode-native", "claude-native", "t3-native", "t3-claude-native")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
