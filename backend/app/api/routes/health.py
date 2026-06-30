from typing import Any

from fastapi import APIRouter, status
from sqlalchemy import text

from app.config.settings import get_settings
from app.database.session import SessionLocal
from app.schemas.health import HealthCheck

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthCheck,
    status_code=status.HTTP_200_OK,
    summary="Service health",
)
def health_check() -> HealthCheck:
    settings = get_settings()
    checks: dict[str, Any] = {"database": "ok"}

    with SessionLocal() as session:
        session.execute(text("SELECT 1"))

    return HealthCheck(
        status="ok",
        service=settings.project_name,
        version=settings.api_version,
        checks=checks,
    )
