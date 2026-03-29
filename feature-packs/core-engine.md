# Core Engine MVP

**Status**: Implemented (Phase: IMPL-01)
**Tech Stack**: Python + FastAPI
**Focus**: Server-side mathematical parity with `Template PV - Março 26_v4.xlsx`.

## Overview 
This feature pack describes the Python backend built to emulate the exact financial calculations and validations of the PVCity template workbook.

### Key Capabilities
- **Slot Preservation Base:** Translates an exact array of slots (39-58) from standard layouts (`Tabela Venda - Parcela`) and processes them row by row, considering start months, periodicities, and quantities.
- **Normal Flow Engine:** Adjusts for 'INCC' or 'IGPM' rates over the lifecycle, building the month-to-month cash flow map (sumproduct).
- **Exchange (Permuta) Engine:** Replicates the alternative mathematical path specific for when `has_permuta = true`.
- **Summary Calculation Engine:** Returns final flags like NPV (VPL variation), total commission bases, capture percentages, and a clear Risk Status (Baixo/Alto).

### Extension Points
If adding support for new real estate operations (e.g. `INCC-M` differentiation or dynamic interest financing), ensure you implement parity traces for the `parity_guard.py` before modifying the core classes in `app/services/`.
