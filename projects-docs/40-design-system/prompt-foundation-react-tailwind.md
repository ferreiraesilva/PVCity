# Prompt 1: Design System Foundation for React + Tailwind

Build or refine the frontend design system using the local reference pack.

## Required Inputs

- `projects-docs/references/images/`
- `projects-docs/40-design-system/intake.json`
- `projects-docs/40-design-system/notes.md`
- `projects-docs/40-design-system/IMAGE_ANALYSIS.md` when available

## First Checks

1. Confirm `projects-docs/references/images/` already contains the external references.
2. Inspect every image before writing code.
3. Read `IMAGE_ANALYSIS.md` to capture the extracted palette, density, contrast, and dominant visual signals.
4. If `liked_examples`, `must_keep`, or `must_avoid` are empty, ask short follow-up questions.
5. Read `MASTER.md` if it already exists and update it instead of replacing the design direction blindly.

## Workflow

1. Extract visual tokens from the references: palette, typography, spacing rhythm, radii, shadows, and motion cues.
2. Compare those observations with the automatic analysis and resolve obvious mismatches.
3. Update or generate `MASTER.md` with React + Tailwind oriented rules.
4. Translate the system into frontend artifacts using the current app structure.
5. Prefer `src/styles/`, `src/components/ui/`, and a preview route such as `/style-guide` or the closest local equivalent.
6. Use CSS variables and Tailwind tokens. Do not assume Next.js files like `app/layout.tsx` or `app/globals.css`.
7. Prefer existing local primitives over adding external UI libraries. If a component library is already in the repo, integrate with it rather than fighting it.

## Output

- token summary
- updated `MASTER.md`
- frontend files changed
- verification notes
