from datetime import date

from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List, Optional

from app.schemas.scenarios import CalculationRequest, ScenarioMode
from app.services.label_normalizer import is_financing_periodicity
from app.services.scenario_builder import ScenarioBuilder, ProposalLineNormalizer, RatesResolver
from app.services.monthly_schedule_engine import MonthlyScheduleEngine, IndirectCommissionEvent
from app.services.commission_calculator import CommissionBaseCalculator
from app.services.summary_engine import SummaryEngine, NormalSummary, PermutaSummary
from app.services.payload_validator import PayloadValidator
from app.services.database_reference_service import DatabaseReferenceService

router = APIRouter()
reference_service = DatabaseReferenceService()

# ---------------------------------------------------------------------------
# Placeholder until PRC + COORD is fully modeled in the runtime domain.
# Workbook remains parity-only; operational flow must not depend on it.
# ---------------------------------------------------------------------------
PLACEHOLDER_PRC_COORD_O34 = 100523.302  # PRC+COORD!O34 raw (before spread)


def _build_parity_trace(
    flow_summary: Any,
    excel_sheet_prefix: str,
) -> List[Dict]:
    return [
        {
            "field": "flow_summary.total_gross_adjustable",
            "actual_value": flow_summary.total_gross_adjustable,
            "excel_sheet": "Fluxo",
            "excel_cell_or_range": "I17" if excel_sheet_prefix == "normal" else "I106",
            "rule_note": "SUM of adjustable flow (INCC-indexed) across all months",
        },
        {
            "field": "flow_summary.total_gross_fixed",
            "actual_value": flow_summary.total_gross_fixed,
            "excel_sheet": "Fluxo",
            "excel_cell_or_range": "J17" if excel_sheet_prefix == "normal" else "J106",
            "rule_note": "SUM of fixed (irreajustável) flow across all months",
        },
        {
            "field": "flow_summary.total_indirect_commission",
            "actual_value": flow_summary.total_indirect_commission,
            "excel_sheet": "Fluxo",
            "excel_cell_or_range": "L17" if excel_sheet_prefix == "normal" else "L106",
            "rule_note": "Indirect commission event fired once at delivery month * (1 + J8)",
        },
        {
            "field": "flow_summary.total_pv_net",
            "actual_value": flow_summary.total_pv_net,
            "excel_sheet": "Fluxo",
            "excel_cell_or_range": "Q17" if excel_sheet_prefix == "normal" else "Q106",
            "rule_note": "Net present value = SUM(N, O, P) columns for all months",
        },
    ]


def _sum_total_vgv(rows: list[Any]) -> float:
    return sum((row.total_vgv or 0.0) for row in rows)


def _financing_metrics(rows: list[Any]) -> tuple[float, date | None]:
    total_vgv = 0.0
    start_month: date | None = None
    for row in rows:
        if not is_financing_periodicity(row.periodicity):
            continue
        total_vgv += row.total_vgv or 0.0
        if start_month is None and row.start_month is not None:
            start_month = row.start_month
    return total_vgv, start_month


def _base_financing_metrics(rows: list[dict[str, Any]]) -> tuple[float, date | None]:
    for row in rows:
        if not is_financing_periodicity(row.get("periodicity")):
            continue
        start_month = (
            date.fromisoformat(row["start_month"])
            if row.get("start_month")
            else None
        )
        return float(row.get("percent") or 0.0), start_month
    return 0.0, None


