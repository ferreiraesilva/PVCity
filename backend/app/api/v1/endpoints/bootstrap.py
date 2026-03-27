from fastapi import APIRouter
from typing import Any, Dict

router = APIRouter()

# ---------------------------------------------------------------------------
# MOCK DATA — will be replaced by DB reads from tbCadastroProduto,
# Referencias, and Imobs tables in MSSQLServer (base: city).
# Marked with TODO:DB for easy grep when wiring the data layer.
# ---------------------------------------------------------------------------
_MOCK_REFERENCE_DATA: Dict[str, Any] = {
    "products": [
        {
            "enterprise_name": "Garten",             # tbCadastroProduto
            "work_code": "6101I",
            "spe_name": "SPE RESIDENCIAL CITY 17 EMPREENDIMENTOS LTDA",
            "default_discount_percent": 0.08,
            "default_vpl_rate_annual": 0.10,          # J7 source
            "delivery_month": "2027-08-01",
            "launch_date": "2023-09-24",
            "stage": "Remanescente",
            "personalization_status": "Finalizada",
            "personalization_deadline": None,
        }
    ],
    "unit_lookup_keys": [
        {
            "product_unit_key": "Garten|601",        # Referencias
            "enterprise_name": "Garten",
            "unit_code": "601",
            "unit_type": "Padrão",
            "suites": 3,
            "private_area_m2": 208.28,
            "garage_spots": "41/41A/45",
            "base_price": 2716846.0,
            "status": "Disponível",
        }
    ],
    "real_estate_agencies": [
        {
            "name": "Autônomo",                       # Imobs
            "manager_cv_name": None,
        }
    ],
    "enums": {
        "boolean_ptbr": ["Sim", "Não"],
        "modification_kind": ["Não", "Decorado (R$/m²)", "Facility (R$/m²)"],
        "periodicity": ["Sinal", "Entrada", "Mensais", "Semestrais", "Única", "Permuta", "Anuais", "Veículo"],
        "financing_kind": ["Financ. Bancário", "Financ. Direto"],
        "adjustment_type": [
            "Fixas Irreajustaveis", "INCC", "IGPM + 12% a.a",
            "IPCA + 0,99% a.m", "IPCA + 13,65% a.a",
        ],
    },
}


@router.get("/reference-data")
def get_reference_data():
    """
    GET /api/v1/bootstrap/reference-data
    Returns enum lists, products, units and agencies to populate the UI.
    Source: tbCadastroProduto, Referencias, Imobs — currently mocked.
    TODO:DB wire to MSSQLServer reads.
    """
    return _MOCK_REFERENCE_DATA
