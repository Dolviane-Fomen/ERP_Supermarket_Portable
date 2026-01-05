# 📊 Guide : Migration SQLite → PostgreSQL en Local (Avant Déploiement OVH)

## 🎯 Objectif

Migrer vos données SQLite vers PostgreSQL **sur votre PC Windows** avant le déploiement sur OVH. Cela vous permet de :
- ✅ Tester la migration en local
- ✅ Vérifier que toutes vos données sont correctement transférées
- ✅ Résoudre les problèmes avant le déploiement
- ✅ Avoir un fichier d'export prêt pour OVH

---

## 📋 Prérequis

- ✅ Windows 10/11
- ✅ Python installé
- ✅ Projet Django fonctionnel avec SQLite
- ✅ PostgreSQL installé (voir étape 1)

---

## 🔧 ÉTAPE 1 : Installer PostgreSQL sur Windows

### Option A : Installer PostgreSQL (Recommandé)

1. **Télécharger PostgreSQL** :
   - Aller sur : https://www.postgresql.org/download/windows/
   - Cliquer sur "Download the installer"
   - Télécharger la version 15 ou 16

2. **Installer PostgreSQL** :
   - Exécuter l'installateur
   - Choisir les composants :
     - ✅ PostgreSQL Server
     - ✅ pgAdmin 4 (interface graphique)
     - ✅ Command Line Tools
   - **Mot de passe pour l'utilisateur `postgres`** : Notez-le bien !
   - Port : `5432` (par défaut)
   - Locale : `French, France` ou `English, United States`

3. **Vérifier l'installation** :
   ```powershell
   # Ouvrir PowerShell
   psql --version
   ```

**Durée** : 10-15 minutes

### Option B : Utiliser Docker (Alternative)

Si vous avez Docker Desktop installé :

```powershell
docker run --name postgres-erp -e POSTGRES_PASSWORD=monmotdepasse -e POSTGRES_DB=erp_db -p 5432:5432 -d postgres:15
```

---

## 📦 ÉTAPE 2 : Installer les Dépendances Python

**Dans votre projet Django, ouvrir PowerShell :**

```powershell
# Activer l'environnement virtuel (si vous en avez un)
.\venv\Scripts\Activate.ps1

# Installer psycopg2 (driver PostgreSQL pour Python)
pip install psycopg2-binary

# Vérifier que c'est installé
pip list | findstr psycopg2
```

**Durée** : 2 minutes

---

## 🗄️ ÉTAPE 3 : Créer la Base de Données PostgreSQL

### Méthode 1 : Via pgAdmin (Interface Graphique)

1. **Ouvrir pgAdmin 4** :
   - Chercher "pgAdmin 4" dans le menu Démarrer
   - Entrer le mot de passe de `postgres` que vous avez défini

2. **Créer la base de données** :
   - Clic droit sur "Databases" → "Create" → "Database"
   - **Name** : `erp_db`
   - **Owner** : `postgres`
   - Cliquer "Save"

3. **Créer l'utilisateur** :
   - Clic droit sur "Login/Group Roles" → "Create" → "Login/Group Role"
   - **General** :
     - **Name** : `erp_user`
   - **Definition** :
     - **Password** : `VOTRE_MOT_DE_PASSE_SECURISE`
   - **Privileges** :
     - ✅ Can login? : Oui
   - Cliquer "Save"

4. **Donner les permissions** :
   - Clic droit sur `erp_db` → "Properties"
   - Onglet "Security"
   - Cliquer "Add" → Sélectionner `erp_user`
   - Cocher "ALL"
   - Cliquer "Save"

### Méthode 2 : Via Ligne de Commande (Plus Rapide)

**Ouvrir PowerShell en tant qu'Administrateur :**

```powershell
# Se connecter à PostgreSQL
psql -U postgres

# Entrer le mot de passe de postgres quand demandé
```

**Dans psql, exécuter :**

```sql
-- Créer la base de données
CREATE DATABASE erp_db;

-- Créer l'utilisateur
CREATE USER erp_user WITH PASSWORD 'VOTRE_MOT_DE_PASSE_SECURISE';

-- Donner les permissions
ALTER ROLE erp_user SET client_encoding TO 'utf8';
ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE erp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;

-- Quitter psql
\q
```

**Durée** : 5 minutes

---

## ⚙️ ÉTAPE 4 : Configurer Django pour PostgreSQL

### 4.1 Créer un Fichier de Configuration Local

**Créer `erp_project/settings_local_postgresql.py` :**

