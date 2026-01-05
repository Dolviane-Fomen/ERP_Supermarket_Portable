# 🌐 Guide Complet : Hébergement + Nom de Domaine sur DigitalOcean

## 📋 Vue d'ensemble

Ce guide vous accompagne étape par étape pour :
1. ✅ Créer un compte DigitalOcean
2. ✅ Obtenir un nom de domaine
3. ✅ Configurer le DNS
4. ✅ Déployer votre ERP
5. ✅ Configurer HTTPS (SSL)

**Coût total estimé : ~30-35€/mois** (serveur + base de données + domaine)

---

## 🎯 ÉTAPE 1 : Créer un compte DigitalOcean

### 1.1 Inscription
1. Aller sur https://www.digitalocean.com
2. Cliquer sur **"Sign Up"**
3. Remplir le formulaire (email, mot de passe)
4. Vérifier votre email

### 1.2 Ajouter une méthode de paiement
1. Dans le dashboard, aller dans **"Settings"** → **"Billing"**
2. Cliquer sur **"Add Payment Method"**
3. Ajouter une carte bancaire ou PayPal
4. **BONUS** : Vous recevrez **200$ de crédit gratuit** pour 60 jours !

---

## 🌍 ÉTAPE 2 : Obtenir un nom de domaine

Vous avez **2 options** :

### **Option A : Acheter le domaine via DigitalOcean (RECOMMANDÉ)**

**Avantages :**
- ✅ Tout au même endroit (plus simple)
- ✅ Configuration DNS automatique
- ✅ Prix compétitifs (~10-15€/an)

**Étapes :**
1. Dans le dashboard DigitalOcean, aller dans **"Networking"** → **"Domains"**
2. Cliquer sur **"Add a domain"**
3. Entrer le nom de domaine souhaité (ex: `monsupermarche.com`)
4. Cliquer sur **"Check availability"**
5. Si disponible, choisir la durée (1 an recommandé)
6. Ajouter au panier et payer
7. Le domaine sera automatiquement configuré dans DigitalOcean

### **Option B : Acheter le domaine ailleurs (Namecheap, OVH, etc.)**

**Avantages :**
- ✅ Parfois moins cher
- ✅ Plus de choix de registrars

