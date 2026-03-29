# Flow

## Purpose

Turn local inspiration images into a reusable design-system artifact that frontend work can follow repeatedly.

## Commands

```bash
python .agent/scripts/design_system_pipeline.py init --project PVCity
python .agent/scripts/design_system_pipeline.py status --project PVCity
python .agent/scripts/design_system_pipeline.py generate --project PVCity --prompt-missing
python .agent/scripts/design_system_pipeline.py generate --project PVCity --page dashboard --prompt-missing
```

## Expected Folder Shape

```text
projects-docs/40-design-system/
|-- README.md
|-- intake.json
|-- notes.md
|-- MASTER.md
|-- page.<name>.md
|-- IMPLEMENTATION_CONTEXT.md
|-- IMAGE_ANALYSIS.md
|-- image-analysis.json
|-- prompt-foundation-react-tailwind.md
|-- prompt-component-react-tailwind.md
`-- prompt-page-react-tailwind.md
```

## Operational Rules

1. `init` scaffolds the folder and the React + Tailwind prompt pack.
2. `status` checks whether the image pack and intake are ready.
3. `generate` derives a query from `intake.json`, can prompt for missing preferences, calls the shared `ui-ux-pro-max` search, and persists `MASTER.md`.
4. The prompt pack exists so agents can reuse the same reasoning when creating components and pages later.

## When To Ask The User

- No images in `references/`
- `liked_examples` is empty
- `must_avoid` is empty
- The user did not say which page should drive the first implementation

Keep follow-up questions short. One question is usually enough.
