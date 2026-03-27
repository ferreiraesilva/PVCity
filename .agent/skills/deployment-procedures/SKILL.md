---
name: deployment-procedures
description: Production deployment principles for the standardized stack, with Docker as the default publishing path.
allowed-tools: Read, Glob, Grep, Bash
---

# Deployment Procedures

Use this skill for safe releases of React/Vite frontend and FastAPI backend systems.

## Default Publishing Path

The standard publishing path is:

- Docker image builds
- Docker Compose when coordinating multiple services
- managed container hosting or self-hosted container runtime as needed

## Platform Selection

| Platform | Typical Use |
|---|---|
| Docker / Docker Compose | default local and production baseline |
| Railway / Render | managed deployments |
| Fly.io | distributed app/API hosting |
| Static host | frontend-only deployments when containers are unnecessary |
| Kubernetes | larger-scale orchestration |

## Pre-Deployment Principles

- tests and lint pass
- frontend build passes
- backend boots cleanly
- container images build successfully
- environment variables are verified
- rollback path exists

## Deployment Workflow

1. prepare
2. backup or tag current release
3. build container images
4. deploy
5. verify health and key flows
6. confirm or rollback

## Rollback Guidance

Prefer:

- previous image tag
- previous Compose revision
- previous platform release

## Verification

Check:

- health endpoints
- logs
- key user flows
- resource usage
- container/runtime status
