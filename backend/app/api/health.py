from typing import Annotated

from fastapi import APIRouter, Depends

from backend.app.core.config import Settings, get_settings
from backend.app.schemas.database import DatabaseStatus
from backend.app.services.database_health import check_database_connection

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health(settings: Annotated[Settings, Depends(get_settings)]) -> dict[str, str]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
        "data_mode": settings.app_data_mode,
    }


@router.get("/health/database", response_model=DatabaseStatus)
def database_health(settings: Annotated[Settings, Depends(get_settings)]) -> DatabaseStatus:
    return check_database_connection(settings)
