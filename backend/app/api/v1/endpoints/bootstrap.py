from fastapi import APIRouter

from app.services.database_reference_service import DatabaseReferenceService


router = APIRouter()
reference_service = DatabaseReferenceService()


@router.get("/reference-data")
def get_reference_data():
    """
    Returns enum lists, enterprises, units from the database.
    """
    return reference_service.get_reference_data()
