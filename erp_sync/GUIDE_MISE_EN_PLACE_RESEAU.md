# Guide Détaillé : Mise en Place de la Synchronisation Réseau Local

## 📋 Vue d'ensemble

Ce guide explique comment configurer la synchronisation automatique entre deux PC (ou plus) sur un réseau local. Chaque PC fonctionne de manière autonome, mais les données sont synchronisées automatiquement en arrière-plan.

**Principe :**
- Chaque PC exporte ses données vers un dossier partagé
- Chaque PC importe automatiquement les données des autres PC
- La synchronisation se fait toutes les 5 minutes (configurable)
- Aucune intervention utilisateur nécessaire

---

## 🔧 ÉTAPE 1 : Vérifier la Connexion Réseau

### 1.1 Vérifier que les PC sont sur le même réseau

**Sur chaque PC :**

1. Appuyez sur `Windows + R`
2. Tapez `cmd` et appuyez sur Entrée
3. Dans la fenêtre noire, tapez :
   ```
   ipconfig
   ```
4. Notez l'**Adresse IPv4** de chaque PC (exemple : `192.168.1.10` et `192.168.1.11`)
5. Vérifiez que les deux adresses commencent par les mêmes 3 nombres (ex: `192.168.1.xxx`)

**✅ Vérification :** Les deux PC doivent avoir des adresses IP sur le même réseau.

### 1.2 Vérifier que les PC peuvent se voir

**Sur le PC 1 :**

1. Ouvrez l'explorateur Windows
2. Dans la barre d'adresse, tapez : `\\IP_DU_PC2` (remplacez par l'IP du PC 2)
   - Exemple : `\\192.168.1.11`
3. Appuyez sur Entrée
4. Si une fenêtre s'ouvre (même vide), c'est bon ✅
5. Si une erreur apparaît, voir la section "Dépannage" à la fin

**Répétez la même opération sur le PC 2** en utilisant l'IP du PC 1.

### 1.3 Noter les noms des PC

**Sur chaque PC :**

1. Clic droit sur "Ce PC" (ou "Poste de travail")
2. Cliquez sur "Propriétés"
3. Notez le **Nom de l'ordinateur** (exemple : `CAISSE01`, `COMPTA01`)

**✅ Vous devez avoir noté :**
- IP du PC 1 : `_____________`
- Nom du PC 1 : `_____________`
- IP du PC 2 : `_____________`
- Nom du PC 2 : `_____________`

---

## 📁 ÉTAPE 2 : Créer les Dossiers de Synchronisation

### 2.1 Exécuter le script d'initialisation

**Sur chaque PC :**

1. Naviguez vers le dossier de l'ERP : `C:\django erp\ERP_Supermarket_Portable`
2. Double-cliquez sur : `erp_sync\INIT_SYNC_ENV.bat`
3. Une fenêtre noire s'ouvre et crée les dossiers automatiquement
4. Attendez le message "✅ Dossiers créés avec succès !"
5. Appuyez sur une touche pour fermer

**✅ Vérification :** Vérifiez que le dossier `C:\erp_sync` existe avec ces sous-dossiers :
- `entrant` (pour recevoir les fichiers)
- `sortant` (pour envoyer les fichiers)
- `archive` (pour sauvegarder les anciens fichiers)
- `logs` (pour les journaux de synchronisation)

---

## 🔐 ÉTAPE 3 : Partager les Dossiers sur le Réseau

### 3.1 Partager le dossier C:\erp_sync

**Sur chaque PC (répétez pour PC 1 et PC 2) :**

#### Méthode 1 : Partage Simple (Recommandé)

