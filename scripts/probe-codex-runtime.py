"""Read effective Codex config, hooks and skills via the installed app-server."""

from __future__ import annotations

import argparse
import json
import queue
import subprocess
import threading
from pathlib import Path


class Runtime:
    def __init__(self, cwd: Path, command: list[str] | None = None):
        self.process = subprocess.Popen(command or ["codex", "app-server", "--stdio"],
            cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, text=True, encoding="utf-8")
        self.messages: queue.Queue = queue.Queue()
        self.sequence = 0
        self.notifications: list[dict] = []
        threading.Thread(target=self._read, daemon=True).start()
        self.request("initialize", {"clientInfo": {"name": "octacom-control-probe", "version": "1"},
                    "capabilities": {"experimentalApi": True}})
        self.send({"method": "initialized", "params": {}})

    def _read(self):
        for line in self.process.stdout:
            try:
                self.messages.put(json.loads(line))
            except ValueError:
                pass
        self.messages.put({"error": "app-server ended"})

    def send(self, message: dict):
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method: str, params: dict, timeout: int = 45):
        self.sequence += 1
        identity = self.sequence
        self.send({"id": identity, "method": method, "params": params})
        while True:
            message = self.messages.get(timeout=timeout)
            if message.get("id") == identity:
                if "error" in message:
                    raise ValueError(f"{method}: {message['error']}")
                return message["result"]
            if "method" in message:
                self.notifications.append(message)
            elif "error" in message:
                raise ValueError(str(message["error"]))

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait()


def probe(cwd: Path) -> dict:
    runtime = Runtime(cwd)
    try:
        config = runtime.request("config/read", {"cwd": str(cwd), "includeLayers": True})
        hooks = runtime.request("hooks/list", {"cwds": [str(cwd)]})
        skills = runtime.request("skills/list", {"cwds": [str(cwd)], "forceReload": True})
        effective = config.get("config", {})
        return {"cwd": str(cwd), "config": {
            key: effective.get(key) for key in ("features", "skills", "project_doc_max_bytes")},
            "layers": [{key: layer.get(key) for key in ("name", "disabledReason")} for layer in config.get("layers", [])],
            "hooks": hooks, "skills": [{"cwd": entry.get("cwd"), "errors": entry.get("errors"),
                "skills": [{key: skill.get(key) for key in ("name", "path", "enabled", "scope")}
                    for skill in entry.get("skills", []) if "wordpress-development-kit" in skill.get("path", "")
                    or str(cwd).lower() in skill.get("path", "").lower()]}
                for entry in skills.get("data", [])]}
    finally:
        runtime.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = probe(args.cwd.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Runtime probe: {args.output.resolve()}")


if __name__ == "__main__":
    main()
