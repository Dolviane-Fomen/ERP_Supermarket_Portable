# 🚀 Guide de Déploiement Production - DigitalOcean

## 🎯 Configuration Recommandée pour Production

### 📦 Package Complet
- **Droplet** : 2GB RAM, 1 vCPU, 50GB SSD → **12€/mois**
- **Managed PostgreSQL** : 1GB RAM → **15€/mois**
- **Backups automatiques** : +2,40€/mois (optionnel mais recommandé)
- **Total : ~27-30€/mois** pour une solution professionnelle et stable

### ✅ Pourquoi DigitalOcean pour la Production ?

1. **Stabilité** : Uptime garanti 99,99%
2. **Performances** : 2GB RAM vs 512MB sur Heroku (4x plus)
3. **Prix compétitif** : 27€/mois vs 30€/mois Heroku (même prix, 4x plus de ressources)
4. **Base de données managée** : Backups automatiques, haute disponibilité
5. **Scaling facile** : Upgrade en quelques clics si besoin
6. **Support excellent** : Documentation complète, communauté active
7. **Monitoring intégré** : Métriques en temps réel

---

## 📋 ÉTAPES DE DÉPLOIEMENT

### Étape 1 : Créer le compte DigitalOcean

1. Aller sur https://www.digitalocean.com
2. Créer un compte (vous recevrez 200$ de crédit pour 60 jours)
3. Ajouter une méthode de paiement

### Étape 2 : Créer le Droplet (Serveur)

1. Dans le dashboard, cliquer sur **"Create"** → **"Droplets"**
2. Configuration recommandée :
   - **Image** : Ubuntu 22.04 (LTS)
   - **Plan** : Basic → **Regular with SSD** → **2GB RAM / 1 vCPU** (12€/mois)
   - **Datacenter region** : Choisir le plus proche de vos utilisateurs (ex: Frankfurt pour Europe)
   - **Authentication** : SSH keys (recommandé) ou Password
   - **Hostname** : `erp-production`
3. Cliquer sur **"Create Droplet"**
4. **Noter l'IP du serveur** qui s'affiche

### Étape 3 : Créer la Base de Données PostgreSQL

1. Dans le dashboard, cliquer sur **"Create"** → **"Databases"**
2. Configuration :
   - **Database Engine** : PostgreSQL
   - **Version** : Latest (15 ou 16)
   - **Plan** : Basic → **1GB RAM / 1 vCPU** (15€/mois)
   - **Datacenter region** : Même région que le Droplet
   - **Database name** : `erp_db` (ou laisser par défaut)
3. Cliquer sur **"Create a Database Cluster"**
4. **IMPORTANT** : Noter les informations de connexion :
   - Host
   - Port
   - Database
   - User
   - Password (cliquer sur "Show" pour voir)

### Étape 4 : Configurer le Firewall

1. Dans le dashboard, aller dans **"Networking"** → **"Firewalls"**
2. Cliquer sur **"Create Firewall"**
3. Configuration :
   - **Name** : `erp-firewall`
   - **Inbound Rules** :
     - SSH (22) - Source: Your IP (pour sécurité)
     - HTTP (80) - Source: All IPv4, All IPv6
     - HTTPS (443) - Source: All IPv4, All IPv6
   - **Outbound Rules** : Laisser par défaut (Allow all)
4. Cliquer sur **"Create Firewall"**
5. Attacher le firewall au Droplet créé

### Étape 5 : Se connecter au serveur

```bash
# Depuis votre machine locale
ssh root@VOTRE_IP_SERVEUR

# Ou si vous avez configuré un utilisateur
ssh erpuser@VOTRE_IP_SERVEUR
```

### Étape 6 : Configuration initiale du serveur

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
sudo apt install python3-pip python3-venv postgresql-client nginx git -y

# Créer un utilisateur pour l'application (si pas déjà fait)
sudo adduser erpuser
sudo usermod -aG sudo erpuser

# Se connecter en tant qu'utilisateur erpuser
su - erpuser
```

### Étape 7 : Déployer l'application

```bash
# Créer le dossier du projet
mkdir -p ~/erp_project
cd ~/erp_project

# Option A : Si vous utilisez Git
git clone VOTRE_REPO_URL .

# Option B : Transférer les fichiers via SCP depuis votre machine locale
# Depuis votre machine locale :
# scp -r /chemin/vers/votre/projet/* erpuser@VOTRE_IP_SERVEUR:~/erp_project/

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

### Étape 8 : Configurer les variables d'environnement

```bash
# Créer le fichier .env
nano .env
```

Copier le contenu suivant et adapter les valeurs :

```bash
# Sécurité
SECRET_KEY=votre-cle-secrete-generee-avec-python
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com,VOTRE_IP_SERVEUR

# Base de données (utiliser les infos de DigitalOcean)
DB_NAME=defaultdb
DB_USER=doadmin
DB_PASSWORD=LE_MOT_DE_PASSE_FOURNI_PAR_DIGITALOCEAN
DB_HOST=LE_HOST_FOURNI_PAR_DIGITALOCEAN
DB_PORT=25060

# HTTPS (activer après configuration SSL)
SECURE_SSL_REDIRECT=False

# Timezone
TIME_ZONE=UTC
```

**Générer SECRET_KEY** :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Sauvegarder avec `Ctrl+X`, puis `Y`, puis `Enter`

