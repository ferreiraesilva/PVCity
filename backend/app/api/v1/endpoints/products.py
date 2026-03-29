from fastapi import APIRouter, HTTPException

from app.services.database_reference_service import DatabaseReferenceService


router = APIRouter()
reference_service = DatabaseReferenceService()


@router.get("/{enterprise_name}/units/{unit_code}/defaults")
def get_unit_defaults(enterprise_name: str, unit_code: str):
    """
    Returns the initial analysis state anchored to the selected enterprise and unit.
    This is operational runtime data and must not depend on the workbook.
    """
    try:
        return reference_service.get_unit_defaults(enterprise_name, unit_code)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
