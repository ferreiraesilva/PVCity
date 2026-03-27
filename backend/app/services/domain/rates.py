from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialRates:
    """
    Encapsulates the three financial rates required by the present value engine.

    incc_rate_annual  -> J6 in Excel (e.g. 0.06 = 6% a.a.)
    vpl_rate_annual   -> J7 in Excel, looked up from tbCadastroProduto
    indirect_spread   -> J8 in Excel (e.g. 0.04 = 4%), applied as multiplier to indirect commission
    """
    incc_rate_annual: float
    vpl_rate_annual: float
    indirect_spread: float

    def monthly_vpl_rate(self) -> float:
        return (1 + self.vpl_rate_annual) ** (1 / 12) - 1

    def monthly_combined_rate(self) -> float:
        """
        Rate used to discount the irreajustável bucket.
        Formula: ((1+J6)^(1/12)) * ((1+J7)^(1/12)) - 1
        """
        incc_monthly = (1 + self.incc_rate_annual) ** (1 / 12)
        vpl_monthly = (1 + self.vpl_rate_annual) ** (1 / 12)
        return incc_monthly * vpl_monthly - 1

    def discount_adjustable(self, gross_value: float, month_offset: int) -> float:
        """
        PV for reajustável bucket (column N).
        Formula: value / ((1 + J7)^(1/12))^offset
        """
        monthly_rate = self.monthly_vpl_rate()
        return gross_value / ((1 + monthly_rate) ** month_offset)

    def discount_fixed(self, gross_value: float, month_offset: int) -> float:
        """
        PV for irreajustável bucket (column O).
        Formula: value / ((1 + combined_monthly)^offset)
        """
        combined = self.monthly_combined_rate()
        return gross_value / ((1 + combined) ** month_offset)
