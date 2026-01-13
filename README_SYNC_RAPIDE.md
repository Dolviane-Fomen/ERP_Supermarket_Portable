# 🔄 Synchronisation Rapide Local ↔ En ligne

## ⚡ Méthode la Plus Simple (Interface Web)

### 📥 Télécharger depuis le serveur en ligne → Local

1. **Sur le serveur en ligne** :
   - Aller sur : `https://VOTRE-DOMAINE.com/supermarket/export-import/`
   - Cliquer sur "Télécharger l'Export"
   - Télécharger le fichier JSON

2. **Sur votre PC local** :
   - Démarrer : `python manage.py runserver`
   - Aller sur : `http://127.0.0.1:8000/supermarket/export-import/`
   - Cliquer sur "Importer des Données"
   - Sélectionner le fichier JSON téléchargé
   - ⚠️ **Décocher** "Supprimer les données existantes" pour fusionner
   - Cliquer sur "Importer les Données"

### 📤 Envoyer depuis Local → Serveur en ligne

1. **Sur votre PC local** :
   - Aller sur : `http://127.0.0.1:8000/supermarket/export-import/`
   - Cliquer sur "Télécharger l'Export"
   - Télécharger le fichier JSON

2. **Sur le serveur en ligne** :
   - Aller sur : `https://VOTRE-DOMAINE.com/supermarket/export-import/`
   - Cliquer sur "Importer des Données"
   - Sélectionner le fichier JSON téléchargé
   - ⚠️ **Décocher** "Supprimer les données existantes" pour fusionner
   - Cliquer sur "Importer les Données"

---

## 🚀 Méthode Automatisée (Ligne de commande)

### Configuration Initiale

1. **Créer un fichier de configuration** `sync_config.json` :
   ```json
   {
     "server_host": "123.45.67.89",
     "server_user": "erpuser",
     "server_path": "/home/erpuser/ERP_Supermarket_Portable",
     "local_path": "C:\\django erp\\ERP_Supermarket_Portable"
   }
   ```

2. **Configurer SSH** (pour que le script fonctionne) :
   - Générer une clé SSH : `ssh-keygen`
   - Copier la clé vers le serveur : `ssh-copy-id erpuser@VOTRE_IP`

### Utilisation

**Télécharger depuis le serveur :**
```powershell
python SYNC_LOCAL_ONLINE.py --mode pull --merge --config sync_config.json
```

**Envoyer vers le serveur :**
```powershell
python SYNC_LOCAL_ONLINE.py --mode push --merge --config sync_config.json
```

**Synchronisation bidirectionnelle :**
```powershell
python SYNC_LOCAL_ONLINE.py --mode sync --merge --config sync_config.json
```

**Ou utiliser le script batch :**
```batch
SYNC_LOCAL_ONLINE.bat pull   # Télécharger
SYNC_LOCAL_ONLINE.bat push   # Envoyer
SYNC_LOCAL_ONLINE.bat sync   # Bidirectionnel
```

---

## ⚠️ Important

- ✅ **Toujours faire une sauvegarde** avant l'import
- ✅ Utiliser `--merge` pour **fusionner** les données (évite la suppression)
- ❌ Sans `--merge`, les données existantes seront **supprimées**
- 🔒 Les **mots de passe** ne sont pas exportés (reconfiguration nécessaire après import)

---

## 📚 Documentation Complète

Pour plus de détails, voir : `GUIDE_SYNCHRONISATION_LOCAL_ONLINE.md`