1. Ouvrez l'explorateur Windows
2. Naviguez vers `C:\`
3. **Clic droit** sur le dossier `erp_sync`
4. Cliquez sur **"Donner l'accès à"** → **"Personnes spécifiques..."**
5. Dans la liste déroulante, sélectionnez **"Tout le monde"**
6. Cliquez sur **"Ajouter"**
7. À droite de "Tout le monde", dans la colonne "Niveau d'autorisation", cliquez et sélectionnez **"Lecture/Écriture"**
8. Cliquez sur **"Partager"**
9. **Notez le chemin réseau affiché** (exemple : `\\CAISSE01\erp_sync`)
10. Cliquez sur **"Terminé"**

#### Méthode 2 : Partage Avancé (Si la méthode 1 ne fonctionne pas)

1. **Clic droit** sur `C:\erp_sync`
2. Cliquez sur **"Propriétés"**
3. Allez dans l'onglet **"Partage"**
4. Cliquez sur **"Partage avancé..."**
5. Cochez **"Partager ce dossier"**
6. Cliquez sur **"Autorisations"**
7. Sélectionnez **"Tout le monde"**
8. Cochez **"Contrôle total"** (ou au minimum "Modifier")
9. Cliquez sur **"OK"** deux fois
10. Notez le chemin réseau (exemple : `\\CAISSE01\erp_sync`)

### 3.2 Vérifier le partage

**Sur le PC 1 :**

1. Ouvrez l'explorateur Windows
2. Dans la barre d'adresse, tapez : `\\NOM_DU_PC2\erp_sync`
   - Exemple : `\\COMPTA01\erp_sync`
3. Appuyez sur Entrée
4. Vous devriez voir les dossiers `entrant`, `sortant`, `archive`, `logs`
5. Essayez de créer un fichier test (clic droit → Nouveau → Document texte)
6. Si ça fonctionne, supprimez le fichier test

**Répétez sur le PC 2** avec le nom du PC 1.

**✅ Vérification :** Vous devez pouvoir accéder au dossier partagé de l'autre PC et y créer/supprimer des fichiers.

---

## ⚙️ ÉTAPE 4 : Configurer le Fichier de Configuration

### 4.1 Identifier l'ID de l'Agence

**Sur chaque PC :**

1. Démarrez l'ERP (double-cliquez sur `ERP_Launcher.bat`)
2. Connectez-vous à l'interface web
3. Allez dans la section "Gestion des Agences" ou "Paramètres"
4. Notez l'**ID de l'agence** de ce PC (exemple : `8` pour MARCHE ESSOS, `7` pour MARCHE HUITIEME)

**✅ Vous devez avoir noté :**
- ID Agence PC 1 : `_____________`
- ID Agence PC 2 : `_____________`

### 4.2 Configurer avec le script automatique (Recommandé)

**Sur le PC 1 :**

1. Naviguez vers : `C:\django erp\ERP_Supermarket_Portable\erp_sync`
2. Double-cliquez sur : `CONFIG_SYNC.bat`
3. Répondez aux questions :
   - **Nom de ce PC :** Tapez le nom exact du PC (ex: `CAISSE01`)
   - **ID de l'agence :** Tapez l'ID noté précédemment (ex: `8`)
   - **Chemin réseau du PC partenaire :** Tapez le chemin UNC (ex: `\\COMPTA01\erp_sync`)
   - Si vous avez plusieurs PC partenaires, vous pourrez les ajouter après
4. Le script affiche "✅ Configuration mise à jour avec succès !"

**Répétez sur le PC 2** avec les informations du PC 2.

### 4.3 Vérifier la configuration

**Sur chaque PC :**

1. Ouvrez le fichier : `erp_sync\erp_launcher_config.json`
2. Vérifiez qu'il y a une section avec le nom de votre PC
3. Vérifiez que `agence_id` correspond à votre agence
4. Vérifiez que `remote_targets` contient le chemin vers l'autre PC

**Exemple de configuration correcte :**

```json
{
  "machines": {
    "CAISSE01": {
      "agence_id": 8,
      "local_sync_dir": "C:/erp_sync",
      "remote_targets": [
        {
          "name": "COMPTA01",
          "path": "\\\\COMPTA01\\erp_sync"
        }
      ]
    },
    "COMPTA01": {
      "agence_id": 7,
      "local_sync_dir": "C:/erp_sync",
      "remote_targets": [
        {
          "name": "CAISSE01",
          "path": "\\\\CAISSE01\\erp_sync"
        }
      ]
    }
  },
  "default": {
    "sync_interval": 300,
    "max_retries": 3
  }
}
```

**✅ Vérification :** Chaque PC doit avoir sa propre entrée dans `machines` avec le bon `agence_id` et le bon chemin vers l'autre PC.

---

## 🚀 ÉTAPE 5 : Démarrer la Synchronisation

### 5.1 Démarrer l'ERP sur chaque PC

**Sur chaque PC :**

1. Naviguez vers : `C:\django erp\ERP_Supermarket_Portable`
2. Double-cliquez sur : `ERP_Launcher.bat`
3. L'ERP démarre normalement (serveur Django + navigateur)
4. **La synchronisation démarre automatiquement en arrière-plan** ✅

**Aucune action supplémentaire n'est nécessaire !**

### 5.2 Vérifier que la synchronisation fonctionne

**Sur chaque PC :**

1. Attendez 5-10 minutes après le démarrage
2. Ouvrez le fichier : `C:\erp_sync\logs\sync.log`
3. Vous devriez voir des lignes comme :
   ```
   [2025-11-20 10:30:15] 🔄 Synchronisation démarrée pour CAISSE01
   [2025-11-20 10:30:16] 📤 Export des données de l'agence 8...
   [2025-11-20 10:30:18] ✅ Export réussi : export_CAISSE01_20251120_103018.json
   [2025-11-20 10:30:19] 📥 Import des données depuis COMPTA01...
   [2025-11-20 10:30:25] ✅ Import réussi : 15 factures, 120 articles
   ```

**✅ Vérification :** Le log doit montrer des exports et imports réussis toutes les 5 minutes.

### 5.3 Test manuel de synchronisation

**Sur le PC 1 (Caisse) :**

1. Créez une facture de test dans l'ERP
2. Attendez 5-10 minutes
3. Vérifiez dans `C:\erp_sync\sortant` qu'un fichier JSON a été créé
4. Vérifiez dans `C:\erp_sync\logs\sync.log` que l'export a réussi

**Sur le PC 2 (Comptable) :**

1. Attendez 5-10 minutes après la création de la facture sur le PC 1
2. Vérifiez dans `C:\erp_sync\entrant` qu'un fichier JSON est arrivé
3. Vérifiez dans `C:\erp_sync\logs\sync.log` que l'import a réussi
4. Dans l'ERP, vérifiez que la facture de test apparaît bien

**✅ Vérification :** Les données créées sur un PC doivent apparaître sur l'autre PC après quelques minutes.

---

## 🔍 ÉTAPE 6 : Vérification et Dépannage

### 6.1 Vérifications courantes

**Problème : Les fichiers ne se synchronisent pas**

1. Vérifiez que les deux PC sont allumés et connectés au réseau
2. Vérifiez que le partage réseau fonctionne (voir étape 3.2)
3. Vérifiez le fichier `C:\erp_sync\logs\sync.log` pour voir les erreurs
4. Vérifiez que `ERP_Launcher.bat` est bien lancé (la synchronisation ne fonctionne que si l'ERP est démarré)

**Problème : Erreur "Accès refusé" lors du partage**

1. Vérifiez que le pare-feu Windows n'bloque pas le partage de fichiers
2. Allez dans "Panneau de configuration" → "Pare-feu Windows" → "Autoriser une application"
3. Cochez "Partage de fichiers et d'imprimantes"
4. Redémarrez les deux PC

**Problème : Les données ne s'importent pas correctement**

1. Vérifiez que l'ID d'agence dans `erp_launcher_config.json` est correct
2. Vérifiez le log `C:\erp_sync\logs\sync.log` pour voir les erreurs d'import
3. Vérifiez que la base de données n'est pas verrouillée (fermez l'ERP et relancez-le)

**Problème : La synchronisation est trop lente**

1. Vérifiez la vitesse de connexion réseau entre les PC
2. Vérifiez que les fichiers JSON ne sont pas trop volumineux (vérifiez dans `C:\erp_sync\sortant`)
3. Vous pouvez augmenter l'intervalle de synchronisation dans `erp_launcher_config.json` (section `default` → `sync_interval`, en secondes)

### 6.2 Commandes de diagnostic

**Sur chaque PC, ouvrez une invite de commande (cmd) et exécutez :**

```cmd
:: Vérifier que les dossiers existent
dir C:\erp_sync

