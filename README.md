# Initialiser un environnement virtuel python avec Poetry
* poetry init

# Pour installer des packages avec Poetry
* poetry add ...

# Pour installer les dépendances du projet avec Poetry
* poetry install

# Lancement des tests
* $env:PYTHONPATH = "."
* poetry run pytest -s

# Création / Modification DB
* poetry run python app/db/init_db.py

# Lancer le serveur FastAPI
* poetry run uvicorn main:app --host 0.0.0.0 --port 8200 --reload

## En cours...