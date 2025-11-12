from fastapi import APIRouter, Depends, HTTPException
from fastapi.exceptions import ValidationException

from src.dependencies import get_service
from src.services.incidents import IncidentService
from src.schemas.incidents import IncidentCreate, IncidentRead, incident_statuses


router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/", response_model=IncidentRead)
async def create_incident(
    incident: IncidentCreate,
    service: IncidentService = Depends(get_service)
):
    return await service.add(incident)

@router.get("/", response_model=list[IncidentRead])
async def list_incidents(
    status: str | None = None,
    service: IncidentService = Depends(get_service)
):
    try:
        return await service.get_all(status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Status must be one of these statuses: {incident_statuses}")

