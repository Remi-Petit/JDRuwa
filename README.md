# Créer un environnement virtuel python
python -m venv env

# Accéder à son environnement virtuel

## Windows :
env/Scripts/activate

## Linux :
source env/bin/activate

# Quitter l'environnement virtuel si besoin :
deactivate

# Installation des requirements du projet :
pip install --no-cache-dir -r requirements.txt

## Créer un fichier requirements.txt (/!\ pour les devs seulement) :
pip freeze > requirements.txt

# Lancer le serveur FastAPI
python main.py

## En cours...