@router.post("", response_model=None)
def calculate(request: CalculationRequest):
    """
    POST /api/v1/scenarios/calculate

    Full calculation pipeline:
    1. Validate payload
    2. Build proposal rows and rates
    3. Run MonthlyScheduleEngine
    4. Compute CommissionSummary
    5. Compute Scenario Summary (pv_status, risk_level, etc.)
    6. Return full contract response
    """
    # --- Step 1: Validate ---
    validator = PayloadValidator()
    warnings = validator.validate(request)
    try:
        workbook_reference = reference_service.get_product_reference(
            request.product_context.enterprise_name,
            request.product_context.unit_code,
        )
        workbook_defaults = reference_service.get_unit_defaults(
            request.product_context.enterprise_name,
            request.product_context.unit_code,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    reference_row = workbook_reference["reference_row"]
    product_row = workbook_reference["product_row"]
    base_financing_percent, base_financing_start_month = _base_financing_metrics(
        workbook_defaults["default_sale_flow_rows"]
    )

    # --- Step 2: Build domain objects ---
    builder = ScenarioBuilder(
        normalizer=ProposalLineNormalizer(),
        rates_resolver=RatesResolver(),
    )
    is_permuta = request.scenario_mode == ScenarioMode.PERMUTA
    vpl_rate_annual = float(product_row.get("VPL") or 0.0)
    enterprise_discount_percent = float(product_row.get("Descontos (%)") or 0.0)
    rates = builder.build_rates(vpl_rate_annual)

    # --- Step 3: Run normal flow engine (always needed for permuta reference) ---
    sale_rows = builder.build_sale_rows(request)
    indirect_event = IndirectCommissionEvent(
        delivery_month=request.product_context.delivery_month,
        prc_coord_o34=PLACEHOLDER_PRC_COORD_O34,
        spread=rates.indirect_spread,
    )
    normal_engine = MonthlyScheduleEngine(
        proposal_rows=sale_rows,
        rates=rates,
        indirect_commission=indirect_event,
        analysis_date=request.product_context.analysis_date,
    )
    normal_flow = normal_engine.build()
    normal_events = normal_engine.build_events()

        # --- Step 3b: Standard (reference) flow  PV do fluxo padrao da unidade ---
    standard_pv_net: float = 0.0
    if request.standard_flow_rows:
        std_rows = builder.build_rows_from_lines(request.standard_flow_rows)
        std_engine = MonthlyScheduleEngine(
            proposal_rows=std_rows,
            rates=rates,
            indirect_commission=indirect_event,
            analysis_date=request.product_context.analysis_date,
        )
        std_flow = std_engine.build()
        standard_pv_net = round(std_flow.total_pv_net, 2)

# --- Step 4: Commission ---
    commission_calc = CommissionBaseCalculator()
    proposal_total_vgv = _sum_total_vgv(request.sale_flow_rows)
    commission = commission_calc.calculate(
        context=request.commission_context,
        base_vgv=proposal_total_vgv,
        prize_enabled=request.product_context.prize_enabled,
        fully_invoiced=request.product_context.fully_invoiced,
        indirect_commission_gross=normal_flow.total_indirect_commission,
    )

    # --- Step 5: Summaries ---
    summary_engine = SummaryEngine()
    financing_rows_total, financing_start_month = _financing_metrics(request.sale_flow_rows)
    financing_level_ratio = (
        financing_rows_total / proposal_total_vgv if proposal_total_vgv else 0.0
    )
    base_price = float(reference_row.get("Valor Total") or proposal_total_vgv)
    prize_commission_percent = (
        request.commission_context.prize_commission_percent or 0.0
        if request.product_context.prize_enabled
        else 0.0
    )

    normal_summary = summary_engine.build_normal(
        flow_summary=normal_flow,
        commission=commission,
        base_price=base_price,
        proposal_total_vgv=proposal_total_vgv,
        standard_pv_net=standard_pv_net,
        financing_level_ratio=financing_level_ratio,
        enterprise_discount_percent=enterprise_discount_percent,
        prize_commission_percent=prize_commission_percent,
        base_financing_percent=base_financing_percent,
        financing_date_matches_base=financing_start_month == base_financing_start_month,
    )

    # --- Step 6: Permuta (conditional) ---
    permuta_summary: Optional[PermutaSummary] = None
    exchange_events = []
    exchange_flow = None

    if is_permuta:
        exchange_rows = builder.build_exchange_rows(request)
        exchange_engine = MonthlyScheduleEngine(
            proposal_rows=exchange_rows,
            rates=rates,
            indirect_commission=indirect_event,
            analysis_date=request.product_context.analysis_date,
        )
        exchange_flow = exchange_engine.build()
        exchange_events = exchange_engine.build_events()

        exchange_vgv = _sum_total_vgv(request.exchange_flow_rows)
        exchange_financing_total, exchange_financing_start_month = _financing_metrics(
            request.exchange_flow_rows
        )
        exchange_financing_level_ratio = (
            exchange_financing_total / exchange_vgv if exchange_vgv else 0.0
        )

        permuta_summary = summary_engine.build_permuta(
            flow_summary=exchange_flow,
            commission=commission,
            normal_summary=normal_summary,
            exchange_total_vgv=exchange_vgv,
            financing_level_ratio=exchange_financing_level_ratio,
            enterprise_discount_percent=enterprise_discount_percent,
            permuta_commission_percent=commission.total_percent,
            base_financing_percent=base_financing_percent,
            financing_date_matches_base=exchange_financing_start_month == base_financing_start_month,
        )

    # --- Build response ---
    def _event_dict(e: Any) -> Dict:
        return {
            "month": e.month.isoformat(),
            "month_offset": e.month_offset,
            "gross_adjustable": round(e.gross_adjustable, 2),
            "gross_fixed": round(e.gross_fixed, 2),
            "direct_commission": round(e.direct_commission, 2),
            "indirect_commission": round(e.indirect_commission, 2),
            "pv_adjustable": round(e.pv_adjustable, 2),
            "pv_fixed": round(e.pv_fixed, 2),
            "pv_net": round(e.pv_net, 2),
        }

    def _normal_summary_dict(s: NormalSummary) -> Dict:
        return {
            "table_total_vgv": s.table_total_vgv,
            "proposal_total_vgv": s.proposal_total_vgv,
            "proposal_total_pv": s.proposal_total_pv,
            "standard_total_pv": s.standard_total_pv,
            "pv_variation_percent": s.pv_variation_percent,
            "commission_total_percent": s.commission_total_percent,
            "commission_total_value": s.commission_total_value,
            "financing_level_ratio": s.financing_level_ratio,
            "pv_status": s.pv_status,
            "commission_status": s.commission_status,
            "financing_date_status": s.financing_date_status,
            "capture_total_percent": s.capture_total_percent,
            "risk_level": s.risk_level,
            "risk_reasons": s.risk_reasons,
        }

    def _permuta_summary_dict(s: PermutaSummary) -> Dict:
        return {
            "exchange_total_vgv": s.exchange_total_vgv,
            "exchange_total_pv": s.exchange_total_pv,
            "exchange_vpl_variation_percent": s.exchange_vpl_variation_percent,
            "exchange_vpl_variation_value": s.exchange_vpl_variation_value,
            "pv_status": s.pv_status,
            "commission_status": s.commission_status,
            "financing_date_status": s.financing_date_status,
            "capture_total_percent": s.capture_total_percent,
            "risk_level": s.risk_level,
            "risk_reasons": s.risk_reasons,
        }

    return {
        "scenario_mode": request.scenario_mode.value,
        "summary": {
            "normal": _normal_summary_dict(normal_summary),
            "permuta": _permuta_summary_dict(permuta_summary) if permuta_summary else None,
        },
        "indirect_commission": {
            "delivery_month_indirect_commission_value": normal_flow.total_indirect_commission,
            "source_cell": "PRC + COORD!O34",
        },
        "sale_monthly_flow": [_event_dict(e) for e in normal_events],
        "exchange_monthly_flow": [_event_dict(e) for e in exchange_events],
        "parity_trace": _build_parity_trace(
            exchange_flow if is_permuta else normal_flow,
            "permuta" if is_permuta else "normal",
        ),
        "warnings": [{"code": w, "message": w} for w in warnings],
    }
