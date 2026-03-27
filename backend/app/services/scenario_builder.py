from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from app.schemas.scenarios import CalculationRequest, ProposalLine
from app.services.domain.proposal import ProposalRows, ProposalSlot
from app.services.domain.rates import FinancialRates


EXCEL_INCC_RATE = 0.06   # J6 - hardcoded in the spreadsheet
EXCEL_SPREAD_RATE = 0.04  # J8 - indirect commission spread


@dataclass
class ParityTraceEntry:
    field: str
    actual_value: object
    excel_sheet: str
    excel_cell_or_range: str
    rule_note: str
    expected_value: Optional[object] = None


class ProposalLineNormalizer:
    """
    Normalizes raw ProposalLine schemas into ProposalSlot domain objects,
    preserving the row_slot ordering and mapping None values strictly as documented.
    """

    def normalize(self, lines: List[ProposalLine]) -> ProposalRows:
        return ProposalRows(slots=[self._to_slot(line) for line in lines])

    def _to_slot(self, line: ProposalLine) -> ProposalSlot:
        return ProposalSlot(
            row_slot=line.row_slot,
            installment_count=line.installment_count,
            periodicity=line.periodicity,
            start_month=line.start_month,
            installment_value=line.installment_value,
            percent=line.percent,
            total_vgv=line.total_vgv,
            adjustment_type=line.adjustment_type,
            notes=line.notes,
        )


class RatesResolver:
    """
    Resolves the financial rates for the calculation engine.
    J6 and J8 are hardcoded in the spreadsheet, J7 comes from tbCadastroProduto.
    """

    def resolve(self, vpl_rate_annual: float) -> FinancialRates:
        return FinancialRates(
            incc_rate_annual=EXCEL_INCC_RATE,
            vpl_rate_annual=vpl_rate_annual,
            indirect_spread=EXCEL_SPREAD_RATE,
        )


class ScenarioBuilder:
    """
    Orchestrator that translates a CalculationRequest into domain primitives
    ready for the calculation engines.
    """

    def __init__(
        self,
        normalizer: ProposalLineNormalizer,
        rates_resolver: RatesResolver,
    ):
        self._normalizer = normalizer
        self._rates_resolver = rates_resolver

    def build_sale_rows(self, request: CalculationRequest) -> ProposalRows:
        return self._normalizer.normalize(request.sale_flow_rows)

    def build_exchange_rows(self, request: CalculationRequest) -> ProposalRows:
        return self._normalizer.normalize(request.exchange_flow_rows)

    def build_rates(self, vpl_rate_annual: float) -> FinancialRates:
        return self._rates_resolver.resolve(vpl_rate_annual)
