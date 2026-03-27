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
5. Use `app-builder` to choose templates
6. Coordinate:
   - `frontend-specialist` for React/Vite/Tailwind UI
   - `backend-specialist` for FastAPI APIs
   - `database-architect` when persistence is required
   - `test-engineer` for unit/integration verification
   - `qa-automation-engineer` when E2E/regression matters
   - `documentation-writer` when deliverables require README/API docs/handover docs
7. Use preview workflow after implementation
8. Use deploy workflow when publication is requested

## Examples

```text
/create admin dashboard
/create customer portal with authentication
/create landing page for a SaaS product
/create API for order management
```
