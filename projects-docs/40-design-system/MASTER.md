# Design System Master File

> **LOGIC:** When building a specific page, first check `page.<page-name>.md` in `projects-docs/40-design-system/`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** PVCity
**Generated:** 2026-03-29 11:32:00
**Category:** Operational Workspace

---

## Reference Pack Signals

- Source directories: `projects-docs/references/images`
- Images analyzed: 4
- New dominant reference: `referencia menu esquerda.jpg`
- Inferred visual direction: immersive shell, full-height sidebar, soft workspace inset on the right
- External brand source analyzed: `https://www.cityinc.com.br/`

### Brand Signals Confirmed From City

- Accent color recurring in site CSS: `#FF8700`
- Primary dark neutral recurring in site CSS: `#212026`
- Secondary neutral recurring in site CSS: `#686D6D`
- Confirmed type families in site CSS:
  - `HalyardDisplay`
  - `HalyardText`
  - `IvyPrestoDisplay`
  - `IvyPrestoItalic`

Source notes:
- Site inspected on `2026-03-29`
- Evidence came from `https://www.cityinc.com.br/` and `https://www.cityinc.com.br/_nuxt/entry.47844333.css`

## Global Rules

### Color Palette

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Brand Accent | `#FF8700` | `--color-primary` |
| Brand Ink | `#212026` | `--color-primary-dark` |
| Neutral Mid | `#686D6D` | `--color-secondary` |
| Workspace Surface | `#F5F1EA` | `--color-background` |
| Card Surface | `#FFFDF9` | `--color-surface` |
| Border | `#E8DED0` | `--color-border` |
| Text Main | `#212026` | `--color-text` |
| Text Muted | `#6E6A68` | `--color-text-muted` |

**Color Notes:** warm ivory surfaces, graphite structure, and restrained use of the City orange as the single energetic accent

### Typography

- **Heading Font:** HalyardDisplay
- **Body Font:** HalyardText
- **Accent/Editorial Font:** IvyPrestoDisplay / IvyPrestoItalic
- **Mood:** premium operational, architectural, composed, immersive, confident

### Spacing Variables

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` | Tight gaps |
| `--space-sm` | `8px` | Inline spacing |
| `--space-md` | `16px` | Standard padding |
| `--space-lg` | `24px` | Panel padding |
| `--space-xl` | `32px` | Section padding |
| `--space-2xl` | `48px` | Workspace spacing |
| `--space-3xl` | `72px` | Shell gutters |

### Shadow Depths

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 6px 16px rgba(33, 32, 38, 0.06)` | Small cards |
| `--shadow-md` | `0 16px 38px rgba(33, 32, 38, 0.08)` | Panels |
| `--shadow-lg` | `0 28px 72px rgba(33, 32, 38, 0.14)` | Main workspace shell |

---

## Component Specs

### Layout Shell

- The application should feel like a single integrated shell, not a page with a sidebar beside it.
- Sidebar occupies full height and visually contains the workspace.
- Main workspace sits inside the shell as a lighter inset surface with rounded large corners.
- Avoid flat page layouts with disconnected cards floating on a generic background.

### Navigation

- Sidebar background: deep brand ink
- Active item: simple left-side white marker plus a lighter row background
- Inactive item: low-contrast text with strong hover lift
- Sidebar itself should not become the scrolling surface during normal desktop use
- The workspace on the right is the scrolling surface
- Include one brand statement block or system note near the bottom

### Admin Navigation

- Do not use top tabs to switch CRUDs inside the main content area
- Each CRUD should be a dedicated routine reachable from sidebar submenu items
- Importacao CSV should also be its own routine, not a panel inside another CRUD
- This isolation is intentional to reduce the chance that a change in one routine breaks the others

### Buttons

```css
.btn-primary {
  background: #FF8700;
  color: #212026;
  border-radius: 999px;
  font-weight: 700;
}

.btn-secondary {
  background: #FFF7EB;
  color: #212026;
  border: 1px solid #F0D2A8;
  border-radius: 999px;
}
```

### Cards

```css
.card {
  background: #FFFDF9;
  border: 1px solid #E8DED0;
  border-radius: 24px;
  box-shadow: 0 16px 38px rgba(33, 32, 38, 0.08);
}
```

### Inputs

```css
.input {
  background: #FFFFFF;
  border: 1px solid #DDD2C2;
  border-radius: 14px;
  color: #212026;
}

.input:focus {
  border-color: #FF8700;
  box-shadow: 0 0 0 4px rgba(255, 135, 0, 0.14);
}
```

---

## Style Guidelines

**Style:** City Immersive Workspace

**Keywords:** immersive shell, full-height sidebar, architectural, premium operational, warm neutrals, brand-orange accents

**Best For:** internal operational systems, proposal simulators, admin backoffices, premium business tools

**Key Effects:** integrated shell, strong left rail presence, inset workspace, warm cards, precise orange accents, premium typography without losing usability

### Page Pattern

**Pattern Name:** Sidebar Shell Workspace

- **Conversion Strategy:** Make the environment feel stable, controlled, and premium while keeping task completion fast.
- **CTA Placement:** Primary actions sit inside content cards and summary rails, never scattered.
- **Section Order:** shell, context, workspace, summary, support

---

## Anti-Patterns (Do NOT Use)

- Neon orange floods or broad orange backgrounds
- Blue SaaS palettes that dilute the City brand
- Tiny sidebars or collapsed nav that loses the immersive-shell effect
- CRUD switching via tabs inside the workspace
- Glassmorphism as the dominant visual language
- Editorial serif overuse in operational labels and controls
- Detached page cards on a generic gray dashboard background

---

## Pre-Delivery Checklist

Before delivering any UI code, verify:

- [ ] Sidebar feels like part of one shell, not a separate column
- [ ] Main workspace reads as an inset surface inside the shell
- [ ] Orange is used as accent, not as a large-area fill
- [ ] Operational text uses Halyard-style hierarchy
- [ ] Premium serif is optional and sparse
- [ ] Responsive behavior preserves navigation clarity on mobile
- [ ] No horizontal scroll introduced by the shell
- [ ] Focus states remain visible and high-contrast
