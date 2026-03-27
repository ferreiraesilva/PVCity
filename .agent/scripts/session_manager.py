#!/usr/bin/env python3
"""
Session Manager - Antigravity Kit
=================================
Analyzes project state, detects tech stack, tracks file statistics, and provides
a summary of the current session.

Usage:
    python .agent/scripts/session_manager.py status [path]
    python .agent/scripts/session_manager.py info [path]
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List


def get_project_root(path: str) -> Path:
    return Path(path).resolve()


def load_json(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def analyze_package_json(root: Path) -> Dict[str, Any]:
    pkg_file = root / "package.json"
    if not pkg_file.exists():
        return {"type": "unknown", "dependencies": {}, "stack": []}

    data = load_json(pkg_file)
    deps = data.get("dependencies", {})
    dev_deps = data.get("devDependencies", {})
    all_deps = {**deps, **dev_deps}

    stack: List[str] = []
    if "react" in all_deps:
        stack.append("React")
    if "vite" in all_deps:
        stack.append("Vite")
    if "tailwindcss" in all_deps:
        stack.append("Tailwind CSS")
    if "typescript" in all_deps:
        stack.append("TypeScript")
    return {
        "name": data.get("name", "unnamed"),
        "version": data.get("version", "0.0.0"),
        "stack": stack,
        "scripts": list(data.get("scripts", {}).keys()),
        "dependencies": all_deps,
    }


def analyze_python_project(root: Path) -> Dict[str, Any]:
    result = {"stack": [], "files": []}

    pyproject = root / "pyproject.toml"
    requirements = root / "requirements.txt"

    text = ""
    for path in (pyproject, requirements):
        if path.exists():
            result["files"].append(path.name)
            try:
                text += "\n" + path.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                pass

    if "fastapi" in text:
        result["stack"].append("FastAPI")
    if "uvicorn" in text:
        result["stack"].append("uvicorn")
    if "sqlalchemy" in text:
        result["stack"].append("SQLAlchemy")
    if "alembic" in text:
        result["stack"].append("Alembic")
    if "pydantic" in text:
        result["stack"].append("Pydantic")

    return result


def count_files(root: Path) -> Dict[str, int]:
    stats = {"created": 0, "modified": 0, "total": 0}
    exclude = {
        ".git",
        "node_modules",
        ".next",
        "dist",
        "build",
        ".agent",
        ".gemini",
        "__pycache__",
        ".venv",
    }

    for root_dir, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in exclude]
        stats["total"] += len(files)
    return stats


def detect_features(root: Path) -> List[str]:
    features = []
    src = root / "src"
    app = root / "app"
    for base in (src, app):
        if base.exists():
            for folder in ("components", "features", "pages", "routes", "services", "api"):
                candidate = base / folder
                if candidate.exists() and candidate.is_dir():
                    for child in candidate.iterdir():
                        if child.is_dir():
                            features.append(child.name)
    return sorted(set(features))[:10]


def merge_stack(package_info: Dict[str, Any], python_info: Dict[str, Any]) -> List[str]:
    merged: List[str] = []
    for item in package_info.get("stack", []) + python_info.get("stack", []):
        if item not in merged:
            merged.append(item)
    return merged


def print_status(root: Path):
    package_info = analyze_package_json(root)
    python_info = analyze_python_project(root)
    stats = count_files(root)
    features = detect_features(root)
    stack = merge_stack(package_info, python_info)

    print("\n=== Project Status ===")
    print(f"\nProject: {package_info.get('name', root.name)}")
    print(f"Path: {root}")
    print(f"Type: {', '.join(stack) if stack else 'Generic'}")
    print("Status: Active")

    print("\nTech Stack:")
    for tech in stack:
        print(f"  - {tech}")

    print(f"\nDetected Modules/Features ({len(features)}):")
    for feat in features:
        print(f"  - {feat}")
    if not features:
        print("  (No distinct feature modules detected)")

    print(f"\nFiles: {stats['total']} total files tracked")
    print("\n====================\n")


def main():
    parser = argparse.ArgumentParser(description="Session Manager")
    parser.add_argument("command", choices=["status", "info"], help="Command to run")
    parser.add_argument("path", nargs="?", default=".", help="Project path")

    args = parser.parse_args()
    root = get_project_root(args.path)

    package_info = analyze_package_json(root)
    python_info = analyze_python_project(root)
    info = {
        "package": package_info,
        "python": python_info,
        "stack": merge_stack(package_info, python_info),
    }

    if args.command == "status":
        print_status(root)
    else:
        print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
