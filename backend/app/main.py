from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.modules import router as modules_router
from app.config.settings import get_settings
from app.core.logging import configure_logging, get_logger
from app.database.session import dispose_database, initialize_database
from app.middleware.request_id import RequestIdMiddleware

settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("starting application", extra={"service": settings.project_name})
    initialize_database()
    try:
        yield
    finally:
        logger.info("stopping application", extra={"service": settings.project_name})
        dispose_database()


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        version=settings.api_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_docs else None,
        openapi_url="/openapi.json" if settings.enable_docs else None,
    )

    application.add_middleware(RequestIdMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    application.include_router(health_router, prefix=settings.api_prefix)
    application.include_router(modules_router, prefix=settings.api_prefix)
    return application


app = create_application()
