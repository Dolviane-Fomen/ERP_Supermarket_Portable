"""
Django settings pour exécutable standalone avec SQLite
Version optimisée pour Auto-py-to-exe
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z1h(-)o^w(hvn*3+13-pv9uj-rulzsv!k$c@yhaka$3ye$fz)*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Changer à True pour le test

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Permet uniquement les connexions locales

# Autoriser explicitement les origines CSRF en HTTP local (mode autonome)
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# Configuration des cookies pour le mode portable - CORRIGÉE
# SESSION_COOKIE_DOMAIN = None  # Commenté pour éviter les conflits
# CSRF_COOKIE_DOMAIN = None     # Commenté pour éviter les conflits
# SESSION_COOKIE_NAME = 'sessionid'  # Utilise la valeur par défaut
# SESSION_COOKIE_PATH = '/'          # Utilise la valeur par défaut
# CSRF_COOKIE_NAME = 'csrftoken'     # Utilise la valeur par défaut
# CSRF_COOKIE_PATH = '/'             # Utilise la valeur par défaut

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'supermarket',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'erp_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'erp_project.wsgi.application'

# Database - SQLite pour exécutable (utilise votre base existante)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_erp.sqlite3',  # Votre base de données existante
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration des sessions - Optimisée pour l'application portable (CORRIGÉE)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 heures
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# SESSION_COOKIE_SECURE = False  # Utilise la valeur par défaut (False)
# SESSION_COOKIE_HTTPONLY = False  # Utilise la valeur par défaut (True) pour la sécurité
# SESSION_COOKIE_SAMESITE = 'Lax'  # Utilise la valeur par défaut ('Lax')

# Configuration CSRF pour le mode portable - SIMPLIFIÉE
CSRF_COOKIE_SECURE = False  # Désactivé pour HTTP local
# CSRF_COOKIE_HTTPONLY = False  # Utilise la valeur par défaut (False)
# CSRF_COOKIE_SAMESITE = 'Lax'  # Utilise la valeur par défaut ('Lax')
# CSRF_USE_SESSIONS = False  # Utilise la valeur par défaut (False)

# Configuration d'authentification
LOGIN_URL = '/caisse/login/'
LOGIN_REDIRECT_URL = '/caisse/'
LOGOUT_REDIRECT_URL = '/'

# Configuration pour exécutable
if getattr(sys, 'frozen', False):
    # Mode exécutable
    STATIC_ROOT = os.path.join(sys._MEIPASS, 'static')
    # Base de données dans le même dossier que l'exécutable (votre base existante)
    DATABASES['default']['NAME'] = os.path.join(os.path.dirname(sys.executable), 'db_erp.sqlite3')