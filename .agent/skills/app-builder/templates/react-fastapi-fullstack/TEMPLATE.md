---
name: react-fastapi-fullstack
description: Standard full-stack template using React/Vite/Tailwind for the frontend and FastAPI for the backend.
---

# React FastAPI Full-Stack Template

## Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + Tailwind CSS |
| Routing | React Router |
| Server State | TanStack Query |
| Backend | FastAPI |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |

## Suggested Layout

```text
project/
|-- frontend/
|   `-- src/
|-- backend/
|   |-- app/
|   `-- alembic/
`-- docs/
```

## Container Publishing

Include by default:

- `frontend/Dockerfile`
- `backend/Dockerfile`
- root `docker-compose.yml`

Recommended flow:

- frontend builds static assets and serves them from a lightweight container
- backend runs FastAPI in its own container
- Compose coordinates service networking and environment wiring

## Notes

- Use for dashboards, internal tools, portals, and full product surfaces.
- Keep frontend and backend as separate services with clear API contracts.
