# Configuration ERP Reseau Local
# Pour utilisation multi-PC en reseau local

from .settings_standalone import *

# Configuration reseau
ALLOWED_HOSTS = ['*']  # Autoriser toutes les adresses IP
DEBUG = True

# Configuration pour acces reseau
CSRF_TRUSTED_ORIGINS = [
    'http://192.168.1.100:8000',  # Remplacez par votre IP locale
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Configuration de la base de donnees partagee
# La base SQLite sera partagee entre tous les PC