```python
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
        'PASSWORD': 'VOTRE_MOT_DE_PASSE_SECURISE',  # Remplacez par votre mot de passe
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Garder les autres paramètres de settings.py
```

**Remplacez `VOTRE_MOT_DE_PASSE_SECURISE` par le mot de passe que vous avez créé.**

### 4.2 Tester la Connexion

**Dans PowerShell, dans votre projet :**

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Tester la connexion
python manage.py check --settings=erp_project.settings_local_postgresql

# Si pas d'erreur, c'est bon !
```

**Durée** : 2 minutes

---

## 📤 ÉTAPE 5 : Exporter les Données depuis SQLite

**Dans PowerShell, dans votre projet :**

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Exporter TOUTES les données depuis SQLite
python manage.py dumpdata > export_data.json

# OU exporter uniquement votre app (plus rapide)
python manage.py dumpdata supermarket > export_data.json

# OU exclure les sessions et contenttypes (recommandé)
python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry > export_data.json
```

**Le fichier `export_data.json` sera créé dans votre dossier de projet.**

**Vérifier la taille du fichier :**

```powershell
Get-Item export_data.json | Select-Object Length
```

**Si le fichier est très gros (>100MB), voir l'option "Export par App" ci-dessous.**

**Durée** : 1-5 minutes (selon taille des données)

---

## 📥 ÉTAPE 6 : Créer les Tables dans PostgreSQL

**Dans PowerShell :**

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Créer les tables (migrations)
python manage.py migrate --settings=erp_project.settings_local_postgresql

# Vérifier que les tables sont créées
python manage.py showmigrations --settings=erp_project.settings_local_postgresql
```

**Durée** : 2-5 minutes

---

## 🔄 ÉTAPE 7 : Importer les Données dans PostgreSQL

**Dans PowerShell :**

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Importer les données
python manage.py loaddata export_data.json --settings=erp_project.settings_local_postgresql

# Si vous avez des erreurs, voir la section "Résolution des Problèmes"
```

**Durée** : 5-30 minutes (selon taille des données)

---

## ✅ ÉTAPE 8 : Vérifier la Migration

### 8.1 Vérifier via Django Shell

**Dans PowerShell :**

```powershell
python manage.py shell --settings=erp_project.settings_local_postgresql
```

**Dans le shell Django :**

```python
from supermarket.models import Agence, Compte, Client, Commande, Article

# Compter les enregistrements
print(f"Agences: {Agence.objects.count()}")
print(f"Comptes: {Compte.objects.count()}")
print(f"Clients: {Client.objects.count()}")
print(f"Commandes: {Commande.objects.count()}")
print(f"Articles: {Article.objects.count()}")

# Vérifier un compte spécifique
compte = Compte.objects.first()
if compte:
    print(f"\nPremier compte: {compte.nom_complet} ({compte.type_compte})")

# Vérifier votre nouveau compte
try:
    nouveau_compte = Compte.objects.get(email="votre-email@example.com")
    print(f"\nNouveau compte trouvé: {nouveau_compte.nom_complet}")
except Compte.DoesNotExist:
    print("\nNouveau compte non trouvé")

# Quitter
exit()
```

### 8.2 Vérifier via pgAdmin

1. Ouvrir pgAdmin 4
2. Se connecter à `erp_db`
3. Clic droit sur `erp_db` → "Query Tool"
4. Exécuter :

```sql
-- Voir toutes les tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Compter les comptes
SELECT COUNT(*) FROM supermarket_compte;

-- Voir quelques comptes
SELECT id, nom, prenom, email, type_compte 
FROM supermarket_compte 
LIMIT 10;
```

### 8.3 Tester l'Application

**Démarrer le serveur Django avec PostgreSQL :**

```powershell
python manage.py runserver --settings=erp_project.settings_local_postgresql
```

**Ouvrir votre navigateur :**
- Aller sur http://127.0.0.1:8000
- Se connecter avec un compte existant
- Vérifier que tout fonctionne

**Durée** : 10 minutes

---

## 🎯 ÉTAPE 9 : Préparer pour OVH

### 9.1 Sauvegarder le Fichier d'Export

**Le fichier `export_data.json` est maintenant prêt pour OVH !**

**Options pour le transférer :**

