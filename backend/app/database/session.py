from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Generator
from sqlalchemy.orm import Session

from app.config.settings import get_settings

settings = get_settings()

engine: Engine = create_engine(
    str(settings.database_url),
    pool_pre_ping=True,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_timeout=settings.database_pool_timeout,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=Session,
)


def initialize_database() -> None:
    with engine.connect() as connection:
        connection.exec_driver_sql("SELECT 1")


def dispose_database() -> None:
    engine.dispose()


def get_database_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
from collections.abc import Generator
