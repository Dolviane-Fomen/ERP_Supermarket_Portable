# 🚀 Guide Complet : Déploiement ERP sur Azure App Service

## 📋 Table des Matières
1. Vue d'ensemble des coûts
2. Création du compte Azure
3. Achat du nom de domaine
4. Création de l'App Service
5. Configuration de la base de données
6. Déploiement de l'application
7. Configuration du domaine et SSL
8. Coûts détaillés et optimisations

---

## 💰 COÛTS COMPLETS - Vue d'ensemble

### Configuration Recommandée (Production)

| Service | Plan | Coût Mensuel | Coût Annuel |
|---------|------|--------------|-------------|
| **Azure App Service** | Basic B1 | 10,20€ | 122,40€ |
| **PostgreSQL Database** | Basic (5GB) | 15,00€ | 180,00€ |
| **Nom de domaine (.com)** | - | 1,25€* | 15,00€ |
| **SSL/HTTPS** | Gratuit | 0,00€ | 0,00€ |
| **Storage (optionnel)** | Standard | 0,02€/GB | Variable |
| **CDN (optionnel)** | Standard | 0,05€/GB | Variable |
| **Backups (optionnel)** | Standard | 0,10€/GB | Variable |
| **TOTAL MINIMUM** | - | **~26,45€** | **~317,40€** |

*Coût du domaine réparti sur 12 mois

### Configuration Économique (Développement/Test)

| Service | Plan | Coût Mensuel |
|---------|------|--------------|
| **Azure App Service** | Free (F1) | 0,00€ |
| **PostgreSQL Database** | Basic (5GB) | 15,00€ |
| **Nom de domaine** | - | 1,25€* |
| **TOTAL** | - | **~16,25€** |

*Limite : 1 App Service gratuit par abonnement

---

## 📊 DÉTAIL DES COÛTS AZURE APP SERVICE

### Plans App Service disponibles

#### **Plan Free (F1)** - Gratuit
- **Coût** : 0€/mois
- **CPU** : Partagé (limité)
- **RAM** : 1GB
- **Disque** : 1GB
- **Bande passante** : 165GB/mois
- **Limitations** :
  - Application s'endort après 20 min d'inactivité
  - Pas de domaine personnalisé SSL
  - Pas de scaling
  - Pas pour la production
- **Idéal pour** : Tests, développement

#### **Plan Shared (D1)** - Partagé
- **Coût** : ~8€/mois
- **CPU** : Partagé
- **RAM** : 1GB
- **Disque** : 1GB
- **Bande passante** : Illimitée
- **Limitations** : Pas recommandé pour production

#### **Plan Basic (B1)** - RECOMMANDÉ pour débuter
- **Coût** : **10,20€/mois**
- **CPU** : Dédié (1 core)
- **RAM** : 1.75GB
- **Disque** : 10GB
- **Bande passante** : Illimitée
- **Avantages** :
  - Domaine personnalisé + SSL gratuit
  - Pas de limitation de temps
  - Scaling manuel jusqu'à 3 instances
  - Backups inclus (10GB)
- **Idéal pour** : Petites applications, début de production

#### **Plan Basic (B2)** - Pour plus de ressources
- **Coût** : **20,40€/mois**
- **CPU** : Dédié (2 cores)
- **RAM** : 3.5GB
- **Disque** : 10GB
- **Idéal pour** : Applications avec trafic modéré

#### **Plan Basic (B3)** - Performance
- **Coût** : **40,80€/mois**
- **CPU** : Dédié (4 cores)
- **RAM** : 7GB
- **Disque** : 50GB
- **Idéal pour** : Applications avec trafic élevé

#### **Plan Standard (S1)** - Production
- **Coût** : **60,00€/mois**
- **CPU** : Dédié (1 core)
- **RAM** : 1.75GB
- **Disque** : 50GB
- **Avantages** :
  - Auto-scaling
  - Staging slots (déploiement sans interruption)
  - Backups automatiques
- **Idéal pour** : Production professionnelle

#### **Plan Premium (P1V2)** - Haute performance
- **Coût** : **120,00€/mois**
- **CPU** : Dédié (2 cores)
- **RAM** : 3.5GB
- **Disque** : 250GB
- **Avantages** :
  - Meilleures performances
  - Plus de staging slots
  - Isolation réseau

---

## 🗄️ COÛTS BASE DE DONNÉES POSTGRESQL

### Azure Database for PostgreSQL - Flexible Server

