---
description: Preview management for React/Vite frontend and FastAPI backend services.
---

# /preview - Preview Management

$ARGUMENTS

## Commands

```text
/preview
/preview start
/preview stop
/preview restart
/preview check
```

## Behavior

Preview should support:

- a Vite frontend service
- a FastAPI backend service
- combined status when both exist

Examples should report `vite`, `fastapi`, or `fullstack` rather than `nextjs`.

## Technical

Use:

```bash
python .agent/scripts/auto_preview.py start
python .agent/scripts/auto_preview.py stop
python .agent/scripts/auto_preview.py status
```
