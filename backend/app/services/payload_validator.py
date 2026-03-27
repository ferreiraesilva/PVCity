from __future__ import annotations
from dataclasses import dataclass
from typing import List, Set

from fastapi import HTTPException

from app.schemas.scenarios import CalculationRequest

VALID_SLOT_RANGE = range(39, 59)  # slots 39 to 58 inclusive
KNOWN_WARNINGS = [
    "hidden_override_commission_rule_unverified",
    "broken_validation_source_l12",
    "permuta_flag_p95_unverified",
    "table_metadata_ref_not_trusted",
]

ERROR_INVALID_SLOT = "INVALID_SLOT"
ERROR_DUPLICATE_SLOT = "DUPLICATE_SLOT"
ERROR_PERMUTA_BLOCK_REQUIRED = "PERMUTA_BLOCK_REQUIRED"
ERROR_ENUM_NOT_ALLOWED = "ENUM_NOT_ALLOWED"
ERROR_MODIFICATION_VALUE_REQUIRED = "MODIFICATION_VALUE_REQUIRED"


@dataclass(frozen=True)
class ValidationError:
    code: str
    message: str
    field: str


class PayloadValidator:
    """
    Validates a CalculationRequest before it reaches the engine.
    Implements the blocking rules from api_contracts_draft.md (lines 1163-1182).
    Raises HTTPException 422 on first failure group.
    """

    def validate(self, request: CalculationRequest) -> List[str]:
        errors: List[ValidationError] = []
        errors.extend(self._validate_permuta_consistency(request))
        errors.extend(self._validate_modification_values(request))
        errors.extend(self._validate_sale_slots(request))
        errors.extend(self._validate_exchange_slots(request))

        if errors:
            raise HTTPException(
                status_code=422,
                detail=[{"code": e.code, "message": e.message, "field": e.field} for e in errors],
            )

        return KNOWN_WARNINGS

    def _validate_permuta_consistency(self, request: CalculationRequest) -> List[ValidationError]:
        errors: List[ValidationError] = []
        is_permuta_mode = request.scenario_mode.value == "PERMUTA"
        has_permuta_flag = request.product_context.has_permuta

        if is_permuta_mode and not has_permuta_flag:
            errors.append(ValidationError(
                code=ERROR_PERMUTA_BLOCK_REQUIRED,
                message="PERMUTA mode requires product_context.has_permuta=true",
                field="product_context.has_permuta",
            ))

        if is_permuta_mode and not request.exchange_flow_rows:
            errors.append(ValidationError(
                code=ERROR_PERMUTA_BLOCK_REQUIRED,
                message="PERMUTA mode requires exchange_flow_rows to be present",
                field="exchange_flow_rows",
            ))

        return errors

    def _validate_modification_values(self, request: CalculationRequest) -> List[ValidationError]:
        errors: List[ValidationError] = []
        ctx = request.product_context
        kind = ctx.modification_kind.value

        if kind == "Decorado (R$/m²)" and ctx.decorated_value_per_m2 is None:
            errors.append(ValidationError(
                code=ERROR_MODIFICATION_VALUE_REQUIRED,
                message="decorated_value_per_m2 is required when modification_kind is 'Decorado (R$/m²)'",
                field="product_context.decorated_value_per_m2",
            ))

        if kind == "Facility (R$/m²)" and ctx.facility_value_per_m2 is None:
            errors.append(ValidationError(
                code=ERROR_MODIFICATION_VALUE_REQUIRED,
                message="facility_value_per_m2 is required when modification_kind is 'Facility (R$/m²)'",
                field="product_context.facility_value_per_m2",
            ))

        return errors

    def _validate_sale_slots(self, request: CalculationRequest) -> List[ValidationError]:
        return self._validate_slots(request.sale_flow_rows, "sale_flow_rows")

    def _validate_exchange_slots(self, request: CalculationRequest) -> List[ValidationError]:
        if not request.exchange_flow_rows:
            return []
        return self._validate_slots(request.exchange_flow_rows, "exchange_flow_rows")

    def _validate_slots(self, rows: list, field_prefix: str) -> List[ValidationError]:
        errors: List[ValidationError] = []
        if not request_strict_mode(rows):
            return errors

        seen: Set[int] = set()
        for row in rows:
            slot = row.row_slot

            if slot not in VALID_SLOT_RANGE:
                errors.append(ValidationError(
                    code=ERROR_INVALID_SLOT,
                    message=f"row_slot {slot} is outside allowed range 39-58",
                    field=f"{field_prefix}[row_slot={slot}]",
                ))

            if slot in seen:
                errors.append(ValidationError(
                    code=ERROR_DUPLICATE_SLOT,
                    message=f"row_slot {slot} appears more than once",
                    field=f"{field_prefix}[row_slot={slot}]",
                ))
            seen.add(slot)

        return errors


def request_strict_mode(rows: list) -> bool:
    # All requests are strict unless explicitly disabled (future flag)
    return True
