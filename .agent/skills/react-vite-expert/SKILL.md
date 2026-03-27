---
name: react-vite-expert
description: React SPA + Vite best practices for web apps. Covers routing, server state, forms, frontend architecture, performance, and Tailwind-friendly implementation.
---

# React Vite Expert

Use this skill for standard web frontend work in this repository.

## Standard Stack

- React
- Vite
- Tailwind CSS
- React Router
- TanStack Query
- Vitest + Testing Library

## Architecture Defaults

```text
src/
|-- app/
|-- components/
|-- features/
|-- pages/
|-- routes/
|-- hooks/
|-- services/
|-- lib/
`-- main.tsx
```

## Decision Rules

### Routing

- Use React Router for multi-screen SPAs
- Keep route-level data concerns close to route modules or feature modules

### Server State

- Use TanStack Query for API-backed state
- Centralize HTTP clients and API contracts
- Model loading, empty, error, and success states explicitly

### Forms

- Use controlled forms only where needed
- Keep validation close to the form boundary
- Prefer reusable field primitives for repeated forms

### Performance

- Split by route or heavy feature boundaries
- Measure before memoizing
- Avoid global state churn
- Keep list rendering predictable and keyed correctly

### Tailwind Integration

- Prefer consistent tokens and semantic composition
- Extract reusable primitives when utility duplication becomes noisy
- Keep responsiveness mobile-first

## Do Not Default To

- SSR-only architectures
- framework-specific APIs outside React/Vite
