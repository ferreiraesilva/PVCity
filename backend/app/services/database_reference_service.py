from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.enterprise import Enterprise
from app.models.unit import Unit
from app.models.unit_standard_flow import UnitStandardFlow
from app.models.real_estate_agency import RealEstateAgency


def _to_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


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

            agencies = db.query(RealEstateAgency).filter_by(is_active=True).order_by(RealEstateAgency.name).all()
            real_estate_agencies = [a.name for a in agencies]

            return {
                "products": products,
                "unit_lookup_keys": unit_lookup_keys,
                "real_estate_agencies": real_estate_agencies,
                "enums": {
                    "boolean_ptbr": ["Sim", "Não"],
                    "modification_kind": ["Não", "Decorado (R$/m²)", "Facility (R$/m²)"],
                    "periodicity": [
                        "Sinal",
                        "Entrada",
                        "Mensais",
                        "Semestrais",
                        "Única",
                        "Permuta",
                        "Anuais",
                        "Veículo",
                        "Financ. Bancário",
                        "Financ. Direto",
                    ],
                    "financing_kind": ["Financ. Bancário", "Financ. Direto"],
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
            
            # Busca o fluxo padrão real do banco
            db_flows = db.query(UnitStandardFlow).filter_by(enterprise_id=enterprise.id).order_by(UnitStandardFlow.row_slot).all()
            
            slots = _get_empty_slots()
            
            # Preenche os slots com os dados do banco
            for i, db_flow in enumerate(db_flows):
                if i < len(slots):
                    # Calcula o valor absoluto baseado no base_price da unidade
                    installment_value = round(unit.base_price * db_flow.percent, 2)
                    slots[i].update({
                        "installment_count": db_flow.installment_count,
                        "periodicity": db_flow.periodicity,
                        "start_month": db_flow.start_month,
                        "installment_value": installment_value,
                        "percent": db_flow.percent,
                        "total_vgv": installment_value * db_flow.installment_count,
                    })

            # Se ainda estiver vazio (sem fluxo cadastrado), aplica o fallback de 100% sinal
            if not db_flows and unit.base_price > 0:
                slots[0].update({
                    "installment_count": 1,
                    "periodicity": "Sinal",
                    "installment_value": unit.base_price,
                    "percent": 1.0,
                    "total_vgv": unit.base_price,
                })

            return {
                "product_context": _runtime_product_defaults(unit, enterprise),
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
                    "N° Escaninho": unit.garage_code,
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