:: Vérifier que le partage est accessible
net share

:: Tester la connexion à l'autre PC
ping NOM_DU_PC_AUTRE
```

### 6.3 Réinitialiser la synchronisation

Si vous devez tout recommencer :

1. Arrêtez l'ERP sur tous les PC
2. Supprimez le dossier `C:\erp_sync` sur tous les PC
3. Relancez `INIT_SYNC_ENV.bat` sur tous les PC
4. Reconfigurez les partages (étape 3)
5. Reconfigurez `erp_launcher_config.json` (étape 4)
6. Redémarrez l'ERP sur tous les PC

---

## 📝 RÉSUMÉ DES ÉTAPES

1. ✅ Vérifier que les PC sont sur le même réseau
2. ✅ Noter les noms et IP des PC
3. ✅ Exécuter `INIT_SYNC_ENV.bat` sur chaque PC
4. ✅ Partager `C:\erp_sync` sur chaque PC
5. ✅ Vérifier l'accès au partage réseau
6. ✅ Configurer `erp_launcher_config.json` avec `CONFIG_SYNC.bat`
7. ✅ Démarrer l'ERP avec `ERP_Launcher.bat`
8. ✅ Vérifier les logs de synchronisation

---

## 🎯 Fonctionnement Final

Une fois tout configuré :

- **Chaque PC fonctionne de manière autonome** (même si l'autre est éteint)
- **Toutes les 5 minutes**, chaque PC :
  - Exporte ses données vers le dossier partagé de l'autre PC
  - Importe les données du dossier partagé de l'autre PC
- **Les utilisateurs ne voient rien** : tout se passe en arrière-plan
- **Les données sont toujours à jour** : dès qu'un PC se reconnecte, la synchronisation reprend automatiquement

**C'est tout ! La synchronisation est maintenant opérationnelle.** 🎉








