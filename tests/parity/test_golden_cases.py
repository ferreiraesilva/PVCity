"""
Parity and integration tests.
Combines engine-level parity (GT-001, GT-002) with REST endpoint tests
and validation tests, per parity_rules.md and api_contracts_draft.md.
"""
import pytest
from datetime import date

from app.services.domain.proposal import ProposalSlot, ProposalRows
from app.services.domain.rates import FinancialRates
from app.services.monthly_schedule_engine import MonthlyScheduleEngine, IndirectCommissionEvent

MONETARY_TOLERANCE = 0.01


def _within_monetary(a: float, b: float) -> bool:
    return abs(a - b) <= MONETARY_TOLERANCE


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def gt001_engine():
    slots = [
        ProposalSlot(39, 1.0,  "Sinal",           date(2026, 3, 10), 108673.84,          0.04,    108673.84,          "Fixas Irreajustaveis", None),
        ProposalSlot(40, 1.0,  "Entrada",          date(2026, 4, 10),  81505.38,          0.03,     81505.38,          "Fixas Irreajustaveis", None),
        ProposalSlot(41, 1.0,  "Entrada",          date(2026, 5, 10),  81505.38,          0.03,     81505.38,          "Fixas Irreajustaveis", None),
        ProposalSlot(42, 1.0,  "Entrada",          date(2026, 6, 10),  81505.38,          0.03,     81505.38,          "Fixas Irreajustaveis", None),
        ProposalSlot(43, 14.0, "Mensais",          date(2026, 7, 10),  38812.085714285706, 0.014285714285714282, 543369.1999999998, "INCC", None),
        ProposalSlot(44, 2.0,  "Semestrais",       date(2026, 9, 10), 135842.30000000002, 0.05,   271684.60000000003, "INCC", None),
        ProposalSlot(45, 1.0,  "Única",            date(2027, 3, 10), 190179.22000000003, 0.07,   190179.22000000003, "INCC", None),
        ProposalSlot(56, 1.0,  "Financ. Bancário", date(2027, 11, 10), 1358423.0,         0.5,   1358423.0,           "IGPM + 12% a.a", None),
    ]
    rows = ProposalRows(slots=slots)
    rates = FinancialRates(incc_rate_annual=0.06, vpl_rate_annual=0.10, indirect_spread=0.04)
    indirect = IndirectCommissionEvent(
        delivery_month=date(2027, 8, 1),
        prc_coord_o34=100523.302,
        spread=0.04,
    )
    return MonthlyScheduleEngine(
        proposal_rows=rows,
        rates=rates,
        indirect_commission=indirect,
        analysis_date=date(2026, 3, 1),
        total_months=83,
    )


@pytest.fixture
def gt002_engine():
    slots = [
        ProposalSlot(39, 1.0, "Sinal",             date(2026, 3, 10),  51129.05, 0.07,  51129.05, "Fixas Irreajustaveis", None),
        ProposalSlot(40, 1.0, "Entrada",            date(2026, 4, 10),  43824.9,  0.06,  43824.9,  "Fixas Irreajustaveis", None),
        ProposalSlot(41, 1.0, "Entrada",            date(2026, 5, 10),  43824.9,  0.06,  43824.9,  "Fixas Irreajustaveis", None),
        ProposalSlot(42, 1.0, "Entrada",            date(2026, 6, 10),  43824.9,  0.06,  43824.9,  "Fixas Irreajustaveis", None),
        ProposalSlot(56, 1.0, "Financ. Bancário",   date(2026, 7, 10), 547811.25, 0.75, 547811.25, "IGPM + 12% a.a", None),
    ]
    rows = ProposalRows(slots=slots)
    rates = FinancialRates(incc_rate_annual=0.06, vpl_rate_annual=0.10, indirect_spread=0.04)
    indirect = IndirectCommissionEvent(
        delivery_month=date(2027, 8, 1),
        prc_coord_o34=100523.302,
        spread=0.04,
    )
    return MonthlyScheduleEngine(
        proposal_rows=rows,
        rates=rates,
        indirect_commission=indirect,
        analysis_date=date(2026, 3, 1),
        total_months=83,
    )


# ---------------------------------------------------------------------------
# GT-001: Normal baseline
# ---------------------------------------------------------------------------

