---
name: design-system-from-references
description: Generate or refine a React + Tailwind design system from reference images stored under projects-docs/references/images and persist the artifacts in projects-docs/40-design-system. Use when the user wants frontend work guided by inspiration images, wants the agent to ask whether references were added, or wants design-system prompts adapted from a Next.js-only flow into the local React/Vite/Tailwind stack.
---

# Design System From References

Use this skill when frontend work should be anchored to the shared reference source in `projects-docs/references/images/` and the design-system artifacts in `projects-docs/40-design-system/`.

## Core Flow

1. Run `python .agent/scripts/design_system_pipeline.py status --project <ProjectName>`.
2. If there are no images in `projects-docs/references/images/`, stop and ask the user to add them first.
3. Read `intake.json` and `notes.md`.
4. If `liked_examples`, `must_keep`, or `must_avoid` are empty and the task is open-ended, ask a short follow-up question before coding.
5. Run `python .agent/scripts/design_system_pipeline.py generate --project <ProjectName> [--page <page>] --prompt-missing`.
6. Read `MASTER.md` before touching frontend code. If `page.<page>.md` exists, it overrides the master rules.

## Default Paths

- `projects-docs/references/images/`
- `projects-docs/40-design-system/intake.json`
- `projects-docs/40-design-system/notes.md`
- `projects-docs/40-design-system/MASTER.md`
- `projects-docs/40-design-system/prompt-*.md`

## Read Next

- For the operational flow and commands: `references/flow.md`
- For the Next.js -> React/Tailwind adaptation rules: `references/react-tailwind-mapping.md`

## Constraints

- Treat the reference pack as design input, not product code.
- Do not assume Next.js files like `app/layout.tsx`, `app/page.tsx`, or `app/globals.css`.
- Prefer the local component system over pulling a new UI library into the repo.
- If recurring patterns appear during page work, push them back into the design system instead of leaving them isolated in a single route.
