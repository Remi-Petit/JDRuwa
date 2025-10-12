# tests/test_connection_db.py
import pytest
import asyncio
from sqlalchemy import text
from app.db.base import engine

@pytest.mark.asyncio
async def test_connection():
    """Vérifie que la base de données est accessible."""
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1;"))
        assert result.scalar() == 1
        print("✅ Connexion à la base réussie !")
