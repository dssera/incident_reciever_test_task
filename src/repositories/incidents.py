# app/repositories/incident_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas.incidents import IncidentCreate
from src.models import Incident


class IncidentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, incident: IncidentCreate) -> Incident:
        db_incident = Incident(
            description=incident.description,
            source=incident.source,
        )
        self.session.add(db_incident)
        await self.session.commit()
        await self.session.refresh(db_incident)
        return db_incident

    async def get_all(self, status: str | None = None) -> list[Incident]:
        stmt = select(Incident)
        if status:
            stmt = stmt.where(Incident.status == status)
        stmt = stmt.order_by(Incident.created_at.desc())

        result = await self.session.execute(stmt)
        return result.scalars().all()
