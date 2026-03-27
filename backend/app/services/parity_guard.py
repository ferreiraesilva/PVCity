from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from app.services.domain.cash_flow import CashFlowSummary, MonthlyCashFlowEvent
from app.services.scenario_builder import ParityTraceEntry


THRESHOLD_MONETARY = 0.01
THRESHOLD_PERCENTAGE = 0.00000001


@dataclass
class ScenarioResultSummary:
    pv_status: str
    commission_status: str
    financing_date_status: str
    capture_total: float
    risk_status: str


@dataclass
class ScenarioResult:
    """
    Top-level calculation result for one scenario (NORMAL or PERMUTA).
    """
    scenario_mode: str
    summary: ScenarioResultSummary
    total_commission_percent: float
    total_commission_value: float
    monthly_flow_events: List[MonthlyCashFlowEvent]
    flow_summary: CashFlowSummary
    parity_trace: List[ParityTraceEntry]
    warnings: List[str]

    # permuta-only fields
    vpl_variation: Optional[float] = None
    vgv_difference: Optional[float] = None


@dataclass
class ParityGuardResult:
    passed: bool
    failures: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class ParityGuardService:
    """
    Validates computed scenario results against expected golden case values.
    Tolerances follow parity_rules.md strictly.
    """

    def validate_flow_totals(
        self,
        computed: CashFlowSummary,
        expected_adjustable: Optional[float] = None,
        expected_fixed: Optional[float] = None,
        expected_direct_commission: Optional[float] = None,
        expected_indirect_commission: Optional[float] = None,
    ) -> ParityGuardResult:
        failures: List[str] = []
        if expected_adjustable is not None and not self._within_monetary(
            computed.total_gross_adjustable, expected_adjustable
        ):
            failures.append(
                f"Gross adjustable total mismatch: computed={computed.total_gross_adjustable:.6f} expected={expected_adjustable:.6f}"
            )
        if expected_fixed is not None and not self._within_monetary(
            computed.total_gross_fixed, expected_fixed
        ):
            failures.append(
                f"Gross fixed total mismatch: computed={computed.total_gross_fixed:.6f} expected={expected_fixed:.6f}"
            )
        if expected_indirect_commission is not None and not self._within_monetary(
            computed.total_indirect_commission, expected_indirect_commission
        ):
            failures.append(
                f"Indirect commission total mismatch: computed={computed.total_indirect_commission:.6f} expected={expected_indirect_commission:.6f}"
            )
        return ParityGuardResult(passed=len(failures) == 0, failures=failures)

    def _within_monetary(self, a: float, b: float) -> bool:
        return abs(a - b) <= THRESHOLD_MONETARY

    def _within_percentage(self, a: float, b: float) -> bool:
        return abs(a - b) <= THRESHOLD_PERCENTAGE
