---
description: Test planning, generation, and execution for React/Vite frontend, FastAPI backend, integration flows, and publication smoke checks.
---

# /test - Testing Workflow

$ARGUMENTS

## Purpose

Use this workflow to define, generate, or execute tests across the standardized stack.

## Standard Coverage Model

### Frontend

- component tests
- route/screen behavior
- form states
- API integration states

### Backend

- FastAPI endpoint tests
- service-level unit tests
- schema/validation tests
- auth and permission tests

### Full-stack

- frontend/backend integration paths
- end-to-end user flows
- preview smoke checks
- publish/container smoke checks when relevant

## Agent Roles

| Agent | Role |
|---|---|
| `test-engineer` | unit/integration strategy, targeted tests, coverage reasoning |
| `qa-automation-engineer` | E2E, regression, pipeline-oriented automation, browser flows |
| `backend-specialist` | backend test data seams and API structure context |
| `frontend-specialist` | frontend interaction and route behavior context |

## Sub-commands

```text
/test
/test [file|feature|flow]
/test coverage
/test e2e
/test smoke
```

## Default Stack Guidance

| Target | Typical Tools |
|---|---|
| React/Vite frontend | Vitest + Testing Library |
| FastAPI backend | pytest + pytest-asyncio |
| Browser/E2E | Playwright |
| Publish smoke | container boot + health/smoke checks |

## Output Expectations

### If generating or planning tests

Return:

- target under test
- test layers to add
- happy path
- sad path
- edge cases
- integration expectations

### If executing tests

Return:

- what ran
- pass/fail summary
- failed scenarios
- next fix recommendation

## Example Focus Areas

- React form submits to FastAPI endpoint
- FastAPI auth rejects invalid token
- dashboard route renders loading/empty/error/success states
- Dockerized backend boots and answers health check
- full login flow works through browser automation

## Principles

- test behavior, not internal implementation details
- prefer project-native frameworks over generic examples
- cover happy path and failure path
- keep frontend, backend, and E2E responsibilities explicit
