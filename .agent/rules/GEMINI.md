---
trigger: always_on
---

# GEMINI.md - Antigravity Kit

> Global behavior rules for this workspace.

---

## Critical Protocol

Before implementation work:

1. Read the appropriate agent file in `.agent/agents/`
2. Read the agent's relevant skills in `.agent/skills/`
3. Apply the project standard stack unless the user explicitly overrides it

Project standard stack:

- **Web:** React + Vite + Tailwind CSS
- **Backend:** Python + FastAPI

Do not default to removed legacy frameworks or framework-specific hosting flows for standard web/API work in this repository.

Priority:

- `GEMINI.md` > agent file > skill instructions

---

## Request Classifier

| Request Type | Trigger | Result |
|---|---|---|
| `QUESTION` | explain, what is, how does | respond directly |
| `SURVEY` | analyze, inspect, list, overview | explore and summarize |
| `SIMPLE CODE` | fix, change, update, adjust | use the primary agent and edit safely |
| `COMPLEX CODE` | build, create, implement, refactor | ask clarifying questions when needed, then use agent workflow |
| `DESIGN/UI` | page, component, layout, style, dashboard | use `frontend-specialist` |
| `SLASH CMD` | `/plan`, `/create`, `/deploy`, etc. | follow workflow file |

---

## Intelligent Routing

Always route through the best specialist.

Use these defaults:

| Domain | Default Agent | Standard Stack |
|---|---|---|
| Web UI | `frontend-specialist` | React + Vite + Tailwind |
| Backend/API | `backend-specialist` | Python + FastAPI |
| Database | `database-architect` | SQLAlchemy/Alembic-friendly SQL design |
| Tests | `test-engineer` | pytest / Vitest / Playwright based on target |
| Deployment | `devops-engineer` | Railway/Fly.io/Docker/Nginx or equivalent |
| Security | `security-auditor` | OWASP-first review |
| Discovery | `explorer-agent` | read-only mapping |
| Multi-domain | `orchestrator` | React frontend + FastAPI backend coordination |

When responding with agent specialization, announce it concisely:

```markdown
🤖 **Applying knowledge of `@frontend-specialist`...**
```

---

## Universal Rules

### Language

- Think in the most useful language internally.
- Reply in the user's language.
- Keep code identifiers and code comments in English unless the project already uses another convention.

### Clean Code

All code should be:

- clear
- testable
- typed where appropriate
- measured before optimization
- safe with secrets and production operations

### Filesystem Truth

Treat the real files under `.agent/` as the source of truth.
If docs and files disagree, prefer the files or update the docs.

### System Map

Read `.agent/ARCHITECTURE.md` early in the session when you need the broader system picture.

---

## Stack Defaults

### Web

The default web interpretation is:

- React SPA
- Vite
- Tailwind CSS
- React Router for routing when routing is needed
- TanStack Query for server state when async remote data is involved

Do not assume SSR-only or framework-specific routing/rendering behavior by default.

### Backend

The default backend interpretation is:

- Python
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0
- Alembic
- `httpx` for outbound HTTP
- `uvicorn` for local serve and development

If backend preferences are not specified, ask in this order:

1. FastAPI project shape
2. database choice
3. auth needs
4. deployment target

Do not default to non-standard backend frameworks for standard API work in this repository.

---

## Project Type Routing

| Project Type | Primary Agent | Notes |
|---|---|---|
| `WEB` | `frontend-specialist` | React + Vite + Tailwind only by default |
| `BACKEND` | `backend-specialist` | Python + FastAPI only by default |
| `FULL STACK WEB` | `orchestrator` | coordinate `frontend-specialist` + `backend-specialist` |
| `MOBILE` | `mobile-developer` | separate from web |

`mobile-developer` must not be used for standard web React work.

---

## Socratic Gate

Ask clarifying questions before implementation when:

- the request is vague
- multiple architecture choices materially change implementation
- auth/data/deployment requirements are unclear
- the user asks for a new system or large feature

Minimum areas to clarify for new builds:

- purpose
- users
- scope

Additional clarifications for standard full-stack work:

- frontend app shape within React/Vite
- backend data/auth requirements within FastAPI
- deployment expectations

---

## Verification Protocol

When work reaches validation or "final checks", prefer these scripts:

| Check | Script |
|---|---|
| Security scan | `python .agent/skills/vulnerability-scanner/scripts/security_scan.py .` |
| Dependency review | `python .agent/skills/vulnerability-scanner/scripts/dependency_analyzer.py .` |
| Lint | `python .agent/skills/lint-and-validate/scripts/lint_runner.py .` |
| Type coverage | `python .agent/skills/lint-and-validate/scripts/type_coverage.py .` |
| Schema validation | `python .agent/skills/database-design/scripts/schema_validator.py .` |
| Tests | `python .agent/skills/testing-patterns/scripts/test_runner.py .` |
| UX audit | `python .agent/skills/frontend-design/scripts/ux_audit.py .` |
| Accessibility | `python .agent/skills/frontend-design/scripts/accessibility_checker.py .` |
| SEO | `python .agent/skills/seo-fundamentals/scripts/seo_checker.py .` |
| Lighthouse | `python .agent/skills/performance-profiling/scripts/lighthouse_audit.py . <URL>` |
| Bundle analysis | `python .agent/skills/performance-profiling/scripts/bundle_analyzer.py .` |
| E2E | `python .agent/skills/webapp-testing/scripts/playwright_runner.py . <URL>` |

Use `.agent/scripts/checklist.py` for incremental validation and `.agent/scripts/verify_all.py` for broad release verification.

---

## Preview and Deployment Assumptions

- Preview should support React/Vite frontend and FastAPI backend.
- Deployment examples should be neutral or aligned to SPA + API hosting.
- Prefer Docker, Docker Compose, Railway, Fly.io, Nginx, or equivalent container-friendly deployment paths.

---

## Hard Failure Conditions

These are protocol violations:

- writing web guidance that defaults to removed legacy web stacks
- writing backend guidance that defaults to removed legacy backend stacks
- skipping agent and skill loading for implementation work
- citing scripts that do not exist when a real equivalent should be used
- mixing mobile and web routing decisions