### Étape 9 : Créer les dossiers nécessaires

```bash
mkdir -p logs staticfiles media
```

### Étape 10 : Exécuter les migrations

```bash
# Toujours dans l'environnement virtuel
python manage.py migrate --settings=erp_project.settings_production

# Créer un superutilisateur
python manage.py createsuperuser --settings=erp_project.settings_production

# Collecter les fichiers statiques
python manage.py collectstatic --settings=erp_project.settings_production --noinput
```

### Étape 11 : Configurer Gunicorn

Le fichier `gunicorn_config.py` est déjà dans votre projet. Vérifiez qu'il est bien présent :

```bash
ls -la gunicorn_config.py
```

Si nécessaire, créez-le avec le contenu du fichier fourni dans le projet.

### Étape 12 : Créer le service systemd

```bash
# Revenir en root
exit

# Créer le fichier de service
sudo nano /etc/systemd/system/erp.service
```

Copier le contenu suivant (adapter les chemins si nécessaire) :

```ini
[Unit]
Description=ERP Supermarket Gunicorn daemon
After=network.target

[Service]
User=erpuser
Group=www-data
WorkingDirectory=/home/erpuser/erp_project
Environment="PATH=/home/erpuser/erp_project/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=erp_project.settings_production
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

Activer et démarrer le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable erp
sudo systemctl start erp
sudo systemctl status erp
```

### Étape 13 : Configurer Nginx

```bash
# Créer la configuration Nginx
sudo nano /etc/nginx/sites-available/erp
```

Copier le contenu suivant (adapter le domaine) :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com VOTRE_IP_SERVEUR;

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

Activer le site :

```bash
sudo ln -s /etc/nginx/sites-available/erp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Supprimer la config par défaut
sudo nginx -t  # Tester la configuration
sudo systemctl reload nginx
```

### Étape 14 : Configurer SSL (HTTPS)

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtenir le certificat SSL (remplacer par votre domaine)
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Suivre les instructions (choisir "Redirect HTTP to HTTPS")
```

Après configuration SSL, activer HTTPS dans `.env` :

```bash
su - erpuser
nano .env
# Changer SECURE_SSL_REDIRECT=True
exit

sudo systemctl restart erp
```

### Étape 15 : Configurer les Backups (Optionnel mais recommandé)

Dans le dashboard DigitalOcean :
1. Aller sur votre Droplet
2. Cliquer sur **"Backups"**
3. Activer **"Enable Backups"** (+2,40€/mois)
4. Les backups seront automatiques tous les jours

---

## ✅ VÉRIFICATIONS POST-DÉPLOIEMENT

### 1. Vérifier que le service fonctionne
```bash
sudo systemctl status erp
```

### 2. Vérifier les logs
```bash
# Logs de l'application
sudo journalctl -u erp -f

# Logs Nginx
sudo tail -f /var/log/nginx/erp_error.log
```

### 3. Tester l'application
- Visiter `http://VOTRE_IP_SERVEUR` ou `https://votre-domaine.com`
- Vérifier que les fichiers statiques se chargent
- Tester la connexion
- Tester les fonctionnalités principales

### 4. Vérifier la sécurité
- ✅ HTTPS fonctionne
- ✅ DEBUG=False en production
- ✅ Fichiers .env non accessibles publiquement
- ✅ Firewall configuré

---

## 🔧 COMMANDES UTILES

### Redémarrer l'application
```bash
sudo systemctl restart erp
```

### Voir les logs en temps réel
```bash
sudo journalctl -u erp -f
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

### Renouveler le certificat SSL
```bash
sudo certbot renew
```

---

## 📊 MONITORING

DigitalOcean fournit des métriques gratuites :
- CPU usage
- Memory usage
- Disk I/O
- Network traffic

Accédez-y via le dashboard de votre Droplet → **"Metrics"**

---

## 🆘 DÉPANNAGE

### L'application ne démarre pas
```bash
# Vérifier les logs
sudo journalctl -u erp -n 50

# Vérifier la configuration
sudo nginx -t

# Vérifier que Gunicorn écoute
sudo netstat -tlnp | grep 8000
```

### Les fichiers statiques ne se chargent pas
```bash
# Vérifier les permissions
sudo chown -R erpuser:www-data /home/erpuser/erp_project/staticfiles
sudo chmod -R 755 /home/erpuser/erp_project/staticfiles

# Re-collecter les fichiers statiques
cd /home/erpuser/erp_project
source venv/bin/activate
python manage.py collectstatic --settings=erp_project.settings_production --noinput
```

### Erreur de connexion à la base de données
- Vérifier les informations dans `.env`
- Vérifier que le firewall DigitalOcean autorise la connexion depuis le Droplet
- Vérifier que la base de données est bien créée et active

---

## 💰 COÛT TOTAL

- **Droplet** : 12€/mois
- **PostgreSQL managé** : 15€/mois
- **Backups** : 2,40€/mois (optionnel)
- **Total** : **27-30€/mois** pour une solution professionnelle

---

## ✅ RÉSUMÉ

Vous avez maintenant :
- ✅ Un serveur stable et performant (2GB RAM)
- ✅ Une base de données managée avec backups
- ✅ HTTPS configuré (SSL)
- ✅ Application Django en production
- ✅ Monitoring et logs
- ✅ Solution scalable

**Votre ERP est maintenant en ligne et prêt pour la production ! 🚀**

