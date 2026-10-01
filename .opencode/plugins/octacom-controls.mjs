import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import path from "node:path";

function workspace(directory) {
  let current = path.resolve(directory);
  while (true) {
    if (existsSync(path.join(current, "AGENTS.md")) && existsSync(path.join(current, ".codex", "hooks"))) return current;
    const parent = path.dirname(current);
    if (parent === current) throw new Error("Octacom workspace not found");
    current = parent;
  }
}

function invoke(root, script, event) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.env.OCTACOM_PYTHON || "python", ["-B", path.join(root, ".codex", "hooks", script)], {
      cwd: root, windowsHide: true, shell: false, stdio: ["pipe", "pipe", "pipe"],
    });
    let stdout = "";
    const timer = setTimeout(() => { child.kill(); reject(new Error("Octacom control timed out")); }, 8000);
    child.stdout.setEncoding("utf8");
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
      if (stdout.length > 1024 * 1024) { child.kill(); reject(new Error("Octacom control output too large")); }
    });
    // Do not copy subprocess diagnostics, arguments, or prompts into model context.
    child.stderr.resume();
    child.on("error", () => { clearTimeout(timer); reject(new Error("Octacom control could not start")); });
    child.on("close", (code) => {
      clearTimeout(timer);
      if (code !== 0) reject(new Error("Octacom control failed"));
      else resolve(stdout);
    });
    child.stdin.on("error", () => {});
    child.stdin.end(JSON.stringify(event));
  });
}

async function toolName(root, nativeName) {
  if (typeof nativeName !== "string" || !nativeName) throw new Error("Missing tool name");
  if (nativeName.startsWith("mcp__")) return nativeName;
  let map = {};
  try { map = JSON.parse(await readFile(path.join(root, ".octacom", "runtime-tool-map.json"), "utf8")); }
  catch (error) { if (error.code !== "ENOENT") throw new Error("Invalid Octacom tool map"); }
  const name = map.opencode?.[nativeName];
  if (name !== undefined) {
    if (typeof name !== "string" || !/^mcp__[^\s]+__[^\s]+$/.test(name)) throw new Error("Invalid mapped MCP name");
    return name;
  }
  if (/oxygen_|wordpress_|wp_/.test(nativeName)) throw new Error("Register the exact OpenCode MCP name in .octacom/runtime-tool-map.json");
  return nativeName;
}

function response(output) {
  // OpenCode exposes rendered output, not a guaranteed raw MCP CallToolResult.
  if (typeof output?.output !== "string") return { isError: true };
  try {
    const parsed = JSON.parse(output.output);
    if (parsed && typeof parsed === "object" && !Array.isArray(parsed) &&
        (Object.hasOwn(parsed, "content") || Object.hasOwn(parsed, "structuredContent") || Object.hasOwn(parsed, "isError"))) return parsed;
  } catch {}
  return { content: [{ type: "text", text: output.output }] };
}

export const OctacomControls = async ({ directory }) => {
  const root = workspace(directory);
  const policy = (await invoke(root, "inject_skill_gate.py", { hook_event_name: "SessionStart", cwd: root, runtime: "opencode" })).trim();
  async function toolEvent(kind, input, args, output) {
    if (typeof input.sessionID !== "string" || !input.sessionID) throw new Error("Missing OpenCode session identity");
    const event = { hook_event_name: kind, cwd: root, runtime: "opencode", session_id: input.sessionID,
      tool_name: await toolName(root, input.tool), tool_input: args, tool_use_id: input.callID };
    if (kind === "PostToolUse") event.tool_response = response(output);
    const result = JSON.parse(await invoke(root, "oxygen_site_gate.py", event));
    if (!result || typeof result !== "object" || Array.isArray(result)) throw new Error("Invalid Octacom control response");
    if (result.hookSpecificOutput?.permissionDecision === "deny") {
      throw new Error(result.hookSpecificOutput.permissionDecisionReason || "Octacom action denied");
    }
    if (result.decision === "block") throw new Error(result.reason || "Octacom action blocked");
    if (kind === "PreToolUse" && result.systemMessage) throw new Error("Octacom control reported an error");
    return result;
  }
  return {
    "tool.execute.before": async (input, output) => toolEvent("PreToolUse", input, output.args),
    "tool.execute.after": async (input, output) => {
      const result = await toolEvent("PostToolUse", input, input.args, output);
      for (const context of [result.hookSpecificOutput?.additionalContext, result.systemMessage]) {
        if (typeof context === "string" && context) output.output += "\n\n" + context;
      }
    },
    "experimental.chat.system.transform": async (_input, output) => {
      if (!output.system.includes(policy)) output.system.push(policy);
    },
    "experimental.session.compacting": async (_input, output) => {
      if (!output.context.includes(policy)) output.context.push(policy);
    },
  };
};
