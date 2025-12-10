# Guide Rapide : Configuration Synchronisation Réseau

## 🎯 Objectif
Synchroniser automatiquement les données ERP entre plusieurs PC sur le réseau local (toutes les 5 minutes).

---

## ✅ Étapes Essentielles

### 1️⃣ Vérifier le Réseau
**Sur chaque PC :**
- `Windows + R` → `cmd` → `ipconfig`
- Noter l'**IP** et le **Nom du PC**
- Tester l'accès : Explorateur → `\\IP_DU_PC2` (doit s'ouvrir)

### 2️⃣ Créer les Dossiers
**Sur chaque PC :**
- Double-cliquer : `erp_sync\INIT_SYNC_ENV.bat`
- Vérifier que `C:\erp_sync` existe avec 4 sous-dossiers

### 3️⃣ Partager le Dossier
**Sur chaque PC :**
- Clic droit sur `C:\erp_sync` → **"Donner l'accès à"** → **"Personnes spécifiques..."**
- Sélectionner **"Tout le monde"** → **"Ajouter"** → **"Lecture/Écriture"** → **"Partager"**
- Noter le chemin réseau (ex: `\\CAISSE01\erp_sync`)
- Vérifier : Explorateur → `\\NOM_PC2\erp_sync` (doit être accessible)

### 4️⃣ Configurer
**Sur chaque PC :**
- Lancer l'ERP → Noter l'**ID de l'agence**
- Double-cliquer : `erp_sync\CONFIG_SYNC.bat`
- Répondre aux questions :
  - Nom du PC (ex: `CAISSE01`)
  - ID de l'agence (ex: `8`)
  - Chemin réseau partenaire (ex: `\\COMPTA01\erp_sync`)

### 5️⃣ Démarrer
**Sur chaque PC :**
- Double-cliquer : `ERP_Launcher.bat`
- ✅ La synchronisation démarre automatiquement

### 6️⃣ Vérifier
**Sur chaque PC :**
- Attendre 5-10 minutes
- Ouvrir : `C:\erp_sync\logs\sync.log`
- Vérifier les messages "✅ Export réussi" et "✅ Import réussi"

---

## 🔧 Dépannage Rapide

| Problème | Solution |
|----------|----------|
| Les PC ne se voient pas | Vérifier le pare-feu Windows → Autoriser "Partage de fichiers" |
| Erreur "Accès refusé" | Vérifier les permissions du partage (Lecture/Écriture) |
| Pas de synchronisation | Vérifier que `ERP_Launcher.bat` est lancé |
| Erreurs dans les logs | Vérifier l'ID d'agence dans `erp_launcher_config.json` |

---

## 📋 Checklist Finale

- [ ] Les PC sont sur le même réseau (même plage IP)
- [ ] Les PC peuvent accéder aux dossiers partagés
- [ ] `C:\erp_sync` existe sur chaque PC
- [ ] Le dossier est partagé avec "Tout le monde" (Lecture/Écriture)
- [ ] `CONFIG_SYNC.bat` a été exécuté sur chaque PC
- [ ] `erp_launcher_config.json` contient les bonnes informations
- [ ] `ERP_Launcher.bat` est lancé sur chaque PC
- [ ] Les logs montrent des synchronisations réussies

---

## 💡 Notes Importantes

- **Chaque PC fonctionne de manière autonome** (même si l'autre est éteint)
- **Synchronisation automatique** : toutes les 5 minutes en arrière-plan
- **Aucune intervention utilisateur** nécessaire après la configuration
- **Les données sont toujours à jour** : synchronisation automatique au redémarrage

---

**✅ C'est tout ! La synchronisation est opérationnelle.**