**Étapes :**
1. Aller sur un registrar (ex: https://www.namecheap.com, https://www.ovh.com)
2. Rechercher votre domaine
3. L'acheter (généralement 8-15€/an pour un .com)
4. **IMPORTANT** : Notez où vous l'avez acheté, vous devrez configurer les DNS

**Recommandations de registrars :**
- **Namecheap** : Interface simple, bon support
- **OVH** : Prix compétitifs, support français
- **Google Domains** : Simple et fiable

---

## 🖥️ ÉTAPE 3 : Créer le serveur (Droplet)

### 3.1 Créer le Droplet
1. Dans le dashboard DigitalOcean, cliquer sur **"Create"** → **"Droplets"**
2. Configuration recommandée :
   - **Image** : Ubuntu 22.04 (LTS)
   - **Plan** : Basic → **Regular with SSD** → **2GB RAM / 1 vCPU** (12€/mois)
   - **Datacenter region** : 
     - **Frankfurt** pour l'Europe
     - **Amsterdam** pour l'Europe
     - **New York** pour les USA
   - **Authentication** : 
     - **SSH keys** (recommandé - plus sécurisé)
     - OU **Password** (plus simple pour débuter)
   - **Hostname** : `erp-production`
   - **Tags** (optionnel) : `production`, `erp`
3. Cliquer sur **"Create Droplet"**
4. Attendre 1-2 minutes que le serveur soit créé
5. **Noter l'IP du serveur** (ex: `157.230.45.123`)

### 3.2 Se connecter au serveur

**Depuis Windows (PowerShell ou CMD) :**
```bash
ssh root@VOTRE_IP_SERVEUR
```

**Depuis Mac/Linux :**
```bash
ssh root@VOTRE_IP_SERVEUR
```

Si vous avez configuré un mot de passe, entrez-le. Si vous avez utilisé SSH keys, la connexion sera automatique.

---

## 🗄️ ÉTAPE 4 : Créer la base de données PostgreSQL

1. Dans le dashboard DigitalOcean, cliquer sur **"Create"** → **"Databases"**
2. Configuration :
   - **Database Engine** : PostgreSQL
   - **Version** : Latest (16 ou 15)
   - **Plan** : Basic → **1GB RAM / 1 vCPU** (15€/mois)
   - **Datacenter region** : **Même région que votre Droplet**
   - **Database name** : `defaultdb` (ou laisser par défaut)
   - **Choose a VPC** : Laisser par défaut
3. Cliquer sur **"Create a Database Cluster"**
4. Attendre 2-3 minutes que la base soit créée
5. **IMPORTANT** : Noter les informations de connexion :
   - Cliquer sur votre base de données
   - Aller dans l'onglet **"Connection Details"**
   - **Noter** :
     - Host
     - Port
     - Database
     - User
     - Password (cliquer sur "Show" pour voir)

---

## 🔗 ÉTAPE 5 : Configurer le DNS (Pointer le domaine vers votre serveur)

### **Si vous avez acheté le domaine via DigitalOcean :**

1. Dans le dashboard, aller dans **"Networking"** → **"Domains"**
2. Cliquer sur votre domaine
3. Cliquer sur **"Add Record"**
4. Ajouter ces enregistrements :

   **Enregistrement A (Principal) :**
   - **Type** : A
   - **Name** : `@` (ou laisser vide)
   - **Will direct to** : `VOTRE_IP_SERVEUR` (l'IP de votre Droplet)
   - **TTL** : 3600
   - Cliquer sur **"Create Record"**

   **Enregistrement A (www) :**
   - **Type** : A
   - **Name** : `www`
   - **Will direct to** : `VOTRE_IP_SERVEUR` (même IP)
   - **TTL** : 3600
   - Cliquer sur **"Create Record"**

### **Si vous avez acheté le domaine ailleurs :**

Vous devez configurer les DNS chez votre registrar pour pointer vers DigitalOcean.

**Option 1 : Utiliser les serveurs DNS de DigitalOcean (RECOMMANDÉ)**

1. Dans DigitalOcean, aller dans **"Networking"** → **"Domains"**
2. Cliquer sur **"Add a domain"**
3. Entrer votre domaine (ex: `monsupermarche.com`)
4. DigitalOcean vous donnera des serveurs DNS (ex: `ns1.digitalocean.com`, `ns2.digitalocean.com`, `ns3.digitalocean.com`)
5. **Aller chez votre registrar** (où vous avez acheté le domaine)
6. Trouver la section **"DNS"** ou **"Nameservers"**
7. Remplacer les serveurs DNS par ceux de DigitalOcean
8. Attendre 24-48h pour la propagation (généralement 1-2h)

**Option 2 : Configurer les DNS manuellement chez votre registrar**

1. Aller dans les paramètres DNS de votre registrar
2. Ajouter ces enregistrements :
   - **Type A** : `@` → `VOTRE_IP_SERVEUR`
   - **Type A** : `www` → `VOTRE_IP_SERVEUR`

**Exemple pour Namecheap :**
1. Se connecter à Namecheap
2. Aller dans **"Domain List"** → Cliquer sur votre domaine → **"Advanced DNS"**
3. Ajouter :
   - **Type** : A Record
   - **Host** : `@`
   - **Value** : `VOTRE_IP_SERVEUR`
   - **TTL** : Automatic
4. Ajouter :
   - **Type** : A Record
   - **Host** : `www`
   - **Value** : `VOTRE_IP_SERVEUR`
   - **TTL** : Automatic

### Vérifier que le DNS fonctionne

Attendre 1-2 heures (parfois quelques minutes), puis tester :

```bash
# Depuis votre machine
ping votre-domaine.com
# Doit afficher l'IP de votre serveur

# Ou utiliser un outil en ligne
# https://www.whatsmydns.net
```

---

## 🚀 ÉTAPE 6 : Déployer votre application

Suivez le guide `DEPLOIEMENT_PRODUCTION_DIGITALOCEAN.md` ou les étapes rapides ci-dessous :

### 6.1 Configuration initiale du serveur

```bash
# Se connecter au serveur
ssh root@VOTRE_IP_SERVEUR

# Mise à jour
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
sudo apt install python3-pip python3-venv nginx git -y

# Créer un utilisateur pour l'application
sudo adduser erpuser
sudo usermod -aG sudo erpuser

# Se connecter en tant qu'utilisateur
su - erpuser
```

### 6.2 Déployer le code

```bash
# Créer le dossier
mkdir -p ~/erp_project
cd ~/erp_project

# Option A : Si vous utilisez Git
git clone VOTRE_REPO_URL .

# Option B : Transférer via SCP depuis votre machine locale
# Depuis votre machine locale :
# scp -r /chemin/vers/projet/* erpuser@VOTRE_IP_SERVEUR:~/erp_project/

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

### 6.3 Configurer les variables d'environnement

```bash
# Créer le fichier .env
nano .env
```

Contenu du fichier `.env` :

```bash
# Sécurité
SECRET_KEY=votre-cle-secrete-generee
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com,VOTRE_IP_SERVEUR

# Base de données (utiliser les infos de DigitalOcean)
DB_NAME=defaultdb
DB_USER=doadmin
DB_PASSWORD=LE_MOT_DE_PASSE_DIGITALOCEAN
DB_HOST=LE_HOST_DIGITALOCEAN
DB_PORT=25060

# HTTPS (activer après SSL)
SECURE_SSL_REDIRECT=False

# Timezone
TIME_ZONE=UTC
```

**Générer SECRET_KEY :**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6.4 Migrations et collectstatic

```bash
# Créer les dossiers
mkdir -p logs staticfiles media

# Migrations
python manage.py migrate --settings=erp_project.settings_production

# Créer superutilisateur
python manage.py createsuperuser --settings=erp_project.settings_production

# Collecter les fichiers statiques
python manage.py collectstatic --settings=erp_project.settings_production --noinput
```

### 6.5 Configurer Gunicorn (service systemd)

```bash
# Revenir en root
exit

# Créer le service
sudo nano /etc/systemd/system/erp.service
```

Contenu :

```ini
[Unit]
Description=ERP Supermarket Gunicorn daemon
After=network.target

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

Activer le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable erp
sudo systemctl start erp
sudo systemctl status erp
```

### 6.6 Configurer Nginx

```bash
# Créer la configuration
sudo nano /etc/nginx/sites-available/erp
```

Contenu (remplacer `votre-domaine.com` par votre domaine) :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

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
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

### 6.7 Tester (sans HTTPS pour l'instant)

Visiter `http://votre-domaine.com` ou `http://VOTRE_IP_SERVEUR`

L'application devrait s'afficher (sans HTTPS pour l'instant).

---

## 🔒 ÉTAPE 7 : Configurer HTTPS (SSL) avec Let's Encrypt

### 7.1 Installer Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 7.2 Obtenir le certificat SSL

```bash
# Remplacer par votre domaine
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

**Réponses aux questions :**
- Email : Entrer votre email (pour notifications)
- Terms of Service : Accepter (A)
- Share email : Votre choix (Y ou N)
- Redirect HTTP to HTTPS : **Oui (2)** - Important pour la sécurité

Certbot va :
- Générer le certificat SSL
- Configurer automatiquement Nginx pour HTTPS
- Configurer le renouvellement automatique

### 7.3 Activer HTTPS dans Django

```bash
su - erpuser
nano .env
# Changer SECURE_SSL_REDIRECT=True
exit

sudo systemctl restart erp
```

### 7.4 Vérifier le renouvellement automatique

```bash
# Tester le renouvellement (ne renouvelle pas vraiment, juste un test)
sudo certbot renew --dry-run
```

Le renouvellement est automatique via un cron job installé par Certbot.

---

## 🔥 ÉTAPE 8 : Configurer le Firewall

1. Dans le dashboard DigitalOcean, aller dans **"Networking"** → **"Firewalls"**
2. Cliquer sur **"Create Firewall"**
3. Configuration :
   - **Name** : `erp-firewall`
   - **Inbound Rules** :
     - SSH (22) - Source: **Your IP** (pour sécurité - seulement vous pouvez vous connecter)
     - HTTP (80) - Source: All IPv4, All IPv6
     - HTTPS (443) - Source: All IPv4, All IPv6
   - **Outbound Rules** : Laisser par défaut (Allow all)
4. Cliquer sur **"Create Firewall"**
5. **Attacher le firewall** :
   - Cliquer sur votre firewall
   - Onglet **"Droplets"**
   - Sélectionner votre Droplet
   - Cliquer sur **"Assign Droplets"**

---

## ✅ VÉRIFICATIONS FINALES

### 1. Tester l'application
- Visiter `https://votre-domaine.com`
- Vérifier que le cadenas vert s'affiche (HTTPS)
- Tester la connexion
- Tester les fonctionnalités principales

### 2. Vérifier les logs
```bash
# Logs de l'application
sudo journalctl -u erp -f

# Logs Nginx
sudo tail -f /var/log/nginx/erp_error.log
```

### 3. Vérifier la sécurité
- ✅ HTTPS fonctionne (cadenas vert)
- ✅ Redirection HTTP → HTTPS
- ✅ DEBUG=False en production
- ✅ Firewall configuré

---

## 💰 RÉCAPITULATIF DES COÛTS

| Service | Coût | Période |
|---------|------|---------|
| **Droplet (2GB RAM)** | 12€ | /mois |
| **PostgreSQL managé** | 15€ | /mois |
| **Backups automatiques** | 2,40€ | /mois (optionnel) |
| **Nom de domaine (.com)** | 10-15€ | /an |
| **SSL (Let's Encrypt)** | 0€ | Gratuit |

**Total mensuel : ~27-30€/mois** (+ 10-15€/an pour le domaine)

---

## 🎯 RÉSUMÉ DES ÉTAPES

1. ✅ Créer compte DigitalOcean
2. ✅ Acheter un nom de domaine (DigitalOcean ou ailleurs)
3. ✅ Créer le Droplet (serveur)
4. ✅ Créer la base de données PostgreSQL
5. ✅ Configurer le DNS (pointer le domaine vers le serveur)
6. ✅ Déployer l'application Django
7. ✅ Configurer HTTPS (SSL)
8. ✅ Configurer le firewall

---

## 🆘 DÉPANNAGE

### Le domaine ne fonctionne pas
- Attendre 1-2h pour la propagation DNS
- Vérifier avec `ping votre-domaine.com` ou https://www.whatsmydns.net
- Vérifier que les enregistrements DNS sont corrects

### HTTPS ne fonctionne pas
- Vérifier que le domaine pointe bien vers le serveur
- Vérifier que le port 443 est ouvert dans le firewall
- Vérifier les logs : `sudo tail -f /var/log/nginx/erp_error.log`

### L'application ne démarre pas
- Vérifier les logs : `sudo journalctl -u erp -n 50`
- Vérifier que les variables d'environnement sont correctes
- Vérifier la connexion à la base de données

---

## ✅ FÉLICITATIONS !

Votre ERP est maintenant :
- ✅ En ligne et accessible via votre domaine
- ✅ Sécurisé avec HTTPS
- ✅ Prêt pour la production
- ✅ Avec une base de données managée
- ✅ Avec backups automatiques

**Votre ERP est prêt ! 🚀**








