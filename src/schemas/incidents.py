from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum


class IncidentStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

incident_statuses = [e.value for e in IncidentStatus]

class IncidentCreate(BaseModel):
    description: str
    source: str

class IncidentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    description: str
    status: IncidentStatus
    source: str
    created_at: datetime
