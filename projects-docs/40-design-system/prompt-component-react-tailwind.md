# Prompt 2: New Component for React + Tailwind

Create or update a component that must follow the existing project design system.

## Required Inputs

- `projects-docs/40-design-system/MASTER.md`
- `projects-docs/40-design-system/page.<page>.md` when relevant
- `projects-docs/40-design-system/IMAGE_ANALYSIS.md`
- `projects-docs/references/images/` when the component is strongly tied to a visual reference

## Workflow

1. Read `MASTER.md` first and collect the component-specific rules.
2. Use `IMAGE_ANALYSIS.md` to verify palette, density, and accent decisions.
3. If the component belongs to a page with overrides, read that page file before coding.
4. Search the local frontend for an existing primitive or pattern before creating a new abstraction.
5. Build in React + Tailwind using the local token system. Prefer `src/components/ui` or the nearest existing component namespace.
6. Add variants only when they are justified by the design system, not as speculative API surface.
7. Document the intended usage in the component preview or style-guide route when the repo has one.

## Output

- component or wrapper created
- design-system rule references used
- preview or showcase updates
- accessibility notes
