---
name: python-fastapi
description: Standard FastAPI backend template. Uses Pydantic v2, SQLAlchemy 2.0, Alembic, and uvicorn.
---

# FastAPI API Template

## Tech Stack

| Component | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python 3.11+ |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| HTTP Client | httpx |
| Local Runtime | uvicorn |

## Suggested Structure

```text
backend/
|-- alembic/
|-- app/
|   |-- main.py
|   |-- core/
|   |-- api/
|   |-- models/
|   |-- schemas/
|   |-- services/
|   |-- repositories/
|   `-- dependencies/
|-- tests/
|-- pyproject.toml
`-- .env.example
```

## Best Practices

- keep route handlers thin
- validate inputs and outputs with Pydantic
- use SQLAlchemy 2.0 patterns consistently
- manage schema evolution with Alembic
- expose clean OpenAPI documentation
- use async for I/O-heavy work

## Container Publishing

Include:

- `Dockerfile` for the FastAPI service
- optional `docker-compose.yml` when running with companion services

Recommended runtime shape:

- install dependencies in image build
- run the app with `uvicorn`
- expose port `8000`
