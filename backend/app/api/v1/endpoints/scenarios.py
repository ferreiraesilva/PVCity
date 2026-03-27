from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List, Optional

from app.schemas.scenarios import CalculationRequest, ScenarioMode
from app.services.scenario_builder import ScenarioBuilder, ProposalLineNormalizer, RatesResolver
from app.services.monthly_schedule_engine import MonthlyScheduleEngine, IndirectCommissionEvent
from app.services.commission_calculator import CommissionBaseCalculator
from app.services.summary_engine import SummaryEngine, NormalSummary, PermutaSummary
from app.services.payload_validator import PayloadValidator
from app.services.parity_guard import ParityTraceEntry

router = APIRouter()

# ---------------------------------------------------------------------------
# Placeholders — TODO:DB resolve from tbCadastroProduto and PRC+COORD
# ---------------------------------------------------------------------------
PLACEHOLDER_VPL_RATE = 0.10       # J7: tbCadastroProduto.default_vpl_rate_annual
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

    # --- Step 2: Build domain objects ---
    builder = ScenarioBuilder(
        normalizer=ProposalLineNormalizer(),
        rates_resolver=RatesResolver(),
    )
    is_permuta = request.scenario_mode == ScenarioMode.PERMUTA
    rates = builder.build_rates(PLACEHOLDER_VPL_RATE)

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

    # --- Step 4: Commission ---
    commission_calc = CommissionBaseCalculator()
    proposal_total_vgv = sum(
        (row.total_vgv or 0.0) for row in request.sale_flow_rows
    )
    commission = commission_calc.calculate(
        context=request.commission_context,
        base_vgv=proposal_total_vgv,
        prize_enabled=request.product_context.prize_enabled,
        fully_invoiced=request.product_context.fully_invoiced,
        indirect_commission_gross=normal_flow.total_indirect_commission,
    )

    # --- Step 5: Summaries ---
    summary_engine = SummaryEngine()
    # capture_total = financing rows VGV / proposal_total_vgv
    financing_rows_total = sum(
        (row.total_vgv or 0.0)
        for row in request.sale_flow_rows
        if row.periodicity in ("Financ. Bancário", "Financ. Direto")
    )
    capture_total = financing_rows_total / proposal_total_vgv if proposal_total_vgv else 0.0

    # Placeholder base price — TODO:DB from Referencias
    base_price = proposal_total_vgv

    normal_summary = summary_engine.build_normal(
        flow_summary=normal_flow,
        commission=commission,
        base_price=base_price,
        proposal_total_vgv=proposal_total_vgv,
        capture_total_percent=capture_total,
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

        exchange_vgv = sum(
            (row.total_vgv or 0.0) for row in request.exchange_flow_rows
        )
        exchange_financing_total = sum(
            (row.total_vgv or 0.0)
            for row in request.exchange_flow_rows
            if row.periodicity in ("Financ. Bancário", "Financ. Direto")
        )
        exchange_capture = exchange_financing_total / exchange_vgv if exchange_vgv else 0.0

        # financing_date_status for permuta: mark NOK if financing date > delivery + 1 month
        # Placeholder logic; full date comparison deferred to DB flag
        has_financing_date_issue = any(
            row.start_month is not None and row.start_month > request.product_context.delivery_month
            for row in request.exchange_flow_rows
            if row.periodicity in ("Financ. Bancário", "Financ. Direto")
        )

        permuta_summary = summary_engine.build_permuta(
            flow_summary=exchange_flow,
            commission=commission,
            normal_summary=normal_summary,
            exchange_total_vgv=exchange_vgv,
            capture_total_percent=exchange_capture,
            has_financing_date_issue=has_financing_date_issue,
        )

    # --- Build response ---
    def _event_dict(e: Any) -> Dict:
        return {
            "month": e.month.isoformat(),
            "month_offset": e.month_offset,
            "gross_adjustable": e.gross_adjustable,
            "gross_fixed": e.gross_fixed,
            "direct_commission": e.direct_commission,
            "indirect_commission": e.indirect_commission,
            "pv_adjustable": e.pv_adjustable,
            "pv_fixed": e.pv_fixed,
            "pv_net": e.pv_net,
        }

    def _normal_summary_dict(s: NormalSummary) -> Dict:
        return {
            "table_total_vgv": s.table_total_vgv,
            "proposal_total_vgv": s.proposal_total_vgv,
            "proposal_total_pv": s.proposal_total_pv,
            "pv_variation_percent": s.pv_variation_percent,
            "commission_total_percent": s.commission_total_percent,
            "commission_total_value": s.commission_total_value,
            "financing_level_ratio": s.financing_level_ratio,
            "pv_status": s.pv_status,
            "commission_status": s.commission_status,
            "financing_date_status": s.financing_date_status,
            "capture_total_percent": s.capture_total_percent,
            "risk_level": s.risk_level,
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
