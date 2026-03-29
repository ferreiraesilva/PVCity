from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from app.services.domain.cash_flow import CashFlowSummary
from app.services.commission_calculator import CommissionSummary

# Parity reference: golden_test_cases.md and api_contracts_draft.md lines 1062-1101
# All status fields map to cells in Analise Proposta!H85:H91 (normal) or Permuta!H88:H96 (permuta)

PV_STATUS_APPROVED = "PV Aprovado"
PV_STATUS_APPROVED_STAR = "PV Aprovado*"
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
    standard_total_pv: float         # Sum of pv_net of the standard flow
    pv_variation_percent: float      # (proposal_total_pv / standard_total_pv) - 1
    commission_total_percent: float  # N12
    commission_total_value: float    # R35
    financing_level_ratio: Optional[float]
    pv_status: str                   # H85
    commission_status: str           # H86
    financing_date_status: str       # H87
    capture_total_percent: float     # H88
    risk_level: str                  # H91
    risk_reasons: List[str]          # Motivos do risco (ex: ["PV Reprovado"])


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
    risk_reasons: List[str]


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
        standard_pv_net: float,
        financing_level_ratio: float,
        enterprise_discount_percent: float,
        prize_commission_percent: float,
        base_financing_percent: float,
        financing_date_matches_base: bool,
    ) -> NormalSummary:
        proposal_total_pv = round(flow_summary.total_pv_net, 2)
        
        # Comparamos o PV da Proposta com o PV do Fluxo Padrão (standard_pv_net).
        # Se standard_pv_net não existir (fallover), usamos o base_price.
        reference_pv = standard_pv_net if standard_pv_net > 0 else base_price
        
        pv_variation = (
            (proposal_total_pv / reference_pv) - 1 if reference_pv else 0.0
        )
        capture_total_percent = round(max(0.0, 1 - financing_level_ratio), 4)
        pv_status = self._pv_status_normal(
            pv_variation=pv_variation,
            enterprise_discount_percent=enterprise_discount_percent,
            prize_commission_percent=prize_commission_percent,
        )
        commission_status = COMMISSION_STATUS_OK if commission.is_within_tolerance else COMMISSION_STATUS_NOK
        risk, reasons = self._risk_level(
            capture_percent=capture_total_percent,
            base_financing_percent=base_financing_percent,
            pv_status=pv_status,
        )
        financing_date_status = (
            FINANCING_DATE_STATUS_OK
            if financing_date_matches_base
            else FINANCING_DATE_STATUS_NOK
        )

        return NormalSummary(
            table_total_vgv=round(base_price, 2),
            proposal_total_vgv=round(proposal_total_vgv, 2),
            proposal_total_pv=proposal_total_pv,
            standard_total_pv=round(standard_pv_net, 2),
            pv_variation_percent=round(pv_variation, 6),
            commission_total_percent=round(commission.total_percent, 6),
            commission_total_value=round(commission.total_value, 2),
            financing_level_ratio=round(financing_level_ratio, 4),
            pv_status=pv_status,
            commission_status=commission_status,
            financing_date_status=financing_date_status,
            capture_total_percent=capture_total_percent,
            risk_level=risk,
            risk_reasons=reasons,
        )


    def build_permuta(
        self,
        flow_summary: CashFlowSummary,
        commission: CommissionSummary,
        normal_summary: NormalSummary,
        exchange_total_vgv: float,
        financing_level_ratio: float,
        enterprise_discount_percent: float,
        permuta_commission_percent: float,
        base_financing_percent: float,
        financing_date_matches_base: bool,
    ) -> PermutaSummary:
        exchange_total_pv = round(flow_summary.total_pv_net, 2)
        exchange_pv_variation = (
            (exchange_total_pv / exchange_total_vgv) - 1 if exchange_total_vgv else 0.0
        )
        vpl_variation_percent = (
            exchange_pv_variation - normal_summary.pv_variation_percent
        )
        vpl_variation_value = round(normal_summary.proposal_total_vgv - exchange_total_vgv, 2)
        capture_total_percent = round(max(0.0, 1 - financing_level_ratio), 4)
        pv_status = self._pv_status_permuta(
            vpl_variation_percent=vpl_variation_percent,
            enterprise_discount_percent=enterprise_discount_percent,
            permuta_commission_percent=permuta_commission_percent,
        )
        commission_status = COMMISSION_STATUS_OK if commission.is_within_tolerance else COMMISSION_STATUS_NOK
        financing_date_status = (
            FINANCING_DATE_STATUS_OK
            if financing_date_matches_base
            else FINANCING_DATE_STATUS_NOK
        )
        risk, reasons = self._risk_level(
            capture_percent=capture_total_percent,
            base_financing_percent=base_financing_percent,
            pv_status=pv_status,
        )

        return PermutaSummary(
            exchange_total_vgv=round(exchange_total_vgv, 2),
            exchange_total_pv=exchange_total_pv,
            exchange_vpl_variation_percent=round(vpl_variation_percent, 6),
            exchange_vpl_variation_value=vpl_variation_value,
            pv_status=pv_status,
            commission_status=commission_status,
            financing_date_status=financing_date_status,
            capture_total_percent=capture_total_percent,
            risk_level=risk,
            risk_reasons=reasons,
        )

    def _pv_status_normal(
        self,
        pv_variation: float,
        enterprise_discount_percent: float,
        prize_commission_percent: float,
    ) -> str:
        discount_used = -pv_variation
        if discount_used > enterprise_discount_percent + prize_commission_percent:
            return PV_STATUS_REJECTED
        if discount_used > enterprise_discount_percent:
            return PV_STATUS_APPROVED
        return PV_STATUS_APPROVED_STAR

    def _pv_status_permuta(
        self,
        vpl_variation_percent: float,
        enterprise_discount_percent: float,
        permuta_commission_percent: float,
    ) -> str:
        discount_used = -vpl_variation_percent
        if discount_used > enterprise_discount_percent + permuta_commission_percent:
            return PV_STATUS_REJECTED
        if discount_used > enterprise_discount_percent:
            return PV_STATUS_APPROVED
        return PV_STATUS_APPROVED_STAR

    def _risk_level(
        self,
        capture_percent: float,
        base_financing_percent: float,
        pv_status: str,
    ) -> tuple[str, List[str]]:
        reasons = []
        
        # Avaliação de PV
        if pv_status == PV_STATUS_REJECTED:
            reasons.append("PV Financeiro Reprovado")
        elif pv_status == PV_STATUS_APPROVED:
            reasons.append("PV Aprovado com ressalvas (Exige Alçada)")
            
        # Avaliação de Captura
        base_capture_target = max(0.0, 1 - base_financing_percent)
        if capture_percent < base_capture_target:
            if capture_percent < base_capture_target * 0.5:
                reasons.append(f"Captura Crítica: {capture_percent*100:.2f}% (Meta: {base_capture_target*100:.2f}%)")
            else:
                reasons.append(f"Captura Insuficiente: {capture_percent*100:.2f}% (Meta: {base_capture_target*100:.2f}%)")

        if PV_STATUS_REJECTED in reasons or any("Crítica" in r for r in reasons):
            return RISK_HIGH, reasons
        
        if reasons:
            return RISK_MEDIUM, reasons
            
        return RISK_LOW, ["Proposta dentro dos parâmetros de tabela"]
