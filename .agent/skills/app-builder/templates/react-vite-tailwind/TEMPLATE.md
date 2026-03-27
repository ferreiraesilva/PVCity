---
name: react-vite-tailwind
description: Standard React SPA template using Vite and Tailwind CSS.
---

# React Vite Tailwind Template

## Tech Stack

| Component | Technology |
|---|---|
| Framework | React |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| Routing | React Router |
| Server State | TanStack Query |
| Testing | Vitest + Testing Library |

## Suggested Structure

```text
src/
|-- app/
|-- components/
|-- features/
|-- pages/
|-- routes/
|-- services/
|-- styles/
`-- main.tsx
```

## Container Publishing

Include:

- `Dockerfile` for multi-stage frontend build
- optional `nginx.conf` for SPA fallback and static serving

Recommended runtime shape:

- build Vite assets in a Node stage
- serve compiled assets from a lightweight web server container

## Notes

- Use this for standard dashboards, portals, CRUD apps, and SPAs.
- Pair with `python-fastapi` when backend/API work is required.
