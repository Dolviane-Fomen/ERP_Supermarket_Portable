# 🚀 Guide de Déploiement - ERP Supermarket

Ce guide vous accompagne étape par étape pour mettre votre ERP en ligne.

---

## 📋 Prérequis

- Un serveur VPS (Ubuntu 22.04 recommandé)
- Un nom de domaine pointant vers votre serveur (optionnel mais recommandé)
- Accès SSH au serveur
- Connaissances de base en ligne de commande Linux

---

## 🎯 Option 1 : Déploiement sur VPS (Recommandé)

### Étape 1 : Préparation locale

1. **Générer une clé secrète Django** :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

2. **Créer le fichier `.env`** :
```bash
cp .env.example .env
# Éditez .env et remplissez toutes les valeurs
```

3. **Tester la configuration de production localement** :
```bash
python manage.py check --settings=erp_project.settings_production
python manage.py collectstatic --settings=erp_project.settings_production --noinput
```

### Étape 2 : Préparation du serveur

1. **Se connecter au serveur** :
```bash
ssh root@VOTRE_IP_SERVEUR
```

2. **Mise à jour du système** :
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Installation des dépendances** :
```bash
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx git -y
```

4. **Créer un utilisateur pour l'application** :
```bash
sudo adduser erpuser
sudo usermod -aG sudo erpuser
```

### Étape 3 : Configuration PostgreSQL

1. **Créer la base de données et l'utilisateur** :
```bash
sudo -u postgres psql
```

Dans PostgreSQL :
```sql
CREATE DATABASE erp_db;
CREATE USER erp_user WITH PASSWORD 'VOTRE_MOT_DE_PASSE_SECURISE';
ALTER ROLE erp_user SET client_encoding TO 'utf8';
ALTER ROLE erp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE erp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;
\q
```

### Étape 4 : Déploiement de l'application

1. **Se connecter en tant qu'utilisateur erpuser** :
```bash
su - erpuser
```

2. **Cloner ou transférer le projet** :
```bash
# Option A: Si vous utilisez Git
git clone VOTRE_REPO_URL erp_project
cd erp_project

# Option B: Transférer via SCP depuis votre machine locale
# scp -r /chemin/vers/projet erpuser@VOTRE_IP:/home/erpuser/erp_project
```

3. **Créer l'environnement virtuel** :
```bash
python3 -m venv venv
source venv/bin/activate
```

4. **Installer les dépendances** :
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. **Créer le fichier `.env` sur le serveur** :
```bash
nano .env
# Copiez le contenu de votre .env local et adaptez les valeurs
```

6. **Créer les dossiers nécessaires** :
```bash
mkdir -p logs staticfiles media
```

7. **Exécuter les migrations** :
```bash
python manage.py migrate --settings=erp_project.settings_production
```

8. **Collecter les fichiers statiques** :
```bash
python manage.py collectstatic --settings=erp_project.settings_production --noinput
```

9. **Créer un superutilisateur** :
```bash
python manage.py createsuperuser --settings=erp_project.settings_production
```

### Étape 5 : Configuration Gunicorn

1. **Copier le fichier de configuration** :
```bash
# Le fichier gunicorn_config.py est déjà à la racine du projet
```

2. **Créer le service systemd** :
```bash
sudo nano /etc/systemd/system/erp.service
```

Copiez le contenu de `deployment/systemd_erp.service` et adaptez les chemins si nécessaire.

3. **Activer et démarrer le service** :
```bash
sudo systemctl daemon-reload
sudo systemctl enable erp
sudo systemctl start erp
sudo systemctl status erp
```

### Étape 6 : Configuration Nginx

1. **Créer la configuration Nginx** :
```bash
sudo nano /etc/nginx/sites-available/erp
```

Copiez le contenu de `deployment/nginx_erp.conf` et adaptez :
- `votre-domaine.com` par votre domaine
- Les chemins si nécessaire

2. **Activer le site** :
```bash
sudo ln -s /etc/nginx/sites-available/erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Étape 7 : Configuration SSL (HTTPS)

1. **Installer Certbot** :
```bash
sudo apt install certbot python3-certbot-nginx -y
```

2. **Obtenir le certificat SSL** :
```bash
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

