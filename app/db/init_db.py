# app/db/init_db.py
import asyncio
from app.db.base import Base, engine
from app.db.models import user  # importe le modèle pour l’inclure dans Base.metadata

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables créées avec succès !")

if __name__ == "__main__":
    asyncio.run(init_db())
