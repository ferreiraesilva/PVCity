from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass(frozen=True)
class MonthlyCashFlowEvent:
    """
    Represents a single row in tbFluxo / tbFluxoPermuta.
    All values map directly to Excel columns I-Q.
    """
    month: date
    month_offset: int
    gross_adjustable: float       # Column I: Fluxo Reajustável
    gross_fixed: float            # Column J: Fluxo Irreajustável
    direct_commission: float      # Column K: Comissão Direta (negative, deduction)
    indirect_commission: float    # Column L: Comissão Indireta (negative, deduction)
    pv_adjustable: float          # Column N: PV do Reajustável
    pv_fixed: float               # Column O: PV do Irreajustável
    pv_indirect_commission: float  # Column P: PV da Comissão Indireta (= L, no further discount)
    pv_net: float                 # Column Q: Fluxo Líquido = sum(N, O, P)


@dataclass(frozen=True)
class CashFlowSummary:
    """
    Computed totals, maps to row 17 in the Excel table (SUM of rows 18-98 or 107-187).
    """
    total_gross_adjustable: float
    total_gross_fixed: float
    total_direct_commission: float
    total_indirect_commission: float
    total_pv_adjustable: float
    total_pv_fixed: float
    total_pv_net: float

    @staticmethod
    def from_events(events: List[MonthlyCashFlowEvent]) -> "CashFlowSummary":
        return CashFlowSummary(
            total_gross_adjustable=sum(e.gross_adjustable for e in events),
            total_gross_fixed=sum(e.gross_fixed for e in events),
            total_direct_commission=sum(e.direct_commission for e in events),
            total_indirect_commission=sum(e.indirect_commission for e in events),
            total_pv_adjustable=sum(e.pv_adjustable for e in events),
            total_pv_fixed=sum(e.pv_fixed for e in events),
            total_pv_net=sum(e.pv_net for e in events),
        )
