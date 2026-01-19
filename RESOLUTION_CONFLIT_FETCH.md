# 🔧 Résolution du problème de Fetch - Conflit avec db_erp.sqlite3

## ❌ Problème
Le fetch ne fonctionne pas car il y a un conflit de merge avec le fichier `db_erp.sqlite3`.

## ✅ Solution étape par étape

### Étape 1 : Annuler le merge en cours
Dans GitHub Desktop :
1. Dans la boîte de dialogue "Resolve conflicts before Merge"
2. Cliquez sur **"Abort merge"**
3. Cela annule le merge et vous permet de continuer

### Étape 2 : Retirer db_erp.sqlite3 du suivi Git

**Option A : Via GitHub Desktop (Recommandé)**
1. Allez dans l'onglet "Changes"
2. Si `db_erp.sqlite3` apparaît, **décochez-le** (ne le commitez pas)
3. Le fichier est déjà dans `.gitignore`, donc il ne devrait pas apparaître

**Option B : Via script (si Git est installé)**
1. Double-cliquez sur `retirer_db_erp_git.bat`
2. Le script retire automatiquement le fichier du suivi Git

**Option C : Manuellement (si vous avez Git en ligne de commande)**
```bash
git rm --cached db_erp.sqlite3
git commit -m "Retirer db_erp.sqlite3 du suivi Git"
```

### Étape 3 : Faire le fetch normalement
1. Dans GitHub Desktop, cliquez sur **"Pull origin"** → **"Fetch origin"**
2. Le fetch devrait maintenant fonctionner sans conflit

### Étape 4 : Faire un pull (si nécessaire)
1. Après le fetch, cliquez sur **"Pull origin"**
2. Si tout est OK, les modifications seront récupérées

## 📝 Pourquoi ce problème ?

- `db_erp.sqlite3` est un fichier de base de données SQLite
- Il est déjà dans `.gitignore` (ligne 63)
- Mais il a probablement été ajouté à Git **avant** d'être ajouté au `.gitignore`
- Git continue donc à le suivre, même s'il est dans `.gitignore`
- La solution : le retirer explicitement du suivi Git avec `git rm --cached`

## ⚠️ Important

- Le fichier `db_erp.sqlite3` restera sur votre ordinateur
- Il ne sera juste plus suivi par Git
- C'est normal et souhaitable pour un fichier de base de données

## 🔄 Après résolution

Une fois le conflit résolu :
1. Vous pourrez faire des fetch/pull normalement
2. Le fichier `db_erp.sqlite3` ne causera plus de problèmes
3. Vos modifications de code pourront être synchronisées sans problème
