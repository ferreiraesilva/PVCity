---
name: frontend-design
description: Design thinking and decision-making for web UI in React/Tailwind applications. Focused on accessible, intentional, responsive interfaces.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Frontend Design System

This skill supports web UI design for the standard stack:

- React web
- Vite
- Tailwind CSS

## Selective Reading

Always read:

- `ux-psychology.md`

Read only when needed:

- `color-system.md`
- `typography-system.md`
- `visual-effects.md`
- `animation-guide.md`
- `motion-graphics.md`
- `decision-trees.md`

## Runtime Scripts

| Script | Purpose |
|---|---|
| `scripts/ux_audit.py` | UX heuristics review |
| `scripts/accessibility_checker.py` | Accessibility review |

## Ask Before Assuming

If the request is open-ended, clarify:

- target audience
- brand constraints
- content readiness
- layout direction
- palette preference

## Design Principles

- Accessibility is part of quality, not an afterthought
- Mobile-first is the baseline
- Visual direction should feel intentional, not templated
- Tailwind should support a system, not a pile of one-off classes
- React UI should remain composable and maintainable

## Avoid

- generic dashboard or landing-page cliches
- framework assumptions tied to removed legacy web frameworks
- form/rendering guidance tied to non-standard SSR-specific flows
- visual decisions disconnected from user goals
