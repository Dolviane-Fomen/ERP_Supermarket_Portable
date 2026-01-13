# Guide de Synchronisation Local ↔ En ligne

Ce guide explique comment synchroniser les données entre votre environnement local et le serveur en ligne.

## 📋 Méthodes de Synchronisation

### Méthode 1 : Via l'Interface Web (Recommandée)

#### Étape 1 : Exporter depuis le Serveur en ligne

1. **Se connecter au serveur en ligne** :
   - Ouvrir votre navigateur
   - Aller sur : `https://VOTRE-DOMAINE.com/supermarket/export-import/`

2. **Télécharger l'export** :
   - Cliquer sur "Télécharger l'Export"
   - Sélectionner l'agence si nécessaire
   - Le fichier JSON sera téléchargé (ex: `export_erp_MARCHE_HUITIEME_20250105_143022.json`)

#### Étape 2 : Importer dans l'environnement Local

1. **Démarrer votre serveur local** :
   ```powershell
   python manage.py runserver
   ```

2. **Accéder à la page d'import** :
   - Ouvrir : `http://127.0.0.1:8000/supermarket/export-import/`
   - Cliquer sur "Importer des Données"

3. **Sélectionner le fichier** :
   - Choisir le fichier JSON téléchargé depuis le serveur en ligne
   - ⚠️ **ATTENTION** : Décocher "Supprimer les données existantes" si vous voulez fusionner les données
   - Cocher uniquement si vous voulez remplacer complètement les données locales

4. **Confirmer l'import** :
   - Cliquer sur "Importer les Données"
   - Vérifier le résumé de l'import

---

### Méthode 2 : Via Django dumpdata/loaddata (Ligne de commande)

#### Étape 1 : Exporter depuis le Serveur en ligne (SSH)

```bash
# Se connecter au serveur
ssh erpuser@VOTRE_IP_SERVEUR

# Aller dans le répertoire du projet
cd /home/erpuser/ERP_Supermarket_Portable

# Activer l'environnement virtuel (si nécessaire)
source venv/bin/activate

# Exporter toutes les données
python manage.py dumpdata --settings=erp_project.settings_production > export_online.json

# OU exporter uniquement certaines apps
python manage.py dumpdata supermarket --settings=erp_project.settings_production > export_online.json

# OU exclure certaines données (sessions, logs)
python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry --settings=erp_project.settings_production > export_online.json
```

#### Étape 2 : Télécharger le fichier vers votre PC

**Option A : Via SCP (depuis PowerShell Windows)**
```powershell
scp erpuser@VOTRE_IP_SERVEUR:/home/erpuser/ERP_Supermarket_Portable/export_online.json .
```

**Option B : Via WinSCP (Interface graphique)**
1. Ouvrir WinSCP
2. Se connecter au serveur
3. Naviguer vers `/home/erpuser/ERP_Supermarket_Portable/`
4. Télécharger `export_online.json`

#### Étape 3 : Importer dans l'environnement Local

```powershell
# Aller dans le répertoire du projet
cd "C:\django erp\ERP_Supermarket_Portable"

# Faire une sauvegarde de la base locale (recommandé)
copy db_erp.sqlite3 db_erp_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sqlite3

# Importer les données
python manage.py loaddata export_online.json
```

---

### Méthode 3 : Synchronisation Bidirectionnelle (Fusion des données)

#### Script Automatisé : `SYNC_LOCAL_ONLINE.py`

Utilisez le script `SYNC_LOCAL_ONLINE.py` pour synchroniser automatiquement :

```powershell
python SYNC_LOCAL_ONLINE.py --mode pull    # Télécharger depuis en ligne
python SYNC_LOCAL_ONLINE.py --mode push    # Envoyer vers en ligne
python SYNC_LOCAL_ONLINE.py --mode sync    # Synchronisation bidirectionnelle
```

---

## 🔄 Workflow Recommandé

### Synchronisation Quotidienne (Pull : En ligne → Local)

```powershell
# 1. Télécharger l'export depuis le serveur en ligne via l'interface web
# 2. Sur votre PC local :
python manage.py loaddata export_online.json --merge
```

