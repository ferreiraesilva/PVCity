---
description: Plan and implement UI with shared design intelligence and the local design-system pipeline
---

# ui-ux-pro-max

Workflow for UI planning and implementation in this workspace. It combines the shared `ui-ux-pro-max` search dataset with the local React + Tailwind design-system wrapper.

## Prerequisites

Check whether Python is available:

```bash
python3 --version || python --version
```

If Python is missing, install it for the current OS before using the shared search scripts.

## Step 0: Check Local References First

When the project already has a visual intake, use it before inventing a new direction:

```bash
python .agent/scripts/design_system_pipeline.py status --project "<Project Name>"
```

If references already exist, prefer the wrapper:

```bash
python .agent/scripts/design_system_pipeline.py generate --project "<Project Name>" --prompt-missing
```

This persists the design system in `projects-docs/40-design-system/` and reads external references from `projects-docs/references/images/`.

## Step 1: Analyze the Request

Extract the minimum inputs needed to choose a UI direction:

- Product type: SaaS, dashboard, landing page, backoffice, portal, etc.
- Style keywords: minimal, premium, operational, playful, editorial, etc.
- Industry: fintech, healthcare, real estate, education, etc.
- Stack: default to `react` unless the user says otherwise.

## Step 2: Generate the Design System

Always start with the design-system mode so the output is opinionated and reusable:

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

For this workspace, the preferred command is still the local wrapper because it:

- reads `projects-docs/references/images/`
- uses `projects-docs/40-design-system/intake.json`
- persists `MASTER.md`, prompt files, image analysis, and implementation context
- keeps the output aligned with React + Tailwind instead of the original Next.js flow

Preferred command:

```bash
python .agent/scripts/design_system_pipeline.py generate --project "<Project Name>" --prompt-missing
```

Generated files:

- `projects-docs/40-design-system/MASTER.md`
- `projects-docs/40-design-system/page.<name>.md`
- `projects-docs/40-design-system/prompt-foundation-react-tailwind.md`
- `projects-docs/40-design-system/prompt-component-react-tailwind.md`
- `projects-docs/40-design-system/prompt-page-react-tailwind.md`
- `projects-docs/40-design-system/IMAGE_ANALYSIS.md`
- `projects-docs/40-design-system/image-analysis.json`
- `projects-docs/40-design-system/IMPLEMENTATION_CONTEXT.md`

If a specific page needs an override:

```bash
python .agent/scripts/design_system_pipeline.py generate --project "<Project Name>" --page "dashboard" --prompt-missing
```

Retrieval order:

1. Read `projects-docs/40-design-system/MASTER.md`.
2. If `projects-docs/40-design-system/page.<name>.md` exists, let it override the master rules for that page.
3. Implement the UI in React + Tailwind using those artifacts as the source of truth.

## Step 3: Run Detailed Searches Only When Needed

After the design system exists, use the shared search dataset for narrower questions:

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

Useful domains:

- `style` for alternative visual directions
- `color` for palette ideas
- `typography` for font pairings
- `ux` for interaction and accessibility guidance
- `chart` for data visualization choices
- `landing` for hero and conversion structure

Examples:

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "operational dashboard light" --domain style
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "real estate analytics" --domain chart
```

## Step 4: Load Stack Guidance

If implementation guidance is needed, query the stack rules directly. Default to React:

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack react
```

Available stacks include `html-tailwind`, `react`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, and `jetpack-compose`.

## Output Formats

The shared search supports terminal and markdown output:

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "fintech dashboard" --design-system
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "fintech dashboard" --design-system -f markdown
```

For project persistence in this repo, prefer the local wrapper instead of saving ad hoc outputs elsewhere.

## Rules of Thumb

1. Start from local references before inventing a style.
2. Keep the design system flat in `projects-docs/40-design-system/`.
3. Treat `projects-docs/references/images/` as the only external image intake.
4. Reuse shared UI patterns instead of solving each page in isolation.
5. Read `MASTER.md` before building components, pages, or routes.
6. Use page overrides only when a page truly deviates from the global system.

## Delivery Checklist

Before shipping UI work, verify:

- The chosen direction matches `MASTER.md` and any page override.
- Components use the shared visual language consistently.
- Light mode and contrast choices are legible.
- Interactive elements have clear hover and focus states.
- Layout works at common mobile and desktop breakpoints.
- Icons are from a real icon set, not emojis.
- Forms, tables, and summary cards follow the same spacing and hierarchy rules.
