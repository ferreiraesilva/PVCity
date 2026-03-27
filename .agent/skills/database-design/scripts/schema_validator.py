#!/usr/bin/env python3
"""
Schema Validator - Database schema validation
Validates schema artifacts for the standardized backend stack and compatible legacy formats.

Usage:
    python schema_validator.py <project_path>

Checks:
    - SQLAlchemy model presence and conventions
    - Alembic migration presence
    - Prisma schema basics (if present)
    - Drizzle schema presence (lightweight)
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def find_schema_targets(project_path: Path) -> list:
    targets = []

    prisma_files = list(project_path.glob("**/prisma/schema.prisma"))
    targets.extend([("prisma", f) for f in prisma_files])

    drizzle_files = list(project_path.glob("**/drizzle/*.ts"))
    drizzle_files.extend(project_path.glob("**/schema/*.ts"))
    for file_path in drizzle_files:
        if "schema" in file_path.name.lower() or "table" in file_path.name.lower():
            targets.append(("drizzle", file_path))

    sqlalchemy_candidates = []
    for pattern in ("**/models.py", "**/models/*.py", "**/db/models.py", "**/app/models/*.py"):
        sqlalchemy_candidates.extend(project_path.glob(pattern))
    seen = set()
    for file_path in sqlalchemy_candidates:
        if file_path.is_file():
            key = str(file_path.resolve())
            if key not in seen:
                seen.add(key)
                targets.append(("sqlalchemy", file_path))

    alembic_env = list(project_path.glob("**/alembic/env.py"))
    versions = list(project_path.glob("**/alembic/versions/*.py"))
    if alembic_env or versions:
        if alembic_env:
            targets.extend([("alembic", f) for f in alembic_env])
        else:
            targets.extend([("alembic", f) for f in versions[:1]])

    return targets[:25]


def validate_prisma_schema(file_path: Path) -> list:
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        models = re.findall(r"model\s+(\w+)\s*{([^}]+)}", content, re.DOTALL)

        for model_name, model_body in models:
            if not model_name[:1].isupper():
                issues.append(f"Model '{model_name}' should be PascalCase")
            if "@id" not in model_body and "id" not in model_body.lower():
                issues.append(f"Model '{model_name}' might be missing @id field")
            if "createdAt" not in model_body and "created_at" not in model_body:
                issues.append(f"Model '{model_name}' missing createdAt field (recommended)")

            foreign_keys = re.findall(r"(\w+Id)\s+\w+", model_body)
            for fk in foreign_keys:
                if f"@@index([{fk}])" not in content and f'@@index(["{fk}"])' not in content:
                    issues.append(f"Consider adding @@index([{fk}]) for better query performance in {model_name}")

        enums = re.findall(r"enum\s+(\w+)\s*{", content)
        for enum_name in enums:
            if not enum_name[:1].isupper():
                issues.append(f"Enum '{enum_name}' should be PascalCase")
    except Exception as exc:
        issues.append(f"Error reading schema: {str(exc)[:80]}")
    return issues


def validate_sqlalchemy_model(file_path: Path) -> list:
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lower = content.lower()

        has_model_signal = any(
            signal in content
            for signal in (
                "DeclarativeBase",
                "declarative_base",
                "Mapped[",
                "mapped_column",
                "__tablename__",
            )
        )
        if not has_model_signal:
            return issues

        if "__tablename__" not in content:
            issues.append(f"{file_path.name}: SQLAlchemy model file missing __tablename__ declarations")

        if "mapped_column" in content and "Mapped[" not in content:
            issues.append(f"{file_path.name}: mapped_column used without typed Mapped annotations")

        if "ForeignKey(" in content and "relationship(" not in content:
            issues.append(f"{file_path.name}: foreign keys found without obvious relationship() usage")

        if "created_at" not in lower and "createdat" not in lower:
            issues.append(f"{file_path.name}: no created_at field detected (recommended for auditable entities)")
    except Exception as exc:
        issues.append(f"{file_path.name}: error reading SQLAlchemy models: {str(exc)[:80]}")
    return issues


def validate_alembic_target(file_path: Path) -> list:
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        if file_path.name == "env.py":
            if "target_metadata" not in content:
                issues.append("Alembic env.py missing target_metadata wiring")
        else:
            if "revision =" not in content and "revision=" not in content:
                issues.append(f"{file_path.name}: migration missing revision identifier")
            if "upgrade(" not in content:
                issues.append(f"{file_path.name}: migration missing upgrade()")
    except Exception as exc:
        issues.append(f"{file_path.name}: error reading Alembic file: {str(exc)[:80]}")
    return issues


def validate_drizzle_target(file_path: Path) -> list:
    issues = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        if "pgTable" not in content and "sqliteTable" not in content and "mysqlTable" not in content:
            issues.append(f"{file_path.name}: no obvious Drizzle table definition found")
    except Exception as exc:
        issues.append(f"{file_path.name}: error reading Drizzle schema: {str(exc)[:80]}")
    return issues


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    print(f"\n{'=' * 60}")
    print("[SCHEMA VALIDATOR] Database Schema Validation")
    print(f"{'=' * 60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    targets = find_schema_targets(project_path)
    print(f"Found {len(targets)} schema targets")

    if not targets:
        output = {
            "script": "schema_validator",
            "project": str(project_path),
            "schemas_checked": 0,
            "issues_found": 0,
            "passed": True,
            "message": "No schema targets found",
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)

    all_issues = []
    for target_type, file_path in targets:
        print(f"\nValidating: {file_path.name} ({target_type})")
        if target_type == "prisma":
            issues = validate_prisma_schema(file_path)
        elif target_type == "sqlalchemy":
            issues = validate_sqlalchemy_model(file_path)
        elif target_type == "alembic":
            issues = validate_alembic_target(file_path)
        else:
            issues = validate_drizzle_target(file_path)

        if issues:
            all_issues.append(
                {
                    "file": str(file_path),
                    "type": target_type,
                    "issues": issues,
                }
            )

    print("\n" + "=" * 60)
    print("SCHEMA ISSUES")
    print("=" * 60)

    if all_issues:
        for item in all_issues:
            print(f"\n{Path(item['file']).name} ({item['type']}):")
            for issue in item["issues"][:6]:
                print(f"  - {issue}")
            if len(item["issues"]) > 6:
                print(f"  ... and {len(item['issues']) - 6} more issues")
    else:
        print("No schema issues found!")

    total_issues = sum(len(item["issues"]) for item in all_issues)
    output = {
        "script": "schema_validator",
        "project": str(project_path),
        "schemas_checked": len(targets),
        "issues_found": total_issues,
        "passed": True,
        "issues": all_issues,
    }

    print("\n" + json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
