from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, Optional

from app.services.parity_guard import ParityGuardService
from app.services.domain.cash_flow import CashFlowSummary

router = APIRouter()

MONETARY_TOLERANCE = 0.01
PERCENTAGE_TOLERANCE = 0.00000001

KNOWN_CRITICAL_CELLS = {
    "summary.normal.pv_status": ("Analise Proposta", "H85"),
    "summary.normal.commission_status": ("Analise Proposta", "H86"),
    "summary.normal.financing_date_status": ("Analise Proposta", "H87"),
    "summary.normal.capture_total_percent": ("Analise Proposta", "H88"),
    "summary.normal.risk_level": ("Analise Proposta", "H91"),
    "summary.permuta.pv_status": ("Permuta", "H90"),
    "summary.permuta.commission_status": ("Permuta", "H91"),
    "summary.permuta.financing_date_status": ("Permuta", "H92"),
    "summary.permuta.capture_total_percent": ("Permuta", "H93"),
    "summary.permuta.risk_level": ("Permuta", "H96"),
    "summary.permuta.exchange_vpl_variation_percent": ("Permuta", "N6"),
    "summary.permuta.exchange_total_vgv": ("Permuta", "I59"),
    "commission.total_percent": ("Analise Proposta", "R36"),
    "commission.total_value": ("Analise Proposta", "R35"),
}


class ParityTraceRequest(BaseModel):
    calculated_result: Dict[str, Any]
    expected_snapshot: Dict[str, Any]


@router.post("/trace")
def trace(request: ParityTraceRequest):
    """
    POST /api/v1/parity/trace

    Compares a calculated result dict against an expected_snapshot dict.
    Each key in expected_snapshot is a dotted field path (e.g. "summary.normal.pv_status").
    Returns match=True only if all compared fields pass their respective tolerances.
    """
    differences = []
    critical_cells_checked = []

    for field_path, expected_value in request.expected_snapshot.items():
        actual_value = _resolve_path(request.calculated_result, field_path)
        cell_ref = KNOWN_CRITICAL_CELLS.get(field_path)

        if cell_ref:
            critical_cells_checked.append(f"{cell_ref[0]}!{cell_ref[1]}")

        if actual_value is None:
            differences.append({
                "field": field_path,
                "expected": expected_value,
                "actual": None,
                "reason": "FIELD_NOT_FOUND",
            })
            continue

        if not _values_match(actual_value, expected_value):
            differences.append({
                "field": field_path,
                "expected": expected_value,
                "actual": actual_value,
                "reason": "VALUE_MISMATCH",
                "tolerance_applied": MONETARY_TOLERANCE if isinstance(expected_value, float) else None,
            })

    return {
        "match": len(differences) == 0,
        "differences": differences,
        "critical_cells_checked": list(set(critical_cells_checked)),
    }


def _resolve_path(data: Dict, path: str) -> Optional[Any]:
    parts = path.split(".")
    current = data
    for part in parts:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
        if current is None:
            return None
    return current


def _values_match(actual: Any, expected: Any) -> bool:
    if isinstance(expected, float) and isinstance(actual, (float, int)):
        return abs(float(actual) - expected) <= MONETARY_TOLERANCE
    if isinstance(expected, str):
        return str(actual).strip() == expected.strip()
    return actual == expected
