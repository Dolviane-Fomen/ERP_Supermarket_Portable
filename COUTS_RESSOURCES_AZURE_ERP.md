# 💰 Ressources et Coûts - ERP Azure App Service
## Pour 20+ Utilisateurs Simultanés

---

## 📦 RESSOURCES NÉCESSAIRES

### 1. Azure App Service Plan
- **Type** : Standard S1
- **Spécifications** :
  - CPU : 1 core dédié par instance
  - RAM : 1.75GB par instance
  - Disque : 50GB
  - Auto-scaling : 2-4 instances
  - Staging slots : 1 inclus
  - Backups : Automatiques (10GB inclus)
- **Quantité** : 1 plan
- **Coût mensuel** : **60,00€** (par instance)
- **Instances** : 2 (minimum recommandé)
- **Coût total App Service** : **120,00€/mois**

### 2. Azure Database for PostgreSQL
- **Type** : Flexible Server - General Purpose
- **Spécifications** :
  - vCores : 2
  - RAM : 8GB
  - Stockage : 128GB SSD
  - IOPS : 3600
  - Backups : 30 jours de rétention (inclus)
- **Quantité** : 1 serveur
- **Coût mensuel** : **60,00€**

### 3. Nom de Domaine
- **Type** : .com (via Azure)
- **Quantité** : 1 domaine
- **Coût annuel** : **15,00€**
- **Coût mensuel** : **1,25€** (réparti sur 12 mois)

