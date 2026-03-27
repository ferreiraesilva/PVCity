---
name: parallel-agents
description: Multi-agent orchestration patterns for React/Vite frontend work, FastAPI backend work, and supporting review/verification specialists.
allowed-tools: Read, Glob, Grep
---

# Native Parallel Agents

Use orchestration when a task touches multiple domains.

## Standard Multi-Agent Patterns

### Full-Stack Web

1. `explorer-agent` for discovery when needed
2. `frontend-specialist` for React/Vite/Tailwind work
3. `backend-specialist` for FastAPI work
4. `test-engineer` for verification

### API + Security

1. `backend-specialist`
2. `security-auditor`
3. `test-engineer`

### UI + Performance

1. `frontend-specialist`
2. `performance-optimizer`
3. `test-engineer`

## Routing Defaults

- Web UI requests -> React/Vite frontend path
- API requests -> FastAPI backend path
- Complex full-stack requests -> orchestrator coordinating both

Do not present removed legacy stacks as the first-path answer for standard requests in this repository.
