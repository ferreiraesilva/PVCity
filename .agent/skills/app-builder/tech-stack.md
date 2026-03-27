# Tech Stack Selection

> Default technology choices for this workspace.

## Default Stack

```yaml
frontend:
  framework: React 19+
  build_tool: Vite
  styling: Tailwind CSS v4
  routing: React Router
  server_state: TanStack Query
  testing: Vitest + Testing Library

backend:
  language: Python 3.11+
  framework: FastAPI
  validation: Pydantic v2
  orm: SQLAlchemy 2.0
  migrations: Alembic
  http_client: httpx
  local_server: uvicorn

database:
  primary: PostgreSQL
  local_option: SQLite

deployment:
  frontend: static hosting or containerized app hosting
  backend: Railway, Fly.io, Docker, or equivalent
```

## Notes

- This repository uses the standardized web and API stack by default.
- Use alternatives only when the user explicitly asks for them or the existing codebase requires them.