#### **Plan Basic (B1ms)** - RECOMMANDÉ pour débuter
- **Coût** : **15,00€/mois**
- **vCores** : 1
- **RAM** : 2GB
- **Stockage** : 32GB (minimum)
- **Backups** : 7 jours inclus
- **Idéal pour** : Petites applications

#### **Plan Basic (B2s)**
- **Coût** : **30,00€/mois**
- **vCores** : 2
- **RAM** : 4GB
- **Stockage** : 32GB
- **Idéal pour** : Applications modérées

#### **Plan General Purpose (D2s_v3)**
- **Coût** : **60,00€/mois**
- **vCores** : 2
- **RAM** : 8GB
- **Stockage** : 128GB
- **Idéal pour** : Production avec trafic moyen

#### **Stockage supplémentaire**
- **Coût** : **0,10€/GB/mois**
- Exemple : +50GB = +5€/mois

#### **Backups supplémentaires**
- **Rétention 7 jours** : Inclus
- **Rétention 14 jours** : +2€/mois
- **Rétention 30 jours** : +5€/mois
- **Rétention 35 jours** : +7€/mois

---

## 🌐 COÛTS NOM DE DOMAINE

### Via Azure (App Service Domains)

| Extension | Prix Annuel | Prix Mensuel* |
|-----------|-------------|---------------|
| **.com** | 15,00€ | 1,25€ |
| **.net** | 18,00€ | 1,50€ |
| **.org** | 15,00€ | 1,25€ |
| **.fr** | 12,00€ | 1,00€ |
| **.eu** | 8,00€ | 0,67€ |

*Réparti sur 12 mois

### Via Autres Registrars (Comparaison)

| Registrar | .com | .fr | Support |
|-----------|------|-----|---------|
| **Azure** | 15€ | 12€ | ✅ Excellent |
| **Namecheap** | 10€ | 12€ | ✅ Bon |
| **OVH** | 12€ | 8€ | ✅ Français |
| **Google Domains** | 12€ | 12€ | ✅ Simple |

**Recommandation** : Azure pour simplicité, OVH/Namecheap pour économie

---

## 💾 AUTRES COÛTS POSSIBLES

### Storage (Stockage de fichiers)

#### **Azure Blob Storage** (pour fichiers médias)
- **Hot Tier** : 0,018€/GB/mois (accès fréquent)
- **Cool Tier** : 0,010€/GB/mois (accès occasionnel)
- **Archive Tier** : 0,002€/GB/mois (archivage)

**Exemple** : 10GB de fichiers médias = 0,18€/mois (Hot)

### CDN (Content Delivery Network)

#### **Azure CDN Standard**
- **Transfert de données** : 0,05€/GB (premiers 10TB)
- **Requêtes** : 0,004€/10 000 requêtes

**Exemple** : 50GB/mois = 2,50€/mois

### Backups supplémentaires

#### **App Service Backups**
- **Plan Basic** : 10GB inclus
- **Stockage supplémentaire** : 0,10€/GB/mois

#### **Database Backups**
- **7 jours** : Inclus
- **14-35 jours** : 2-7€/mois selon durée

### Monitoring et Logs

#### **Application Insights** (optionnel)
- **Plan Gratuit** : 5GB de données/mois inclus
- **Au-delà** : 2,30€/GB

**Recommandation** : Plan gratuit suffit généralement

### Bandwidth (Bande passante)

#### **App Service**
- **Plans Basic+** : Illimité (inclus)
- **Plan Free** : 165GB/mois inclus

### SSL/HTTPS

- **Let's Encrypt** : **GRATUIT** (inclus dans Azure App Service)
- **Certificat managé** : **GRATUIT** (Azure gère automatiquement)

---

## 📝 GUIDE DE DÉPLOIEMENT ÉTAPE PAR ÉTAPE

### Étape 1 : Créer un compte Azure

1. Aller sur https://azure.microsoft.com
2. Cliquer sur "Start free"
3. Créer un compte Microsoft (ou utiliser existant)
4. Ajouter une méthode de paiement
5. **BONUS** : Recevoir 200$ de crédit gratuit (30 jours)

**Coût** : 0€ (crédit gratuit inclus)

### Étape 2 : Créer un Resource Group

1. Azure Portal → "Resource groups"
2. "Create"
3. Nom : `erp-supermarket-rg`
4. Region : West Europe (ou proche de vous)
5. Create

**Coût** : 0€ (organisation uniquement)

### Étape 3 : Acheter un nom de domaine

**Option A : Via Azure**

