---
description: Create new applications using the standardized stack. Defaults to React/Vite/Tailwind for web and FastAPI for backend.
---

# /create - Create Application

$ARGUMENTS

## Task

Create a new application using these defaults unless the user explicitly overrides them:

- Web frontend: React + Vite + Tailwind CSS
- Backend API: Python + FastAPI

## Flow

1. Analyze the request
2. Use `product-manager` or `product-owner` when the request needs PRD/MVP/scope clarification
3. Clarify purpose, users, and scope when needed
4. Use `project-planner` for task breakdown
5. For frontend work, scaffold or inspect the visual intake:
   - `python .agent/scripts/design_system_pipeline.py init --project <ProjectName>`
   - `python .agent/scripts/design_system_pipeline.py status --project <ProjectName>`
6. If the user already provided references, generate the design system before frontend implementation:
   - `python .agent/scripts/design_system_pipeline.py generate --project <ProjectName> --prompt-missing`
7. Use `app-builder` to choose templates
8. Coordinate:
   - `frontend-specialist` for React/Vite/Tailwind UI
   - `backend-specialist` for FastAPI APIs
   - `database-architect` when persistence is required
   - `test-engineer` for unit/integration verification
   - `qa-automation-engineer` when E2E/regression matters
   - `documentation-writer` when deliverables require README/API docs/handover docs
9. Use preview workflow after implementation
10. Use deploy workflow when publication is requested

## Examples

```text
/create admin dashboard
/create customer portal with authentication
/create landing page for a SaaS product
/create API for order management
```
