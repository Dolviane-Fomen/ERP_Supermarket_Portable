# 🚀 Guide Complet : Hébergement ERP sur OVH depuis Windows avec GitHub

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Coûts détaillés](#couts)
3. [Étape 1 : Créer un compte OVH](#etape1)
4. [Étape 2 : Créer un VPS](#etape2)
5. [Étape 3 : Se connecter au VPS depuis Windows](#etape3)
6. [Étape 4 : Configuration initiale du serveur](#etape4)
7. [Étape 5 : Installer les dépendances](#etape5)
8. [Étape 6 : Configurer PostgreSQL](#etape6)
9. [Étape 7 : Cloner votre projet depuis GitHub](#etape7)
10. [Étape 8 : Configurer l'application Django](#etape8)
11. [Étape 9 : Configurer Gunicorn](#etape9)
12. [Étape 10 : Configurer Nginx](#etape10)
13. [Étape 11 : Configurer SSL/HTTPS](#etape11)
14. [Étape 12 : Configurer le déploiement automatique depuis GitHub](#etape12)
15. [Étape 13 : Migrer les données](#etape13)
16. [Maintenance et mises à jour](#maintenance)

---

## 🎯 VUE D'ENSEMBLE {#vue-densemble}

### Architecture

```
┌─────────────────────────────────────────┐
│  Votre PC Windows                       │
│  - Navigateur (OVH, GitHub)            │
│  - Windows Terminal (SSH)              │
│  - GitHub Desktop                       │
└──────────────┬──────────────────────────┘
               │ SSH / Git
               ▼
┌─────────────────────────────────────────┐
│  VPS OVH (Ubuntu 22.04)                 │
│  - Django Application                   │
│  - PostgreSQL                           │
│  - Nginx                                │
│  - Gunicorn                             │
└─────────────────────────────────────────┘
```

### Prérequis

- ✅ Compte OVH
- ✅ Compte GitHub (avec votre code)
- ✅ PC Windows avec navigateur
- ✅ Windows Terminal ou PuTTY (pour SSH)

---

## 💰 COÛTS DÉTAILLÉS {#couts}

### Configuration Recommandée (20+ Utilisateurs)

| Service | Spécifications | Coût Mensuel | Coût Annuel |
|---------|----------------|--------------|-------------|
| **VPS Value** | 4GB RAM, 2 vCPU, 80GB SSD | 5,00€ | 60,00€ |
| **PostgreSQL** | Inclus (installé sur VPS) | 0,00€ | 0,00€ |
| **Nom de domaine (.com)** | Via OVH | 1,00€ | 12,00€ |
| **SSL/HTTPS** | Let's Encrypt (gratuit) | 0,00€ | 0,00€ |
| **Backups** | Snapshots OVH (optionnel) | 0,50€ | 6,00€ |
| **TOTAL** | - | **6,00€** | **72,00€** |

### Configuration Minimum (Test/Développement)

| Service | Spécifications | Coût Mensuel |
|---------|----------------|--------------|
| **VPS Starter** | 2GB RAM, 1 vCPU, 20GB SSD | 3,50€ |
| **PostgreSQL** | Inclus | 0,00€ |
| **Nom de domaine** | Optionnel | 1,00€ |
| **TOTAL** | - | **4,50€** |

### Configuration Performance (50+ Utilisateurs)

| Service | Spécifications | Coût Mensuel |
|---------|----------------|--------------|
| **VPS Elite** | 8GB RAM, 4 vCPU, 160GB SSD | 10,00€ |
| **PostgreSQL** | Inclus | 0,00€ |
| **Nom de domaine** | Via OVH | 1,00€ |
| **TOTAL** | - | **11,00€** |

### Comparaison avec Railway

| Hébergeur | Coût Mensuel | Configuration |
|-----------|--------------|---------------|
| **OVH VPS Value** | 6€ | 4GB RAM, 2 vCPU, 80GB |
| **Railway** | 18-25€ | 2GB RAM, 2 vCPU |
| **Économie OVH** | **12-19€/mois** | - |

---

## 📝 ÉTAPE 1 : Créer un Compte OVH {#etape1}

### 1.1 Aller sur OVH

1. Ouvrir votre navigateur (Chrome, Edge, Firefox)
2. Aller sur https://www.ovh.com
3. Cliquer sur "Mon compte" → "Créer un compte"

### 1.2 Créer le Compte

1. Remplir le formulaire :
   - Email
   - Mot de passe
   - Nom, Prénom
   - Téléphone
2. Vérifier votre email
3. Ajouter une méthode de paiement

**Durée** : 5 minutes

✅ **Votre compte OVH est créé !**

---

## 🖥️ ÉTAPE 2 : Créer un VPS {#etape2}

### 2.1 Accéder aux VPS

1. Se connecter à https://www.ovh.com
2. Aller dans "Bare Metal Cloud" → "VPS"
3. Cliquer sur "Commander un VPS"

### 2.2 Choisir le VPS

**Configuration Recommandée :**

1. **Gamme** : VPS Value
2. **Localisation** : Europe (France ou Allemagne)
3. **OS** : Ubuntu 22.04
4. **Durée** : Mensuel (ou annuel pour économie)
5. Cliquer sur "Commander"

### 2.3 Finaliser la Commande

1. Vérifier la configuration
2. Ajouter un nom pour le VPS (ex: "erp-production")
3. Valider la commande
4. Payer

**Durée** : 5 minutes

### 2.4 Noter les Informations

OVH vous enverra par email :
- **IP du serveur** : `xxx.xxx.xxx.xxx`
- **Nom d'utilisateur** : `root` (par défaut)
- **Mot de passe** : Celui que vous avez défini

**IMPORTANT** : Notez ces informations !

✅ **Votre VPS est créé !**

---

## 🔌 ÉTAPE 3 : Se Connecter au VPS depuis Windows {#etape3}

### 3.1 Méthode 1 : Windows Terminal (Recommandé)

**Windows 10/11 inclut Windows Terminal :**

1. Appuyer sur `Windows + X`
2. Sélectionner "Windows Terminal" ou "Terminal"
3. Ou chercher "Terminal" dans le menu Démarrer

**Dans Windows Terminal, taper :**
```powershell
ssh root@VOTRE_IP_OVH
```

**Exemple :**
```powershell
ssh root@51.38.123.45
```

4. Entrer "yes" pour accepter la clé
5. Entrer le mot de passe (celui fourni par OVH)

### 3.2 Méthode 2 : PuTTY (Alternative)

**Si Windows Terminal ne fonctionne pas :**

1. Télécharger PuTTY : https://www.putty.org
2. Installer PuTTY
3. Ouvrir PuTTY
4. Configuration :
   - **Host Name** : `VOTRE_IP_OVH`
   - **Port** : `22`
   - **Connection type** : SSH
5. Cliquer "Open"
6. Entrer le nom d'utilisateur : `root`
7. Entrer le mot de passe

**Durée** : 2 minutes

✅ **Vous êtes connecté au VPS !**

---

## ⚙️ ÉTAPE 4 : Configuration Initiale du Serveur {#etape4}

### 4.1 Mise à Jour du Système

**Dans votre session SSH, exécutez :**

```bash
apt update && apt upgrade -y
```

**Durée** : 5-10 minutes

### 4.2 Créer un Utilisateur pour l'Application

```bash
# Créer un utilisateur
adduser erpuser

# Ajouter aux sudoers
usermod -aG sudo erpuser

# Se connecter en tant qu'utilisateur
su - erpuser
```

**Durée** : 2 minutes

✅ **Le serveur est prêt !**

---

## 📦 ÉTAPE 5 : Installer les Dépendances {#etape5}

### 5.1 Installer Python et Outils

```bash
# Installer Python et pip
sudo apt install python3 python3-pip python3-venv git curl -y

# Installer PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Installer Nginx
sudo apt install nginx -y

# Installer autres outils
sudo apt install build-essential libpq-dev -y
```

**Durée** : 5-10 minutes

### 5.2 Vérifier les Installations

```bash
python3 --version
pip3 --version
git --version
postgresql --version
nginx -v
```

✅ **Toutes les dépendances sont installées !**

---

## 🗄️ ÉTAPE 6 : Configurer PostgreSQL {#etape6}

### 6.1 Créer la Base de Données

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Dans PostgreSQL, exécuter :
CREATE DATABASE erp_db;
CREATE USER erp_user WITH PASSWORD 'VOTRE_MOT_DE_PASSE_SECURISE';
ALTER ROLE erp_user SET client_encoding TO 'utf8';
ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE erp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;
\q
```

**Remplacez `VOTRE_MOT_DE_PASSE_SECURISE` par un mot de passe fort.**

### 6.2 Noter les Informations

- **Database** : `erp_db`
- **User** : `erp_user`
- **Password** : Celui que vous avez créé
- **Host** : `localhost`
- **Port** : `5432`

**Durée** : 5 minutes

✅ **PostgreSQL est configuré !**

---

## 📥 ÉTAPE 7 : Cloner votre Projet depuis GitHub {#etape7}

### 7.1 Créer le Dossier du Projet

```bash
# Retourner dans le dossier home
cd ~

# Créer le dossier du projet
mkdir -p erp_project
cd erp_project
```

### 7.2 Cloner depuis GitHub

**Option A : HTTPS (Simple)**

```bash
git clone https://github.com/VOTRE_USERNAME/ERP_Supermarket_Portable.git .
```

**Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub.**

**Option B : SSH (Plus sécurisé)**

1. Générer une clé SSH sur le serveur :
```bash
ssh-keygen -t ed25519 -C "votre-email@example.com"
cat ~/.ssh/id_ed25519.pub
```

2. Copier la clé affichée
3. Sur GitHub → Settings → SSH Keys → Add SSH Key
4. Coller la clé
5. Cloner :
```bash
git clone git@github.com:VOTRE_USERNAME/ERP_Supermarket_Portable.git .
```

**Durée** : 5 minutes

✅ **Votre code est sur le serveur !**

---

## ⚙️ ÉTAPE 8 : Configurer l'Application Django {#etape8}

### 8.1 Créer l'Environnement Virtuel

```bash
# Dans le dossier du projet
python3 -m venv venv
source venv/bin/activate
```

### 8.2 Installer les Dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Durée** : 5-10 minutes

### 8.3 Créer le Fichier .env

```bash
nano .env
```

**Contenu du fichier .env :**

```bash
# Sécurité
SECRET_KEY=votre-cle-secrete-generee
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com,VOTRE_IP_OVH
DEBUG=False

# Base de données PostgreSQL
DB_NAME=erp_db
DB_USER=erp_user
DB_PASSWORD=VOTRE_MOT_DE_PASSE_POSTGRESQL
DB_HOST=localhost
DB_PORT=5432

# HTTPS
SECURE_SSL_REDIRECT=True

# Timezone
TIME_ZONE=UTC
```

**Générer SECRET_KEY :**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Sauvegarder** : `Ctrl+X`, puis `Y`, puis `Enter`

### 8.4 Exécuter les Migrations

```bash
python manage.py migrate --settings=erp_project.settings_production
python manage.py collectstatic --settings=erp_project.settings_production --noinput
python manage.py createsuperuser --settings=erp_project.settings_production
```

**Durée** : 5 minutes

✅ **Django est configuré !**

---

## 🔧 ÉTAPE 9 : Configurer Gunicorn {#etape9}

### 9.1 Créer le Fichier de Configuration Gunicorn

```bash
nano gunicorn_config.py
```

**Contenu :**

```python
bind = "127.0.0.1:8000"
workers = 4
timeout = 120
worker_class = "sync"
max_requests = 1000
max_requests_jitter = 50
```

**Sauvegarder** : `Ctrl+X`, `Y`, `Enter`

### 9.2 Créer le Service Systemd

```bash
sudo nano /etc/systemd/system/erp.service
```

**Contenu :**

```ini
[Unit]
Description=ERP Supermarket Gunicorn daemon
After=network.target postgresql.service

[Service]
User=erpuser
Group=www-data
WorkingDirectory=/home/erpuser/erp_project
Environment="PATH=/home/erpuser/erp_project/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=erp_project.settings_production"
ExecStart=/home/erpuser/erp_project/venv/bin/gunicorn \
    --config /home/erpuser/erp_project/gunicorn_config.py \
    erp_project.wsgi:application

Restart=always
RestartSec=3
LimitNOFILE=65535

StandardOutput=journal
StandardError=journal
SyslogIdentifier=erp

[Install]
WantedBy=multi-user.target
```

**Sauvegarder** : `Ctrl+X`, `Y`, `Enter`

### 9.3 Activer et Démarrer le Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable erp
sudo systemctl start erp
sudo systemctl status erp
```

**Vérifier que le service fonctionne :**
- Vous devriez voir "active (running)" en vert

**Durée** : 5 minutes

✅ **Gunicorn est configuré et démarré !**

---

## 🌐 ÉTAPE 10 : Configurer Nginx {#etape10}

### 10.1 Créer la Configuration Nginx

```bash
sudo nano /etc/nginx/sites-available/erp
```

**Contenu (remplacer `votre-domaine.com` par votre domaine) :**

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com VOTRE_IP_OVH;

    client_max_body_size 10M;

    # Fichiers statiques
    location /static/ {
        alias /home/erpuser/erp_project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Fichiers médias
    location /media/ {
        alias /home/erpuser/erp_project/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Proxy vers Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    server_tokens off;
    access_log /var/log/nginx/erp_access.log;
    error_log /var/log/nginx/erp_error.log;
}
```

**Sauvegarder** : `Ctrl+X`, `Y`, `Enter`

### 10.2 Activer le Site

```bash
sudo ln -s /etc/nginx/sites-available/erp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

**Vérifier que Nginx fonctionne :**
```bash
sudo systemctl status nginx
```

**Durée** : 5 minutes

✅ **Nginx est configuré !**

---

## 🔒 ÉTAPE 11 : Configurer SSL/HTTPS {#etape11}

### 11.1 Installer Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 11.2 Obtenir le Certificat SSL

**Si vous avez un domaine :**

```bash
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

**Réponses aux questions :**
- Email : Votre email
- Terms : Accepter (A)
- Share email : Votre choix (Y ou N)
- Redirect HTTP to HTTPS : **Oui (2)**

**Si vous n'avez pas de domaine :**

Vous pouvez tester avec l'IP pour l'instant, mais SSL nécessite un domaine.

**Durée** : 5 minutes

### 11.3 Vérifier le Renouvellement Automatique

```bash
sudo certbot renew --dry-run
```

✅ **HTTPS est configuré !**

---

## 🔄 ÉTAPE 12 : Configurer le Déploiement Automatique depuis GitHub {#etape12}

### 12.1 Méthode 1 : Script de Déploiement Simple

**Créer un script de déploiement :**

```bash
nano ~/deploy.sh
```

**Contenu :**

```bash
#!/bin/bash
cd /home/erpuser/erp_project
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
python manage.py migrate --settings=erp_project.settings_production --noinput
python manage.py collectstatic --settings=erp_project.settings_production --noinput
sudo systemctl restart erp
echo "Déploiement terminé !"
```

**Rendre exécutable :**

```bash
chmod +x ~/deploy.sh
```

**Pour déployer manuellement :**
```bash
~/deploy.sh
```

### 12.2 Méthode 2 : GitHub Actions (Automatique)

**Créer le fichier `.github/workflows/deploy.yml` dans votre projet :**

```yaml
name: Deploy to OVH

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.OVH_HOST }}
        username: ${{ secrets.OVH_USERNAME }}
        key: ${{ secrets.OVH_SSH_KEY }}
        script: |
          cd /home/erpuser/erp_project
          source venv/bin/activate
          git pull origin main
          pip install -r requirements.txt
          python manage.py migrate --settings=erp_project.settings_production --noinput
          python manage.py collectstatic --settings=erp_project.settings_production --noinput
          sudo systemctl restart erp
```

**Configurer les Secrets GitHub :**

1. GitHub → Votre dépôt → "Settings" → "Secrets" → "Actions"
2. Ajouter :
   - `OVH_HOST` : IP de votre VPS
   - `OVH_USERNAME` : `erpuser`
   - `OVH_SSH_KEY` : Clé SSH privée du serveur

**Générer la clé SSH sur le serveur :**

```bash
ssh-keygen -t ed25519 -C "deploy@ovh"
cat ~/.ssh/id_ed25519
```

Copier la clé privée et l'ajouter dans GitHub Secrets.

**Durée** : 15 minutes

✅ **Déploiement automatique configuré !**

---

## 📊 ÉTAPE 13 : Migrer les Données depuis SQLite vers PostgreSQL {#etape13}

**OUI, c'est tout à fait possible !** Voici plusieurs méthodes pour migrer vos données SQLite vers PostgreSQL sur OVH.

### 13.1 Méthode 1 : Django dumpdata/loaddata (Recommandée)

**Cette méthode est la plus simple et la plus sûre pour Django.**

#### Étape 1 : Exporter depuis SQLite (Sur votre PC Windows)

**Sur votre PC Windows :**

1. Ouvrir PowerShell dans le dossier de votre projet local
2. Activer l'environnement virtuel (si vous en avez un)
3. Exécuter :

```powershell
# Exporter toutes les données
python manage.py dumpdata > export_data.json

# OU exporter uniquement certaines apps (plus rapide)
python manage.py dumpdata supermarket > export_data.json

# OU exclure certaines données (comme les sessions)
python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry > export_data.json
```

**Le fichier `export_data.json` sera créé dans votre dossier de projet.**

#### Étape 2 : Transférer le Fichier vers le Serveur OVH

**Option A : Via SCP (depuis Windows PowerShell)**

```powershell
scp export_data.json erpuser@VOTRE_IP_OVH:/home/erpuser/erp_project/
```

**Remplacez `VOTRE_IP_OVH` par l'IP de votre VPS OVH.**

**Option B : Via WinSCP (Interface graphique - Plus facile)**

1. Télécharger WinSCP : https://winscp.net
2. Installer WinSCP
3. Ouvrir WinSCP
4. Se connecter :
   - **Host name** : `VOTRE_IP_OVH`
   - **User name** : `erpuser`
   - **Password** : Votre mot de passe SSH
   - **Protocol** : SFTP
5. Glisser-déposer `export_data.json` vers `/home/erpuser/erp_project/`

**Option C : Via GitHub (Si le fichier n'est pas trop gros)**

1. Ajouter `export_data.json` temporairement au dépôt
2. Pousser sur GitHub
3. Sur le serveur : `git pull`

⚠️ **Attention** : N'oubliez pas de supprimer le fichier du dépôt après migration pour des raisons de sécurité.

#### Étape 3 : Importer dans PostgreSQL (Sur le serveur OVH)

**Se connecter au serveur via SSH :**

```bash
ssh erpuser@VOTRE_IP_OVH
```

**Sur le serveur, exécuter :**

```bash
cd /home/erpuser/erp_project
source venv/bin/activate

# Vérifier que le fichier est présent
ls -lh export_data.json

# Importer les données
python manage.py loaddata export_data.json --settings=erp_project.settings_production
```

**Si vous avez des erreurs de clés étrangères, utilisez :**

```bash
python manage.py loaddata export_data.json --settings=erp_project.settings_production --verbosity=2
```

**Durée** : 10-30 minutes (selon taille des données)

✅ **Les données sont migrées !**

---

### 13.2 Méthode 2 : Migration Table par Table (Pour grandes bases)

**Si vous avez beaucoup de données, migrez table par table :**

#### Sur votre PC Windows :

```powershell
# Exporter chaque app séparément
python manage.py dumpdata supermarket.Agence > agence.json
python manage.py dumpdata supermarket.Compte > compte.json
python manage.py dumpdata supermarket.Client > client.json
python manage.py dumpdata supermarket.Article > article.json
python manage.py dumpdata supermarket.Commande > commande.json
python manage.py dumpdata supermarket.FactureCommande > facture.json
# ... etc pour chaque modèle
```

#### Transférer tous les fichiers vers le serveur

**Via WinSCP, glisser-déposer tous les fichiers JSON.**

#### Importer sur le serveur

```bash
cd /home/erpuser/erp_project
source venv/bin/activate

# Importer dans l'ordre des dépendances
python manage.py loaddata agence.json --settings=erp_project.settings_production
python manage.py loaddata compte.json --settings=erp_project.settings_production
python manage.py loaddata client.json --settings=erp_project.settings_production
python manage.py loaddata article.json --settings=erp_project.settings_production
python manage.py loaddata commande.json --settings=erp_project.settings_production
python manage.py loaddata facture.json --settings=erp_project.settings_production
# ... etc
```

---

### 13.3 Méthode 3 : Script de Migration Automatique

**Créer un script pour automatiser la migration :**

#### Sur le serveur OVH :

```bash
nano ~/migrate_data.sh
```

**Contenu du script :**

```bash
#!/bin/bash

echo "=== Migration des données SQLite vers PostgreSQL ==="

cd /home/erpuser/erp_project
source venv/bin/activate

# Vérifier que le fichier existe
if [ ! -f "export_data.json" ]; then
    echo "ERREUR: export_data.json introuvable!"
    exit 1
fi

# Sauvegarder la base actuelle (au cas où)
echo "Sauvegarde de la base PostgreSQL actuelle..."
pg_dump -U erp_user -d erp_db > backup_before_migration_$(date +%Y%m%d_%H%M%S).sql

# Importer les données
echo "Importation des données..."
python manage.py loaddata export_data.json --settings=erp_project.settings_production

if [ $? -eq 0 ]; then
    echo "✅ Migration réussie!"
    echo "Nettoyage du fichier d'export..."
    rm export_data.json
else
    echo "❌ Erreur lors de la migration!"
    exit 1
fi
```

**Rendre exécutable :**

```bash
chmod +x ~/migrate_data.sh
```

**Exécuter :**

```bash
~/migrate_data.sh
```

---

### 13.4 Vérification après Migration

**Vérifier que les données sont bien importées :**

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql -d erp_db

# Dans PostgreSQL, vérifier les tables
\dt

# Compter les enregistrements
SELECT COUNT(*) FROM supermarket_agence;
SELECT COUNT(*) FROM supermarket_compte;
SELECT COUNT(*) FROM supermarket_client;
SELECT COUNT(*) FROM supermarket_commande;
# ... etc

# Quitter PostgreSQL
\q
```

**Vérifier via Django :**

```bash
cd /home/erpuser/erp_project
source venv/bin/activate
python manage.py shell --settings=erp_project.settings_production
```

**Dans le shell Django :**

```python
from supermarket.models import Agence, Compte, Client, Commande

# Vérifier les comptes
print(f"Nombre de comptes: {Compte.objects.count()}")
print(f"Nombre de clients: {Client.objects.count()}")
print(f"Nombre de commandes: {Commande.objects.count()}")

# Vérifier un compte spécifique
compte = Compte.objects.first()
print(f"Premier compte: {compte.nom_complet}")
```

---

### 13.5 Résolution des Problèmes Courants

#### Problème 1 : Erreur de clés étrangères

**Solution :** Importer dans l'ordre des dépendances

```bash
# D'abord les tables sans dépendances
python manage.py loaddata agence.json --settings=erp_project.settings_production
python manage.py loaddata compte.json --settings=erp_project.settings_production
# Ensuite les tables qui dépendent
python manage.py loaddata client.json --settings=erp_project.settings_production
python manage.py loaddata commande.json --settings=erp_project.settings_production
```

#### Problème 2 : Erreur "IntegrityError"

**Solution :** Utiliser `--verbosity=2` pour voir les détails

```bash
python manage.py loaddata export_data.json --settings=erp_project.settings_production --verbosity=2
```

#### Problème 3 : Fichier trop volumineux

**Solution :** Compresser avant transfert

**Sur Windows :**
```powershell
Compress-Archive -Path export_data.json -DestinationPath export_data.zip
```

**Transférer le ZIP, puis sur le serveur :**
```bash
unzip export_data.zip
python manage.py loaddata export_data.json --settings=erp_project.settings_production
```

#### Problème 4 : Données corrompues

**Solution :** Vérifier le format JSON

```bash
# Vérifier que le JSON est valide
python -m json.tool export_data.json > /dev/null
```

---

### 13.6 Sauvegarde Avant Migration

**IMPORTANT : Toujours faire une sauvegarde avant migration !**

```bash
# Sur le serveur OVH, sauvegarder PostgreSQL
pg_dump -U erp_user -d erp_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Stocker la sauvegarde dans un endroit sûr
mkdir -p ~/backups
mv backup_*.sql ~/backups/
```

---

### 13.7 Récapitulatif des Étapes

1. ✅ Exporter depuis SQLite local : `python manage.py dumpdata > export_data.json`
2. ✅ Transférer vers OVH : Via SCP ou WinSCP
3. ✅ Sauvegarder PostgreSQL actuel : `pg_dump`
4. ✅ Importer dans PostgreSQL : `python manage.py loaddata`
5. ✅ Vérifier les données : Via shell Django ou PostgreSQL
6. ✅ Nettoyer : Supprimer `export_data.json`

**Durée totale** : 15-30 minutes (selon taille des données)

✅ **Migration SQLite → PostgreSQL terminée sur OVH !**

---

## 🔧 MAINTENANCE ET MISES À JOUR {#maintenance}

### Mises à Jour via GitHub

**Méthode Simple (Manuelle) :**

1. Faire vos modifications localement
2. Tester
3. Pousser sur GitHub :
   ```powershell
   git add .
   git commit -m "Description des modifications"
   git push
   ```
4. Se connecter au serveur :
   ```bash
   ssh erpuser@VOTRE_IP_OVH
   ```
5. Exécuter le script de déploiement :
   ```bash
   ~/deploy.sh
   ```

**Méthode Automatique (GitHub Actions) :**

- Les mises à jour se déploient automatiquement à chaque push sur GitHub

### Commandes Utiles

**Vérifier le statut du service :**
```bash
sudo systemctl status erp
```

**Voir les logs :**
```bash
sudo journalctl -u erp -f
```

**Redémarrer l'application :**
```bash
sudo systemctl restart erp
```

**Vérifier Nginx :**
```bash
sudo nginx -t
sudo systemctl status nginx
```

**Voir les logs Nginx :**
```bash
sudo tail -f /var/log/nginx/erp_error.log
```

---

## 💰 RÉCAPITULATIF DES COÛTS

### Configuration Recommandée

| Service | Coût Mensuel | Coût Annuel |
|---------|--------------|-------------|
| **VPS Value** | 5,00€ | 60,00€ |
| **Nom de domaine** | 1,00€ | 12,00€ |
| **Backups (optionnel)** | 0,50€ | 6,00€ |
| **TOTAL** | **6,50€** | **78,00€** |

### Économies vs Railway

- **OVH** : 6,50€/mois
- **Railway** : 18-25€/mois
- **Économie** : **11,50-18,50€/mois** = **138-222€/an**

---

## ✅ CHECKLIST DE DÉPLOIEMENT

- [ ] Compte OVH créé
- [ ] VPS créé (VPS Value recommandé)
- [ ] Connexion SSH depuis Windows réussie
- [ ] Dépendances installées (Python, PostgreSQL, Nginx)
- [ ] PostgreSQL configuré
- [ ] Projet cloné depuis GitHub
- [ ] Environnement virtuel créé
- [ ] Dépendances Python installées
- [ ] Fichier .env configuré
- [ ] Migrations exécutées
- [ ] Gunicorn configuré et démarré
- [ ] Nginx configuré
- [ ] SSL/HTTPS configuré
- [ ] Déploiement automatique configuré (optionnel)
- [ ] Données migrées (si nécessaire)
- [ ] Application testée et fonctionnelle

---

## 🆘 DÉPANNAGEMENT

### L'application ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u erp -n 50

# Vérifier que Gunicorn écoute
sudo netstat -tlnp | grep 8000

# Vérifier les permissions
sudo chown -R erpuser:www-data /home/erpuser/erp_project
```

### Erreur de connexion à la base de données

```bash
# Vérifier que PostgreSQL est démarré
sudo systemctl status postgresql

# Vérifier la connexion
sudo -u postgres psql -c "\l"
```

### Les fichiers statiques ne se chargent pas

```bash
# Re-collecter les fichiers statiques
cd /home/erpuser/erp_project
source venv/bin/activate
python manage.py collectstatic --settings=erp_project.settings_production --noinput

# Vérifier les permissions
sudo chown -R erpuser:www-data /home/erpuser/erp_project/staticfiles
sudo chmod -R 755 /home/erpuser/erp_project/staticfiles
```

### Le domaine ne fonctionne pas

1. Vérifier les enregistrements DNS chez votre registrar
2. Attendre 1-2h pour propagation
3. Vérifier avec `ping votre-domaine.com`

---

## 📞 SUPPORT

- **Documentation OVH** : https://docs.ovh.com
- **Support OVH** : Disponible dans l'interface
- **Communauté** : Forum OVH

---

## 🎯 CONCLUSION

Vous avez maintenant :
- ✅ Un VPS OVH configuré (~6€/mois)
- ✅ Votre ERP Django déployé
- ✅ PostgreSQL configuré
- ✅ HTTPS activé
- ✅ Déploiement depuis GitHub
- ✅ Économie de ~12-19€/mois vs Railway

**Votre ERP est maintenant en ligne sur OVH ! 🚀**

---

**Dernière mise à jour** : Décembre 2024

