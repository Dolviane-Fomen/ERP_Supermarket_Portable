# Configuration Base de Données Partagée - Temps Réel

## 🎯 Objectif

Configurer tous les PCs pour qu'ils utilisent la **même base de données PostgreSQL sur OVH**, afin que toutes les modifications soient visibles **en temps réel** partout.

---

## ÉTAPE 1 : Configurer PostgreSQL sur OVH pour accepter les connexions distantes

### 1.1 Se connecter au serveur OVH

```bash
ssh ubuntu@51.68.124.152
```

### 1.2 Modifier la configuration PostgreSQL

```bash
# Éditer le fichier de configuration PostgreSQL
sudo nano /etc/postgresql/*/main/postgresql.conf

# Trouver et modifier cette ligne :
# listen_addresses = 'localhost'
# Par :
listen_addresses = '*'

# Sauvegarder : Ctrl+X, Y, Enter
```

### 1.3 Autoriser les connexions depuis l'extérieur

```bash
# Éditer le fichier pg_hba.conf
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Ajouter à la fin du fichier :
host    all             all             0.0.0.0/0               md5

# Sauvegarder : Ctrl+X, Y, Enter
```

### 1.4 Redémarrer PostgreSQL

```bash
sudo systemctl restart postgresql
```

### 1.5 Ouvrir le port 5432 dans le firewall

```bash
# Si vous utilisez ufw
sudo ufw allow 5432/tcp

# Vérifier
sudo ufw status
```

---

## ÉTAPE 2 : Récupérer les informations de connexion

**Sur le serveur OVH, récupérez :**

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Dans PostgreSQL, vérifier :
\l                          # Liste des bases de données
\du                         # Liste des utilisateurs

# Noter les informations :
# - Nom de la base : erp_db
# - Utilisateur : erp_user
# - Mot de passe : (celui que vous avez créé)
```

---

## ÉTAPE 3 : Configurer chaque PC local

### 3.1 Créer/modifier le fichier .env

Sur chaque PC, dans le dossier du projet :

```bash
# Si .env n'existe pas, le créer
copy env.example.txt .env
```

**Ouvrir `.env` et ajouter :**

```env
# Base de données partagée sur OVH
SHARED_DB_NAME=erp_db
SHARED_DB_USER=erp_user
SHARED_DB_PASSWORD=VOTRE_MOT_DE_PASSE_POSTGRESQL
SHARED_DB_HOST=51.68.124.152
SHARED_DB_PORT=5432
```

### 3.2 Modifier manage.py pour utiliser la base partagée

**Option 1 : Modifier manage.py (tous les PCs)**

Ouvrir `manage.py` et changer :

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
```

Par :

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_shared_db')
```

**Option 2 : Variable d'environnement (par PC)**

Créer un fichier `runserver_shared.bat` :

```batch
@echo off
set DJANGO_SETTINGS_MODULE=erp_project.settings_shared_db
python manage.py runserver
```

### 3.3 Installer psycopg2 sur chaque PC local

```bash
pip install psycopg2-binary
```

---

## ÉTAPE 4 : Tester la connexion

**Sur un PC local :**

```bash
python manage.py migrate --settings=erp_project.settings_shared_db
python manage.py runserver --settings=erp_project.settings_shared_db
```

Si ça fonctionne, vous êtes connecté à la base partagée !

---

## ✅ Résultat

Une fois configuré :
- ✅ Modifications de stock en local → Visibles immédiatement en ligne
- ✅ Modifications en ligne → Visibles immédiatement sur tous les PCs
- ✅ Une seule base de données → Synchronisation automatique

---

## ⚠️ Important

- **Sécurité** : La base est accessible depuis Internet. Utilisez un mot de passe fort !
- **Performance** : La connexion peut être un peu plus lente (dépend de votre connexion)
- **Sauvegarde** : Faites des sauvegardes régulières de PostgreSQL sur OVH

---

## 🔧 Vérifier que ça fonctionne

1. Faites une modification de stock sur PC 1
2. Vérifiez immédiatement sur le site en ligne → Devrait apparaître
3. Vérifiez sur PC 2 → Devrait aussi apparaître

**C'est ça le temps réel !**




