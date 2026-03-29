---
description: Build or refresh a frontend design system from local reference images stored in projects-docs.
---

# /design-system - Reference Driven UI Foundation

$ARGUMENTS

## Purpose

Create a reusable design-system artifact before or during frontend work.

## Flow

1. Scaffold or inspect the local intake:
   - `python .agent/scripts/design_system_pipeline.py init --project <ProjectName>`
   - `python .agent/scripts/design_system_pipeline.py status --project <ProjectName>`
2. If there are no images in `projects-docs/references/images/`, stop and ask the user to add them.
3. Read `intake.json` and `notes.md`.
4. Ask a concise follow-up question only when key preferences are missing.
5. Generate the shared design system:
   - `python .agent/scripts/design_system_pipeline.py generate --project <ProjectName> --prompt-missing`
6. For page-specific work, generate or refresh an override:
   - `python .agent/scripts/design_system_pipeline.py generate --project <ProjectName> --page <page> --prompt-missing`
7. Only then move into frontend implementation.

## Output

- `projects-docs/40-design-system/MASTER.md`
- `projects-docs/40-design-system/page.<name>.md`
- `projects-docs/40-design-system/prompt-*.md`
- `projects-docs/40-design-system/IMPLEMENTATION_CONTEXT.md`

## Rules

- React + Vite + Tailwind is the default target stack.
- Do not assume Next.js paths or conventions.
- Frontend tasks should read `MASTER.md` first, then `page.<name>.md` when it exists.
