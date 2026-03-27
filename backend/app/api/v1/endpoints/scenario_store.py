from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid

router = APIRouter()

# ---------------------------------------------------------------------------
# In-memory store — will be replaced by MSSQLServer persistence.
# Schema maps to api_contracts_draft.md Endpoint 4.
# TODO:DB replace dict with SQLAlchemy model write/read.
# ---------------------------------------------------------------------------
_scenarios_store: Dict[str, Any] = {}


class ScenarioSaveRequest(BaseModel):
    name: str
    scenario_payload: Dict[str, Any]
    last_calculation_hash: Optional[str] = None
    tags: List[str] = []


@router.post("", status_code=201)
def save_scenario(request: ScenarioSaveRequest):
    """
    POST /api/v1/scenarios
    Persists a scenario payload without recalculating.
    TODO:DB replace in-memory store with INSERT into MSSQLServer.
    """
    scenario_id = str(uuid.uuid4())
    saved_at = datetime.now(timezone.utc).isoformat()
    record = {
        "scenario_id": scenario_id,
        "name": request.name,
        "version": 1,
        "saved_at": saved_at,
        "last_calculation_hash": request.last_calculation_hash,
        "tags": request.tags,
        "scenario_payload": request.scenario_payload,
    }
    _scenarios_store[scenario_id] = record
    return {
        "scenario_id": scenario_id,
        "name": request.name,
        "version": 1,
        "saved_at": saved_at,
        "last_calculation_hash": request.last_calculation_hash,
    }


@router.get("/{scenario_id}")
def get_scenario(scenario_id: str):
    """
    GET /api/v1/scenarios/{scenario_id}
    Returns the persisted payload exactly as saved.
    TODO:DB replace dict lookup with SELECT FROM MSSQLServer.
    """
    record = _scenarios_store.get(scenario_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {scenario_id}")
    return record
