from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from dateutil.relativedelta import relativedelta
from typing import List, Optional

from app.services.domain.proposal import ProposalRows
from app.services.domain.rates import FinancialRates
from app.services.domain.cash_flow import MonthlyCashFlowEvent, CashFlowSummary

FLOW_START_MONTH_OFFSET = 0
FLOW_TOTAL_MONTHS = 83  # rows 18-98 in tbFluxo (N=1 means offset=0)


@dataclass(frozen=True)
class IndirectCommissionEvent:
    """
    Encapsulates the indirect commission event.
    It fires once, at the delivery month, with value = -PRC_COORD_O34 * (1 + J8).
    """
    delivery_month: date
    prc_coord_o34: float
    spread: float

    def gross_at(self, current_month: date) -> float:
        if current_month.year == self.delivery_month.year and current_month.month == self.delivery_month.month:
            return -(self.prc_coord_o34 * (1 + self.spread))
        return 0.0


class MonthlyScheduleEngine:
    """
    Translates ProposalRows into a full list of MonthlyCashFlowEvents.
    Mirrors the exact logic of tbFluxo and tbFluxoPermuta from the Excel source of truth.

    Formula source: fluxo_formula_map.md and fluxo_bucket_rules.md
    """

    def __init__(
        self,
        proposal_rows: ProposalRows,
        rates: FinancialRates,
        indirect_commission: IndirectCommissionEvent,
        analysis_date: date,
        total_months: int = FLOW_TOTAL_MONTHS,
        direct_commission_by_slot: Optional[List[float]] = None,
    ):
        self._proposal_rows = proposal_rows
        self._rates = rates
        self._indirect_commission = indirect_commission
        self._analysis_date = analysis_date
        self._total_months = total_months
        self._direct_commission_by_slot = direct_commission_by_slot or []

    def build(self) -> CashFlowSummary:
        events = self._build_events()
        return CashFlowSummary.from_events(events)

    def build_events(self) -> List[MonthlyCashFlowEvent]:
        return self._build_events()

    def _build_events(self) -> List[MonthlyCashFlowEvent]:
        events = []
        for offset in range(self._total_months):
            current_month = self._month_at_offset(offset)
            events.append(self._event_for_month(current_month, offset))
        return events

    def _month_at_offset(self, offset: int) -> date:
        raw = self._analysis_date + relativedelta(months=offset)
        return raw.replace(day=1)

    def _event_for_month(self, current_month: date, offset: int) -> MonthlyCashFlowEvent:
        gross_adjustable = self._proposal_rows.adjustable_value_at(current_month)
        gross_fixed = self._proposal_rows.fixed_value_at(current_month)
        direct_commission = self._proposal_rows.direct_commission_at(
            current_month, self._direct_commission_by_slot
        )
        indirect_commission = self._indirect_commission.gross_at(current_month)

        pv_adjustable = self._rates.discount_adjustable(gross_adjustable, offset)
        pv_fixed = self._rates.discount_fixed(gross_fixed + direct_commission, offset)
        pv_indirect = indirect_commission  # Column P = L (no additional discount applied)
        pv_net = pv_adjustable + pv_fixed + pv_indirect

        return MonthlyCashFlowEvent(
            month=current_month,
            month_offset=offset,
            gross_adjustable=gross_adjustable,
            gross_fixed=gross_fixed,
            direct_commission=direct_commission,
            indirect_commission=indirect_commission,
            pv_adjustable=pv_adjustable,
            pv_fixed=pv_fixed,
            pv_indirect_commission=pv_indirect,
            pv_net=pv_net,
        )
