from __future__ import annotations

from datetime import date, datetime
from typing import Any

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.enterprise import Enterprise
from app.models.global_parameter import GlobalParameter
from app.models.real_estate_agency import RealEstateAgency
from app.models.unit import Unit
from app.models.unit_standard_flow import UnitStandardFlow
from app.services.label_normalizer import (
    is_financing_periodicity,
    normalize_periodicity_label,
)


def _to_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def _to_iso(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _runtime_product_defaults(unit: Unit, enterprise: Enterprise) -> dict[str, Any]:
    today = date.today().isoformat()
    return {
        "enterprise_name": enterprise.name,
        "unit_code": unit.code,
        "product_unit_key": unit.product_unit_key or f"{enterprise.name}|{unit.code}",
        "garage_code": unit.garage_code,
        "private_area_m2": unit.private_area_m2,
        "delivery_month": _to_iso(enterprise.delivery_month),
        "default_analysis_date": today,
        "default_modification_kind": settings.DEFAULT_MODIFICATION_KIND,
        "default_decorated_value_per_m2": settings.DEFAULT_DECORATED_VALUE_PER_M2,
        "default_facility_value_per_m2": settings.DEFAULT_FACILITY_VALUE_PER_M2,
        "default_area_for_modification_m2": unit.private_area_m2,
        "default_prize_enabled": settings.DEFAULT_PRIZE_ENABLED,
        "default_fully_invoiced": settings.DEFAULT_FULLY_INVOICED,
        "default_has_permuta": settings.DEFAULT_HAS_PERMUTA,
        "base_price": unit.base_price,
        "enterprise_discount_percent": _to_float(enterprise.discount_percent),
        "enterprise_vpl_rate_annual": _to_float(enterprise.vpl_rate_annual),
    }


def _get_empty_slots() -> list[dict[str, Any]]:
    return [
        {
            "row_slot": 39 + i,
            "installment_count": 0,
            "periodicity": "",
            "start_month": None,
            "installment_value": 0.0,
            "percent": 0.0,
            "total_vgv": 0.0,
            "adjustment_type": "INCC",
            "notes": None,
        }
        for i in range(20)
    ]


def _start_month_to_iso(
    offset_or_date: Any,
    periodicity: str | None,
    analysis_date: date,
    delivery_month: Any,
) -> str | None:
    if offset_or_date in (None, ""):
        return None
    if isinstance(offset_or_date, datetime):
        return offset_or_date.date().replace(day=10).isoformat()
    if isinstance(offset_or_date, date):
        return offset_or_date.replace(day=10).isoformat()

    raw_value = str(offset_or_date).strip()
    if not raw_value:
        return None
    if "-" in raw_value:
        try:
            return date.fromisoformat(raw_value).replace(day=10).isoformat()
        except ValueError:
            return raw_value

    offset = _to_optional_int(offset_or_date)
    if offset is None:
        return raw_value

    anchor = analysis_date.replace(day=1)
    if is_financing_periodicity(periodicity):
        if isinstance(delivery_month, datetime):
            anchor = delivery_month.date().replace(day=1)
        elif isinstance(delivery_month, date):
            anchor = delivery_month.replace(day=1)
        elif delivery_month:
            try:
                anchor = date.fromisoformat(str(delivery_month)).replace(day=1)
            except ValueError:
                pass

    return (anchor + relativedelta(months=offset)).replace(day=10).isoformat()


def _normalize_runtime_periodicity(value: Any, fallback_index: int) -> str:
    normalized = normalize_periodicity_label(value)
    if normalized and not str(normalized).strip().isdigit():
        return normalized

    numeric = _to_optional_int(value)
    if numeric == 6:
        return "Semestrais"
    if numeric == 12:
        return "Anuais"

    legacy_order = {
        0: "Sinal",
        1: "Entrada",
        2: "Mensais",
        3: "Semestrais",
        4: "Única",
        5: "Financ. Bancário",
    }
    return legacy_order.get(fallback_index, str(value).strip())


def _default_adjustment_type(periodicity: str | None) -> str:
    if periodicity in {"Sinal", "Entrada", "Veículo"}:
        return "Fixas Irreajustaveis"
    if is_financing_periodicity(periodicity):
        return "IGPM + 12% a.a"
    return "INCC"


class DatabaseReferenceService:
    """
    Operational source of truth for the application runtime.
    The workbook is reserved for reverse engineering, parity checks, and comparative recalculation.
    """

    def get_reference_data(self) -> dict[str, Any]:
        db: Session = SessionLocal()
        try:
            enterprises = (
                db.query(Enterprise)
                .filter_by(is_active=True)
                .order_by(Enterprise.name)
                .all()
            )
            units = db.query(Unit).join(Enterprise).order_by(Enterprise.name, Unit.code).all()

            products = [
                {
                    "enterprise_name": e.name,
                    "work_code": e.work_code,
                    "spe_name": e.spe_name,
                    "default_discount_percent": _to_float(e.discount_percent),
                    "default_vpl_rate_annual": _to_float(e.vpl_rate_annual),
                    "delivery_month": _to_iso(e.delivery_month),
                    "launch_date": _to_iso(e.launch_date),
                    "stage": e.stage,
                }
                for e in enterprises
            ]

            unit_lookup_keys = [
                {
                    "product_unit_key": u.product_unit_key,
                    "enterprise_name": u.enterprise.name,
                    "unit_code": u.code,
                    "unit_type": u.unit_type,
                    "suites": u.suites,
                    "private_area_m2": _to_float(u.private_area_m2),
                    "garage_spots": u.garage_spots,
                    "base_price": _to_float(u.base_price),
                    "status": u.status,
                }
                for u in units
            ]

            agencies = (
                db.query(RealEstateAgency)
                .filter_by(is_active=True)
                .order_by(RealEstateAgency.name)
                .all()
            )
            real_estate_agencies = [a.name for a in agencies]

            global_params = db.query(GlobalParameter).all()
            financial_rates = {p.key: p.value for p in global_params}

            return {
                "products": products,
                "unit_lookup_keys": unit_lookup_keys,
                "real_estate_agencies": real_estate_agencies,
                "financial_rates": financial_rates,
                "enums": {
                    "boolean_ptbr": ["Sim", "NÃ£o"],
                    "modification_kind": ["NÃ£o", "Decorado (R$/mÂ²)", "Facility (R$/mÂ²)"],
                    "periodicity": [
                        "Sinal",
                        "Entrada",
                        "Mensais",
                        "Semestrais",
                        "Ãšnica",
                        "Permuta",
                        "Anuais",
                        "VeÃ­culo",
                        "Financ. BancÃ¡rio",
                        "Financ. Direto",
                    ],
                    "financing_kind": ["Financ. BancÃ¡rio", "Financ. Direto"],
                    "adjustment_type": [
                        "Fixas Irreajustaveis",
                        "INCC",
                        "IGPM + 12% a.a",
                        "IPCA + 0,99% a.m",
                        "IPCA + 13,65% a.a",
                    ],
                },
            }
        finally:
            db.close()

    def get_unit_defaults(self, enterprise_name: str, unit_code: str) -> dict[str, Any]:
        db: Session = SessionLocal()
        try:
            unit = (
                db.query(Unit)
                .join(Enterprise)
                .filter(Enterprise.name == enterprise_name, Unit.code == unit_code)
                .first()
            )
            if not unit:
                raise KeyError(f"Unknown unit: {enterprise_name}|{unit_code}")

            enterprise = unit.enterprise
            product_context = _runtime_product_defaults(unit, enterprise)
            analysis_date = date.fromisoformat(product_context["default_analysis_date"])

            db_flows = (
                db.query(UnitStandardFlow)
                .filter_by(enterprise_id=enterprise.id)
                .order_by(UnitStandardFlow.row_slot)
                .all()
            )

            slots = _get_empty_slots()

            for index, db_flow in enumerate(db_flows):
                slot_index = (
                    db_flow.row_slot - 39
                    if db_flow.row_slot is not None and 39 <= db_flow.row_slot <= 58
                    else index
                )
                if not 0 <= slot_index < len(slots):
                    continue

                periodicity = _normalize_runtime_periodicity(db_flow.periodicity, index)
                installment_count = db_flow.installment_count or 0
                installment_value = round(unit.base_price * (db_flow.percent or 0.0), 2)

                slots[slot_index].update(
                    {
                        "row_slot": db_flow.row_slot or slots[slot_index]["row_slot"],
                        "installment_count": installment_count,
                        "periodicity": periodicity,
                        "start_month": _start_month_to_iso(
                            db_flow.start_month,
                            periodicity,
                            analysis_date,
                            enterprise.delivery_month,
                        ),
                        "installment_value": installment_value,
                        "percent": db_flow.percent,
                        "total_vgv": round(installment_value * installment_count, 2),
                        "adjustment_type": _default_adjustment_type(periodicity),
                    }
                )

            if not db_flows and unit.base_price > 0:
                slots[0].update(
                    {
                        "installment_count": 1,
                        "periodicity": "Sinal",
                        "installment_value": unit.base_price,
                        "percent": 1.0,
                        "total_vgv": unit.base_price,
                        "adjustment_type": "Fixas Irreajustaveis",
                    }
                )

            return {
                "product_context": product_context,
                "default_sale_flow_rows": slots,
                "default_exchange_flow_rows": [dict(s) for s in slots],
                "commercial_context": {
                    "city_sales_manager_name": "",
                    "real_estate_name": "",
                    "broker_name": "",
                    "manager_name": "",
                },
                "commission_context": {
                    "primary_commission_label": settings.DEFAULT_PRIMARY_COMMISSION_LABEL,
                    "primary_commission_percent": settings.DEFAULT_PRIMARY_COMMISSION_PERCENT,
                    "prize_commission_label": settings.DEFAULT_PRIZE_COMMISSION_LABEL,
                    "prize_commission_percent": settings.DEFAULT_PRIZE_COMMISSION_PERCENT,
                    "secondary_commission_slots": [
                        {"slot": 1, "label": None, "percent": None},
                        {"slot": 2, "label": None, "percent": None},
                    ],
                },
            }
        finally:
            db.close()

    def get_product_reference(self, enterprise_name: str, unit_code: str) -> dict[str, Any]:
        db: Session = SessionLocal()
        try:
            unit = (
                db.query(Unit)
                .join(Enterprise)
                .filter(Enterprise.name == enterprise_name, Unit.code == unit_code)
                .first()
            )
            if not unit:
                raise KeyError(f"Unknown unit: {enterprise_name}|{unit_code}")

            enterprise = unit.enterprise
            return {
                "reference_row": {
                    "Valor Total": unit.base_price,
                    "Area Privativa Total (m2)": unit.private_area_m2,
                    "NÂ° Escaninho": unit.garage_code,
                    "Status": unit.status,
                },
                "product_row": {
                    "VPL": enterprise.vpl_rate_annual,
                    "Descontos (%)": enterprise.discount_percent,
                    "Data de entrega": enterprise.delivery_month,
                },
            }
        finally:
            db.close()
