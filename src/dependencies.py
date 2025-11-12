from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.config.db_config import get_session
from src.repositories.incidents import IncidentRepository
from src.services.incidents import IncidentService


def get_service(session: AsyncSession = Depends(get_session)):
    repo = IncidentRepository(session)
    return IncidentService(repo)