1. **Via GitHub** (si le fichier n'est pas trop gros <50MB) :
   - Ajouter temporairement `export_data.json` au dépôt
   - Pousser sur GitHub
   - Sur OVH : `git pull` puis importer
   - ⚠️ **Supprimer du dépôt après migration** pour sécurité

2. **Via WinSCP** (recommandé) :
   - Télécharger WinSCP : https://winscp.net
   - Se connecter au VPS OVH
   - Glisser-déposer `export_data.json`

3. **Via SCP** (ligne de commande) :
   ```powershell
   scp export_data.json erpuser@VOTRE_IP_OVH:/home/erpuser/erp_project/
   ```

### 9.2 Créer un Script de Migration pour OVH

**Créer `scripts/migrate_to_postgresql.sh` dans votre projet :**

```bash
#!/bin/bash
# Script de migration SQLite → PostgreSQL pour OVH

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

**Rendre exécutable sur OVH :**
```bash
chmod +x scripts/migrate_to_postgresql.sh
```

---

## 🔧 RÉSOLUTION DES PROBLÈMES

### Problème 1 : Erreur "psycopg2 not found"

**Solution :**
```powershell
pip install psycopg2-binary
```

### Problème 2 : Erreur de connexion à PostgreSQL

**Vérifier :**
1. PostgreSQL est démarré :
   ```powershell
   # Voir les services Windows
   Get-Service | Where-Object {$_.Name -like "*postgresql*"}
   ```
2. Le mot de passe est correct
3. Le port 5432 est libre

### Problème 3 : Erreur "IntegrityError" lors de l'import

**Solution :** Importer dans l'ordre des dépendances

```powershell
# Exporter par app
python manage.py dumpdata supermarket.Agence > agence.json
python manage.py dumpdata supermarket.Compte > compte.json
python manage.py dumpdata supermarket.Client > client.json
python manage.py dumpdata supermarket.Article > article.json
python manage.py dumpdata supermarket.Commande > commande.json

# Importer dans l'ordre
python manage.py loaddata agence.json --settings=erp_project.settings_local_postgresql
python manage.py loaddata compte.json --settings=erp_project.settings_local_postgresql
python manage.py loaddata client.json --settings=erp_project.settings_local_postgresql
python manage.py loaddata article.json --settings=erp_project.settings_local_postgresql
python manage.py loaddata commande.json --settings=erp_project.settings_local_postgresql
```

### Problème 4 : Fichier JSON trop volumineux

**Solution :** Compresser avant transfert

```powershell
# Compresser
Compress-Archive -Path export_data.json -DestinationPath export_data.zip

# Transférer le ZIP vers OVH
# Sur OVH : décompresser puis importer
```

### Problème 5 : Erreur "relation does not exist"

**Solution :** Les migrations ne sont pas appliquées

```powershell
python manage.py migrate --settings=erp_project.settings_local_postgresql
```

---

## 📝 RÉCAPITULATIF DES ÉTAPES

1. ✅ Installer PostgreSQL sur Windows
2. ✅ Installer `psycopg2-binary`
3. ✅ Créer la base de données `erp_db` et l'utilisateur `erp_user`
4. ✅ Créer `settings_local_postgresql.py`
5. ✅ Exporter les données : `python manage.py dumpdata > export_data.json`
6. ✅ Créer les tables : `python manage.py migrate --settings=...`
7. ✅ Importer les données : `python manage.py loaddata export_data.json --settings=...`
8. ✅ Vérifier que tout fonctionne
9. ✅ Préparer `export_data.json` pour OVH

**Durée totale** : 30-60 minutes

---

## ✅ CHECKLIST

- [ ] PostgreSQL installé sur Windows
- [ ] Base de données `erp_db` créée
- [ ] Utilisateur `erp_user` créé avec permissions
- [ ] `psycopg2-binary` installé
- [ ] `settings_local_postgresql.py` créé
- [ ] Données exportées depuis SQLite (`export_data.json`)
- [ ] Tables créées dans PostgreSQL (migrations)
- [ ] Données importées dans PostgreSQL
- [ ] Vérification réussie (comptes, clients, commandes présents)
- [ ] Application testée avec PostgreSQL
- [ ] Fichier `export_data.json` sauvegardé pour OVH

---

## 🚀 PROCHAINES ÉTAPES

Une fois la migration réussie en local :

1. **Sur OVH** : Suivre le guide de déploiement
2. **Sur OVH** : Créer PostgreSQL (déjà fait dans le guide OVH)
3. **Sur OVH** : Transférer `export_data.json`
4. **Sur OVH** : Exécuter `python manage.py loaddata export_data.json --settings=erp_project.settings_production`

**Votre ERP sera alors complètement migré vers PostgreSQL ! 🎉**

---

**Dernière mise à jour** : Décembre 2024






