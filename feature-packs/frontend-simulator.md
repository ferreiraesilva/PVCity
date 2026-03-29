# Frontend UI Simulator MVP

**Status**: Implemented (Phase: IMPL-02)
**Tech Stack**: React + Vite + Tailwind CSS v4 + Chart.js
**Focus**: Premium UX without losing structural precision.

## Overview
This feature pack documents the web interface built to replace the Excel spreadsheet interaction model. It enforces data structure via a strict mapping of slots.

### Key Capabilities
- **Glassmorphism Design:** Employs `.glass-panel` utilities integrated with the new `@tailwindcss/vite` setup, respecting the specific design tokens (`city-blue`, `success-green`, `danger-red`).
- **Slot Mapping Editor:** Centralizes input logic within `ProposalForm`, forcing inputs line-by-line (Linha 39, Linha 40, etc.) to ensure perfect backend mapping.
- **Mode Toggle:** Instantly switches between Normal flow and "Com Permuta" mode, activating specialized slots and warning the user accordingly.
- **Visual Feedback:** Uses `SummaryCard` for high-level business status and a stacked Bar Chart (`Chart.js`) via `MonthlyFlow` to decompose adjustable vs non-adjustable payments across real dates.

### Extension Points
Future features (e.g. PDF generation, or integration with a Database for `getBootstrapData()`) should be wired to the `App.jsx` action handlers without changing the core component structure unless required by new data fields.