class TestGT001NormalBaseline:
    def test_gross_adjustable_total(self, gt001_engine):
        summary = gt001_engine.build()
        assert _within_monetary(summary.total_gross_adjustable, 2363656.02), (
            f"Fluxo!I17 mismatch: {summary.total_gross_adjustable}"
        )

    def test_gross_fixed_total(self, gt001_engine):
        summary = gt001_engine.build()
        assert _within_monetary(summary.total_gross_fixed, 353189.98), (
            f"Fluxo!J17 mismatch: {summary.total_gross_fixed}"
        )

    def test_indirect_commission_total(self, gt001_engine):
        summary = gt001_engine.build()
        assert _within_monetary(summary.total_indirect_commission, -104544.23407999998), (
            f"Fluxo!L17 mismatch: {summary.total_indirect_commission}"
        )

    def test_march_2026_zero_adjustable(self, gt001_engine):
        events = gt001_engine.build_events()
        march = next(e for e in events if e.month == date(2026, 3, 1))
        assert march.gross_adjustable == 0.0

    def test_march_2026_sinal_in_fixed(self, gt001_engine):
        events = gt001_engine.build_events()
        march = next(e for e in events if e.month == date(2026, 3, 1))
        assert _within_monetary(march.gross_fixed, 108673.84), (
            f"Fluxo!J18 mismatch: {march.gross_fixed}"
        )


# ---------------------------------------------------------------------------
# GT-002: Permuta baseline
# ---------------------------------------------------------------------------

class TestGT002PermutaBaseline:
    def test_gross_adjustable_total(self, gt002_engine):
        summary = gt002_engine.build()
        assert _within_monetary(summary.total_gross_adjustable, 547811.25), (
            f"Fluxo!I106 mismatch: {summary.total_gross_adjustable}"
        )

    def test_gross_fixed_total(self, gt002_engine):
        summary = gt002_engine.build()
        assert _within_monetary(summary.total_gross_fixed, 182603.75), (
            f"Fluxo!J106 mismatch: {summary.total_gross_fixed}"
        )


# ---------------------------------------------------------------------------
# REST endpoint smoke tests
# ---------------------------------------------------------------------------

def test_root(client):
    r = client.get("/")
    assert r.status_code == 200


def test_bootstrap_returns_expected_keys(client):
    r = client.get("/api/v1/bootstrap/reference-data")
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) == {"products", "unit_lookup_keys", "real_estate_agencies", "enums"}


def test_unit_defaults_found(client):
    r = client.get("/api/v1/products/Garten/units/601/defaults")
    assert r.status_code == 200
    assert "product_context" in r.json()
    assert "default_sale_flow_rows" in r.json()


def test_unit_defaults_not_found(client):
    r = client.get("/api/v1/products/Unknown/units/999/defaults")
    assert r.status_code == 404