3. **Activer HTTPS dans `.env`** :
```bash
nano .env
# Changez SECURE_SSL_REDIRECT=True
```

4. **Redémarrer Gunicorn** :
```bash
sudo systemctl restart erp
```

---

## 🎯 Option 2 : Déploiement sur Railway (Plus simple)

1. **Créer un compte sur [Railway.app](https://railway.app)**

2. **Créer un nouveau projet** et connecter votre dépôt Git

3. **Ajouter PostgreSQL** :
   - Cliquez sur "New" → "Database" → "PostgreSQL"
   - Railway créera automatiquement les variables d'environnement

4. **Configurer les variables d'environnement** :
   - `DJANGO_SETTINGS_MODULE=erp_project.settings_production`
   - `SECRET_KEY` (générez-en une)
   - `ALLOWED_HOSTS` (votre domaine Railway)
   - Les variables de base de données sont automatiques

5. **Déployer** :
   - Railway détectera automatiquement Django
   - Ajoutez cette commande dans "Settings" → "Deploy" :
     ```
     gunicorn erp_project.wsgi:application
     ```

---

## 🎯 Option 3 : Déploiement sur Render

1. **Créer un compte sur [Render.com](https://render.com)**

2. **Créer un nouveau "Web Service"** :
   - Connectez votre dépôt Git
   - Build Command : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command : `gunicorn erp_project.wsgi:application`

3. **Créer une base de données PostgreSQL** :
   - "New" → "PostgreSQL"
   - Notez les informations de connexion

4. **Configurer les variables d'environnement** :
   - `DJANGO_SETTINGS_MODULE=erp_project.settings_production`
   - `SECRET_KEY`
   - `ALLOWED_HOSTS`
   - Variables de base de données PostgreSQL

---

## ✅ Vérifications post-déploiement

1. **Vérifier que le service fonctionne** :
```bash
sudo systemctl status erp
```

2. **Vérifier les logs** :
```bash
sudo journalctl -u erp -f
```

3. **Tester l'application** :
   - Visitez votre domaine dans un navigateur
   - Vérifiez que les fichiers statiques se chargent
   - Testez la connexion

4. **Sécurité** :
   - Vérifiez que `DEBUG=False` en production
   - Vérifiez que HTTPS fonctionne
   - Vérifiez que les fichiers `.env` ne sont pas accessibles publiquement

---

## 🔧 Commandes utiles

### Redémarrer l'application
```bash
sudo systemctl restart erp
```

### Voir les logs en temps réel
```bash
sudo journalctl -u erp -f
```

### Vérifier la configuration Nginx
```bash
sudo nginx -t
```

### Renouveler le certificat SSL
```bash
sudo certbot renew
```

### Mettre à jour l'application
```bash
cd /home/erpuser/erp_project
source venv/bin/activate
git pull  # Si vous utilisez Git
pip install -r requirements.txt
python manage.py migrate --settings=erp_project.settings_production
python manage.py collectstatic --settings=erp_project.settings_production --noinput
sudo systemctl restart erp
```

---

## 🆘 Dépannage

### L'application ne démarre pas
- Vérifiez les logs : `sudo journalctl -u erp -n 50`
- Vérifiez que PostgreSQL est démarré : `sudo systemctl status postgresql`
- Vérifiez les permissions des fichiers

### Les fichiers statiques ne se chargent pas
- Vérifiez que `collectstatic` a été exécuté
- Vérifiez les permissions du dossier `staticfiles`
- Vérifiez la configuration Nginx

### Erreur de connexion à la base de données
- Vérifiez que PostgreSQL est démarré
- Vérifiez les identifiants dans `.env`
- Vérifiez que l'utilisateur PostgreSQL a les bonnes permissions

---

## 📞 Support

Si vous rencontrez des problèmes, vérifiez :
1. Les logs Django : `logs/django.log`
2. Les logs Gunicorn : `logs/gunicorn_error.log`
3. Les logs Nginx : `/var/log/nginx/erp_error.log`
4. Les logs systemd : `sudo journalctl -u erp`

---

**Bon déploiement ! 🚀**

