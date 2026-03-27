#!/usr/bin/env python3
"""
Lightweight bundle analyzer for Antigravity Kit.
Reports presence of frontend build output directories and package manifest hints.
"""

import sys
from pathlib import Path


def main() -> int:
    project = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    outputs = []
    for folder in ("dist", "build"):
        path = project / folder
        if path.exists():
            outputs.append(folder)

    package_json = project / "package.json"
    if package_json.exists():
        print("Bundle analyzer summary:")
        print("- package.json found")
        if outputs:
            for output in outputs:
                print(f"- build output directory found: {output}")
        else:
            print("- no build output directory found yet")
        return 0

    print("Bundle analyzer skipped: no frontend package.json found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
