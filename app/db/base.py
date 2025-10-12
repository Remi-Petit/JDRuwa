# app/db/base.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Base declarative pour les modèles
Base = declarative_base()

# Moteur de connexion (async)
engine = create_async_engine(
    settings.database_url,
    echo=settings.APP_DEBUG,  # affiche les requêtes SQL en mode debug
    future=True
)

# Factory de session
async_session_factory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Dependency FastAPI
async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
