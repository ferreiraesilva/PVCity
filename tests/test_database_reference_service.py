from datetime import date

from app.services.database_reference_service import (
    _default_adjustment_type,
    _normalize_runtime_periodicity,
    _start_month_to_iso,
)


def test_start_month_offset_uses_analysis_date_for_sale_rows():
    result = _start_month_to_iso(
        offset_or_date=4,
        periodicity="Mensais",
        analysis_date=date(2026, 3, 29),
        delivery_month=date(2027, 8, 1),
    )
    assert result == "2026-07-10"


def test_start_month_offset_uses_delivery_month_for_financing_rows():
    result = _start_month_to_iso(
        offset_or_date=3,
        periodicity="Financ. Bancário",
        analysis_date=date(2026, 3, 29),
        delivery_month=date(2027, 8, 1),
    )
    assert result == "2027-11-10"


def test_legacy_numeric_periodicity_is_normalized_by_frequency_or_order():
    assert _normalize_runtime_periodicity("6", 3) == "Semestrais"
    assert _normalize_runtime_periodicity("12", 4) == "Anuais"
    assert _normalize_runtime_periodicity("1", 5) == "Financ. Bancário"


def test_adjustment_type_is_derived_from_periodicity():
    assert _default_adjustment_type("Sinal") == "Fixas Irreajustaveis"
    assert _default_adjustment_type("Mensais") == "INCC"
    assert _default_adjustment_type("Financ. Bancário") == "IGPM + 12% a.a"
