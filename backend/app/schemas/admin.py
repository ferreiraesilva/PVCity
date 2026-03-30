from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class EnterpriseBase(BaseModel):
    name: str
    work_code: str | None = None
    spe_name: str | None = None
    city: str | None = None
    is_active: bool = True
    vpl_rate_annual: float = 0.0
    discount_percent: float = 0.0
    delivery_month: str | None = None
    launch_date: str | None = None
    stage: str | None = None


class EnterpriseCreate(EnterpriseBase):
    pass


class EnterpriseUpdate(EnterpriseBase):
    pass


class EnterpriseRead(EnterpriseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UnitBase(BaseModel):
    enterprise_id: int
    code: str
    product_unit_key: str | None = None
    unit_type: str | None = None
    suites: int | None = None
    garage_code: str | None = None
    garage_spots: int | None = None
    private_area_m2: float = 0.0
    base_price: float = 0.0
    status: str | None = None
    ideal_capture_percent: float = 1.0


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    pass


class UnitRead(UnitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class StandardFlowBase(BaseModel):
    enterprise_id: int
    periodicity: str
    installment_count: int = 1
    start_month: int | None = None
    installment_value: float = 0.0
    percent: float = 0.0
    row_slot: int


class StandardFlowCreate(StandardFlowBase):
    pass


class StandardFlowUpdate(StandardFlowBase):
    pass


class StandardFlowRead(StandardFlowBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class RealEstateAgencyBase(BaseModel):
    name: str
    is_active: bool = True


class RealEstateAgencyCreate(RealEstateAgencyBase):
    pass


class RealEstateAgencyUpdate(RealEstateAgencyBase):
    pass


class RealEstateAgencyRead(RealEstateAgencyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ImportPreviewItem(BaseModel):
    line_number: int
    action: Literal["create", "update", "reject"]
    natural_key: str
    errors: list[str] = Field(default_factory=list)
    normalized: dict[str, Any] = Field(default_factory=dict)


class ImportPreviewResponse(BaseModel):
    resource: Literal["enterprises", "units", "standard-flows", "real-estate-agencies"]
    can_commit: bool
    summary: dict[str, int]
    items: list[ImportPreviewItem]


class ImportCommitResponse(BaseModel):
    resource: Literal["enterprises", "units", "standard-flows", "real-estate-agencies"]
    summary: dict[str, int]
    errors: list[dict[str, Any]] = Field(default_factory=list)


class GlobalParameterBase(BaseModel):
    key: str
    value: float
    description: str | None = None


class GlobalParameterUpdate(BaseModel):
    value: float


class GlobalParameterRead(GlobalParameterBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
