# Guide d'Export/Import des Données ERP

Ce guide explique comment migrer les données d'une ancienne version vers une nouvelle version du système ERP.

## 📋 Prérequis

- Python installé
- Accès à la base de données de l'ancienne version
- Nouvelle version avec fonctionnalité export/import installée

## 🔄 Processus de Migration

### Étape 1: Export depuis l'Ancienne Version

Si votre ancienne version **n'a pas** la fonctionnalité d'export/import dans l'interface web :

1. **Copier le script d'export** :
   - Copiez le fichier `EXPORT_DONNEES_STANDALONE.py` dans le répertoire de votre ancienne version

2. **Exécuter le script** :
   ```bash
   python EXPORT_DONNEES_STANDALONE.py
   ```

3. **Vérifier le fichier généré** :
   - Le script va créer un fichier `export_erp_standalone_YYYYMMDD_HHMMSS.json`
   - Ce fichier contient toutes vos données

### Étape 2: Import dans la Nouvelle Version

Si votre nouvelle version **a** la fonctionnalité d'export/import :

1. **Démarrer le serveur** de la nouvelle version :
   ```bash
   python manage.py runserver
   ```

2. **Accéder à la page d'export/import** :
   - Ouvrir votre navigateur
   - Aller sur : `http://127.0.0.1:8000/supermarket/export-import/`

3. **Importer les données** :
   - Cliquer sur "Importer des Données"
   - Sélectionner le fichier JSON exporté
   - Choisir les options :
     - ✅ Cocher "Supprimer les données existantes" si vous voulez remplacer toutes les données
     - ⚠️ **ATTENTION** : Cette action est irréversible !
   - Cliquer sur "Importer les Données"

4. **Vérifier l'import** :
   - Le système affichera un résumé de l'import
   - Vérifiez que toutes les données ont été importées correctement

## 🔧 Utilisation Alternative : Export depuis l'Interface Web

Si votre version **a déjà** la fonctionnalité d'export/import :

1. **Se connecter** à l'interface web
2. **Aller sur** `/supermarket/export-import/`
3. **Cliquer sur** "Télécharger l'Export"
4. Le fichier JSON sera téléchargé automatiquement

## ⚠️ Notes Importantes

### Sécurité des Données

- **Faites toujours une sauvegarde** de votre base de données avant l'import
- Les **mots de passe des utilisateurs ne sont pas exportés** pour des raisons de sécurité
- Vous devrez **recréer les comptes utilisateurs** manuellement après l'import

### Compatibilité

- Le fichier d'export est au format JSON et peut être ouvert avec n'importe quel éditeur de texte
- Les IDs des enregistrements peuvent changer lors de l'import
- Les relations entre les données sont préservées

### Données Exportées

Le script exporte :
- ✅ Agences et configurations
- ✅ Familles d'articles
- ✅ Articles et stocks
- ✅ Clients et fournisseurs
- ✅ Factures (vente, achat, transfert)
- ✅ Mouvements de stock
- ✅ Caisses et sessions de caisse
- ✅ Comptes utilisateurs (sans mots de passe)

## 🐛 Résolution de Problèmes

### Erreur lors de l'export

Si vous obtenez une erreur lors de l'exécution du script :
1. Vérifiez que vous êtes dans le bon répertoire
2. Vérifiez que Django est correctement configuré
3. Vérifiez que la base de données est accessible

### Erreur lors de l'import

Si l'import échoue :
1. Vérifiez que le fichier JSON est valide
2. Vérifiez les permissions de la base de données
3. Consultez les messages d'erreur affichés
4. Vérifiez que toutes les agences et familles existent avant d'importer les articles

## 📞 Support

En cas de problème, vérifiez :
- Les logs du serveur Django
- Les messages d'erreur dans l'interface
- La console du navigateur (F12)

---

**Date de création** : 2025-11-18  
**Version** : 1.0




