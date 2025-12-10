# 🚀 GUIDE COMPLET - CONFIGURATION ACCÈS MULTI-AGENCES

## 📋 TABLE DES MATIÈRES
1. [Prérequis](#prérequis)
2. [Architecture](#architecture)
3. [Connexion Réseau](#connexion-réseau)
4. [Installation Dépendances](#installation-dépendances)
5. [Configuration PC Principal](#configuration-pc-principal)
6. [Configuration PC Agence 1](#configuration-pc-agence-1)
7. [Configuration PC Agence 2](#configuration-pc-agence-2)
8. [Test de Fonctionnement](#test-de-fonctionnement)
9. [Scénarios de Fonctionnement](#scénarios-de-fonctionnement)
10. [Dépannage](#dépannage)
11. [Maintenance](#maintenance)

---

## 🔧 PRÉREQUIS

### **Matériel Requis :**
- ✅ **3 PC** avec Windows
- ✅ **3 Câbles Ethernet**
- ✅ **1 Routeur/Switch**
- ✅ **ERP_Launcher.bat** sur chaque PC

### **Logiciel Requis :**
- ✅ **Python 3.8+** sur chaque PC
- ✅ **Dépendances** : openpyxl, reportlab, django
- ✅ **Fichiers de synchronisation** sur chaque PC

### **Architecture Cible :**
```
PC1 (Principal + Accès Multi-Agences) ←→ Routeur ←→ PC2 (Caisse Agence 1)
  ↑                                              ↑
  └─────────── PC3 (Caisse Agence 2) ←──────────┘
```

---

## 🏗️ ARCHITECTURE

### **PC1 (Principal + Accès Multi-Agences) :**
- 🎯 **Se connecte** - Avec les accès de chaque agence
- 🎯 **Voit tout** - Données de PC2 et PC3
- 🎯 **Centralise** - Toutes les données des 2 agences
- 🎯 **Fonctionne seul** - Même si PC2 et PC3 éteints

### **PC2 (Caisse Agence 1) :**
- 🎯 **Caisse Agence 1** - Enregistre les ventes de l'agence 1
- 🎯 **Envoie vers PC1** - Données de vente agence 1
- 🎯 **Fonctionne seul** - Même si PC1 et PC3 éteints
- 🎯 **Fonctionne offline** - Quand PC1 est éteint

### **PC3 (Caisse Agence 2) :**
- 🎯 **Caisse Agence 2** - Enregistre les ventes de l'agence 2
- 🎯 **Envoie vers PC1** - Données de vente agence 2
- 🎯 **Fonctionne seul** - Même si PC1 et PC2 éteints
- 🎯 **Fonctionne offline** - Quand PC1 est éteint

---

## 🌐 CONNEXION RÉSEAU

### **ÉTAPE 1 : CONNEXION PHYSIQUE**

#### **1.1 Câblage :**
```
Routeur/Switch
    ↓
┌─────┬─────┬─────┐
│ PC1 │ PC2 │ PC3 │
│ ERP │ ERP │ ERP │
└─────┴─────┴─────┘
```

#### **1.2 Vérification :**
- ✅ Tous les câbles connectés
- ✅ LEDs de connexion allumées
- ✅ Routeur allumé

### **ÉTAPE 2 : OBTENIR LES IPs**

#### **2.1 Sur chaque PC :**
```bash
# Double-cliquer sur
OBTENIR_IP.bat

# Noter l'IP de chaque PC
# Exemple :
# PC1 : 192.168.1.100
# PC2 : 192.168.1.101
# PC3 : 192.168.1.102
```

#### **2.2 Test de connectivité :**
```bash
# Sur PC1, tester les autres PC
ping 192.168.1.101  # PC2 (Agence 1)
ping 192.168.1.102  # PC3 (Agence 2)

# Sur PC2, tester seulement PC1
ping 192.168.1.100  # PC1

# Sur PC3, tester seulement PC1
ping 192.168.1.100  # PC1
```

---

## 📦 INSTALLATION DÉPENDANCES

### **ÉTAPE 3 : INSTALLATION SUR CHAQUE PC**

#### **3.1 Sur PC1, PC2, PC3 :**
```bash
# Double-cliquer sur
INSTALLER_DEPENDANCES_ERP.bat

# Attendre la fin de l'installation
# Vérifier que tout est installé
```

#### **3.2 Vérification :**
```bash
# Tester Python
py --version

# Tester les dépendances
py -c "import openpyxl; print('openpyxl OK')"
py -c "import reportlab; print('reportlab OK')"
py -c "import django; print('django OK')"
```

---

## ⚙️ CONFIGURATION PC PRINCIPAL

### **ÉTAPE 4 : CONFIGURATION PC1 (PRINCIPAL + ACCÈS MULTI-AGENCES)**

#### **4.1 Démarrer le gestionnaire :**
```bash
# Sur PC1, double-cliquer sur
GESTIONNAIRE_SYNC.bat

# Choisir l'option "1" - Démarrer la synchronisation
# Noter l'IP affichée (ex: 192.168.1.100)
```

#### **4.2 Vérifier la configuration :**
```bash
# Vérifier le fichier erp_sync/erp_launcher_config.json
{
    "network_ips": [
        "192.168.1.100",
        "192.168.1.101",
        "192.168.1.102"
    ],
    "sync_interval": 30,
    "max_retries": 3,
    "timeout": 10
}
```

#### **4.3 Démarrer l'ERP :**
```bash
# Double-cliquer sur
ERP_Launcher.bat

# Vérifier que l'ERP démarre correctement
# L'IP sera : 192.168.1.100:8000
```

#### **4.4 Accès multi-agences :**
```bash
# PC1 peut maintenant :
# - Se connecter avec les accès de chaque agence
# - Voir les données de l'agence 1 (PC2)
# - Voir les données de l'agence 2 (PC3)
# - Centraliser toutes les données
# - Générer des rapports complets
```

---

## 🔗 CONFIGURATION PC AGENCE 1

### **ÉTAPE 5 : CONFIGURATION PC2 (CAISSE AGENCE 1)**

#### **5.1 Se connecter au réseau :**
```bash
# Sur PC2, double-cliquer sur
GESTIONNAIRE_SYNC.bat

# Choisir l'option "2" - Se connecter au réseau
# Entrer l'IP du PC principal : 192.168.1.100
```

#### **5.2 Vérifier la connexion :**
```bash
# Choisir l'option "3" - Voir le statut
# Vérifier que la connexion est active
```

#### **5.3 Démarrer l'ERP :**
```bash
# Double-cliquer sur
ERP_Launcher.bat

# L'IP sera : 192.168.1.101:8000
```

#### **5.4 Fonctionnement Agence 1 :**
```bash
# PC2 peut maintenant :
# - Enregistrer les ventes de l'agence 1
# - Envoyer les données vers PC1
# - Fonctionner seul (même si PC1 éteint)
# - Synchroniser avec PC1 quand allumé
```

---

## 🔗 CONFIGURATION PC AGENCE 2

### **ÉTAPE 6 : CONFIGURATION PC3 (CAISSE AGENCE 2)**

#### **6.1 Se connecter au réseau :**
```bash
# Sur PC3, double-cliquer sur
GESTIONNAIRE_SYNC.bat

# Choisir l'option "2" - Se connecter au réseau
# Entrer l'IP du PC principal : 192.168.1.100
```

#### **6.2 Vérifier la connexion :**
```bash
# Choisir l'option "3" - Voir le statut
# Vérifier que la connexion est active
```

#### **6.3 Démarrer l'ERP :**
```bash
# Double-cliquer sur
ERP_Launcher.bat

# L'IP sera : 192.168.1.102:8000
```

#### **6.4 Fonctionnement Agence 2 :**
```bash
# PC3 peut maintenant :
# - Enregistrer les ventes de l'agence 2
# - Envoyer les données vers PC1
# - Fonctionner seul (même si PC1 éteint)
# - Synchroniser avec PC1 quand allumé
```

---

## 🧪 TEST DE FONCTIONNEMENT

### **ÉTAPE 7 : TEST COMPLET**

#### **7.1 Test avec tous les PC allumés :**
```bash
# PC1 : Vérifier l'accès multi-agences
# PC2 : Créer une vente "Vente Agence 1"
# PC3 : Créer une vente "Vente Agence 2"
# PC1 : Vérifier que les 2 ventes apparaissent
```

#### **7.2 Test avec PC1 éteint :**
```bash
# Éteindre PC1
# PC2 : Vérifier qu'il fonctionne toujours
# PC3 : Vérifier qu'il fonctionne toujours
# PC2 : Créer une vente "Vente Offline Agence 1"
# PC3 : Créer une vente "Vente Offline Agence 2"
```

#### **7.3 Test avec PC1 rallumé :**
```bash
# Allumer PC1
# PC1 : Vérifier que les ventes offline apparaissent
# Synchronisation automatique
# PC2 : Vérifier que la synchronisation fonctionne
# PC3 : Vérifier que la synchronisation fonctionne
```

#### **7.4 Test avec PC2 éteint :**
```bash
# Éteindre PC2
# PC1 : Vérifier qu'il fonctionne toujours
# PC3 : Vérifier qu'il fonctionne toujours
# PC1 : Créer un article "Article PC1"
# PC3 : Vérifier que l'article apparaît
```

#### **7.5 Test avec PC3 éteint :**
```bash
# Éteindre PC3
# PC1 : Vérifier qu'il fonctionne toujours
# PC2 : Vérifier qu'il fonctionne toujours
# PC1 : Créer un article "Article PC1"
# PC2 : Vérifier que l'article apparaît
```

---

## 📊 SCÉNARIOS DE FONCTIONNEMENT

### **SCÉNARIO 1 : TOUS ALLUMÉS**
```
PC1 ←→ PC2 ←→ PC3
  ↑      ↑      ↑
Principal Caisse Caisse
Multi-Agences Agence 1 Agence 2
```

#### **Fonctionnement :**
- ✅ **PC1** : Accès multi-agences, voit tout
- ✅ **PC2** : Caisse Agence 1, synchronise avec PC1
- ✅ **PC3** : Caisse Agence 2, synchronise avec PC1 
- ✅ **Synchronisation** : Complète entre tous les PC

### **SCÉNARIO 2 : PC1 ÉTEINT**
```
PC2 (Fonctionne seul - Agence 1)
PC3 (Fonctionne seul - Agence 2)
```

#### **Fonctionnement :**
- ✅ **PC2** : Fonctionne seul, sauvegarde locale
- ✅ **PC3** : Fonctionne seul, sauvegarde locale
- ❌ **PC1** : Éteint, pas d'accès multi-agences
- ✅ **Continuité** : Service maintenu sur PC2 et PC3

### **SCÉNARIO 3 : PC2 ÉTEINT**
```
PC1 ←→ PC3
  ↑      ↑
Principal Caisse
Multi-Agences Agence 2
```

#### **Fonctionnement :**
- ✅ **PC1** : Fonctionne, accès à l'agence 2
- ✅ **PC3** : Fonctionne, synchronise avec PC1
- ❌ **PC2** : Éteint, pas de données agence 1
- ✅ **Continuité** : Service maintenu sur PC1 et PC3

### **SCÉNARIO 4 : PC3 ÉTEINT**
```
PC1 ←→ PC2
  ↑      ↑
Principal Caisse
Multi-Agences Agence 1
```

#### **Fonctionnement :**
- ✅ **PC1** : Fonctionne, accès à l'agence 1
- ✅ **PC2** : Fonctionne, synchronise avec PC1
- ❌ **PC3** : Éteint, pas de données agence 2
- ✅ **Continuité** : Service maintenu sur PC1 et PC2

---

## 🔧 DÉPANNAGE

### **PROBLÈME 1 : CONNEXION RÉSEAU**

#### **Symptômes :**
- ❌ Ping échoue
- ❌ Synchronisation ne fonctionne pas
- ❌ Erreur de connexion

#### **Solutions :**
```bash
# Vérifier les câbles
# Vérifier le routeur
# Vérifier les IPs
ipconfig

# Tester la connectivité
ping 192.168.1.101
ping 192.168.1.102
```

### **PROBLÈME 2 : DÉPENDANCES MANQUANTES**

#### **Symptômes :**
- ❌ Erreur Python
- ❌ Modules non trouvés
- ❌ ERP ne démarre pas

#### **Solutions :**
```bash
# Réinstaller les dépendances
INSTALLER_DEPENDANCES_ERP.bat

# Vérifier Python
py --version

# Vérifier les modules
py -c "import openpyxl; import reportlab; import django"
```

### **PROBLÈME 3 : SYNCHRONISATION LENTE**

#### **Symptômes :**
- ⏰ Synchronisation lente
- ⏰ Délais importants
- ⏰ Timeout

#### **Solutions :**
```bash
# Modifier erp_sync/erp_launcher_config.json
{
    "sync_interval": 60,  # Augmenter l'intervalle
    "timeout": 30,        # Augmenter le timeout
    "max_retries": 5      # Augmenter les tentatives
}
```

### **PROBLÈME 4 : CONFLITS DE DONNÉES**

#### **Symptômes :**
- ❌ Données incohérentes
- ❌ Erreurs de synchronisation
- ❌ Perte de données

#### **Solutions :**
```bash
# Redémarrer la synchronisation
GESTIONNAIRE_SYNC.bat
# Choisir "4" - Redémarrer

# Vérifier les logs
type erp_sync\sync_log.txt

# Restaurer depuis la sauvegarde
```

---

## 🔄 MAINTENANCE

### **ÉTAPE 8 : MAINTENANCE QUOTIDIENNE**

#### **8.1 Vérifications quotidiennes :**
```bash
# Sur chaque PC, vérifier que la synchronisation est active
GESTIONNAIRE_SYNC.bat
# Choisir "3" - Voir le statut

# Vérifier les logs d'erreur
type erp_sync\sync_log.txt

# Vérifier que les sauvegardes sont à jour
dir erp_sync\backups\
```

#### **8.2 Nettoyage :**
```bash
# Nettoyer les logs anciens
del erp_sync\sync_log.txt

# Nettoyer les sauvegardes anciennes
forfiles /p erp_sync\backups\ /s /m *.* /d -30 /c "cmd /c del @path"
```

### **ÉTAPE 9 : OPTIMISATION**

#### **9.1 Optimiser les performances :**
```bash
# Modifier erp_sync/erp_launcher_config.json
{
    "sync_interval": 30,   # Synchronisation plus fréquente
    "batch_size": 50,      # Traiter par lots plus petits
    "compression": true,   # Compresser les données
    "timeout": 15          # Timeout plus court
}
```

#### **9.2 Sécurité :**
```bash
# Changer les mots de passe par défaut
# Configurer un firewall
# Limiter l'accès réseau
# Chiffrer les communications
```

---

## 📊 MONITORING

### **ÉTAPE 10 : SURVEILLANCE**

#### **10.1 Surveillance automatique :**
```bash
# Créer un script de surveillance sur chaque PC
@echo off
echo Surveillance ERP...
GESTIONNAIRE_SYNC.bat
# Choisir "3" - Voir le statut
pause
```

#### **10.2 Alertes :**
```bash
# Configurer des alertes en cas de problème
# Surveiller les logs
# Vérifier la connectivité
# Tester la synchronisation
```

---

## 🎯 RÉSUMÉ DES ÉTAPES

### **ORDRE DE CONFIGURATION :**

1. **🔌 Connexion physique** - Câbles réseau
2. **🌐 Obtenir les IPs** - Avec OBTENIR_IP.bat
3. **📦 Installation dépendances** - Sur tous les PC
4. **⚙️ Configuration PC1** - Principal + Accès multi-agences
5. **🔗 Configuration PC2** - Caisse Agence 1
6. **🔗 Configuration PC3** - Caisse Agence 2
7. **🧪 Test complet** - Vérifier le fonctionnement
8. **🔧 Dépannage** - Résoudre les problèmes
9. **🔄 Maintenance** - Surveillance quotidienne

### **FICHIERS IMPORTANTS :**

- `ERP_Launcher.bat` - Lanceur principal
- `GESTIONNAIRE_SYNC.bat` - Gestionnaire de synchronisation
- `INSTALLER_DEPENDANCES_ERP.bat` - Installation des dépendances
- `OBTENIR_IP.bat` - Obtenir l'IP du PC
- `erp_sync/erp_launcher_config.json` - Configuration réseau
- `erp_sync/sync_log.txt` - Logs de synchronisation

### **IPs SUGGÉRÉES :**

- **PC1 (Principal + Accès Multi-Agences)** : 192.168.1.100:8000
- **PC2 (Caisse Agence 1)** : 192.168.1.101:8000
- **PC3 (Caisse Agence 2)** : 192.168.1.102:8000

---

## 🚀 CONCLUSION

Ce guide vous permet de configurer une synchronisation ERP distribuée avec accès multi-agences sur vos 3 PC. Chaque PC peut fonctionner seul, même si les autres sont éteints, tout en maintenant la synchronisation et l'accès multi-agences quand tous sont allumés.

**En cas de problème, consultez la section Dépannage ou contactez le support.**

---

## 📞 SUPPORT

Pour toute question ou problème :
1. Consultez la section Dépannage
2. Vérifiez les logs dans `erp_sync/sync_log.txt`
3. Testez la connectivité réseau
4. Redémarrez la synchronisation

**Bonne configuration ! 🎉**

