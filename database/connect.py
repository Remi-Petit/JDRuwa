# database/connect.py
from fastapi import HTTPException
import asyncpg
from typing import AsyncGenerator, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from config.env import get_settings

_settings = get_settings()

engine = create_async_engine(
    _settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    future=True,
)

# Session factory (SQLAlchemy 2.x)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Dépendance FastAPI pour obtenir une session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except asyncpg.exceptions.ConnectionDoesNotExistError:
        raise HTTPException(
            status_code=503,
            detail="Database connection error. Please try again later."
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection error. Please try again later."
        )

# Healthcheck DB: SELECT 1 + métadonnées
async def check_db() -> Dict[str, Any]:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": _settings.POSTGRES_DB,
            "host": _settings.POSTGRES_HOST,
            "port": _settings.POSTGRES_PORT,
            "driver": "asyncpg",
        }
    except SQLAlchemyError as exc:
        low = str(getattr(exc, "orig", exc))
        raise RuntimeError(f"database_unreachable: {low}") from exc
