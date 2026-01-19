# Liste des Fichiers de Synchronisation - Base de Données Locale ↔ En Ligne

Ce document liste tous les fichiers créés pour synchroniser les données de la base de données locale avec celle hébergée en ligne.

---

## 📁 FICHIERS PRINCIPAUX DE SYNCHRONISATION

### 🔄 Scripts Python de Synchronisation

#### 1. **SYNC_LOCAL_ONLINE.py**
- **Description** : Script principal de synchronisation entre environnement local et serveur en ligne
- **Fonctionnalités** :
  - Synchronisation bidirectionnelle (pull/push/sync)
  - Sauvegarde automatique avant synchronisation
  - Export/Import des données
  - Support SSH/SCP pour transfert
- **Usage** : `python SYNC_LOCAL_ONLINE.py --mode [pull|push|sync]`
- **Fichier associé** : `SYNC_LOCAL_ONLINE.bat`

#### 2. **SYNC_DATA.py**
- **Description** : Script de synchronisation des données ERP avec autres PC sur le réseau
- **Fonctionnalités** :
  - Synchronisation via réseau local
  - Communication HTTP entre PC
  - Configuration via `sync_data/network_config.json`
- **Usage** : `python SYNC_DATA.py`
- **Emplacement** : Racine du projet

#### 3. **ERP_LAUNCHER_SYNC.py**
- **Description** : Service de synchronisation automatique pour ERP_Launcher
- **Fonctionnalités** :
  - Synchronisation automatique à intervalles réguliers
  - Chaque PC garde sa base locale
  - Export vers dossier partagé
  - Import depuis autres PC
  - Configuration via `erp_sync/erp_launcher_config.json`
- **Usage** : Démarre automatiquement avec ERP_Launcher.bat
- **Intervalle par défaut** : 300 secondes (5 minutes)

#### 4. **CONFIGURER_SYNC_DISTRIBUE.py**
- **Description** : Script de configuration pour ERP distribué avec synchronisation
- **Fonctionnalités** :
  - Création du système de synchronisation
  - Configuration réseau multi-PC
  - Génération des scripts de synchronisation
  - Configuration des dossiers de sync
- **Usage** : `python CONFIGURER_SYNC_DISTRIBUE.py`

#### 5. **CONFIGURER_SYNC_ERP_LAUNCHER.py**
- **Description** : Configuration de la synchronisation pour ERP_Launcher
- **Fonctionnalités** :
  - Configuration du système de sync ERP_Launcher
  - Paramétrage des intervalles
  - Configuration des chemins
- **Usage** : `python CONFIGURER_SYNC_ERP_LAUNCHER.py`

---

### 🪟 Scripts Batch (.bat) de Synchronisation

#### 6. **SYNC_LOCAL_ONLINE.bat**
- **Description** : Wrapper batch pour SYNC_LOCAL_ONLINE.py
- **Modes** :
  - `pull` : Télécharger depuis le serveur en ligne
  - `push` : Envoyer vers le serveur en ligne
  - `sync` : Synchronisation bidirectionnelle
- **Usage** : `SYNC_LOCAL_ONLINE.bat [pull|push|sync]`

#### 7. **SYNC_DONNEES.bat**
- **Description** : Script de synchronisation des données
- **Usage** : `SYNC_DONNEES.bat`

#### 8. **SYNC_DONNEES_BIDIRECTIONNEL.bat**
- **Description** : Synchronisation bidirectionnelle des données (fusion sans remplacement)
- **Fonctionnalités** :
  - Export données locales
  - Export données depuis OVH
  - Fusion des deux (sans remplacement)
  - Synchronisation dans les deux sens
- **Usage** : `SYNC_DONNEES_BIDIRECTIONNEL.bat`
- **Fichier associé** : `sync_donnees_bidirectionnel.ps1`

#### 9. **SYNC_OVH.bat**
- **Description** : Script de synchronisation avec serveur OVH
- **Usage** : `SYNC_OVH.bat`
- **Fichier associé** : `sync_ovh.ps1` et `sync_data_ovh.ps1`

#### 10. **GESTIONNAIRE_SYNC.bat**
- **Description** : Gestionnaire de synchronisation ERP_Launcher avec menu interactif
- **Fonctionnalités** :
  - Démarrer ERP_Launcher avec/sans sync
  - Vérifier statut synchronisation
  - Tester connexions réseau
  - Arrêter synchronisation
  - Configuration réseau
  - Restaurer ERP_Launcher original
- **Usage** : `GESTIONNAIRE_SYNC.bat`

#### 11. **CREER_RACCOURCI_SYNC.bat**
- **Description** : Création de raccourcis pour les scripts de synchronisation
- **Usage** : `CREER_RACCOURCI_SYNC.bat`

---

### 🔷 Scripts PowerShell (.ps1) de Synchronisation

#### 12. **sync_donnees_bidirectionnel.ps1**
- **Description** : Script PowerShell pour synchronisation bidirectionnelle
- **Usage** : Appelé par `SYNC_DONNEES_BIDIRECTIONNEL.bat`

#### 13. **sync_data_ovh.ps1**
- **Description** : Script PowerShell pour synchronisation avec OVH
- **Usage** : Appelé par `SYNC_OVH.bat`

#### 14. **sync_ovh.ps1**
- **Description** : Script PowerShell pour synchronisation OVH (version alternative)
- **Usage** : `powershell -ExecutionPolicy Bypass -File sync_ovh.ps1`

---

