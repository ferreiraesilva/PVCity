---
name: app-builder
description: Main application-building orchestrator for the standardized stack. Detects project type, selects React/Vite/Tailwind and FastAPI defaults, and coordinates implementation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# App Builder

Use this skill when creating new applications or major new product surfaces.

## Standard Defaults

- Frontend web: React + Vite + Tailwind CSS
- Backend API: Python + FastAPI

## Selective Reading

Read only what is needed:

| File | Use |
|---|---|
| `project-detection.md` | detect product type and template |
| `tech-stack.md` | apply the standard stack |
| `agent-coordination.md` | plan multi-agent work |
| `scaffolding.md` | structure folders and responsibilities |
| `feature-building.md` | expand existing projects |
| `templates/SKILL.md` | choose the right template |

## Standard Creation Flow

1. Detect project type
2. Default to the standard stack unless the user overrides it
3. Use React/Vite/Tailwind templates for web UI
4. Use FastAPI template for backend/API
5. Coordinate frontend, backend, database, testing, and deployment agents as needed

## Default Example

User: "Create a customer dashboard with authentication and reporting"

Default interpretation:

- frontend: React + Vite + Tailwind
- backend: FastAPI
- DB: SQL-friendly relational store
- planning: separate frontend/backend tasks with explicit integration points
