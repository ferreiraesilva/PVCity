from fastapi import APIRouter, HTTPException
from typing import Any, Dict

router = APIRouter()

# ---------------------------------------------------------------------------
# MOCK DATA — will be substituted by DB reads from Referencias + tbCadastroProduto.
# TODO:DB wire to MSSQLServer for dynamic lookup.
# ---------------------------------------------------------------------------
_MOCK_UNIT_DEFAULTS: Dict[str, Any] = {
    "Garten|601": {
        "product_context": {
            "enterprise_name": "Garten",
            "unit_code": "601",
            "product_unit_key": "Garten|601",
            "garage_code": "E28",
            "private_area_m2": 208.28,
            "delivery_month": "2027-08-01",
            "default_analysis_date_kind": "server_today",
            "default_modification_kind": "Não",
            "default_decorated_value_per_m2": 3300.0,
            "default_facility_value_per_m2": 2700.0,
            "default_area_for_modification_m2": 208.28,
            "default_prize_enabled": True,
            "default_fully_invoiced": False,
            "default_has_permuta": False,
        },
        "base_sale_table_rows": [
            {"row_slot": 20, "installment_count": 1, "periodicity": "Sinal",            "start_month": "2026-03-10", "installment_value": 108673.84, "percent": 0.04, "total_vgv": 108673.84, "commission_target_value": 104598.571, "commission_paid_value": 27168.46, "net_value": 81505.38},
            {"row_slot": 21, "installment_count": 1, "periodicity": "Entrada",          "start_month": "2026-04-10", "installment_value": 81505.38,  "percent": 0.03, "total_vgv": 81505.38,  "commission_target_value": 78489.429, "commission_paid_value": 20376.35, "net_value": 61129.03},
            {"row_slot": 22, "installment_count": 1, "periodicity": "Entrada",          "start_month": "2026-05-10", "installment_value": 81505.38,  "percent": 0.03, "total_vgv": 81505.38,  "commission_target_value": 78489.429, "commission_paid_value": 20376.35, "net_value": 61129.03},
            {"row_slot": 23, "installment_count": 1, "periodicity": "Entrada",          "start_month": "2026-06-10", "installment_value": 81505.38,  "percent": 0.03, "total_vgv": 81505.38,  "commission_target_value": 78489.429, "commission_paid_value": 20376.35, "net_value": 61129.03},
            {"row_slot": 24, "installment_count": 14,"periodicity": "Mensais",          "start_month": "2026-07-10", "installment_value": 38812.09,  "percent": 0.20, "total_vgv": 543369.20, "commission_target_value": 522823.45, "commission_paid_value": 135842.30, "net_value": 407527.15},
            {"row_slot": 25, "installment_count": 2, "periodicity": "Semestrais",       "start_month": "2026-09-10", "installment_value": 135842.30, "percent": 0.10, "total_vgv": 271684.60, "commission_target_value": 261344.72, "commission_paid_value": 67921.15, "net_value": 203763.57},
            {"row_slot": 26, "installment_count": 1, "periodicity": "Única",            "start_month": "2027-03-10", "installment_value": 190179.22, "percent": 0.07, "total_vgv": 190179.22, "commission_target_value": 183072.47, "commission_paid_value": 47544.81, "net_value": 142634.42},
            {"row_slot": 27, "installment_count": 1, "periodicity": "Financ. Bancário", "start_month": "2027-11-10", "installment_value": 1358423.0, "percent": 0.50, "total_vgv": 1358423.0, "commission_target_value": 1307847.69,"commission_paid_value": 0.0,      "net_value": 1358423.0},
        ],
        "default_sale_flow_rows": [
            {"row_slot": 39, "installment_count": 1,    "periodicity": "Sinal",            "start_month": "2026-03-10", "installment_value": 108673.84, "percent": 0.04, "total_vgv": 108673.84, "adjustment_type": "Fixas Irreajustaveis", "notes": None},
            {"row_slot": 40, "installment_count": 1,    "periodicity": "Entrada",          "start_month": "2026-04-10", "installment_value": 81505.38,  "percent": 0.03, "total_vgv": 81505.38,  "adjustment_type": "Fixas Irreajustaveis", "notes": None},
            {"row_slot": 41, "installment_count": 1,    "periodicity": "Entrada",          "start_month": "2026-05-10", "installment_value": 81505.38,  "percent": 0.03, "total_vgv": 81505.38,  "adjustment_type": "Fixas Irreajustaveis", "notes": None},
            {"row_slot": 42, "installment_count": 1,    "periodicity": "Entrada",          "start_month": "2026-06-10", "installment_value": 81505.38,  "percent": 0.03, "total_vgv": 81505.38,  "adjustment_type": "Fixas Irreajustaveis", "notes": None},
            {"row_slot": 43, "installment_count": 14.0, "periodicity": "Mensais",          "start_month": "2026-07-10", "installment_value": 38812.09,  "percent": 0.2,  "total_vgv": 543369.20, "adjustment_type": "INCC", "notes": None},
            {"row_slot": 44, "installment_count": 2.0,  "periodicity": "Semestrais",       "start_month": "2026-09-10", "installment_value": 135842.30, "percent": 0.1,  "total_vgv": 271684.60, "adjustment_type": "INCC", "notes": None},
            {"row_slot": 45, "installment_count": 1.0,  "periodicity": "Única",            "start_month": "2027-03-10", "installment_value": 190179.22, "percent": 0.07, "total_vgv": 190179.22, "adjustment_type": "INCC", "notes": None},
            {"row_slot": 56, "installment_count": 1.0,  "periodicity": "Financ. Bancário", "start_month": "2027-11-10", "installment_value": 1358423.0,  "percent": 0.5,  "total_vgv": 1358423.0, "adjustment_type": "IGPM + 12% a.a", "notes": None},
        ],
    }
}


@router.get("/{enterprise_name}/units/{unit_code}/defaults")
def get_unit_defaults(enterprise_name: str, unit_code: str):
    """
    GET /api/v1/products/{enterprise_name}/units/{unit_code}/defaults
    Returns the initial state of an analysis before human editing.
    Source: Tabela Venda - Parcela, Referencias, tbCadastroProduto — currently mocked.
    TODO:DB wire to MSSQLServer reads.
    """
    key = f"{enterprise_name}|{unit_code}"
    data = _MOCK_UNIT_DEFAULTS.get(key)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Unit not found: {key}")
    return data
