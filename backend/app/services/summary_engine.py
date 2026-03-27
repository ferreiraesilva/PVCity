from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.services.domain.cash_flow import CashFlowSummary
from app.services.commission_calculator import CommissionSummary

# Parity reference: golden_test_cases.md and api_contracts_draft.md lines 1062-1101
# All status fields map to cells in Analise Proposta!H85:H91 (normal) or Permuta!H88:H96 (permuta)

PV_STATUS_APPROVED = "PV Aprovado*"
PV_STATUS_REJECTED = "PV Reprovado"
COMMISSION_STATUS_OK = "OK"
COMMISSION_STATUS_NOK = "NÃO OK"
FINANCING_DATE_STATUS_OK = "OK"
FINANCING_DATE_STATUS_NOK = "NÃO OK"
RISK_LOW = "Baixo"
RISK_MEDIUM = "Médio"
RISK_HIGH = "Alto"


@dataclass(frozen=True)
class NormalSummary:
    table_total_vgv: float           # Base price
    proposal_total_vgv: float        # Sum of total_vgv across all proposal rows
    proposal_total_pv: float         # Sum of pv_net across all months
    pv_variation_percent: float      # (proposal_total_pv - table_total_vgv) / table_total_vgv
    commission_total_percent: float   # N12
    commission_total_value: float    # R35
    financing_level_ratio: Optional[float]
    pv_status: str                   # H85
    commission_status: str           # H86
    financing_date_status: str       # H87
    capture_total_percent: float     # H88
    risk_level: str                  # H91


@dataclass(frozen=True)
class PermutaSummary:
    exchange_total_vgv: float        # I59 in Permuta
    exchange_total_pv: float         # Sum of pv_net in exchange flow
    exchange_vpl_variation_percent: float  # N6
    exchange_vpl_variation_value: float    # N7
    pv_status: str                   # H90
    commission_status: str           # H91
    financing_date_status: str       # H92
    capture_total_percent: float     # H93
    risk_level: str                  # H96


class SummaryEngine:
    """
    Computes the high-level summary fields from engine outputs.
    Maps directly to the summary block in Analise Proposta!G83:H91 (normal)
    and Permuta!G88:H96 (permuta).
    """

    def build_normal(
        self,
        flow_summary: CashFlowSummary,
        commission: CommissionSummary,
        base_price: float,
        proposal_total_vgv: float,
        capture_total_percent: float,
    ) -> NormalSummary:
        proposal_total_pv = flow_summary.total_pv_net
        pv_variation = (
            (proposal_total_pv - base_price) / base_price if base_price else 0.0
        )
        pv_status = self._pv_status_normal(pv_variation)
        commission_status = COMMISSION_STATUS_OK if commission.is_within_tolerance else COMMISSION_STATUS_NOK
        risk = self._risk_level(capture_total_percent, pv_status)

        # H87: financing date OK when financing slots fall before or on delivery month
        # Placeholder: always OK until DB-resolved date validation is wired
        financing_date_status = FINANCING_DATE_STATUS_OK

        return NormalSummary(
            table_total_vgv=base_price,
            proposal_total_vgv=proposal_total_vgv,
            proposal_total_pv=proposal_total_pv,
            pv_variation_percent=pv_variation,
            commission_total_percent=commission.total_percent,
            commission_total_value=commission.total_value,
            financing_level_ratio=capture_total_percent,
            pv_status=pv_status,
            commission_status=commission_status,
            financing_date_status=financing_date_status,
            capture_total_percent=capture_total_percent,
            risk_level=risk,
        )

    def build_permuta(
        self,
        flow_summary: CashFlowSummary,
        commission: CommissionSummary,
        normal_summary: NormalSummary,
        exchange_total_vgv: float,
        capture_total_percent: float,
        has_financing_date_issue: bool,
    ) -> PermutaSummary:
        exchange_total_pv = flow_summary.total_pv_net
        vpl_variation_percent = (
            (exchange_total_pv - normal_summary.proposal_total_pv)
            / normal_summary.proposal_total_pv
            if normal_summary.proposal_total_pv
            else 0.0
        )
        vpl_variation_value = exchange_total_pv - normal_summary.proposal_total_pv
        pv_status = PV_STATUS_APPROVED if vpl_variation_percent >= 0 else PV_STATUS_REJECTED
        commission_status = COMMISSION_STATUS_OK if commission.is_within_tolerance else COMMISSION_STATUS_NOK
        financing_date_status = FINANCING_DATE_STATUS_NOK if has_financing_date_issue else FINANCING_DATE_STATUS_OK
        risk = self._risk_level(capture_total_percent, pv_status)

        return PermutaSummary(
            exchange_total_vgv=exchange_total_vgv,
            exchange_total_pv=exchange_total_pv,
            exchange_vpl_variation_percent=vpl_variation_percent,
            exchange_vpl_variation_value=vpl_variation_value,
            pv_status=pv_status,
            commission_status=commission_status,
            financing_date_status=financing_date_status,
            capture_total_percent=capture_total_percent,
            risk_level=risk,
        )

    def _pv_status_normal(self, pv_variation: float) -> str:
        # Excel shows "PV Aprovado*" when PV >= base price or within expected discount.
        # GT-001 shows pv_status = "PV Aprovado*" with pv_variation = 0.0 (discount rate used exactly)
        # The asterisk (*) appears when result is at the limit — preserved as exact text from Excel.
        # Exact logic TBD from DB discount rate; placeholder uses 0 threshold.
        if pv_variation >= 0.0:
            return PV_STATUS_APPROVED
        return PV_STATUS_REJECTED

    def _risk_level(self, capture_percent: float, pv_status: str) -> str:
        # Mirrors Analise Proposta!H91 logic.
        # GT-001: capture=0.5, pv_status=Aprovado -> Baixo
        # GT-002: capture=0.25, pv_status=Reprovado -> Alto
        if pv_status == PV_STATUS_REJECTED:
            return RISK_HIGH
        if capture_percent >= 0.5:
            return RISK_LOW
        if capture_percent >= 0.25:
            return RISK_MEDIUM
        return RISK_HIGH
