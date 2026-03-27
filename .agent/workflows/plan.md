---
description: Create an implementation plan using the project-planner agent. Planning only, no product code.
---

# /plan - Project Planning

$ARGUMENTS

## Purpose

Create a planning artifact for the requested work before implementation.

## Rules

1. No product code during this workflow
2. Use `project-planner` as the lead planning agent
3. Use `product-manager` or `product-owner` when the request is vague, business-heavy, or needs clearer scope
4. Use `explorer-agent` when repository discovery is needed before task breakdown
5. Produce a plan file in the project root, not in `docs/`

## Plan Artifact Contract

The plan file should use a dynamic root-level name:

- `./{task-slug}.md`

Examples:

- `./customer-portal.md`
- `./auth-refactor.md`
- `./dashboard-analytics.md`

## Standard Flow

1. Clarify goal, users, and scope
2. Use `product-manager` or `product-owner` if requirement shaping is needed
3. Use `project-planner` to produce implementation phases and agent assignments
4. Add explicit verification steps
5. Stop after the plan is created and ask for approval before implementation

## Expected Plan Contents

- goal and success criteria
- target stack
- scope and exclusions
- task breakdown by agent
- verification plan
- publication considerations when relevant

## After Planning

Report:

```text
[OK] Plan created: ./{task-slug}.md

Next:
- Review and approve the plan
- Then use /create, /enhance, or implementation flow
```