1. Azure Portal → "App Service Domains"
2. "Add domain"
3. Rechercher votre domaine
4. Ajouter au panier et payer
5. Configuration DNS automatique

**Coût** : 15€/an pour .com

**Option B : Via Autre Registrar**

1. Aller sur Namecheap/OVH/etc.
2. Acheter le domaine
3. Configurer DNS plus tard dans Azure

**Coût** : 10-15€/an pour .com

### Étape 4 : Créer l'App Service

1. Azure Portal → "Create a resource"
2. Chercher "Web App" → "Create"
3. Configuration :
   - **Subscription** : Votre abonnement
   - **Resource Group** : `erp-supermarket-rg`
   - **Name** : `erp-supermarket-app` (doit être unique)
   - **Publish** : Code
   - **Runtime stack** : Python 3.11
   - **Operating System** : Linux (recommandé)
   - **Region** : West Europe
   - **App Service Plan** :
     - Créer nouveau : `erp-plan`
     - **Sku and size** : Basic B1 (10,20€/mois)
4. "Review + create" → "Create"

**Coût** : 10,20€/mois

### Étape 5 : Créer la base de données PostgreSQL

1. Azure Portal → "Create a resource"
2. Chercher "Azure Database for PostgreSQL"
3. Choisir "Flexible server" → "Create"
4. Configuration :
   - **Subscription** : Votre abonnement
   - **Resource Group** : `erp-supermarket-rg`
   - **Server name** : `erp-postgres-server`
   - **Region** : Même que App Service
   - **PostgreSQL version** : 15 (latest)
   - **Compute + storage** :
     - **Compute tier** : Burstable
     - **Size** : Basic_B1ms (1 vCore, 2GB RAM)
     - **Storage** : 32GB
   - **Backup** : 7 days (inclus)
   - **Admin username** : `adminuser`
   - **Password** : Créer un mot de passe fort
5. "Review + create" → "Create"

**Coût** : 15,00€/mois

**IMPORTANT** : Noter les informations de connexion :
- Host : `erp-postgres-server.postgres.database.azure.com`
- Port : 5432
- Database : `postgres` (par défaut)
- Username : `adminuser@erp-postgres-server`
- Password : Celui que vous avez créé

### Étape 6 : Configurer les règles de pare-feu PostgreSQL

1. Aller sur votre serveur PostgreSQL
2. "Networking" → "Firewall rules"
3. Ajouter :
   - **Rule name** : `AllowAzureServices`
   - **Start IP** : 0.0.0.0
   - **End IP** : 0.0.0.0
   - (Autorise tous les services Azure)
4. "Save"

### Étape 7 : Préparer votre code Django

**Créer un fichier `requirements.txt`** (si pas déjà fait) :
```
django>=5.2.7
psycopg2-binary>=2.9.9
gunicorn>=21.2.0
whitenoise>=6.6.0
pillow>=11.3.0
openpyxl>=3.1.5
reportlab>=4.4.4
```

**Créer un fichier `startup.sh`** (pour Azure) :
```bash
#!/bin/bash
gunicorn --bind 0.0.0.0:8000 erp_project.wsgi:application
```

**Vérifier `settings_production.py`** :
- Utiliser les variables d'environnement Azure
- `DEBUG = False`
- `ALLOWED_HOSTS` avec votre domaine

### Étape 8 : Déployer depuis GitHub

1. Pousser votre code sur GitHub (voir guide précédent)
2. Azure Portal → Votre App Service
3. "Deployment Center" → "Settings"
4. Source : GitHub
5. Autoriser Azure à accéder à GitHub
6. Sélectionner :
   - Organization : Votre compte GitHub
   - Repository : `erp-supermarket` (ou votre repo)
   - Branch : `main`
7. "Save"

Azure déploiera automatiquement votre code.

### Étape 9 : Configurer les variables d'environnement

1. App Service → "Configuration" → "Application settings"
2. Ajouter :

```
DJANGO_SETTINGS_MODULE = erp_project.settings_production
SECRET_KEY = votre-cle-secrete-generee
ALLOWED_HOSTS = votre-domaine.com,www.votre-domaine.com
DB_NAME = postgres
DB_USER = adminuser@erp-postgres-server
DB_PASSWORD = votre-mot-de-passe-postgres
DB_HOST = erp-postgres-server.postgres.database.azure.com
DB_PORT = 5432
SECURE_SSL_REDIRECT = True
```

3. "Save"

### Étape 10 : Configurer le domaine personnalisé

