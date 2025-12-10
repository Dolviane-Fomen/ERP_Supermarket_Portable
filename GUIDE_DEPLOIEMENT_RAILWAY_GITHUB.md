# 🚀 Guide Complet : Déployer votre ERP sur Railway via GitHub

## 📋 Table des Matières

1. [Prérequis](#prerequis)
2. [Étape 1 : Créer un compte GitHub](#etape1)
3. [Étape 2 : Préparer votre projet local](#etape2)
4. [Étape 3 : Créer un dépôt GitHub](#etape3)
4. [Étape 4 : Pousser votre code sur GitHub](#etape4)
5. [Étape 5 : Créer un compte Railway](#etape5)
6. [Étape 6 : Connecter Railway à GitHub](#etape6)
7. [Étape 7 : Configurer l'application Django](#etape7)
8. [Étape 8 : Ajouter PostgreSQL](#etape8)
9. [Étape 9 : Configurer les variables d'environnement](#etape9)
10. [Étape 10 : Exécuter les migrations](#etape10)
11. [Étape 11 : Configurer le domaine personnalisé](#etape11)
12. [Étape 12 : Tester et finaliser](#etape12)
13. [Mises à jour futures](#mises-a-jour)

---

## ✅ PRÉREQUIS {#prerequis}

Avant de commencer, assurez-vous d'avoir :

- ✅ Votre projet ERP Django fonctionnel localement
- ✅ Un ordinateur Windows avec accès Internet
- ✅ GitHub Desktop (sera installé à l'étape 2)
- ✅ Un compte email pour GitHub et Railway

**Durée totale estimée** : ~66 minutes (plus rapide avec GitHub Desktop !)

---

## 📝 ÉTAPE 1 : Créer un Compte GitHub {#etape1}

### 1.1 Aller sur GitHub

1. Ouvrir votre navigateur (Chrome, Edge, Firefox)
2. Aller sur https://github.com
3. Cliquer sur "Sign up" (en haut à droite)

### 1.2 Créer le Compte

1. **Email** : Entrer votre adresse email
2. **Password** : Créer un mot de passe fort (minimum 8 caractères)
3. **Username** : Choisir un nom d'utilisateur unique (ex: `votre-nom` ou `votre-entreprise`)
4. Cliquer sur "Continue"

### 1.3 Vérification

1. GitHub vous enverra un code de vérification par email
2. Entrer le code reçu
3. Cliquer sur "Continue"

### 1.4 Configuration Initiale

1. **Product updates** : Choisir selon préférence (peut être désactivé)
2. Cliquer sur "Continue"
3. Cliquer sur "Complete setup"

**Durée** : 5 minutes

✅ **Votre compte GitHub est créé !**

---

## 🔧 ÉTAPE 2 : Installer GitHub Desktop {#etape2}

### 2.1 Télécharger GitHub Desktop

1. Aller sur https://desktop.github.com
2. Cliquer sur "Download for Windows"
3. Télécharger l'installateur
4. Exécuter l'installateur
5. Installer GitHub Desktop (garder les options par défaut)

### 2.2 Ouvrir GitHub Desktop

1. Lancer GitHub Desktop depuis le menu Démarrer
2. GitHub Desktop s'ouvre automatiquement

### 2.2 Préparer les Fichiers Nécessaires

**Vérifier que ces fichiers existent dans votre projet :**

#### `requirements.txt` (à la racine du projet)

Doit contenir au minimum :
```
django>=5.2.7
gunicorn>=21.2.0
psycopg2-binary>=2.9.9
whitenoise>=6.6.0
dj-database-url>=2.1.0
pillow>=11.3.0
openpyxl>=3.1.5
reportlab>=4.4.4
```

#### `Procfile` (à la racine du projet)

Créer un fichier `Procfile` (sans extension) avec :
```
web: gunicorn erp_project.wsgi:application --bind 0.0.0.0:$PORT
```

#### `erp_project/settings_production.py`

Créer ou vérifier ce fichier :
```python
import os
from .settings import *
import dj_database_url

# Sécurité
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Base de données (Railway fournit DATABASE_URL)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# HTTPS
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Fichiers statiques
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# WhiteNoise pour fichiers statiques
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

#### `.gitignore` (à la racine du projet)

Créer un fichier `.gitignore` pour exclure les fichiers sensibles :
```
# Django
*.log
*.pot
*.pyc
__pycache__/
db.sqlite3
db_erp*.sqlite3
local_settings.py

# Environnement virtuel
venv/
env/
.venv

# Fichiers d'environnement
.env
.env.local

# Fichiers statiques collectés
staticfiles/
static_root/

# Médias
media/
media_root/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

**Durée** : 10 minutes

✅ **Votre projet est prêt pour GitHub !**

---

## 📦 ÉTAPE 3 : Se Connecter à GitHub via GitHub Desktop {#etape3}

### 3.1 Se Connecter

1. Dans GitHub Desktop, cliquer sur "Sign in to GitHub.com"
2. Une fenêtre de navigateur s'ouvre
3. Autoriser GitHub Desktop à accéder à votre compte GitHub
4. Se connecter avec votre compte GitHub (créé à l'étape 1)

**Si vous n'avez pas encore de compte GitHub :**
- Cliquer sur "Create your free account"
- Suivre les étapes pour créer un compte
- Revenir à GitHub Desktop et se connecter

**Durée** : 2 minutes

✅ **GitHub Desktop est connecté à votre compte GitHub !**

---

## 📤 ÉTAPE 4 : Ajouter votre Projet à GitHub Desktop {#etape4}

### 4.1 Ajouter le Dossier Local

1. Dans GitHub Desktop, cliquer sur "File" → "Add local repository"
2. Cliquer sur "Choose..." (ou "Browse" selon la version)
3. Naviguer vers votre dossier ERP : `C:\django erp\ERP_Supermarket_Portable`
4. Sélectionner le dossier
5. Cliquer sur "Add repository"

**Si le dossier n'est pas encore un dépôt Git :**
- GitHub Desktop vous proposera de créer un dépôt
- Cliquer sur "Create a repository"
- Configuration :
  - **Name** : `erp-supermarket`
  - **Description** : "ERP Supermarket - Système de gestion Django" (optionnel)
  - **Local path** : Vérifier que c'est le bon chemin
  - **Git ignore** : Python (déjà sélectionné)
  - **License** : None (ou choisir selon préférence)
6. Cliquer sur "Create repository"

**Durée** : 2 minutes

✅ **Votre projet est maintenant dans GitHub Desktop !**

---

## 📦 ÉTAPE 5 : Publier sur GitHub {#etape5}

### 5.1 Voir vos Fichiers

Dans GitHub Desktop, vous verrez :
- **Colonne de gauche** : Tous vos fichiers du projet
- **Colonne du bas** : Zone pour le message de commit

### 5.2 Faire le Premier Commit

1. En bas à gauche, dans la zone "Summary", écrire :
   ```
   Initial commit - ERP Supermarket
   ```
2. (Optionnel) Ajouter une description dans "Description"
3. Cliquer sur le bouton "Commit to main" (en bas à gauche)

### 5.3 Publier sur GitHub

1. Après le commit, vous verrez un bouton "Publish repository" en haut
2. Cliquer sur "Publish repository"
3. Configuration :
   - **Name** : `erp-supermarket` (ou autre nom)
   - **Description** : "ERP Supermarket - Système de gestion Django" (optionnel)
   - **Keep this code private** : ✅ **COCHER** (recommandé pour la sécurité)
4. Cliquer sur "Publish repository"

GitHub Desktop va automatiquement :
- Créer le dépôt sur GitHub
- Pousser tous vos fichiers
- Configurer la connexion

**Durée** : 2-3 minutes (selon la taille de votre projet)

### 5.4 Vérifier sur GitHub

1. Ouvrir votre navigateur
2. Aller sur https://github.com
3. Vous devriez voir votre nouveau dépôt `erp-supermarket`
4. Cliquer dessus pour voir tous vos fichiers

**Durée** : 1 minute

✅ **Votre code est maintenant sur GitHub !**

---

## 🚂 ÉTAPE 6 : Créer un Compte Railway {#etape6}

### 5.1 Aller sur Railway

1. Ouvrir votre navigateur
2. Aller sur https://railway.app
3. Cliquer sur "Start a New Project"

### 5.2 Se Connecter avec GitHub

1. Cliquer sur "Login with GitHub"
2. Autoriser Railway à accéder à votre compte GitHub
3. Railway vous redirige vers le dashboard

**Durée** : 2 minutes

✅ **Votre compte Railway est créé !**

---

## 🔗 ÉTAPE 7 : Connecter Railway à GitHub {#etape7}

### 6.1 Créer un Nouveau Projet

1. Dans Railway, cliquer sur "New Project"
2. Sélectionner "Deploy from GitHub repo"

### 6.2 Sélectionner votre Dépôt

1. Railway affiche la liste de vos dépôts GitHub
2. Chercher `erp-supermarket` (ou le nom de votre dépôt)
3. Cliquer sur votre dépôt

### 6.3 Configuration Automatique

Railway va automatiquement :
- Détecter que c'est un projet Django/Python
- Installer les dépendances depuis `requirements.txt`
- Configurer le déploiement

**Durée** : 2 minutes

✅ **Railway est connecté à GitHub !**

---

## ⚙️ ÉTAPE 8 : Configurer l'Application Django {#etape8}

### 7.1 Vérifier le Déploiement

1. Railway commence automatiquement le déploiement
2. Vous pouvez voir les logs en temps réel
3. Attendre 2-5 minutes pour le premier déploiement

### 7.2 Vérifier les Paramètres

1. Cliquer sur votre service Django (dans Railway)
2. Onglet "Settings"
3. Vérifier :
   - **Build Command** : Laissé vide (automatique)
   - **Start Command** : Doit être `gunicorn erp_project.wsgi:application --bind 0.0.0.0:$PORT`
   - Si le `Procfile` est présent, Railway l'utilisera automatiquement

### 7.3 Configurer les Ressources (Optionnel)

Pour 20+ utilisateurs simultanés :

1. Service → "Settings" → "Resources"
2. Ajuster :
   - **RAM** : 2048 MB (2GB)
   - **CPU** : 2 vCPU
3. "Save"

**Durée** : 3 minutes

✅ **L'application Django est configurée !**

---

## 🗄️ ÉTAPE 9 : Ajouter PostgreSQL {#etape9}

### 8.1 Créer la Base de Données

1. Dans votre projet Railway, cliquer sur "New"
2. Sélectionner "Database" → "Add PostgreSQL"
3. Railway crée automatiquement la base de données

### 8.2 Vérifier les Variables d'Environnement

Railway ajoute automatiquement ces variables à votre service Django :
- `DATABASE_URL`
- `PGHOST`
- `PGPORT`
- `PGUSER`
- `PGPASSWORD`
- `PGDATABASE`

**Ces variables sont automatiquement disponibles dans votre application Django.**

### 8.3 Configurer les Ressources PostgreSQL (Optionnel)

Pour 20+ utilisateurs simultanés :

1. Service PostgreSQL → "Settings" → "Resources"
2. Ajuster :
   - **RAM** : 2048 MB (2GB)
   - **Storage** : 20GB
3. "Save"

**Durée** : 2 minutes

✅ **PostgreSQL est configuré !**

---

## 🔐 ÉTAPE 10 : Configurer les Variables d'Environnement {#etape10}

### 9.1 Accéder aux Variables

1. Cliquer sur votre service Django (pas PostgreSQL)
2. Onglet "Variables"
3. Vous verrez déjà `DATABASE_URL` (ajouté automatiquement)

### 9.2 Ajouter les Variables Nécessaires

Cliquer sur "New Variable" et ajouter :

#### Variable 1 : DJANGO_SETTINGS_MODULE
- **Name** : `DJANGO_SETTINGS_MODULE`
- **Value** : `erp_project.settings_production`
- "Add"

#### Variable 2 : SECRET_KEY
- **Name** : `SECRET_KEY`
- **Value** : Générer une clé secrète

**Générer SECRET_KEY :**

Ouvrir PowerShell dans votre projet local :
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copier la clé générée et l'utiliser comme valeur.

- "Add"

#### Variable 3 : ALLOWED_HOSTS
- **Name** : `ALLOWED_HOSTS`
- **Value** : `votre-domaine.com,www.votre-domaine.com,*.railway.app`
- (Remplacez `votre-domaine.com` par votre domaine, ou laissez `*.railway.app` pour l'instant)
- "Add"

#### Variable 4 : DEBUG
- **Name** : `DEBUG`
- **Value** : `False`
- "Add"

#### Variable 5 : SECURE_SSL_REDIRECT
- **Name** : `SECURE_SSL_REDIRECT`
- **Value** : `True`
- "Add"

### 9.3 Vérifier les Variables

Vous devriez avoir :
- ✅ `DATABASE_URL` (automatique)
- ✅ `DJANGO_SETTINGS_MODULE`
- ✅ `SECRET_KEY`
- ✅ `ALLOWED_HOSTS`
- ✅ `DEBUG`
- ✅ `SECURE_SSL_REDIRECT`

### 9.4 Redéployer

Après avoir ajouté les variables, Railway redéploie automatiquement.

**Durée** : 5 minutes

✅ **Les variables d'environnement sont configurées !**

---

## 🗃️ ÉTAPE 11 : Exécuter les Migrations {#etape11}

### 10.1 Installer Railway CLI (Optionnel mais Recommandé)

**Sur Windows (PowerShell) :**

```powershell
iwr https://railway.app/install.ps1 | iex
```

**Ou télécharger manuellement :**
1. Aller sur https://railway.app/cli
2. Télécharger pour Windows
3. Installer

### 10.2 Se Connecter à Railway

```powershell
railway login
```

Ouvre le navigateur pour autoriser Railway CLI.

### 10.3 Lier le Projet

```powershell
railway link
```

Sélectionner votre projet dans la liste.

### 10.4 Exécuter les Migrations

```powershell
railway run python manage.py migrate
```

### 10.5 Collecter les Fichiers Statiques

```powershell
railway run python manage.py collectstatic --noinput
```

### 10.6 Créer un Superutilisateur

```powershell
railway run python manage.py createsuperuser
```

Suivre les instructions pour créer le compte admin.

**Alternative sans CLI :**

1. Railway → Service Django → "Deployments"
2. Cliquer sur le dernier déploiement
3. "View Logs"
4. Utiliser "Run Command" pour exécuter des commandes

**Durée** : 10 minutes

✅ **La base de données est configurée !**

---

## 🌐 ÉTAPE 12 : Configurer le Domaine Personnalisé {#etape12}

### 11.1 Obtenir l'URL Railway

1. Service Django → "Settings" → "Networking"
2. Vous verrez l'URL Railway : `votre-app.railway.app`
3. Cette URL fonctionne déjà avec SSL gratuit !

### 11.2 Ajouter un Domaine Personnalisé (Optionnel)

**Si vous avez un domaine :**

#### Option A : Acheter via Railway

1. Railway → "Settings" → "Domains"
2. "Add Domain"
3. Rechercher et acheter votre domaine (~10-15$/an)
4. Configuration automatique

#### Option B : Utiliser un Domaine Existant

1. Service Django → "Settings" → "Networking"
2. "Custom Domain"
3. Ajouter votre domaine : `votre-domaine.com`
4. Railway affiche les enregistrements DNS :
   - **Type CNAME** : `www` → `votre-app.railway.app`
   - **Type A** : `@` → [IP fournie]

5. Aller chez votre registrar (Namecheap, OVH, etc.)
6. Ajouter ces enregistrements DNS
7. Attendre 1-2h pour propagation
8. Railway génère automatiquement le certificat SSL (gratuit)

**Durée** : 15 minutes + attente propagation DNS

✅ **Le domaine est configuré !**

---

## ✅ ÉTAPE 13 : Tester et Finaliser {#etape13}

### 12.1 Tester l'Application

1. Visiter votre URL Railway : `https://votre-app.railway.app`
   - Ou votre domaine personnalisé si configuré
2. Vérifier :
   - ✅ Page d'accueil s'affiche
   - ✅ Cadenas vert (HTTPS)
   - ✅ Connexion fonctionne
   - ✅ Toutes les fonctionnalités marchent

### 12.2 Vérifier les Logs

1. Service Django → "Deployments"
2. Cliquer sur le dernier déploiement
3. "View Logs"
4. Vérifier qu'il n'y a pas d'erreurs

### 12.3 Vérifier les Métriques (Plan Pro)

1. Service Django → "Metrics"
2. Vérifier :
   - CPU usage
   - RAM usage
   - Request count

**Durée** : 10 minutes

✅ **Votre ERP est en ligne sur Railway !**

---

## 🔄 MISES À JOUR FUTURES {#mises-a-jour}

### Comment Mettre à Jour votre Application avec GitHub Desktop

**Méthode Simple (Sans Commandes) :**

1. Faire vos modifications dans votre projet local
2. Tester localement
3. Ouvrir GitHub Desktop
4. Vous verrez vos fichiers modifiés dans la colonne de gauche
5. En bas à gauche, dans "Summary", écrire un message de commit :
   ```
   Ajout nouvelle fonctionnalité
   ```
   (ou toute autre description de vos modifications)
6. Cliquer sur "Commit to main"
7. Cliquer sur "Push origin" (bouton en haut, à droite)
8. Railway déploie automatiquement en quelques minutes !

**Vérifier le Déploiement :**

1. Railway → "Deployments"
2. Voir le nouveau déploiement en cours
3. Attendre qu'il soit "Success"
4. Tester l'application

**Durée** : 5-10 minutes par mise à jour

### Avantages de GitHub Desktop

- ✅ Pas besoin de connaître les commandes Git
- ✅ Interface graphique intuitive
- ✅ Voir tous les fichiers modifiés visuellement
- ✅ Un clic pour commit et push

---

## 📊 RÉCAPITULATIF DES ÉTAPES

| Étape | Description | Durée |
|-------|-------------|-------|
| 1 | Créer compte GitHub | 5 min |
| 2 | Installer GitHub Desktop | 3 min |
| 3 | Se connecter à GitHub | 2 min |
| 4 | Ajouter projet à GitHub Desktop | 2 min |
| 5 | Publier sur GitHub | 3 min |
| 6 | Créer compte Railway | 2 min |
| 7 | Connecter Railway à GitHub | 2 min |
| 8 | Configurer Django | 3 min |
| 9 | Ajouter PostgreSQL | 2 min |
| 10 | Variables d'environnement | 5 min |
| 11 | Migrations | 10 min |
| 12 | Domaine personnalisé | 15 min |
| 13 | Tester | 10 min |
| **TOTAL** | - | **~66 minutes** |

---

## 🆘 DÉPANNAGEMENT

### Le déploiement échoue

1. Vérifier les logs : Service → "Deployments" → "View Logs"
2. Vérifier que `requirements.txt` contient toutes les dépendances
3. Vérifier que `Procfile` est correct
4. Vérifier les variables d'environnement

### Erreur de connexion à la base de données

1. Vérifier que PostgreSQL est créé
2. Vérifier que `DATABASE_URL` est présent dans les variables
3. Vérifier que `dj-database-url` est dans `requirements.txt`

### L'application ne démarre pas

1. Vérifier les logs
2. Vérifier que `SECRET_KEY` est configuré
3. Vérifier que `ALLOWED_HOSTS` contient votre domaine

### Le domaine ne fonctionne pas

1. Vérifier les enregistrements DNS
2. Attendre 1-2h pour propagation
3. Vérifier avec https://www.whatsmydns.net

---

## ✅ CHECKLIST FINALE

- [ ] Compte GitHub créé
- [ ] GitHub Desktop installé
- [ ] Projet ajouté à GitHub Desktop
- [ ] Code publié sur GitHub (via GitHub Desktop)
- [ ] Compte Railway créé
- [ ] Projet Railway créé depuis GitHub
- [ ] PostgreSQL ajouté
- [ ] Variables d'environnement configurées
- [ ] Migrations exécutées
- [ ] Superutilisateur créé
- [ ] Domaine configuré (optionnel)
- [ ] Application testée et fonctionnelle

---

## 🎯 CONCLUSION

Votre ERP est maintenant :
- ✅ En ligne sur Railway
- ✅ Connecté à GitHub pour mises à jour automatiques
- ✅ Avec base de données PostgreSQL
- ✅ Avec SSL/HTTPS gratuit
- ✅ Prêt pour la production

**Toutes les futures mises à jour se feront automatiquement via GitHub ! 🚀**

---

**Besoin d'aide ?** Consultez la documentation Railway : https://docs.railway.app