### Synchronisation des Modifications Locales (Push : Local → En ligne)

```powershell
# 1. Exporter depuis local
python manage.py dumpdata supermarket > export_local.json

# 2. Transférer vers le serveur (via SCP ou WinSCP)
scp export_local.json erpuser@VOTRE_IP_SERVEUR:/home/erpuser/ERP_Supermarket_Portable/

# 3. Sur le serveur, importer :
ssh erpuser@VOTRE_IP_SERVEUR
cd /home/erpuser/ERP_Supermarket_Portable
python manage.py loaddata export_local.json --merge --settings=erp_project.settings_production
```

---

## ⚠️ Points Importants

### 1. Sauvegarde Avant Synchronisation

**Toujours faire une sauvegarde avant l'import !**

**Sur Windows (local) :**
```powershell
copy db_erp.sqlite3 db_erp_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sqlite3
```

**Sur Linux (serveur) :**
```bash
pg_dump -U erp_user -d erp_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. Gestion des Conflits

- **IDs en conflit** : Django peut changer les IDs lors de l'import
- **Relations** : Les relations entre les données sont préservées
- **Utilisateurs** : Les mots de passe ne sont pas exportés pour des raisons de sécurité

### 3. Fusion vs Remplacement

- **`--merge`** : Fusionne les données (évite les doublons)
- **Sans `--merge`** : Remplace les données existantes (⚠️ supprime tout)

### 4. Données Non Exportées

Les données suivantes ne sont **PAS** exportées :
- ❌ Mots de passe des utilisateurs
- ❌ Sessions Django
- ❌ Logs d'administration
- ❌ Cache Django

---

## 🔧 Résolution de Problèmes

### Erreur : "No such table"

**Solution** : Exécuter les migrations avant l'import
```powershell
python manage.py migrate
```

### Erreur : "IntegrityError: UNIQUE constraint failed"

**Solution** : Utiliser `--merge` pour fusionner au lieu de remplacer
```powershell
python manage.py loaddata export_online.json --merge
```

### Erreur : "JSON decode error"

**Solution** : Vérifier que le fichier JSON est valide
```powershell
python -m json.tool export_online.json > nul
```

### Fichier trop volumineux

**Solution** : Exporter uniquement les données nécessaires
```powershell
# Exporter uniquement les commandes
python manage.py dumpdata supermarket.Commande supermarket.Client > export_commandes.json
```

---

## 📊 Comparaison des Méthodes

| Méthode | Avantages | Inconvénients | Quand l'utiliser |
|---------|-----------|---------------|------------------|
| **Interface Web** | ✅ Facile à utiliser<br>✅ Pas besoin de SSH<br>✅ Interface graphique | ❌ Nécessite un navigateur<br>❌ Limité par la taille du fichier | Synchronisation occasionnelle |
| **dumpdata/loaddata** | ✅ Automatisable<br>✅ Contrôle total<br>✅ Scripts personnalisables | ❌ Nécessite SSH<br>❌ Ligne de commande | Synchronisation régulière |
| **Script Automatisé** | ✅ Complètement automatique<br>✅ Bidirectionnel | ❌ Configuration initiale nécessaire | Synchronisation quotidienne |

---

## 🔐 Sécurité

### Transfert Sécurisé

- Utilisez **SCP** ou **WinSCP** avec **SSH** pour transférer les fichiers
- Ne partagez **jamais** les fichiers d'export par email non sécurisé
- Supprimez les fichiers d'export après utilisation

### Mots de Passe

- Les mots de passe ne sont **jamais** exportés
- Après l'import, vous devrez recréer les mots de passe des utilisateurs
- Utilisez `python manage.py changepassword USERNAME` pour réinitialiser

---

## 📞 Support

En cas de problème :
1. Vérifier les logs Django : `python manage.py runserver` (dans la console)
2. Vérifier les messages d'erreur dans l'interface web
3. Consulter les fichiers de sauvegarde si nécessaire

---

**Dernière mise à jour** : 2025-01-05




