from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

class ScenarioMode(str, Enum):
    NORMAL = "NORMAL"
    PERMUTA = "PERMUTA"

class ModificationKind(str, Enum):
    NONE = "Não"
    DECORATED = "Decorado (R$/m²)"
    FACILITY = "Facility (R$/m²)"

class Periodicity(str, Enum):
    SINAL = "Sinal"
    ENTRADA = "Entrada"
    MENSAIS = "Mensais"
    SEMESTRAIS = "Semestrais"
    UNICA = "Única"
    PERMUTA = "Permuta"
    ANUAIS = "Anuais"
    VEICULO = "Veículo"
    FINANC_BANCARIO = "Financ. Bancário"
    FINANC_DIRETO = "Financ. Direto"

class ProductContext(BaseModel):
    enterprise_name: str
    unit_code: str
    product_unit_key: str
    garage_code: Optional[str] = None
    private_area_m2: float
    analysis_date: Optional[date] = None
    delivery_month: Optional[date] = None
    modification_kind: ModificationKind
    decorated_value_per_m2: Optional[float] = None
    facility_value_per_m2: Optional[float] = None
    area_for_modification_m2: float
    prize_enabled: bool
    fully_invoiced: bool
    has_permuta: bool

class CommercialContext(BaseModel):
    city_sales_manager_name: Optional[str] = None
    real_estate_name: Optional[str] = None
    broker_name: Optional[str] = None
    manager_name: Optional[str] = None

class SecondaryCommissionSlot(BaseModel):
    slot: int
    label: Optional[str] = None
    percent: Optional[float] = None

class CommissionContext(BaseModel):
    primary_commission_label: Optional[str] = None
    primary_commission_percent: Optional[float] = None
    prize_commission_label: Optional[str] = None
    prize_commission_percent: Optional[float] = None
    secondary_commission_slots: List[SecondaryCommissionSlot] = []

class ProposalLine(BaseModel):
    row_slot: int
    installment_count: Optional[float] = None
    periodicity: Optional[str] = None
    start_month: Optional[date] = None
    installment_value: Optional[float] = None
    percent: Optional[float] = None
    total_vgv: Optional[float] = None
    adjustment_type: Optional[str] = None
    notes: Optional[str] = None

class CalculationRequest(BaseModel):
    strict_excel_mode: bool = True
    parity_trace_requested: bool = True
    scenario_mode: ScenarioMode
    product_context: ProductContext
    commercial_context: CommercialContext
    commission_context: CommissionContext
    sale_flow_rows: List[ProposalLine]
    exchange_flow_rows: List[ProposalLine]
    # Fluxo padrão da unidade — enviado pelo front para cálculo independente do PV de referência
    standard_flow_rows: List[ProposalLine] = []
