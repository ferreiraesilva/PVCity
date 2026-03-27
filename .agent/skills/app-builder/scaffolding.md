# Project Scaffolding

> Directory structure and core files for new projects in the standardized stack.

## Standard Full-Stack Structure

```text
project-name/
|-- frontend/
|   |-- src/
|   |   |-- app/
|   |   |-- components/
|   |   |-- features/
|   |   |-- pages/
|   |   |-- routes/
|   |   |-- services/
|   |   `-- main.tsx
|   |-- public/
|   |-- package.json
|   `-- vite.config.ts
|-- backend/
|   |-- app/
|   |   |-- main.py
|   |   |-- core/
|   |   |-- api/
|   |   |-- models/
|   |   |-- schemas/
|   |   |-- services/
|   |   |-- repositories/
|   |   `-- dependencies/
|   |-- alembic/
|   `-- pyproject.toml
|-- .env.example
`-- README.md
```

## Structure Principles

| Principle | Implementation |
|---|---|
| Feature isolation | React features grouped clearly |
| Thin transport layers | routes/routers stay thin |
| Clear API boundary | frontend services call backend HTTP APIs explicitly |
| Shared UI primitives | reusable frontend components live in a stable shared layer |
| Backend layering | FastAPI routes -> services -> repositories |

## Core Files

| File | Purpose |
|---|---|
| `frontend/package.json` | frontend dependencies and scripts |
| `frontend/vite.config.ts` | Vite configuration |
| `frontend/src/main.tsx` | React entrypoint |
| `backend/app/main.py` | FastAPI app entrypoint |
| `backend/pyproject.toml` | Python dependencies and tool config |
| `backend/alembic/` | migration history |
| `.env.example` | environment template |