### 4. SSL/HTTPS
- **Type** : Certificat managé Azure (Let's Encrypt)
- **Quantité** : 1 certificat
- **Coût mensuel** : **0,00€** (GRATUIT)

### 5. Application Insights (Monitoring)
- **Type** : Plan Gratuit
- **Spécifications** :
  - Données : 5GB/mois inclus
  - Métriques : Illimitées
- **Quantité** : 1 instance
- **Coût mensuel** : **0,00€** (GRATUIT jusqu'à 5GB/mois)

### 6. Azure Blob Storage (Fichiers médias - Optionnel)
- **Type** : Hot Tier
- **Spécifications** : 20GB pour fichiers médias
- **Quantité** : 1 compte de stockage
- **Coût mensuel** : **0,36€** (0,018€/GB)

### 7. Azure CDN (Accélération - Optionnel)
- **Type** : Standard
- **Spécifications** : 100GB/mois
- **Quantité** : 1 profil CDN
- **Coût mensuel** : **5,00€** (0,05€/GB)

---

## 💵 RÉCAPITULATIF DES COÛTS

### Configuration Minimum (Essentiel)

| Ressource | Quantité | Coût Mensuel | Coût Annuel |
|-----------|-----------|--------------|-------------|
| **App Service Plan (Standard S1)** | 2 instances | 120,00€ | 1 440,00€ |
| **PostgreSQL (General Purpose D2s_v3)** | 1 serveur | 60,00€ | 720,00€ |
| **Nom de domaine (.com)** | 1 domaine | 1,25€ | 15,00€ |
| **SSL/HTTPS** | 1 certificat | 0,00€ | 0,00€ |
| **Application Insights** | 1 instance | 0,00€ | 0,00€ |
| **TOTAL MENSUEL** | - | **181,25€** | **2 175,00€** |

### Configuration Recommandée (Complète)

| Ressource | Quantité | Coût Mensuel | Coût Annuel |
|-----------|-----------|--------------|-------------|
| **App Service Plan (Standard S1)** | 2 instances | 120,00€ | 1 440,00€ |
| **PostgreSQL (General Purpose D2s_v3)** | 1 serveur | 60,00€ | 720,00€ |
| **Nom de domaine (.com)** | 1 domaine | 1,25€ | 15,00€ |
| **SSL/HTTPS** | 1 certificat | 0,00€ | 0,00€ |
| **Application Insights** | 1 instance | 0,00€ | 0,00€ |
| **Blob Storage (20GB)** | 1 compte | 0,36€ | 4,32€ |
| **CDN (100GB/mois)** | 1 profil | 5,00€ | 60,00€ |
| **TOTAL MENSUEL** | - | **186,61€** | **2 239,32€** |

---

## 💰 ÉCONOMIES AVEC RESERVED INSTANCES

### Engagement 1 An

| Ressource | Coût Normal | Coût avec RI (1 an) | Économie |
|-----------|-------------|---------------------|----------|
| **App Service Plan** | 120,00€/mois | 69,60€/mois | -42% (-50,40€) |
| **PostgreSQL** | 60,00€/mois | 40,20€/mois | -33% (-19,80€) |
| **Économie totale** | - | - | **-70,20€/mois** |

**Coût mensuel avec Reserved Instances (1 an) :**
- Configuration Minimum : **111,05€/mois** (au lieu de 181,25€)
- Configuration Recommandée : **116,41€/mois** (au lieu de 186,61€)
- **Économie annuelle** : ~840€/an

### Engagement 3 Ans

| Ressource | Coût Normal | Coût avec RI (3 ans) | Économie |
|-----------|-------------|----------------------|----------|
| **App Service Plan** | 120,00€/mois | 50,40€/mois | -58% (-69,60€) |
| **PostgreSQL** | 60,00€/mois | 27,00€/mois | -55% (-33,00€) |
| **Économie totale** | - | - | **-102,60€/mois** |

**Coût mensuel avec Reserved Instances (3 ans) :**
- Configuration Minimum : **78,65€/mois** (au lieu de 181,25€)
- Configuration Recommandée : **84,01€/mois** (au lieu de 186,61€)
- **Économie annuelle** : ~1 230€/an

---

## 📊 COÛTS ADDITIONNELS POSSIBLES

### Si Scaling au-delà de 2 Instances

| Nombre d'Instances | Coût Mensuel App Service |
|-------------------|---------------------------|
| 2 instances (minimum) | 120,00€ |
| 3 instances | 180,00€ (+60€) |
| 4 instances (maximum auto-scaling) | 240,00€ (+120€) |

### Si Stockage PostgreSQL Augmente

| Stockage | Coût Additionnel |
|----------|------------------|
| 128GB (inclus) | 0,00€ |
| 150GB | +2,20€/mois |
| 200GB | +7,20€/mois |
| 250GB | +12,20€/mois |

### Si Application Insights dépasse 5GB/mois

| Données | Coût Additionnel |
|---------|------------------|
| 0-5GB (inclus) | 0,00€ |
| 10GB | +11,50€/mois |
| 20GB | +34,50€/mois |
| 50GB | +103,50€/mois |

### Si CDN dépasse 100GB/mois

| Données | Coût Additionnel |
|---------|------------------|
| 0-100GB | 5,00€ |
| 200GB | +5,00€/mois |
| 500GB | +20,00€/mois |
| 1TB | +45,00€/mois |

### Options Supplémentaires

| Service | Description | Coût Mensuel |
|---------|-------------|--------------|
| **Haute Disponibilité PostgreSQL** | Redondance automatique | +30,00€ |
| **Read Replica PostgreSQL** | Réplique en lecture | +60,00€ |
| **Azure Redis Cache** | Cache pour performances | +15,00€ (Basic C0) |
| **Azure Key Vault** | Gestion des secrets | +0,03€/secret |
| **Backup Storage supplémentaire** | Au-delà de 10GB | +0,10€/GB |

---

## 💳 ESTIMATION BUDGETAIRE

### Première Année (Sans Reserved Instances)

| Période | Coût Mensuel | Coût Cumulé |
|---------|--------------|-------------|
| **Mois 1** | 186,61€ | 186,61€ |
| **Mois 2-12** | 186,61€/mois | 2 239,32€ |
| **TOTAL ANNÉE 1** | - | **2 239,32€** |

### Première Année (Avec Reserved Instances 1 an)

| Période | Coût Mensuel | Coût Cumulé |
|---------|--------------|-------------|
| **Mois 1** | 186,61€ | 186,61€ |
| **Mois 2-12** | 116,41€/mois | 1 467,11€ |
| **TOTAL ANNÉE 1** | - | **1 653,72€** |
| **ÉCONOMIE** | - | **-585,60€** |

### Coûts Récurrents Mensuels

**Configuration Minimum :**
- Sans RI : **181,25€/mois**
- Avec RI (1 an) : **111,05€/mois**
- Avec RI (3 ans) : **78,65€/mois**

**Configuration Recommandée :**
- Sans RI : **186,61€/mois**
- Avec RI (1 an) : **116,41€/mois**
- Avec RI (3 ans) : **84,01€/mois**

---

## 🎯 RÉSUMÉ FINANCIER

### Coût Total Mensuel

| Configuration | Sans RI | Avec RI (1 an) | Avec RI (3 ans) |
|---------------|---------|----------------|-----------------|
| **Minimum** | 181,25€ | 111,05€ | 78,65€ |
| **Recommandée** | 186,61€ | 116,41€ | 84,01€ |

### Coût Total Annuel

| Configuration | Sans RI | Avec RI (1 an) | Avec RI (3 ans) |
|---------------|---------|----------------|-----------------|
| **Minimum** | 2 175,00€ | 1 332,60€ | 943,80€ |
| **Recommandée** | 2 239,32€ | 1 396,92€ | 1 008,12€ |

### Économie avec Reserved Instances

| Engagement | Économie Mensuelle | Économie Annuelle |
|------------|-------------------|-------------------|
| **1 an** | 70,20€ | 842,40€ |
| **3 ans** | 102,60€ | 1 231,20€ |

---

## ✅ RECOMMANDATION FINANCIÈRE

### Pour Optimiser les Coûts

1. **Commencer avec Reserved Instances (1 an)**
   - Économie immédiate de 70€/mois
   - Engagement raisonnable (1 an)

2. **Configuration Recommandée**
   - Coût : **116,41€/mois** avec RI (1 an)
   - Tous les services nécessaires inclus

3. **Monitoring des Coûts**
   - Utiliser Azure Cost Management
   - Définir des budgets et alertes
   - Réviser mensuellement

### Budget Recommandé

**Mensuel** : **120-150€/mois** (avec marge pour variations)
**Annuel** : **1 400-1 800€/an** (avec Reserved Instances)

---

## 📝 NOTES IMPORTANTES

1. **Crédit Gratuit Azure** : 200$ pour 30 jours (nouveaux comptes)
2. **Prix en EUR** : Les prix peuvent varier selon la région et les taxes
3. **Facturation** : Azure facture à l'heure, arrondi au mois
4. **Arrêt des services** : App Service peut être arrêté (pas de coût), PostgreSQL continue de facturer
5. **Scaling** : Les coûts peuvent augmenter si auto-scaling ajoute des instances

---

**Dernière mise à jour** : Décembre 2024
**Région** : West Europe (prix peuvent varier selon région)

