---
description: Deployment workflow for React/Vite frontend and FastAPI backend releases.
---

# /deploy - Production Deployment

$ARGUMENTS

## Purpose

Deploy the standardized stack safely:

- React/Vite frontend
- FastAPI backend
- Docker-based publish flow by default

## Pre-Deployment Checklist

### Frontend

- [ ] frontend build passes
- [ ] lint/test checks pass where applicable
- [ ] static assets and environment config are correct
- [ ] frontend Docker image or container stage builds correctly

### Backend

- [ ] FastAPI app boots cleanly
- [ ] migrations reviewed or applied safely
- [ ] env vars documented and set
- [ ] health endpoint or smoke test is ready
- [ ] backend Docker image builds correctly

### Security and Ops

- [ ] no hardcoded secrets
- [ ] rollback plan exists
- [ ] logs/monitoring path is known

## Platform Guidance

| Platform | Fit |
|---|---|
| Docker Compose | default local/prod publishing baseline |
| Railway | simple full-stack deployments |
| Fly.io | distributed API/app workloads |
| Docker | self-hosted or reproducible deployments |
| Nginx + service manager | VPS/self-hosted setups |

Container delivery should be considered the primary release path unless the user requests another hosting strategy.

## Successful Output

```markdown
## Deployment Complete

- Frontend: deployed
- Backend: deployed
- Health check: passing
- Rollback plan: ready
```
