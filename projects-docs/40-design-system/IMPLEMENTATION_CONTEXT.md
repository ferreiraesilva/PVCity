# Design System Implementation Context

Project: PVCity
Root: `projects-docs/40-design-system/`
Generated query: `operations web app sales operations light operational structured card-based trustworthy clear, calm, practical, trustworthy Travel dashboard layout with airy cards, soft surfaces, and clear workspace zoning Restaurant POS order and payment panels with fast status reading and modular summaries Fintech marketing page with crisp white canvas, muted accents, and restrained visual noise light canvas with quiet neutral surfaces and restrained accent colors modular cards, summary strips, and panels that make task grouping obvious clear current-state emphasis with low-noise chrome airy cards with soft borders, quiet elevation, and strong internal hierarchy grouped forms with explicit labels and comfortable spacing compact transactional tables with readable status and summary rows light-ui muted spacious balanced-contrast dashboard`

## Inputs

- Intake: `projects-docs/40-design-system/intake.json`
- Notes: `projects-docs/40-design-system/notes.md`
- References: `projects-docs/references/images`
- Image analysis: `projects-docs/40-design-system/IMAGE_ANALYSIS.md`

## Reference Images

- `projects-docs/references/images/2023 Travel Agency Web App Dashboard Design.jpg`
- `projects-docs/references/images/Bitepoint - Restaurant POS System _ Orders + Payment.jpg`
- `projects-docs/references/images/Redesigning fintech website - Design_ naz.jpg`

## Intake Summary

- Product type: operations web app
- Industry: sales operations
- Style keywords: light, operational, structured, card-based, trustworthy
- Target feel: clear, calm, practical, trustworthy
- Liked examples: Travel dashboard layout with airy cards, soft surfaces, and clear workspace zoning, Restaurant POS order and payment panels with fast status reading and modular summaries, Fintech marketing page with crisp white canvas, muted accents, and restrained visual noise
- Must keep: light canvas with quiet neutral surfaces and restrained accent colors, modular cards, summary strips, and panels that make task grouping obvious, high scannability for status, totals, and transactional information
- Must avoid: dark-first UI direction when the reference pack is predominantly light, luxury or editorial serif typography for operational product screens, heavy gradients, neon glow, or decorative effects that reduce clarity

## Automatic Visual Signals

- Inferred tone: light, muted, spacious
- Suggested query terms: light-ui, muted, spacious, balanced-contrast, web, app, dashboard, pos, orders, payment
- Primary token hint: `(unknown)`
- Accent token hint: `(unknown)`
- Background token hint: `#FFFFFF`
- Text token hint: `(unknown)`

## Generated Artifacts

- Master rules: `projects-docs/40-design-system/MASTER.md`
- Page overrides: `projects-docs/40-design-system/page.<name>.md`
- Prompt pack: `projects-docs/40-design-system/prompt-*.md`
- Image analysis JSON: `projects-docs/40-design-system/image-analysis.json`

## Implementation Notes

- Use the local reference pack as the visual source of truth.
- React + Vite + Tailwind is the default target stack.
- Read `MASTER.md` before coding, then apply page overrides when they exist.
- Use `IMAGE_ANALYSIS.md` to keep color, density, and contrast decisions anchored to the references.
- Keep recurring patterns in the shared design system instead of burying them inside pages.

