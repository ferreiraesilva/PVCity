---
name: docker-expert
description: Docker and container delivery best practices for React/Vite frontend and FastAPI backend publishing.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Docker Expert

Use this skill when preparing services for publication or reproducible runtime environments.

## Standard Container Path

- frontend published as a container serving built SPA assets
- backend published as a FastAPI container
- local or production coordination through Docker Compose when appropriate

## Core Principles

- keep images deterministic
- prefer multi-stage builds
- keep runtime images minimal
- externalize secrets and environment-specific config
- expose health checks where practical

## Default Targets

| Service | Default Container Pattern |
|---|---|
| React/Vite frontend | build static assets, serve with lightweight web server |
| FastAPI backend | Python image running ASGI app |
| Full-stack local/prod | Compose orchestration |

## Avoid

- publishing without a container path
- bloated runtime images
- mixing build-time secrets into images
