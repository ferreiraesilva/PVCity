---
name: monorepo-turborepo
description: Turborepo monorepo template principles for React/Vite frontend and FastAPI backend workspaces.
---

# Turborepo Monorepo Template

## Tech Stack

| Component | Technology |
|---|---|
| Build System | Turborepo |
| Package Manager | pnpm |
| Apps | React/Vite frontend + FastAPI backend |
| Packages | Shared UI, config, types |
| Language | TypeScript for frontend packages, Python for backend service |

## Directory Structure

```text
project-name/
|-- apps/
|   |-- web/             # React + Vite app
|   |-- api/             # FastAPI service
|   `-- docs/            # Documentation
|-- packages/
|   |-- ui/              # Shared UI
|   |-- config/          # ESLint, TS, Tailwind
|   |-- types/           # Shared frontend types/contracts
|   `-- utils/           # Shared utilities
|-- turbo.json
|-- pnpm-workspace.yaml
`-- package.json
```

## Best Practices

- keep frontend and backend boundaries explicit
- share contracts intentionally
- use workspace tooling for frontend packages
- publish/deploy services through container-friendly flows
