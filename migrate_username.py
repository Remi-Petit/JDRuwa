"""
Script de mise à jour de la base de données pour ajouter le champ username
À exécuter une fois après avoir modifié le modèle User
"""
from sqlalchemy import text
from app.db.base import engine, Base

async def migrate_database():
    """Ajoute la colonne username à la table users existante"""
    async with engine.begin() as conn:
        # Vérifier si la colonne username existe déjà
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'users' AND column_name = 'username'
        """))
        
        if result.fetchone() is None:
            print("Ajout de la colonne 'username' à la table 'users'...")
            
            # Ajouter la colonne username
            await conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN username VARCHAR(50) UNIQUE
            """))
            
            # Créer un index sur username
            await conn.execute(text("""
                CREATE INDEX ix_users_username ON users (username)
            """))
            
            print("✓ Colonne 'username' ajoutée avec succès")
        else:
            print("✓ La colonne 'username' existe déjà")

async def main():
    """Point d'entrée principal"""
    try:
        await migrate_database()
        print("\n✓ Migration terminée avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de la migration : {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())