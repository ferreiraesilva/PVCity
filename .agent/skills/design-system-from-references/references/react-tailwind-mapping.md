# React Tailwind Mapping

## Why This Exists

The original external prompt pack assumes Next.js and shadcn-first setup. This workspace is standardized for React + Vite + Tailwind.

## Mapping Rules

| Original Assumption | Local Adaptation |
|---|---|
| `app/layout.tsx` | `src/main.tsx`, route layouts, or the closest local shell component |
| `app/globals.css` | `src/styles/*.css`, `src/index.css`, or the current theme entrypoint |
| `app/<page>/page.tsx` | route component under `src/pages/`, `src/routes/`, or feature-local route files |
| shadcn as the default primitive source | existing local primitives first; external library only when already present or explicitly requested |
| one-off prompt run | persisted design-system artifacts inside `projects-docs/40-design-system/` |

## Token Rules

- Prefer CSS variables for colors, spacing, radius, and shadows.
- Use Tailwind utilities as the consumption layer for those tokens.
- Keep token names semantic instead of tying them to a single page.

## Component Rules

- Search existing components before creating new ones.
- New recurring patterns belong in shared UI, not inside a page file.
- Variants must be justified by the design system, not added speculatively.

## Page Rules

- Read `MASTER.md` first.
- If `page.<page>.md` exists, it overrides the shared rules for that page only.
- Keep responsive behavior explicit; reference images are usually desktop-biased.
