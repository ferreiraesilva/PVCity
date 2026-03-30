from __future__ import annotations

import csv
import io
from typing import Any

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session, joinedload

from app.models.enterprise import Enterprise
from app.models.global_parameter import GlobalParameter
from app.models.proposal import Proposal
from app.models.real_estate_agency import RealEstateAgency
from app.models.unit import Unit
from app.models.unit_standard_flow import UnitStandardFlow
from app.schemas.admin import (
    EnterpriseCreate,
    EnterpriseUpdate,
    ImportCommitResponse,
    ImportPreviewItem,
    ImportPreviewResponse,
    RealEstateAgencyCreate,
    RealEstateAgencyUpdate,
    StandardFlowCreate,
    StandardFlowUpdate,
    UnitCreate,
    UnitUpdate,
    GlobalParameterUpdate,
)


RESOURCE_NAMES = {
    "enterprises": "enterprises",
    "units": "units",
    "standard-flows": "standard-flows",
    "real-estate-agencies": "real-estate-agencies",
}


def _to_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "sim", "yes", "y"}:
        return True
    if normalized in {"0", "false", "nao", "não", "no", "n"}:
        return False
    return default


def _to_optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(float(value))


def _to_float(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    normalized = str(value).strip()
    if "," in normalized and "." in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    elif "," in normalized:
        normalized = normalized.replace(",", ".")
    return float(normalized)


def _decode_csv(upload: UploadFile) -> list[dict[str, str]]:
    content = upload.file.read()
    if not content:
        raise HTTPException(status_code=400, detail="CSV vazio.")

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV sem cabeçalho.")

    return list(reader)


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def list_enterprises(self) -> list[Enterprise]:
        return self.db.query(Enterprise).order_by(Enterprise.name).all()

    def create_enterprise(self, payload: EnterpriseCreate) -> Enterprise:
        existing = self.db.query(Enterprise).filter(Enterprise.name == payload.name).first()
        if existing:
            raise HTTPException(status_code=409, detail="Empreendimento já cadastrado.")

        entity = Enterprise(**payload.model_dump())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update_enterprise(self, enterprise_id: int, payload: EnterpriseUpdate) -> Enterprise:
        entity = self._get_enterprise(enterprise_id)
        duplicate = (
            self.db.query(Enterprise)
            .filter(Enterprise.name == payload.name, Enterprise.id != enterprise_id)
            .first()
        )
        if duplicate:
            raise HTTPException(status_code=409, detail="Já existe outro empreendimento com este nome.")
        for field, value in payload.model_dump().items():
            setattr(entity, field, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_enterprise(self, enterprise_id: int) -> None:
        entity = self._get_enterprise(enterprise_id)
        if entity.units or entity.standard_flows:
            raise HTTPException(
                status_code=409,
                detail="Empreendimento possui unidades ou fluxos vinculados e não pode ser removido.",
            )
        self.db.delete(entity)
        self.db.commit()

    def list_units(self) -> list[Unit]:
        return (
            self.db.query(Unit)
            .options(joinedload(Unit.enterprise))
            .join(Enterprise)
            .order_by(Enterprise.name, Unit.code)
            .all()
        )

    def create_unit(self, payload: UnitCreate) -> Unit:
        self._get_enterprise(payload.enterprise_id)
        existing = (
            self.db.query(Unit)
            .filter(Unit.enterprise_id == payload.enterprise_id, Unit.code == payload.code)
            .first()
        )
        if existing:
            raise HTTPException(status_code=409, detail="Unidade já cadastrada para este empreendimento.")
        entity = Unit(**payload.model_dump())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update_unit(self, unit_id: int, payload: UnitUpdate) -> Unit:
        entity = self._get_unit(unit_id)
        self._get_enterprise(payload.enterprise_id)
        duplicate = (
            self.db.query(Unit)
            .filter(
                Unit.enterprise_id == payload.enterprise_id,
                Unit.code == payload.code,
                Unit.id != unit_id,
            )
            .first()
        )
        if duplicate:
            raise HTTPException(status_code=409, detail="Já existe outra unidade com este código no empreendimento.")
        for field, value in payload.model_dump().items():
            setattr(entity, field, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_unit(self, unit_id: int) -> None:
        entity = self._get_unit(unit_id)
        has_proposal = self.db.query(Proposal.id).filter(Proposal.unit_id == unit_id).first()
        if has_proposal:
            raise HTTPException(status_code=409, detail="Unidade possui propostas vinculadas e não pode ser removida.")
        self.db.delete(entity)
        self.db.commit()

    def list_standard_flows(self) -> list[UnitStandardFlow]:
        return (
            self.db.query(UnitStandardFlow)
            .options(joinedload(UnitStandardFlow.enterprise))
            .join(Enterprise)
            .order_by(Enterprise.name, UnitStandardFlow.row_slot)
            .all()
        )

    def create_standard_flow(self, payload: StandardFlowCreate) -> UnitStandardFlow:
        self._get_enterprise(payload.enterprise_id)
        existing = (
            self.db.query(UnitStandardFlow)
            .filter(
                UnitStandardFlow.enterprise_id == payload.enterprise_id,
                UnitStandardFlow.row_slot == payload.row_slot,
            )
            .first()
        )
        if existing:
            raise HTTPException(status_code=409, detail="Já existe fluxo padrão neste slot para o empreendimento.")
        entity = UnitStandardFlow(**payload.model_dump())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update_standard_flow(self, flow_id: int, payload: StandardFlowUpdate) -> UnitStandardFlow:
        entity = self._get_standard_flow(flow_id)
        self._get_enterprise(payload.enterprise_id)
        duplicate = (
            self.db.query(UnitStandardFlow)
            .filter(
                UnitStandardFlow.enterprise_id == payload.enterprise_id,
                UnitStandardFlow.row_slot == payload.row_slot,
                UnitStandardFlow.id != flow_id,
            )
            .first()
        )
        if duplicate:
            raise HTTPException(status_code=409, detail="Já existe fluxo padrão neste slot para o empreendimento.")
        for field, value in payload.model_dump().items():
            setattr(entity, field, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_standard_flow(self, flow_id: int) -> None:
        entity = self._get_standard_flow(flow_id)
        self.db.delete(entity)
        self.db.commit()

    def list_real_estate_agencies(self) -> list[RealEstateAgency]:
        return self.db.query(RealEstateAgency).order_by(RealEstateAgency.name).all()

    def create_real_estate_agency(self, payload: RealEstateAgencyCreate) -> RealEstateAgency:
        existing = self.db.query(RealEstateAgency).filter(RealEstateAgency.name == payload.name).first()
        if existing:
            raise HTTPException(status_code=409, detail="Imobiliária já cadastrada.")
        entity = RealEstateAgency(**payload.model_dump())
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update_real_estate_agency(self, agency_id: int, payload: RealEstateAgencyUpdate) -> RealEstateAgency:
        entity = self._get_real_estate_agency(agency_id)
        duplicate = (
            self.db.query(RealEstateAgency)
            .filter(RealEstateAgency.name == payload.name, RealEstateAgency.id != agency_id)
            .first()
        )
        if duplicate:
            raise HTTPException(status_code=409, detail="Já existe outra imobiliária com este nome.")
        for field, value in payload.model_dump().items():
            setattr(entity, field, value)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete_real_estate_agency(self, agency_id: int) -> None:
        entity = self._get_real_estate_agency(agency_id)
        self.db.delete(entity)
        self.db.commit()

    def list_global_parameters(self) -> list[GlobalParameter]:
        return self.db.query(GlobalParameter).order_by(GlobalParameter.key).all()

    def update_global_parameter(self, key: str, payload: GlobalParameterUpdate) -> GlobalParameter:
        entity = self.db.query(GlobalParameter).filter(GlobalParameter.key == key).first()
        if not entity:
            raise HTTPException(status_code=404, detail=f"Parâmetro '{key}' não encontrado.")
        entity.value = payload.value
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def preview_import(self, resource: str, upload: UploadFile) -> ImportPreviewResponse:
        if resource not in RESOURCE_NAMES:
            raise HTTPException(status_code=404, detail="Recurso de importação não suportado.")
        rows = _decode_csv(upload)
        items = self._build_import_items(resource, rows)
        summary = self._build_preview_summary(items)
        return ImportPreviewResponse(
            resource=RESOURCE_NAMES[resource],
            can_commit=summary["reject"] == 0 and len(items) > 0,
            summary=summary,
            items=items,
        )

    def commit_import(self, resource: str, upload: UploadFile) -> ImportCommitResponse:
        if resource not in RESOURCE_NAMES:
            raise HTTPException(status_code=404, detail="Recurso de importação não suportado.")
        rows = _decode_csv(upload)
        items = self._build_import_items(resource, rows)
        summary = self._build_preview_summary(items)
        if summary["reject"] > 0:
            return ImportCommitResponse(
                resource=RESOURCE_NAMES[resource],
                summary={"created": 0, "updated": 0, "ignored": 0, "rejected": summary["reject"]},
                errors=[
                    {
                        "line_number": item.line_number,
                        "natural_key": item.natural_key,
                        "errors": item.errors,
                    }
                    for item in items
                    if item.action == "reject"
                ],
            )

        created = 0
        updated = 0
        for item in items:
            normalized = item.normalized
            if resource == "enterprises":
                changed = self._upsert_enterprise_from_import(normalized)
            elif resource == "units":
                changed = self._upsert_unit_from_import(normalized)
            elif resource == "standard-flows":
                changed = self._upsert_standard_flow_from_import(normalized)
            else:
                changed = self._upsert_real_estate_agency_from_import(normalized)
            if changed == "create":
                created += 1
            elif changed == "update":
                updated += 1

        self.db.commit()
        return ImportCommitResponse(
            resource=RESOURCE_NAMES[resource],
            summary={"created": created, "updated": updated, "ignored": 0, "rejected": 0},
            errors=[],
        )

    def _build_import_items(self, resource: str, rows: list[dict[str, str]]) -> list[ImportPreviewItem]:
        builders = {
            "enterprises": self._preview_enterprises,
            "units": self._preview_units,
            "standard-flows": self._preview_standard_flows,
            "real-estate-agencies": self._preview_real_estate_agencies,
        }
        return builders[resource](rows)

    def _preview_enterprises(self, rows: list[dict[str, str]]) -> list[ImportPreviewItem]:
        items: list[ImportPreviewItem] = []
        for index, row in enumerate(rows, start=2):
            errors: list[str] = []
            name = (row.get("name") or "").strip()
            if not name:
                errors.append("Campo obrigatório: name.")
            normalized = {
                "name": name,
                "work_code": (row.get("work_code") or "").strip() or None,
                "spe_name": (row.get("spe_name") or "").strip() or None,
                "city": (row.get("city") or "").strip() or None,
                "is_active": _to_bool(row.get("is_active"), True),
                "vpl_rate_annual": _to_float(row.get("vpl_rate_annual"), 0.0),
                "discount_percent": _to_float(row.get("discount_percent"), 0.0),
                "delivery_month": (row.get("delivery_month") or "").strip() or None,
                "launch_date": (row.get("launch_date") or "").strip() or None,
                "stage": (row.get("stage") or "").strip() or None,
            }
            existing = self.db.query(Enterprise).filter(Enterprise.name == name).first() if name else None
            items.append(
                ImportPreviewItem(
                    line_number=index,
                    action="reject" if errors else ("update" if existing else "create"),
                    natural_key=name or "<sem nome>",
                    errors=errors,
                    normalized=normalized,
                )
            )
        return items

    def _preview_units(self, rows: list[dict[str, str]]) -> list[ImportPreviewItem]:
        items: list[ImportPreviewItem] = []
        for index, row in enumerate(rows, start=2):
            errors: list[str] = []
            enterprise_name = (row.get("enterprise_name") or "").strip()
            code = (row.get("code") or "").strip()
            enterprise = (
                self.db.query(Enterprise).filter(Enterprise.name == enterprise_name).first()
                if enterprise_name
                else None
            )
            if not enterprise_name:
                errors.append("Campo obrigatório: enterprise_name.")
            if not code:
                errors.append("Campo obrigatório: code.")
            if enterprise_name and not enterprise:
                errors.append("Empreendimento não encontrado.")
            normalized = {
                "enterprise_id": enterprise.id if enterprise else None,
                "code": code,
                "product_unit_key": (row.get("product_unit_key") or "").strip() or None,
                "unit_type": (row.get("unit_type") or "").strip() or None,
                "suites": _to_optional_int(row.get("suites")),
                "garage_code": (row.get("garage_code") or "").strip() or None,
                "garage_spots": _to_optional_int(row.get("garage_spots")),
                "private_area_m2": _to_float(row.get("private_area_m2"), 0.0),
                "base_price": _to_float(row.get("base_price"), 0.0),
                "status": (row.get("status") or "").strip() or None,
                "ideal_capture_percent": _to_float(row.get("ideal_capture_percent"), 1.0),
            }
            existing = (
                self.db.query(Unit)
                .filter(Unit.enterprise_id == normalized["enterprise_id"], Unit.code == code)
                .first()
                if normalized["enterprise_id"] and code
                else None
            )
            items.append(
                ImportPreviewItem(
                    line_number=index,
                    action="reject" if errors else ("update" if existing else "create"),
                    natural_key=f"{enterprise_name}|{code}".strip("|") or "<sem chave>",
                    errors=errors,
                    normalized=normalized,
                )
            )
        return items

    def _preview_standard_flows(self, rows: list[dict[str, str]]) -> list[ImportPreviewItem]:
        items: list[ImportPreviewItem] = []
        for index, row in enumerate(rows, start=2):
            errors: list[str] = []
            enterprise_name = (row.get("enterprise_name") or "").strip()
            enterprise = (
                self.db.query(Enterprise).filter(Enterprise.name == enterprise_name).first()
                if enterprise_name
                else None
            )
            if not enterprise_name:
                errors.append("Campo obrigatório: enterprise_name.")
            if not row.get("row_slot"):
                errors.append("Campo obrigatório: row_slot.")
            if not row.get("periodicity"):
                errors.append("Campo obrigatório: periodicity.")
            if enterprise_name and not enterprise:
                errors.append("Empreendimento não encontrado.")
            row_slot = _to_optional_int(row.get("row_slot"))
            normalized = {
                "enterprise_id": enterprise.id if enterprise else None,
                "periodicity": (row.get("periodicity") or "").strip(),
                "installment_count": _to_optional_int(row.get("installment_count")) or 1,
                "start_month": _to_optional_int(row.get("start_month")),
                "installment_value": _to_float(row.get("installment_value"), 0.0),
                "percent": _to_float(row.get("percent"), 0.0),
                "row_slot": row_slot,
            }
            existing = (
                self.db.query(UnitStandardFlow)
                .filter(
                    UnitStandardFlow.enterprise_id == normalized["enterprise_id"],
                    UnitStandardFlow.row_slot == row_slot,
                )
                .first()
                if normalized["enterprise_id"] and row_slot is not None
                else None
            )
            items.append(
                ImportPreviewItem(
                    line_number=index,
                    action="reject" if errors else ("update" if existing else "create"),
                    natural_key=f"{enterprise_name}|slot:{row_slot}" if enterprise_name else "<sem chave>",
                    errors=errors,
                    normalized=normalized,
                )
            )
        return items

    def _preview_real_estate_agencies(self, rows: list[dict[str, str]]) -> list[ImportPreviewItem]:
        items: list[ImportPreviewItem] = []
        for index, row in enumerate(rows, start=2):
            errors: list[str] = []
            name = (row.get("name") or "").strip()
            if not name:
                errors.append("Campo obrigatório: name.")
            normalized = {
                "name": name,
                "is_active": _to_bool(row.get("is_active"), True),
            }
            existing = self.db.query(RealEstateAgency).filter(RealEstateAgency.name == name).first() if name else None
            items.append(
                ImportPreviewItem(
                    line_number=index,
                    action="reject" if errors else ("update" if existing else "create"),
                    natural_key=name or "<sem nome>",
                    errors=errors,
                    normalized=normalized,
                )
            )
        return items

    def _upsert_enterprise_from_import(self, payload: dict[str, Any]) -> str:
        entity = self.db.query(Enterprise).filter(Enterprise.name == payload["name"]).first()
        if entity:
            for key, value in payload.items():
                setattr(entity, key, value)
            return "update"
        self.db.add(Enterprise(**payload))
        return "create"

    def _upsert_unit_from_import(self, payload: dict[str, Any]) -> str:
        entity = (
            self.db.query(Unit)
            .filter(Unit.enterprise_id == payload["enterprise_id"], Unit.code == payload["code"])
            .first()
        )
        if entity:
            for key, value in payload.items():
                setattr(entity, key, value)
            return "update"
        self.db.add(Unit(**payload))
        return "create"

    def _upsert_standard_flow_from_import(self, payload: dict[str, Any]) -> str:
        entity = (
            self.db.query(UnitStandardFlow)
            .filter(
                UnitStandardFlow.enterprise_id == payload["enterprise_id"],
                UnitStandardFlow.row_slot == payload["row_slot"],
            )
            .first()
        )
        if entity:
            for key, value in payload.items():
                setattr(entity, key, value)
            return "update"
        self.db.add(UnitStandardFlow(**payload))
        return "create"

    def _upsert_real_estate_agency_from_import(self, payload: dict[str, Any]) -> str:
        entity = self.db.query(RealEstateAgency).filter(RealEstateAgency.name == payload["name"]).first()
        if entity:
            for key, value in payload.items():
                setattr(entity, key, value)
            return "update"
        self.db.add(RealEstateAgency(**payload))
        return "create"

    @staticmethod
    def _build_preview_summary(items: list[ImportPreviewItem]) -> dict[str, int]:
        return {
            "create": sum(1 for item in items if item.action == "create"),
            "update": sum(1 for item in items if item.action == "update"),
            "reject": sum(1 for item in items if item.action == "reject"),
        }

    def _get_enterprise(self, enterprise_id: int) -> Enterprise:
        entity = self.db.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
        if not entity:
            raise HTTPException(status_code=404, detail="Empreendimento não encontrado.")
        return entity

    def _get_unit(self, unit_id: int) -> Unit:
        entity = self.db.query(Unit).filter(Unit.id == unit_id).first()
        if not entity:
            raise HTTPException(status_code=404, detail="Unidade não encontrada.")
        return entity

    def _get_standard_flow(self, flow_id: int) -> UnitStandardFlow:
        entity = self.db.query(UnitStandardFlow).filter(UnitStandardFlow.id == flow_id).first()
        if not entity:
            raise HTTPException(status_code=404, detail="Fluxo padrão não encontrado.")
        return entity

    def _get_real_estate_agency(self, agency_id: int) -> RealEstateAgency:
        entity = self.db.query(RealEstateAgency).filter(RealEstateAgency.id == agency_id).first()
        if not entity:
            raise HTTPException(status_code=404, detail="Imobiliária não encontrada.")
        return entity
