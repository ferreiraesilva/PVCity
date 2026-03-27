#!/usr/bin/env python3
"""
Auto Preview - Antigravity Kit
==============================
Manages React/Vite frontend and FastAPI backend preview services.

Usage:
    python .agent/scripts/auto_preview.py start
    python .agent/scripts/auto_preview.py stop
    python .agent/scripts/auto_preview.py status
"""

import argparse
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


AGENT_DIR = Path(".agent")
STATE_FILE = AGENT_DIR / "preview-state.json"


def get_project_root() -> Path:
    return Path(".").resolve()


def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def load_state() -> Dict[str, Dict[str, object]]:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: Dict[str, Dict[str, object]]) -> None:
    AGENT_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def detect_frontend(root: Path) -> Optional[Dict[str, object]]:
    pkg = root / "package.json"
    if not pkg.exists():
        return None

    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except Exception:
        return None

    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    scripts = data.get("scripts", {})
    if "vite" in deps and "dev" in scripts:
        return {
            "name": "frontend",
            "type": "vite",
            "cmd": ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"],
            "url": "http://localhost:3000",
            "cwd": str(root),
            "log": str(AGENT_DIR / "preview-frontend.log"),
        }
    return None


def detect_backend(root: Path) -> Optional[Dict[str, object]]:
    candidates = [
        ("app.main:app", root / "app" / "main.py"),
        ("main:app", root / "main.py"),
        ("src.main:app", root / "src" / "main.py"),
    ]

    pyproject = root / "pyproject.toml"
    requirements = root / "requirements.txt"
    text = ""
    for path in (pyproject, requirements):
        if path.exists():
            try:
                text += path.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                pass

    if "fastapi" not in text and "uvicorn" not in text:
        return None

    for app_path, file_path in candidates:
        if file_path.exists():
            return {
                "name": "backend",
                "type": "fastapi",
                "cmd": ["python", "-m", "uvicorn", app_path, "--reload", "--host", "0.0.0.0", "--port", "8000"],
                "url": "http://localhost:8000",
                "cwd": str(root),
                "log": str(AGENT_DIR / "preview-backend.log"),
            }
    return None


def start_service(service: Dict[str, object]) -> Dict[str, object]:
    log_path = Path(str(service["log"]))
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as log:
        process = subprocess.Popen(
            service["cmd"],
            cwd=str(service["cwd"]),
            stdout=log,
            stderr=log,
            shell=False,
        )
    return {
        "pid": process.pid,
        "type": service["type"],
        "url": service["url"],
        "log": service["log"],
    }


def start_preview() -> None:
    state = load_state()
    for service_name, service_state in list(state.items()):
        pid = int(service_state.get("pid", 0))
        if pid and is_running(pid):
            continue
        state.pop(service_name, None)

    root = get_project_root()
    frontend = detect_frontend(root)
    backend = detect_backend(root)

    if not frontend and not backend:
        print("No Vite frontend or FastAPI backend detected.")
        sys.exit(1)

    if frontend and "frontend" not in state:
        state["frontend"] = start_service(frontend)
    if backend and "backend" not in state:
        state["backend"] = start_service(backend)

    save_state(state)
    print("Preview started.")
    for name, service_state in state.items():
        print(f"- {name}: {service_state['type']} -> {service_state['url']} (PID {service_state['pid']})")


def stop_preview() -> None:
    state = load_state()
    if not state:
        print("No preview services found.")
        return

    for service_state in state.values():
        pid = int(service_state.get("pid", 0))
        if not pid:
            continue
        try:
            if sys.platform == "win32":
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(pid)])
            else:
                os.kill(pid, signal.SIGTERM)
        except Exception:
            pass

    if STATE_FILE.exists():
        STATE_FILE.unlink()
    print("Preview stopped.")


def status_preview() -> None:
    state = load_state()
    print("\n=== Preview Status ===")
    if not state:
        print("Status: Stopped")
        print("======================\n")
        return

    running_services = 0
    for name, service_state in state.items():
        pid = int(service_state.get("pid", 0))
        running = pid and is_running(pid)
        if running:
            running_services += 1
        status = "Running" if running else "Stopped"
        print(f"{name}: {status}")
        print(f"  Type: {service_state.get('type')}")
        print(f"  PID: {pid}")
        print(f"  URL: {service_state.get('url')}")
        print(f"  Log: {service_state.get('log')}")
    overall = "Running" if running_services else "Stopped"
    print(f"Overall: {overall}")
    print("======================\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop", "status"])
    args = parser.parse_args()

    if args.action == "start":
        start_preview()
    elif args.action == "stop":
        stop_preview()
    else:
        status_preview()


if __name__ == "__main__":
    main()