def test_scenario_save_and_retrieve(client):
    payload = {"name": "test-scenario", "scenario_payload": {"key": "value"}}
    r = client.post("/api/v1/scenarios", json=payload)
    assert r.status_code == 201
    scenario_id = r.json()["scenario_id"]

    r2 = client.get(f"/api/v1/scenarios/{scenario_id}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "test-scenario"


def test_scenario_not_found(client):
    r = client.get("/api/v1/scenarios/non-existent-id")
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

_NORMAL_CALCULATE_PAYLOAD = {
    "strict_excel_mode": True,
    "parity_trace_requested": True,
    "scenario_mode": "NORMAL",
    "product_context": {
        "enterprise_name": "Garten",
        "unit_code": "601",
        "product_unit_key": "Garten|601",
        "garage_code": "E28",
        "private_area_m2": 208.28,
        "analysis_date": "2026-03-26",
        "delivery_month": "2027-08-01",
        "modification_kind": "Não",
        "decorated_value_per_m2": None,
        "facility_value_per_m2": None,
        "area_for_modification_m2": 208.28,
        "prize_enabled": True,
        "fully_invoiced": False,
        "has_permuta": False,
    },
    "commercial_context": {
        "city_sales_manager_name": "Clara Soyer",
        "real_estate_name": "Autônomo",
        "broker_name": None,
        "manager_name": None,
    },
    "commission_context": {
        "primary_commission_label": "Intermediada",
        "primary_commission_percent": 0.05,
        "prize_commission_label": "Prêmio",
        "prize_commission_percent": 0.005,
        "secondary_commission_slots": [
            {"slot": 1, "label": None, "percent": None},
            {"slot": 2, "label": None, "percent": None},
        ],
    },
    "sale_flow_rows": [
        {"row_slot": 39, "installment_count": 1,    "periodicity": "Sinal",            "start_month": "2026-03-10", "installment_value": 108673.84, "percent": 0.04, "total_vgv": 108673.84, "adjustment_type": "Fixas Irreajustaveis", "notes": None},
        {"row_slot": 40, "installment_count": 1,    "periodicity": "Entrada",          "start_month": "2026-04-10", "installment_value": 81505.38,  "percent": 0.03, "total_vgv": 81505.38,  "adjustment_type": "Fixas Irreajustaveis", "notes": None},
        {"row_slot": 43, "installment_count": 14.0, "periodicity": "Mensais",          "start_month": "2026-07-10", "installment_value": 38812.09,  "percent": 0.20, "total_vgv": 543369.20, "adjustment_type": "INCC",                "notes": None},
        {"row_slot": 56, "installment_count": 1.0,  "periodicity": "Financ. Bancário", "start_month": "2027-11-10", "installment_value": 1358423.0,  "percent": 0.5, "total_vgv": 1358423.0, "adjustment_type": "IGPM + 12% a.a",      "notes": None},
    ],
    "exchange_flow_rows": [],
}


def test_calculate_normal_returns_200(client):
    r = client.post("/api/v1/scenarios/calculate", json=_NORMAL_CALCULATE_PAYLOAD)
    assert r.status_code == 200
    body = r.json()
    assert "summary" in body
    assert "normal" in body["summary"]
    assert "sale_monthly_flow" in body
    assert "parity_trace" in body
    assert "warnings" in body


def test_calculate_normal_summary_structure(client):
    r = client.post("/api/v1/scenarios/calculate", json=_NORMAL_CALCULATE_PAYLOAD)
    summary = r.json()["summary"]["normal"]
    required_keys = {
        "pv_status", "commission_status", "financing_date_status",
        "capture_total_percent", "risk_level", "commission_total_percent",
        "commission_total_value",
    }
    assert required_keys.issubset(set(summary.keys()))


def test_calculate_commission_total_percent(client):
    r = client.post("/api/v1/scenarios/calculate", json=_NORMAL_CALCULATE_PAYLOAD)
    commission_percent = r.json()["summary"]["normal"]["commission_total_percent"]
    # primary=0.05 + prize=0.005 = 0.055 (GT-001 golden)
    assert abs(commission_percent - 0.055) < 1e-8


def test_calculate_invalid_slot_rejected(client):
    payload = dict(_NORMAL_CALCULATE_PAYLOAD)
    payload["sale_flow_rows"] = [
        {"row_slot": 10, "installment_count": 1, "periodicity": "Sinal",
         "start_month": "2026-03-10", "installment_value": 100.0,
         "percent": 0.01, "total_vgv": 100.0,
         "adjustment_type": "Fixas Irreajustaveis", "notes": None},
    ]
    r = client.post("/api/v1/scenarios/calculate", json=payload)
    assert r.status_code == 422
    codes = [e["code"] for e in r.json()["detail"]]
    assert "INVALID_SLOT" in codes


def test_calculate_permuta_mode_without_flag_rejected(client):
    payload = dict(_NORMAL_CALCULATE_PAYLOAD)
    payload["scenario_mode"] = "PERMUTA"
    r = client.post("/api/v1/scenarios/calculate", json=payload)
    assert r.status_code == 422
    codes = [e["code"] for e in r.json()["detail"]]
    assert "PERMUTA_BLOCK_REQUIRED" in codes


# ---------------------------------------------------------------------------
# Parity trace endpoint
# ---------------------------------------------------------------------------

def test_parity_trace_full_match(client):
    r = client.post("/api/v1/scenarios/calculate", json=_NORMAL_CALCULATE_PAYLOAD)
    assert r.status_code == 200
    calculated = r.json()

    expected = {
        "summary.normal.commission_total_percent": 0.055,
        "summary.normal.pv_status": calculated["summary"]["normal"]["pv_status"],
        "summary.normal.risk_level": calculated["summary"]["normal"]["risk_level"],
    }
    r2 = client.post("/api/v1/parity/trace", json={
        "calculated_result": calculated,
        "expected_snapshot": expected,
    })
    assert r2.status_code == 200
    assert r2.json()["match"] is True
    assert r2.json()["differences"] == []


def test_parity_trace_detects_mismatch(client):
    r = client.post("/api/v1/scenarios/calculate", json=_NORMAL_CALCULATE_PAYLOAD)
    calculated = r.json()

    r2 = client.post("/api/v1/parity/trace", json={
        "calculated_result": calculated,
        "expected_snapshot": {"summary.normal.pv_status": "WRONG_STATUS"},
    })
    assert r2.status_code == 200
    assert r2.json()["match"] is False
    assert len(r2.json()["differences"]) == 1
