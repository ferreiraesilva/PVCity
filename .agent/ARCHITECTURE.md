# Antigravity Kit Architecture

> Standardized for React + Vite + Tailwind on the web, and Python + FastAPI on the backend.

---

## Overview

Antigravity Kit is a modular workspace system built around:

- **20 Specialist Agents** for domain-specific execution
- **Workspace Skills** for progressive knowledge loading
- **Workflows** for repeatable planning, implementation, preview, and deployment flows
- **Validation Scripts** for security, quality, UX, performance, and release checks

The official stack for this workspace is:

- **Frontend Web:** React SPA + Vite + Tailwind CSS
- **Backend API:** Python + FastAPI

Alternative stacks may still exist in the repository as legacy material, but they are not the default path and must not be suggested first.

---

## Directory Structure

```text
.agent/
|-- ARCHITECTURE.md
|-- agents/
|-- rules/
|-- scripts/
|-- skills/
|-- workflows/
`-- .shared/
```

---

## Agents

The main agent routing for the standardized stack is:

| Agent | Primary Focus | Default Skills |
|---|---|---|
| `frontend-specialist` | React web UI, Vite, Tailwind, SPA architecture | `frontend-design`, `react-vite-expert`, `tailwind-patterns` |
| `backend-specialist` | FastAPI, business logic, API design, integration | `python-patterns`, `api-patterns`, `database-design` |
| `database-architect` | Schema design, SQL, migrations, indexing | `database-design` |
| `devops-engineer` | Deployment, environments, rollback, preview ops | `deployment-procedures`, `docker-expert`, `server-management` |
| `test-engineer` | Unit, integration, E2E strategy | `testing-patterns`, `tdd-workflow`, `webapp-testing` |
| `security-auditor` | Security posture and remediation | `vulnerability-scanner`, `red-team-tactics` |
| `performance-optimizer` | Frontend and backend performance | `performance-profiling` |
| `project-planner` | Planning, decomposition, execution sequencing | `app-builder`, `plan-writing`, `brainstorming` |
| `orchestrator` | Multi-agent coordination | `parallel-agents`, `behavioral-modes` |
| `explorer-agent` | Codebase discovery and mapping | `architecture`, `systematic-debugging` |

All other agents remain available for specialized domains such as mobile, game development, SEO, documentation, QA, and debugging.

---

## Skills

### Official Web & API Stack Skills

| Skill | Purpose |
|---|---|
| `react-vite-expert` | React SPA architecture, Vite workflows, React Router, TanStack Query, forms, performance |
| `frontend-design` | UI/UX thinking, layout, accessibility, design decisions |
| `tailwind-patterns` | Tailwind CSS architecture and component styling patterns |
| `python-patterns` | Python structure, async decisions, typing, FastAPI thinking |
| `api-patterns` | REST, OpenAPI, request/response shape, auth and validation |
| `database-design` | Schema design, migrations, indexing, normalization |

### Supporting Skills

| Skill | Purpose |
|---|---|
| `app-builder` | Project detection, tech stack selection, template routing |
| `parallel-agents` | Multi-agent orchestration patterns |
| `brainstorming` | Socratic discovery and requirement clarification |
| `lint-and-validate` | Linting, static checks, type coverage |
| `testing-patterns` | Test design and test strategy |
| `webapp-testing` | Browser and E2E testing |
| `performance-profiling` | Lighthouse, bundle checks, runtime profiling |
| `vulnerability-scanner` | Security scans and dependency checks |
| `deployment-procedures` | Deployment sequencing and release hygiene |
| `server-management` | Operations, service supervision, environments |

### Legacy or Secondary Material

Some skill folders remain in the repository for historical or niche usage. They should not be auto-selected or documented as defaults for web/API work if they conflict with the official stack.

Examples:

- legacy mobile- or platform-specific materials that are outside the default web/API path

### Deployment Skill

| Skill | Purpose |
|---|---|
| `docker-expert` | Dockerfiles, Compose, image strategy, containerized delivery |

---

## Workflows

| Workflow | Purpose |
|---|---|
| `/plan` | Produce implementation plans and task breakdown |
| `/create` | Create new applications using the standardized stack |
| `/debug` | Investigate and fix defects |
| `/enhance` | Improve existing systems |
| `/orchestrate` | Coordinate multiple agents |
| `/preview` | Start, stop, and inspect local preview services |
| `/test` | Execute project testing workflow |
| `/deploy` | Production/staging deployment flow |
| `/status` | Summarize project and work progress |
| `/brainstorm` | Clarify goals, users, and scope |
| `/ui-ux-pro-max` | Use shared design references, prioritizing React or HTML + Tailwind |

---

## Lifecycle Coverage

The intended software-delivery journey in this workspace is:

| Phase | Primary Agents | Primary Workflows / Skills |
|---|---|---|
| Ideation | `product-manager`, `product-owner` | `/brainstorm`, `brainstorming` |
| Discovery | `explorer-agent` | survey/intel flows, `architecture`, `systematic-debugging` |
| Planning | `project-planner` | `/plan`, `plan-writing`, `app-builder` |
| Implementation | `frontend-specialist`, `backend-specialist`, `database-architect`, `orchestrator` | `/create`, `/enhance`, `react-vite-expert`, `python-patterns` |
| Validation | `test-engineer`, `qa-automation-engineer`, `security-auditor`, `performance-optimizer` | `/test`, `checklist.py`, `verify_all.py` |
| Preview | `devops-engineer` | `/preview`, `auto_preview.py` |
| Publication | `devops-engineer` | `/deploy`, `deployment-procedures`, `docker-expert` |
| Documentation Handoff | `documentation-writer` | `documentation-templates` |

This repository intentionally scopes the lifecycle through publication. Ongoing production observability and operational stewardship are out of scope for this kit.

---

## Validation Scripts

Top-level script runners:

- `.agent/scripts/checklist.py`
- `.agent/scripts/verify_all.py`
- `.agent/scripts/auto_preview.py`
- `.agent/scripts/session_manager.py`

Key referenced skill scripts:

- `.agent/skills/vulnerability-scanner/scripts/security_scan.py`
- `.agent/skills/vulnerability-scanner/scripts/dependency_analyzer.py`
- `.agent/skills/lint-and-validate/scripts/lint_runner.py`
- `.agent/skills/lint-and-validate/scripts/type_coverage.py`
- `.agent/skills/database-design/scripts/schema_validator.py`
- `.agent/skills/testing-patterns/scripts/test_runner.py`
- `.agent/skills/frontend-design/scripts/ux_audit.py`
- `.agent/skills/frontend-design/scripts/accessibility_checker.py`
- `.agent/skills/seo-fundamentals/scripts/seo_checker.py`
- `.agent/skills/performance-profiling/scripts/lighthouse_audit.py`
- `.agent/skills/performance-profiling/scripts/bundle_analyzer.py`
- `.agent/skills/webapp-testing/scripts/playwright_runner.py`
- `.agent/skills/mobile-design/scripts/mobile_audit.py`

---

## Skill Loading Protocol

1. Classify the request.
2. Select the appropriate agent.
3. Read the agent file.
4. Read only the relevant `SKILL.md` files listed by that agent.
5. Load only the specific companion references/scripts needed for the request.

Always treat the actual filesystem as the source of truth over stale documentation.
