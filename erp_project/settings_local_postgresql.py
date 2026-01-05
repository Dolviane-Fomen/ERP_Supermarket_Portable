"""
Configuration Django pour PostgreSQL en local
Copie de settings.py avec PostgreSQL au lieu de SQLite
"""
from .settings import *
import os

# Base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'erp_db',
        'USER': 'erp_user',
        'PASSWORD': 'VOTRE_MOT_DE_PASSE_SECURISE',  # À REMPLACER par votre mot de passe
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Garder les autres paramètres de settings.py






