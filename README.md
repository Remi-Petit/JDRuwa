# Initialiser un environnement virtuel python avec Poetry
* poetry init

# Pour installer des packages avec Poetry
* poetry add ...

# Pour installer les dépendances du projet avec Poetry
* poetry install --no-root

# Lancement des tests
* $env:PYTHONPATH = "."
* poetry run pytest -s

# Gestion de la base de données avec Alembic

## Gestion des migrations avec Alembic
* poetry run alembic upgrade head           # Appliquer toutes les migrations
* poetry run alembic revision --autogenerate -m "Description"  # Créer une nouvelle migration
* poetry run alembic current                # Voir l'état actuel
* poetry run alembic history                # Voir l'historique

# Lancer le serveur FastAPI
* poetry run uvicorn main:app --host 0.0.0.0 --port 8200 --reload

## Documentation
* Voir `ALEMBIC_GUIDE.md` pour un guide complet des migrations

## En cours...
* ✅ Architecture en couches (Repository + Service + GraphQL)
* ✅ Authentification JWT avec Argon2
* ✅ Validations de sécurité renforcées
* ✅ Hooks SQLAlchemy pour hashage automatique des mots de passe
* ✅ Migrations Alembic configurées et testées