## 📂 DOSSIERS DE SYNCHRONISATION

### 15. **erp_sync/**
Dossier contenant les fichiers de configuration et scripts pour la synchronisation ERP_Launcher :
- `CONFIG_SYNC.bat` : Configuration de synchronisation
- `CONFIG_SYNC.ps1` : Configuration PowerShell
- `INIT_SYNC_ENV.bat` : Initialisation de l'environnement de sync
- `erp_launcher_config.json` : Configuration JSON pour ERP_Launcher
- `DOCUMENTATION_SYNC.md` : Documentation de synchronisation
- `GUIDE_MISE_EN_PLACE_RESEAU.md` : Guide de mise en place réseau
- `GUIDE_RAPIDE_CONFIGURATION.md` : Guide rapide de configuration

### 16. **sync_data/**
Dossier contenant les fichiers de configuration pour la synchronisation réseau :
- `network_config.json` : Configuration réseau (liste des PC, IPs, ports)

### 17. **network_sync/**
Dossier contenant les fichiers de configuration réseau :
- `network_config.json` : Configuration réseau alternative

### 18. **syncro_ligne/**
Dossier contenant des scripts de synchronisation en ligne :
- `SYNC_DATA.py` : Script de synchronisation
- `SYNC_OVH.bat` : Script batch OVH
- `sync_ovh.ps1` : Script PowerShell OVH
- `sync_data_ovh.ps1` : Script PowerShell données OVH

---

## 📋 FICHIERS DE CONFIGURATION

### 19. **sync_config_example.json**
- **Description** : Exemple de fichier de configuration pour la synchronisation
- **Usage** : Modèle à copier et personnaliser

### 20. **sync_data/network_config.json**
- **Description** : Configuration réseau pour synchronisation multi-PC
- **Structure** :
  ```json
  {
    "pc_list": [
      {"name": "PC1", "ip": "192.168.1.100", "port": 8001},
      ...
    ],
    "sync_interval": 30,
    "last_sync": null
  }
  ```

### 21. **erp_sync/erp_launcher_config.json**
- **Description** : Configuration pour synchronisation ERP_Launcher
- **Contenu** : Paramètres de synchronisation, chemins, intervalles

---

## 🔧 FICHIERS D'EXPORT/IMPORT

### 22. **EXPORT_DONNEES_STANDALONE.py**
- **Description** : Export des données en mode standalone
- **Usage** : `python EXPORT_DONNEES_STANDALONE.py`

### 23. **EXPORTER_DONNEES.bat** / **EXPORTER_DONNEES_AVANCE.bat**
- **Description** : Scripts batch pour exporter les données
- **Usage** : `EXPORTER_DONNEES.bat`

---

## 📚 DOCUMENTATION ASSOCIÉE

### 24. **GUIDE_SYNCHRONISATION_LOCAL_ONLINE.md**
- **Description** : Guide complet de synchronisation local ↔ en ligne

### 25. **EXPLICATION_SYNCHRONISATION.md**
- **Description** : Explication du système de synchronisation

### 26. **README_SYNC_RAPIDE.md**
- **Description** : Guide rapide de synchronisation

---

## 🎯 RÉSUMÉ PAR TYPE DE SYNCHRONISATION

### Synchronisation Local ↔ En Ligne
- `SYNC_LOCAL_ONLINE.py` / `.bat`
- `SYNC_OVH.bat` / `sync_ovh.ps1`
- `sync_data_ovh.ps1`

### Synchronisation Réseau Local (Multi-PC)
- `SYNC_DATA.py`
- `ERP_LAUNCHER_SYNC.py`
- `CONFIGURER_SYNC_DISTRIBUE.py`
- `GESTIONNAIRE_SYNC.bat`

### Synchronisation Bidirectionnelle
- `SYNC_DONNEES_BIDIRECTIONNEL.bat`
- `sync_donnees_bidirectionnel.ps1`

### Configuration
- `CONFIGURER_SYNC_DISTRIBUE.py`
- `CONFIGURER_SYNC_ERP_LAUNCHER.py`
- `erp_sync/CONFIG_SYNC.bat` / `.ps1`
- `erp_sync/INIT_SYNC_ENV.bat`

---

## 🚀 UTILISATION RAPIDE

### Pour synchroniser Local ↔ En Ligne :
```bash
SYNC_LOCAL_ONLINE.bat pull   # Télécharger depuis serveur
SYNC_LOCAL_ONLINE.bat push   # Envoyer vers serveur
SYNC_LOCAL_ONLINE.bat sync   # Synchronisation bidirectionnelle
```

### Pour synchronisation réseau local :
```bash
GESTIONNAIRE_SYNC.bat        # Menu interactif
python ERP_LAUNCHER_SYNC.py  # Service de sync automatique
```

### Pour synchronisation bidirectionnelle :
```bash
SYNC_DONNEES_BIDIRECTIONNEL.bat
```

---

## 📝 NOTES IMPORTANTES

1. **Base de données** : Les fichiers `*.sqlite3` sont généralement exclus du versioning (dans `.gitignore`)
2. **Sauvegarde** : La plupart des scripts créent des sauvegardes avant synchronisation
3. **Configuration** : Vérifiez les fichiers de configuration JSON avant utilisation
4. **Réseau** : Pour la synchronisation réseau, assurez-vous que les PC sont accessibles
5. **Permissions** : Certains scripts PowerShell nécessitent `ExecutionPolicy Bypass`

---

*Dernière mise à jour : Généré automatiquement*
