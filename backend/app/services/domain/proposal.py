from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import List, Optional


ADJUSTMENT_TYPE_FIXED_NON_ADJUSTABLE = "Fixas Irreajustaveis"
PERIODICITY_MENSAIS = "Mensais"
PERIODICITY_SEMESTRAIS = "Semestrais"
PERIODICITY_ANUAIS = "Anuais"
PERIODICITY_PERMUTA = "permuta"


@dataclass(frozen=True)
class MonthOffset:
    value: int

    @staticmethod
    def between(current: date, reference: date) -> "MonthOffset":
        return MonthOffset((current.year * 12 + current.month) - (reference.year * 12 + reference.month))


@dataclass(frozen=True)
class ProposalSlot:
    row_slot: int
    installment_count: Optional[float]
    periodicity: Optional[str]
    start_month: Optional[date]
    installment_value: Optional[float]
    percent: Optional[float]
    total_vgv: Optional[float]
    adjustment_type: Optional[str]
    notes: Optional[str]

    def has_start_month(self) -> bool:
        return self.start_month is not None

    def is_fixed_non_adjustable(self) -> bool:
        if self.adjustment_type is None:
            return False
        return self.adjustment_type.lower() == ADJUSTMENT_TYPE_FIXED_NON_ADJUSTABLE.lower()

    def is_adjustable(self) -> bool:
        return self.has_start_month() and not self.is_fixed_non_adjustable()

    def effective_installment_value(self) -> float:
        return self.installment_value if self.installment_value is not None else 0.0

    def effective_installment_count(self) -> float:
        return self.installment_count if self.installment_count is not None else 0.0

    def periodicity_step(self) -> int:
        if self.periodicity == PERIODICITY_MENSAIS:
            return 1
        if self.periodicity == PERIODICITY_SEMESTRAIS:
            return 6
        if self.periodicity == PERIODICITY_ANUAIS:
            return 12
        return 1

    def permuta_offset(self) -> int:
        if self.periodicity is not None and self.periodicity.lower() == PERIODICITY_PERMUTA:
            return 12
        return 0

    def month_delta(self, current_month: date) -> int:
        if not self.has_start_month():
            return -1
        return MonthOffset.between(current_month, self.start_month).value - self.permuta_offset()

    def occurs_at(self, current_month: date) -> bool:
        d = self.month_delta(current_month)
        n = self.effective_installment_count()
        passo = self.periodicity_step()
        if n == 1:
            return d == 0
        if d < 0:
            return False
        if passo == 0:
            return False
        return (d % passo == 0) and (d / passo <= n - 1)


@dataclass(frozen=True)
class ProposalRows:
    slots: List[ProposalSlot]

    def adjustable_value_at(self, current_month: date) -> float:
        total = 0.0
        for slot in self.slots:
            if slot.is_adjustable() and slot.occurs_at(current_month):
                total += slot.effective_installment_value()
        return total

    def fixed_value_at(self, current_month: date) -> float:
        total = 0.0
        for slot in self.slots:
            if slot.is_fixed_non_adjustable() and slot.has_start_month() and slot.occurs_at(current_month):
                total += slot.effective_installment_value()
        return total

    def direct_commission_at(self, current_month: date, commission_values: List[float]) -> float:
        total = 0.0
        for i, slot in enumerate(self.slots):
            if slot.has_start_month() and slot.occurs_at(current_month):
                if i < len(commission_values):
                    total += commission_values[i]
        return total
