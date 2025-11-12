from src.schemas.incidents import IncidentCreate, IncidentStatus, incident_statuses
from src.repositories.incidents import IncidentRepository

class IncidentService:
    def __init__(self, repository: IncidentRepository):
        self.repository = repository

    async def add(self, data: IncidentCreate):
        return await self.repository.add(data)

    async def get_all(self, status: str | None = None):
        if status:
            if status in incident_statuses:
                return await self.repository.get_all(status)
            else:
                raise ValueError("Status must be one of the values of IncidentStatus enum")
        return await self.repository.get_all()
