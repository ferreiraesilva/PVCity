from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from app.schemas.scenarios import CommissionContext

# Parity reference: parity_rules.md section "Regras sensíveis que exigem parity_trace"
# Commission path: N8 -> N12 -> R36 -> R35


@dataclass(frozen=True)
class CommissionInput:
    primary_percent: float          # N8
    prize_percent: float            # N9  (active only when prize_enabled=True)
    secondary_slot_1_percent: float # N10
    secondary_slot_2_percent: float # N11
    prize_enabled: bool
    fully_invoiced: bool            # N5: when True, total commission = 0


@dataclass(frozen=True)
class CommissionSummary:
    """
    Computed commission result.
    Maps to: Analise Proposta R36 (percent), R35 (value).
    """
    total_percent: float            # N12 = sum of active slots
    total_value: float              # R35 = total_percent * base_vgv
    indirect_commission_value: float  # From PRC+COORD O34 (fired at delivery month)

    @property
    def is_within_tolerance(self) -> bool:
        # Commission OK when the cap chain doesn't overflow — placeholder logic
        # Real rule: parity_rules.md "Cap sequencial da comissão por ordem de linha"
        return self.total_percent <= 0.20  # Reasonable upper bound; DB rule will refine


class CommissionBaseCalculator:
    """
    Assembles the commission percentages from CommissionContext.
    Mirrors the logic of cells N8:N12 and R35:R36 in Analise Proposta.
    """

    def calculate(
        self,
        context: CommissionContext,
        base_vgv: float,
        prize_enabled: bool,
        fully_invoiced: bool,
        indirect_commission_gross: float,
    ) -> CommissionSummary:
        total_percent = self._total_percent(context, prize_enabled, fully_invoiced)
        total_value = total_percent * base_vgv
        return CommissionSummary(
            total_percent=total_percent,
            total_value=total_value,
            indirect_commission_value=indirect_commission_gross,
        )

    def _total_percent(
        self,
        context: CommissionContext,
        prize_enabled: bool,
        fully_invoiced: bool,
    ) -> float:
        # R36 = 0 when N5 = "Sim" (fully_invoiced)
        if fully_invoiced:
            return 0.0

        primary = context.primary_commission_percent or 0.0
        prize = (context.prize_commission_percent or 0.0) if prize_enabled else 0.0
        secondary = sum(
            (slot.percent or 0.0) for slot in (context.secondary_commission_slots or [])
        )
        # N12 = N8 + N9 + N10 + N11
        return primary + prize + secondary
