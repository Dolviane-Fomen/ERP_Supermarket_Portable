# 🚂 Documentation Complète : Railway pour ERP Django
## Guide de Déploiement et Coûts Détaillés

---

## 📋 TABLE DES MATIÈRES

1. [Présentation de Railway](#presentation)
2. [Avantages et Inconvénients](#avantages)
3. [Coûts Détaillés](#couts)
4. [Guide de Déploiement](#deploiement)
5. [Configuration pour 20+ Utilisateurs](#configuration)
6. [Gestion du Domaine](#domaine)
7. [Base de Données PostgreSQL](#database)
8. [Monitoring et Logs](#monitoring)
9. [Scaling et Performance](#scaling)
10. [Maintenance](#maintenance)

---

## 🎯 PRÉSENTATION DE RAILWAY {#presentation}

### Qu'est-ce que Railway ?

Railway est une plateforme PaaS (Platform as a Service) moderne qui permet de déployer des applications rapidement sans configuration complexe de serveurs.

**Caractéristiques principales :**
- Déploiement automatique depuis Git
- Base de données PostgreSQL incluse
- SSL/HTTPS automatique
- Interface graphique simple
- Scaling automatique
- Support Docker et nativement Django/Python

### Pourquoi Railway pour votre ERP ?

✅ **Simplicité** : Déploiement en 10 minutes
✅ **Prix** : Beaucoup moins cher qu'Azure (~25€ vs 186€/mois)
✅ **Interface** : Tout se fait depuis le navigateur (Windows-friendly)
✅ **Base de données** : PostgreSQL inclus
✅ **SSL** : Certificat automatique et gratuit
✅ **Scaling** : Automatique selon la charge

---

## ✅ AVANTAGES ET INCONVÉNIENTS {#avantages}

### ✅ Avantages

1. **Simplicité Extrême**
   - Pas besoin de configurer Nginx, Gunicorn, etc.
   - Tout est automatique
   - Interface graphique intuitive

2. **Prix Compétitif**
   - Gratuit pour commencer (5$ crédit/mois)
   - Payant : ~20-30€/mois pour production
   - Beaucoup moins cher qu'Azure

3. **Déploiement Rapide**
   - Connecter Git → Déploiement automatique
   - Mises à jour en quelques minutes
   - Pas de configuration complexe

4. **Base de Données Incluse**
   - PostgreSQL managé inclus
   - Backups automatiques
   - Pas de configuration supplémentaire

5. **SSL Automatique**
   - Certificat généré automatiquement
   - Renouvellement automatique
   - Gratuit

6. **Scaling Automatique**
   - S'adapte à la charge
   - Pas de configuration nécessaire

### ⚠️ Inconvénients

1. **Moins de Contrôle**
   - Pas d'accès SSH direct (sauf Pro)
   - Configuration limitée comparé à VPS

2. **Coût Variable**
   - Payez à l'usage
   - Peut augmenter avec le trafic

3. **Support**
   - Support communautaire principalement
   - Pas de support téléphonique

4. **Limites du Plan Gratuit**
   - Application s'endort après inactivité
   - Crédit limité (5$/mois)

---

## 💰 COÛTS DÉTAILLÉS {#couts}

### Modèle de Tarification Railway

Railway utilise un système de **crédits** :
- Vous achetez des crédits
- Les services consomment des crédits selon l'usage
- 1$ = 1 crédit

### Plans Disponibles

#### **Plan Hobby (Gratuit)**

**Crédit mensuel** : 5$ (gratuit)
**Prix** : 0€/mois

**Limites :**
- 5$ de crédit/mois
- Application s'endort après 30 min d'inactivité
- Domaine Railway uniquement (ex: `votre-app.railway.app`)
- Pas de domaine personnalisé SSL

**Idéal pour** : Tests, développement, petits projets

#### **Plan Pro (Payant)**

**Prix** : À partir de 20$/mois (~18€/mois)
**Crédit inclus** : 20$ de crédit/mois

**Avantages :**
- Application toujours active
- Domaine personnalisé + SSL gratuit
- Backups automatiques
- Support prioritaire
- Métriques avancées

**Idéal pour** : Production, applications professionnelles

### Coûts par Service

#### **Application Web (Django)**

**Consommation de crédits :**
- **RAM** : 0,000463$/GB/heure
- **CPU** : 0,000231$/vCPU/heure

**Exemple pour 1GB RAM, 0.5 vCPU :**
- Par heure : ~0,00035$
- Par jour : ~0,0084$ (24h)
- Par mois : ~0,25$ (30 jours)

**Pour une application Django moyenne :**
- **512MB RAM, 0.5 vCPU** : ~0,15$/mois
- **1GB RAM, 1 vCPU** : ~0,50$/mois
- **2GB RAM, 2 vCPU** : ~2,00$/mois

#### **Base de Données PostgreSQL**

**Consommation de crédits :**
- **RAM** : 0,000463$/GB/heure
- **Stockage** : 0,000231$/GB/heure

**Exemple pour 1GB RAM, 10GB stockage :**
- RAM : 0,000463$/heure = 0,33$/mois
- Stockage : 0,00231$/heure = 1,66$/mois
- **Total** : ~2$/mois

**Pour une base de données moyenne :**
- **512MB RAM, 5GB stockage** : ~1$/mois
- **1GB RAM, 10GB stockage** : ~2$/mois
- **2GB RAM, 20GB stockage** : ~4$/mois
- **4GB RAM, 50GB stockage** : ~8$/mois

#### **Bandwidth (Bande Passante)**

**Coût** : 0,10$/GB

**Exemple :**
- 10GB/mois : 1$
- 50GB/mois : 5$
- 100GB/mois : 10$
- 500GB/mois : 50$

#### **Autres Services**

- **Redis Cache** : Même tarification que PostgreSQL
- **Storage (Blob)** : 0,000231$/GB/heure
- **Logs** : Gratuit (7 jours de rétention)

---

## 📊 ESTIMATION DES COÛTS POUR VOTRE ERP

### Configuration Minimum (Développement/Test)

| Service | Spécifications | Coût Mensuel |
|---------|----------------|--------------|
| **Application Django** | 512MB RAM, 0.5 vCPU | 0,15$ |
| **PostgreSQL** | 512MB RAM, 5GB stockage | 1,00$ |
| **Bandwidth** | 10GB/mois | 1,00$ |
| **TOTAL** | - | **~2,15$/mois (~2€)** |

**Avec Plan Hobby (5$ crédit gratuit)** : **0€/mois** ✅

### Configuration Recommandée (20+ Utilisateurs)

| Service | Spécifications | Coût Mensuel |
|---------|----------------|--------------|
| **Application Django** | 2GB RAM, 2 vCPU | 2,00$ |
| **PostgreSQL** | 2GB RAM, 20GB stockage | 4,00$ |
| **Bandwidth** | 50GB/mois | 5,00$ |
| **Plan Pro** | - | 20,00$ (crédit inclus) |
| **TOTAL** | - | **~31$/mois (~28€)** |

**Note** : Le plan Pro inclut 20$ de crédit, donc vous payez seulement la différence.

### Configuration Performance (50+ Utilisateurs)

| Service | Spécifications | Coût Mensuel |
|---------|----------------|--------------|
| **Application Django** | 4GB RAM, 4 vCPU | 8,00$ |
| **PostgreSQL** | 4GB RAM, 50GB stockage | 8,00$ |
| **Bandwidth** | 100GB/mois | 10,00$ |
| **Plan Pro** | - | 20,00$ (crédit inclus) |
| **Crédits supplémentaires** | - | 6,00$ |
| **TOTAL** | - | **~52$/mois (~47€)** |

### Comparaison avec Azure

| Configuration | Railway | Azure App Service | Économie |
|---------------|---------|-------------------|----------|
| **Minimum** | 2€/mois | 186€/mois | **184€/mois** |
| **Recommandée** | 28€/mois | 186€/mois | **158€/mois** |
| **Performance** | 47€/mois | 186€/mois | **139€/mois** |

**Économie moyenne** : **~150€/mois** avec Railway ! 💰

---

## 🚀 GUIDE DE DÉPLOIEMENT {#deploiement}

### PRÉREQUIS

- Compte GitHub/GitLab (avec votre code ERP)
- Compte Railway (gratuit)
- Nom de domaine (optionnel, pour production)

### ÉTAPE 1 : Créer un Compte Railway

1. Aller sur https://railway.app
2. Cliquer sur "Start a New Project"
3. Se connecter avec GitHub (recommandé) ou Email
4. Autoriser Railway à accéder à GitHub

**Durée** : 2 minutes

### ÉTAPE 2 : Créer un Nouveau Projet

1. Dans Railway, cliquer sur "New Project"
2. Choisir "Deploy from GitHub repo"
3. Sélectionner votre dépôt ERP
4. Railway détecte automatiquement Django

**Durée** : 1 minute

### ÉTAPE 3 : Configurer l'Application Django

Railway détecte automatiquement Django et configure :
- Runtime : Python
- Build : Installe les dépendances depuis `requirements.txt`
- Start : Lance l'application

**Vérifier `requirements.txt`** (doit contenir) :
```
django>=5.2.7
gunicorn>=21.2.0
psycopg2-binary>=2.9.9
whitenoise>=6.6.0
pillow>=11.3.0
openpyxl>=3.1.5
reportlab>=4.4.4
```

**Créer `Procfile`** (à la racine du projet) :
```
web: gunicorn erp_project.wsgi:application --bind 0.0.0.0:$PORT
```

**Ou créer `railway.json`** (optionnel, pour configuration avancée) :
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn erp_project.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### ÉTAPE 4 : Ajouter PostgreSQL

1. Dans votre projet Railway, cliquer sur "New"
2. Sélectionner "Database" → "Add PostgreSQL"
3. Railway crée automatiquement la base de données
4. Les variables d'environnement sont automatiquement ajoutées :
   - `DATABASE_URL`
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

**Durée** : 1 minute

### ÉTAPE 5 : Configurer les Variables d'Environnement

1. Cliquer sur votre service Django
2. Onglet "Variables"
3. Ajouter les variables suivantes :

```
DJANGO_SETTINGS_MODULE=erp_project.settings_production
SECRET_KEY=votre-cle-secrete-generee
ALLOWED_HOSTS=votre-domaine.com,*.railway.app
DEBUG=False
SECURE_SSL_REDIRECT=True
```

**Générer SECRET_KEY** :
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Variables automatiques (ne pas modifier) :**
- `DATABASE_URL` (déjà configuré par Railway)
- `PORT` (déjà configuré)

**Durée** : 5 minutes

### ÉTAPE 6 : Configurer settings_production.py

**Créer/modifier `erp_project/settings_production.py`** :

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

**Installer `dj-database-url` et `whitenoise`** :
```
pip install dj-database-url whitenoise
```

Ajouter à `requirements.txt` :
```
dj-database-url>=2.1.0
whitenoise>=6.6.0
```

### ÉTAPE 7 : Configurer le Build et le Déploiement

**Railway détecte automatiquement Django**, mais vous pouvez personnaliser :

**Créer `nixpacks.toml`** (optionnel) :
```toml
[phases.setup]
nixPkgs = ['python311', 'postgresql']

[phases.install]
cmds = [
    'pip install -r requirements.txt',
]

[phases.build]
cmds = [
    'python manage.py collectstatic --noinput',
]

[start]
cmd = 'gunicorn erp_project.wsgi:application --bind 0.0.0.0:$PORT --workers 4'
```

### ÉTAPE 8 : Déployer

1. Railway déploie automatiquement à chaque push sur GitHub
2. Ou cliquer manuellement sur "Deploy" dans Railway
3. Attendre 2-5 minutes pour le déploiement
4. Vérifier les logs dans l'onglet "Deployments"

**Durée** : 5-10 minutes (premier déploiement)

### ÉTAPE 9 : Exécuter les Migrations

**Option A : Via Railway CLI**

1. Installer Railway CLI :
```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex
```

2. Se connecter :
```bash
railway login
```

3. Lier le projet :
```bash
railway link
```

4. Exécuter les migrations :
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
railway run python manage.py createsuperuser
```

**Option B : Via Railway Dashboard**

1. Service Django → "Deployments"
2. Cliquer sur le dernier déploiement
3. "View Logs"
4. Utiliser "Run Command" pour exécuter des commandes

**Durée** : 10 minutes

### ÉTAPE 10 : Tester l'Application

1. Railway génère automatiquement une URL : `votre-app.railway.app`
2. Visiter l'URL
3. Vérifier que l'application fonctionne
4. Tester la connexion
5. Tester les fonctionnalités

**Durée** : 5 minutes

---

## ⚙️ CONFIGURATION POUR 20+ UTILISATEURS {#configuration}

### Ressources Recommandées

#### **Application Django**

**Configuration :**
- **RAM** : 2GB
- **CPU** : 2 vCPU
- **Coût** : ~2$/mois

**Comment configurer :**
1. Service Django → "Settings"
2. "Resources"
3. Ajuster :
   - RAM : 2048 MB
   - CPU : 2 vCPU

#### **PostgreSQL**

**Configuration :**
- **RAM** : 2GB
- **Stockage** : 20GB
- **Coût** : ~4$/mois

**Comment configurer :**
1. Service PostgreSQL → "Settings"
2. "Resources"
3. Ajuster :
   - RAM : 2048 MB
   - Storage : 20GB

### Auto-Scaling

Railway scale automatiquement selon la charge, mais vous pouvez définir des limites :

1. Service → "Settings"
2. "Scaling"
3. Configurer :
   - **Min instances** : 1
   - **Max instances** : 3
   - **Target CPU** : 70%

---

## 🌐 GESTION DU DOMAINE {#domaine}

### Domaine Railway (Gratuit)

Railway fournit automatiquement :
- `votre-app.railway.app`
- SSL automatique
- Gratuit

### Domaine Personnalisé (Plan Pro requis)

#### Étape 1 : Acheter un Domaine

**Via Railway (recommandé) :**
1. Railway → "Settings" → "Domains"
2. "Add Domain"
3. Rechercher et acheter (~10-15$/an)

**Via Autre Registrar :**
- Namecheap, OVH, etc.
- Acheter le domaine (~10-15€/an)

#### Étape 2 : Configurer le Domaine dans Railway

1. Railway → Votre Service → "Settings" → "Networking"
2. "Custom Domain"
3. Ajouter votre domaine : `votre-domaine.com`
4. Railway affiche les enregistrements DNS :
   - **Type CNAME** : `www` → `votre-app.railway.app`
   - **Type A** : `@` → [IP fournie par Railway]

#### Étape 3 : Configurer DNS chez votre Registrar

**Si domaine acheté via Railway :**
- Configuration automatique

**Si domaine acheté ailleurs :**
1. Aller chez votre registrar
2. Ajouter les enregistrements DNS fournis par Railway
3. Attendre 1-2h pour propagation

#### Étape 4 : SSL Automatique

Railway génère automatiquement un certificat SSL gratuit :
- Renouvellement automatique
- Support de tous les sous-domaines
- Actif en quelques minutes

**Coût** : 0€ (GRATUIT)

---

## 🗄️ BASE DE DONNÉES POSTGRESQL {#database}

### Configuration Automatique

Railway configure automatiquement :
- Connexion sécurisée
- Variables d'environnement
- Backups automatiques

### Variables d'Environnement

Railway fournit automatiquement :
```
DATABASE_URL=postgresql://user:password@host:port/database
PGHOST=host
PGPORT=5432
PGUSER=user
PGPASSWORD=password
PGDATABASE=database
```

### Utilisation dans Django

**Avec `dj-database-url`** (recommandé) :
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}
```

### Backups

**Railway fait automatiquement :**
- Backups quotidiens
- Rétention : 7 jours (gratuit)
- Rétention : 30 jours (Plan Pro)

**Restauration :**
1. Service PostgreSQL → "Backups"
2. Sélectionner un backup
3. "Restore"

### Scaling de la Base de Données

1. Service PostgreSQL → "Settings"
2. "Resources"
3. Augmenter :
   - RAM (pour plus de performances)
   - Storage (pour plus d'espace)

---

## 📊 MONITORING ET LOGS {#monitoring}

### Logs en Temps Réel

1. Service → "Deployments"
2. Cliquer sur un déploiement
3. "View Logs"
4. Voir les logs en temps réel

### Métriques

**Plan Pro inclut :**
- CPU usage
- RAM usage
- Network traffic
- Request count
- Error rate

**Accès :**
1. Service → "Metrics"
2. Voir les graphiques en temps réel

### Alertes (Plan Pro)

1. Railway → "Settings" → "Notifications"
2. Configurer :
   - Email alerts
   - Slack notifications (optionnel)
   - Discord notifications (optionnel)

---

## 📈 SCALING ET PERFORMANCE {#scaling}

### Scaling Horizontal (Auto)

Railway scale automatiquement, mais vous pouvez configurer :

1. Service → "Settings" → "Scaling"
2. Configurer :
   - **Min instances** : 1
   - **Max instances** : 3-5
   - **Target CPU** : 70%

### Scaling Vertical (Ressources)

1. Service → "Settings" → "Resources"
2. Augmenter :
   - **RAM** : 512MB → 2GB → 4GB
   - **CPU** : 0.5 → 1 → 2 → 4 vCPU

### Optimisations Performance

1. **Caching** : Utiliser Redis (disponible sur Railway)
2. **CDN** : Railway utilise Cloudflare (automatique)
3. **Database Indexing** : Optimiser les requêtes
4. **Static Files** : Utiliser WhiteNoise (déjà configuré)

---

## 🔧 MAINTENANCE {#maintenance}

### Mises à Jour

**Automatique :**
- Railway déploie automatiquement à chaque push Git
- Pas d'interruption de service

**Manuel :**
1. Faire les modifications dans votre code
2. Push sur GitHub
3. Railway déploie automatiquement

### Backups

**Application :**
- Code : Sur GitHub (votre responsabilité)
- Base de données : Automatique (Railway)

**Base de données :**
- Backups quotidiens automatiques
- Rétention : 7 jours (gratuit) ou 30 jours (Pro)
- Restauration : Via dashboard Railway

### Monitoring Quotidien

1. Vérifier les logs : Service → "Deployments" → "View Logs"
2. Vérifier les métriques : Service → "Metrics"
3. Vérifier les erreurs : Service → "Deployments" → Voir les erreurs

**Durée** : 5 minutes/jour

---

## 💡 CONSEILS ET BONNES PRATIQUES

### Pour Optimiser les Coûts

1. **Commencer avec Plan Hobby** : Gratuit pour tester
2. **Monitorer l'usage** : Railway → "Usage" pour voir la consommation
3. **Optimiser les ressources** : Ajuster RAM/CPU selon besoins réels
4. **Utiliser le caching** : Réduire les requêtes à la base de données

### Pour la Sécurité

1. **Variables d'environnement** : Ne jamais commiter les secrets
2. **HTTPS** : Toujours activé (automatique)
3. **Backups** : Vérifier régulièrement
4. **Mises à jour** : Maintenir Django et dépendances à jour

### Pour les Performances

1. **Database Indexing** : Optimiser les requêtes lentes
2. **Caching** : Utiliser Redis pour sessions et cache
3. **Static Files** : Utiliser WhiteNoise (déjà configuré)
4. **CDN** : Automatique via Cloudflare (Railway)

---

## 📊 RÉCAPITULATIF DES COÛTS

### Configuration Minimum (Test)

| Service | Coût Mensuel |
|---------|--------------|
| Application (512MB) | 0,15$ |
| PostgreSQL (512MB) | 1,00$ |
| Bandwidth (10GB) | 1,00$ |
| **TOTAL** | **2,15$ (~2€)** |
| **Avec Plan Hobby (5$ crédit)** | **0€** ✅ |

### Configuration Recommandée (20+ Utilisateurs)

| Service | Coût Mensuel |
|---------|--------------|
| Application (2GB RAM, 2 vCPU) | 2,00$ |
| PostgreSQL (2GB RAM, 20GB) | 4,00$ |
| Bandwidth (50GB) | 5,00$ |
| Plan Pro (20$ crédit inclus) | 20,00$ |
| **Crédits utilisés** | 11,00$ |
| **Crédits supplémentaires** | 0,00$ |
| **TOTAL** | **20$/mois (~18€)** |

### Configuration Performance (50+ Utilisateurs)

| Service | Coût Mensuel |
|---------|--------------|
| Application (4GB RAM, 4 vCPU) | 8,00$ |
| PostgreSQL (4GB RAM, 50GB) | 8,00$ |
| Bandwidth (100GB) | 10,00$ |
| Plan Pro (20$ crédit inclus) | 20,00$ |
| **Crédits utilisés** | 26,00$ |
| **Crédits supplémentaires** | 6,00$ |
| **TOTAL** | **26$/mois (~24€)** |

### Comparaison avec Azure

| Configuration | Railway | Azure | Économie |
|---------------|---------|-------|----------|
| Minimum | 2€ | 186€ | **184€** |
| Recommandée | 18€ | 186€ | **168€** |
| Performance | 24€ | 186€ | **162€** |

**Économie moyenne** : **~165€/mois** avec Railway ! 💰

---

## ✅ CHECKLIST DE DÉPLOIEMENT

- [ ] Compte Railway créé
- [ ] Projet créé depuis GitHub
- [ ] PostgreSQL ajouté
- [ ] Variables d'environnement configurées
- [ ] `settings_production.py` configuré
- [ ] `requirements.txt` à jour
- [ ] `Procfile` créé
- [ ] Migrations exécutées
- [ ] Superutilisateur créé
- [ ] Domaine personnalisé configuré (optionnel)
- [ ] Application testée
- [ ] Monitoring configuré

---

## 🆘 DÉPANNAGEMENT

### L'application ne démarre pas

1. Vérifier les logs : Service → "Deployments" → "View Logs"
2. Vérifier les variables d'environnement
3. Vérifier que `Procfile` est correct
4. Vérifier que `requirements.txt` contient toutes les dépendances

### Erreur de connexion à la base de données

1. Vérifier que PostgreSQL est créé
2. Vérifier les variables d'environnement `DATABASE_URL`
3. Vérifier que `dj-database-url` est installé

### Le domaine ne fonctionne pas

1. Vérifier les enregistrements DNS
2. Attendre 1-2h pour propagation
3. Vérifier avec https://www.whatsmydns.net

### Coûts trop élevés

1. Vérifier l'usage : Railway → "Usage"
2. Réduire les ressources si possible
3. Optimiser le code pour réduire la consommation

---

## 📞 SUPPORT ET RESSOURCES

- **Documentation Railway** : https://docs.railway.app
- **Support** : support@railway.app
- **Communauté** : Discord Railway
- **Status** : https://status.railway.app

---

## 🎯 CONCLUSION

Railway est une excellente alternative à Azure App Service :
- ✅ **Beaucoup moins cher** (~18€ vs 186€/mois)
- ✅ **Plus simple** à configurer
- ✅ **Interface graphique** (Windows-friendly)
- ✅ **Déploiement automatique**
- ✅ **Base de données incluse**
- ✅ **SSL gratuit**

**Parfait pour votre ERP avec 20+ utilisateurs simultanés ! 🚀**

---

**Dernière mise à jour** : Décembre 2024

