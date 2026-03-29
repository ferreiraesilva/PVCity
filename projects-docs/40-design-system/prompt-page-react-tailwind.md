# Prompt 3: New Page for React + Tailwind

Build a page from the local reference pack and the generated design system.

## Required Inputs

- `projects-docs/40-design-system/MASTER.md`
- `projects-docs/40-design-system/page.<page>.md` when available
- `projects-docs/40-design-system/IMAGE_ANALYSIS.md`
- `projects-docs/references/images/`

## Workflow

1. Inspect the reference images and identify the layout, spacing rhythm, visual hierarchy, and interaction model.
2. Read `IMAGE_ANALYSIS.md` to align light or dark balance, density, accent colors, and contrast expectations.
3. Map those decisions to the existing React application structure instead of assuming Next.js app routes.
4. Reuse design-system components first. Only create page-specific wrappers when the layout genuinely needs them.
5. Implement the page with responsive Tailwind layouts and CSS variables from the shared token system.
6. Keep mobile behavior explicit instead of inheriting desktop-only assumptions from inspiration shots.
7. If the page introduces a new recurring pattern, push it back into the design system instead of leaving it isolated inside the route.

## Output

- page sections identified
- design-system components reused
- responsive behavior described
- verification notes
