---
name: intelligent-routing
description: Automatic agent selection for the standardized workspace stack. Routes web requests to React/Vite specialists and backend requests to FastAPI specialists.
version: 1.0.0
---

# Intelligent Agent Routing

## Core Principle

The router should send standard work toward:

- `frontend-specialist` for React + Vite + Tailwind web work
- `backend-specialist` for Python + FastAPI backend work
- `orchestrator` for cross-domain full-stack work

## Selection Matrix

| User Intent | Selected Agent(s) |
|---|---|
| button, card, layout, dashboard, route, Tailwind | `frontend-specialist` |
| login API, auth backend, endpoint, webhook, service | `backend-specialist` |
| database, migration, schema | `database-architect` + `backend-specialist` |
| bug, failing flow, broken integration | `debugger` |
| deploy, release, production | `devops-engineer` |
| security, vulnerability, auth review | `security-auditor` |
| full product, frontend + backend, portal + API | `orchestrator` |

## Response Format

```markdown
🤖 **Applying knowledge of `@frontend-specialist`...**
```

## Routing Constraints

- Standard web requests should stay on the standardized React/Vite path
- Standard API requests should stay on the standardized FastAPI path
- Multi-domain product requests should assume React/Vite + FastAPI unless the user overrides it