**Si domaine acheté via Azure :**
- Configuration automatique

**Si domaine acheté ailleurs :**

1. App Service → "Custom domains"
2. "Add custom domain"
3. Entrer votre domaine : `votre-domaine.com`
4. Azure vous donnera des enregistrements DNS à ajouter :
   - Type : CNAME
   - Name : `@` ou `www`
   - Value : `votre-app.azurewebsites.net`
5. Aller chez votre registrar et ajouter ces enregistrements
6. Attendre 1-2h pour propagation DNS
7. Dans Azure, cliquer "Validate"
8. Azure génère automatiquement le certificat SSL (gratuit)

### Étape 11 : Exécuter les migrations

1. App Service → "SSH" ou "Console"
2. Ou utiliser "Advanced Tools" → "Go" → "SSH"
3. Exécuter :
```bash
python manage.py migrate --settings=erp_project.settings_production
python manage.py collectstatic --settings=erp_project.settings_production --noinput
python manage.py createsuperuser --settings=erp_project.settings_production
```

### Étape 12 : Vérifier le déploiement

1. Visiter `https://votre-domaine.com`
2. Vérifier que le cadenas vert s'affiche (HTTPS)
3. Tester la connexion
4. Tester les fonctionnalités

---

## 💡 OPTIMISATIONS DES COÛTS

### Pour réduire les coûts :

1. **Utiliser le plan Free pour tester**
   - 0€/mois
   - Limité mais suffisant pour tests

2. **Arrêter les services quand non utilisés**
   - App Service peut être arrêté (pas de coût)
   - PostgreSQL peut être arrêté (économie)

3. **Utiliser Reserved Instances** (engagement 1-3 ans)
   - Réduction jusqu'à 72% sur App Service
   - Réduction jusqu'à 55% sur PostgreSQL

4. **Optimiser le stockage**
   - Utiliser Cool/Archive tier pour fichiers anciens
   - Nettoyer régulièrement les backups

5. **Monitorer l'utilisation**
   - Azure Cost Management
   - Définir des budgets et alertes

---

## 📊 RÉCAPITULATIF DES COÛTS

### Configuration Minimum (Production)
- App Service Basic B1 : 10,20€/mois
- PostgreSQL Basic : 15,00€/mois
- Domaine .com : 1,25€/mois (15€/an)
- **TOTAL : ~26,45€/mois**

### Configuration Recommandée (Production)
- App Service Basic B2 : 20,40€/mois
- PostgreSQL Basic B2s : 30,00€/mois
- Domaine .com : 1,25€/mois
- Storage 10GB : 0,18€/mois
- **TOTAL : ~51,83€/mois**

### Configuration Performance (Production)
- App Service Standard S1 : 60,00€/mois
- PostgreSQL General Purpose : 60,00€/mois
- Domaine .com : 1,25€/mois
- Storage 50GB : 0,90€/mois
- CDN 100GB : 5,00€/mois
- **TOTAL : ~127,15€/mois**

---

## ✅ CHECKLIST DE DÉPLOIEMENT

- [ ] Compte Azure créé
- [ ] Resource Group créé
- [ ] Nom de domaine acheté
- [ ] App Service créé (Basic B1)
- [ ] PostgreSQL créé (Basic B1ms)
- [ ] Code poussé sur GitHub
- [ ] Déploiement configuré dans Azure
- [ ] Variables d'environnement configurées
- [ ] Domaine personnalisé configuré
- [ ] SSL/HTTPS activé
- [ ] Migrations exécutées
- [ ] Superutilisateur créé
- [ ] Application testée
- [ ] Monitoring configuré

---

## 🆘 DÉPANNAGEMENT

### L'application ne démarre pas
- Vérifier les logs : App Service → "Log stream"
- Vérifier les variables d'environnement
- Vérifier que `startup.sh` est configuré

### Erreur de connexion à la base de données
- Vérifier les règles de pare-feu PostgreSQL
- Vérifier les identifiants dans les variables d'environnement
- Vérifier que le serveur PostgreSQL est démarré

### Le domaine ne fonctionne pas
- Vérifier les enregistrements DNS
- Attendre 1-2h pour propagation
- Utiliser https://www.whatsmydns.net pour vérifier

---

## 📞 SUPPORT

- **Documentation Azure** : https://docs.microsoft.com/azure
- **Support Azure** : Disponible dans le portail
- **Communauté** : Stack Overflow, Reddit r/AZURE

---

**Votre ERP est maintenant prêt pour la production sur Azure ! 🚀**

