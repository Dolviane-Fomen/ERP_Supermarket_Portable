"""
Configuration Django pour la production
Hérite de settings.py et surcharge les paramètres pour la production
"""
from .settings import *
import os
from pathlib import Path
import dj_database_url

# ============================================
# SÉCURITÉ - CRITIQUE EN PRODUCTION
# ============================================
DEBUG = False

# SECRET_KEY doit être dans les variables d'environnement
SECRET_KEY = os.environ.get('SECRET_KEY', 'changez-moi-en-production-avec-une-cle-secrete-longue-et-aleatoire')

# Domaines autorisés - À MODIFIER avec votre domaine
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ============================================
# BASE DE DONNÉES
# ============================================
# Railway fournit DATABASE_URL, utiliser dj-database-url pour le parser
# Si DATABASE_URL n'existe pas, utiliser les variables individuelles
if 'DATABASE_URL' in os.environ:
    # Railway fournit DATABASE_URL automatiquement
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback pour autres environnements (Azure, etc.)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'erp_db'),
            'USER': os.environ.get('DB_USER', 'erp_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            },
        }
    }

# Option 2: SQLite (pour tests ou petits déploiements)
# Décommentez si vous préférez SQLite (non recommandé pour production)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db_erp_production.sqlite3',
#     }
# }

# ============================================
# HTTPS ET SÉCURITÉ
# ============================================
# Redirection HTTPS (activer après configuration SSL)
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ============================================
# FICHIERS STATIQUES
# ============================================
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Créer le dossier staticfiles s'il n'existe pas
STATIC_ROOT.mkdir(exist_ok=True)

# WhiteNoise pour servir les fichiers statiques en production
# Ajouter WhiteNoise au middleware (après SecurityMiddleware)
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Configuration WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================
# FICHIERS MÉDIAS (si vous avez des uploads)
# ============================================
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Créer le dossier media s'il n'existe pas
MEDIA_ROOT.mkdir(exist_ok=True)

# ============================================
# LOGGING
# ============================================
# Créer le dossier logs s'il n'existe pas
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'supermarket': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================
# PERFORMANCE
# ============================================
# Cache (optionnel - peut utiliser Redis ou Memcached)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#     }
# }

# ============================================
# EMAIL (si vous envoyez des emails)
# ============================================
# Configuration email pour la production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@votre-domaine.com')

# ============================================
# SESSIONS
# ============================================
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 heures
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ============================================
# TIMEZONE
# ============================================
# Ajustez selon votre localisation
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
USE_TZ = True

