---
description: Coordinate multiple agents through the full implementation journey after planning.
---

# /orchestrate - Multi-Agent Delivery

$ARGUMENTS

## Purpose

Coordinate specialist agents for complex work that spans multiple domains.

## Standard Lifecycle

1. clarify
2. plan
3. implement
4. verify
5. prepare publication

## Planning Gate

Before implementation orchestration:

- ensure a root-level plan file exists for the task
- ensure the user has approved the plan

Do not use stale assumptions or old `docs/PLAN.md` conventions.

## Recommended Agent Patterns

### Product-heavy or vague request

- `product-manager` or `product-owner`
- `project-planner`
- optional `explorer-agent`

### Standard full-stack web

- `project-planner`
- `frontend-specialist`
- `backend-specialist`
- `database-architect` when needed
- `test-engineer`
- `qa-automation-engineer` for E2E/regression-sensitive work
- `devops-engineer` for preview/publication concerns

### API-focused

- `project-planner`
- `backend-specialist`
- `security-auditor`
- `test-engineer`
- `qa-automation-engineer` when integration/E2E matters

## Context Passing

Every sub-agent should receive:

- original request
- clarified decisions
- current plan summary
- relevant paths/files
- current implementation phase

## Verification Gate

Before orchestration is considered complete, run the relevant checks:

- security
- lint/type checks
- tests
- UX/accessibility when frontend changed
- schema validation when DB changed
- preview/build checks
- deploy-readiness checks when publication is in scope

## Deliverable

Return one unified synthesis with:

- task summary
- agents involved
- major outputs
- verification completed
- remaining risks, if any
