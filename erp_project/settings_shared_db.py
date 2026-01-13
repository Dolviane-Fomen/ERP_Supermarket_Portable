"""
Configuration Django pour utiliser la base de données PostgreSQL partagée sur OVH
Tous les PCs locaux se connectent à la même base de données sur OVH
Les modifications en local sont visibles IMMEDIATEMENT en ligne (temps réel)
"""
from .settings import *
import os
from decouple import config

# Garder le DEBUG activé pour le développement local
DEBUG = True

# Base de données PostgreSQL partagée sur OVH
# Tous les PCs utilisent la même base de données = synchronisation temps réel
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('SHARED_DB_NAME', default='erp_db'),
        'USER': config('SHARED_DB_USER', default='erp_user'),
        'PASSWORD': config('SHARED_DB_PASSWORD', default=''),
        'HOST': config('SHARED_DB_HOST', default='51.68.124.152'),  # IP du serveur OVH
        'PORT': config('SHARED_DB_PORT', default='5432'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 600,  # Garder les connexions ouvertes
    }
}

# Les autres paramètres héritent de settings.py
# Tout est identique sauf la base de données qui est partagée

