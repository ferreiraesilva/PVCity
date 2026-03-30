from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.admin import (
    EnterpriseCreate,
    EnterpriseRead,
    EnterpriseUpdate,
    ImportCommitResponse,
    ImportPreviewResponse,
    RealEstateAgencyCreate,
    RealEstateAgencyRead,
    RealEstateAgencyUpdate,
    StandardFlowCreate,
    StandardFlowRead,
    StandardFlowUpdate,
    UnitCreate,
    UnitRead,
    UnitUpdate,
    GlobalParameterRead,
    GlobalParameterUpdate,
)
from app.services.admin_service import AdminService


router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]


def get_admin_service(db: DbSession) -> AdminService:
    return AdminService(db)


@router.get("/enterprises", response_model=list[EnterpriseRead])
def list_enterprises(db: DbSession):
    return get_admin_service(db).list_enterprises()


@router.post("/enterprises", response_model=EnterpriseRead, status_code=201)
def create_enterprise(payload: EnterpriseCreate, db: DbSession):
    return get_admin_service(db).create_enterprise(payload)


@router.put("/enterprises/{enterprise_id}", response_model=EnterpriseRead)
def update_enterprise(enterprise_id: int, payload: EnterpriseUpdate, db: DbSession):
    return get_admin_service(db).update_enterprise(enterprise_id, payload)


@router.delete("/enterprises/{enterprise_id}", status_code=204)
def delete_enterprise(enterprise_id: int, db: DbSession):
    get_admin_service(db).delete_enterprise(enterprise_id)


@router.get("/units", response_model=list[UnitRead])
def list_units(db: DbSession):
    return get_admin_service(db).list_units()


@router.post("/units", response_model=UnitRead, status_code=201)
def create_unit(payload: UnitCreate, db: DbSession):
    return get_admin_service(db).create_unit(payload)


@router.put("/units/{unit_id}", response_model=UnitRead)
def update_unit(unit_id: int, payload: UnitUpdate, db: DbSession):
    return get_admin_service(db).update_unit(unit_id, payload)


@router.delete("/units/{unit_id}", status_code=204)
def delete_unit(unit_id: int, db: DbSession):
    get_admin_service(db).delete_unit(unit_id)


@router.get("/standard-flows", response_model=list[StandardFlowRead])
def list_standard_flows(db: DbSession):
    return get_admin_service(db).list_standard_flows()


@router.post("/standard-flows", response_model=StandardFlowRead, status_code=201)
def create_standard_flow(payload: StandardFlowCreate, db: DbSession):
    return get_admin_service(db).create_standard_flow(payload)


@router.put("/standard-flows/{flow_id}", response_model=StandardFlowRead)
def update_standard_flow(flow_id: int, payload: StandardFlowUpdate, db: DbSession):
    return get_admin_service(db).update_standard_flow(flow_id, payload)


@router.delete("/standard-flows/{flow_id}", status_code=204)
def delete_standard_flow(flow_id: int, db: DbSession):
    get_admin_service(db).delete_standard_flow(flow_id)


@router.get("/real-estate-agencies", response_model=list[RealEstateAgencyRead])
def list_real_estate_agencies(db: DbSession):
    return get_admin_service(db).list_real_estate_agencies()


@router.post("/real-estate-agencies", response_model=RealEstateAgencyRead, status_code=201)
def create_real_estate_agency(payload: RealEstateAgencyCreate, db: DbSession):
    return get_admin_service(db).create_real_estate_agency(payload)


@router.put("/real-estate-agencies/{agency_id}", response_model=RealEstateAgencyRead)
def update_real_estate_agency(agency_id: int, payload: RealEstateAgencyUpdate, db: DbSession):
    return get_admin_service(db).update_real_estate_agency(agency_id, payload)


@router.delete("/real-estate-agencies/{agency_id}", status_code=204)
def delete_real_estate_agency(agency_id: int, db: DbSession):
    get_admin_service(db).delete_real_estate_agency(agency_id)


@router.post("/import/{resource}/preview", response_model=ImportPreviewResponse)
def preview_import(resource: str, db: DbSession, file: UploadFile = File(...)):
    return get_admin_service(db).preview_import(resource, file)


@router.post("/import/{resource}/commit", response_model=ImportCommitResponse)
def commit_import(resource: str, db: DbSession, file: UploadFile = File(...)):
    return get_admin_service(db).commit_import(resource, file)


@router.get("/config", response_model=list[GlobalParameterRead])
def list_global_parameters(db: DbSession):
    return get_admin_service(db).list_global_parameters()


@router.put("/config/{key}", response_model=GlobalParameterRead)
def update_global_parameter(key: str, payload: GlobalParameterUpdate, db: DbSession):
    return get_admin_service(db).update_global_parameter(key, payload)
