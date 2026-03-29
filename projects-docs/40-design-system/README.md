# PVCity Design System Intake

This directory is the design-system source of truth for frontend work.

## Workflow

1. Drop inspiration images into `projects-docs/references/images/`.
2. Update `intake.json` with the product type, style cues, and preferences.
3. Add free-form notes in `notes.md` when the references need extra explanation.
4. Run `python .agent/scripts/design_system_pipeline.py status --project PVCity`.
5. Run `python .agent/scripts/design_system_pipeline.py generate --project PVCity --prompt-missing` to persist `MASTER.md` and the prompt pack.

## Generated Artifacts

- `MASTER.md`: global design rules used by frontend implementation
- `IMAGE_ANALYSIS.md`: automatic visual analysis from the reference pack
- `image-analysis.json`: machine-readable analysis output
- `page.<name>.md`: optional page-specific override in flat-file form
- `prompt-*.md`: React + Tailwind prompt pack adapted from the original Next.js flow
- `IMPLEMENTATION_CONTEXT.md`: generated summary for the next UI task

## Rules

- External visual references belong in `projects-docs/references/images/`.
- Do not store product code here; this directory is documentation and guidance only.
- Frontend work should read `MASTER.md` first, then `page.<page>.md` when it exists.
