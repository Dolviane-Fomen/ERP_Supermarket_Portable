# Guide de Résolution du Conflit Git - db_erp.sqlite3

## Problème
Le fichier `db_erp.sqlite3` (base de données SQLite) est en conflit lors d'un merge. Ce fichier ne devrait **PAS** être versionné dans Git car c'est une base de données locale.

## Solution : Résoudre le conflit dans GitHub Desktop

### Option 1 : Annuler le merge (Recommandé si vous n'avez pas besoin du merge)

1. Dans GitHub Desktop, dans la fenêtre "Resolve conflicts before Merge" :
   - Cliquez sur le bouton **"Abort merge"**
   - Cela annulera le merge en cours

2. Ensuite, retirez le fichier du suivi Git :
   - Ouvrez le terminal dans GitHub Desktop (Repository > Open in Command Prompt/Terminal)
   - Exécutez : `git rm --cached db_erp.sqlite3`
   - Commitez : `git commit -m "Remove db_erp.sqlite3 from version control"`
   - Poussez : `git push`

### Option 2 : Résoudre le conflit et continuer

1. Dans GitHub Desktop, dans la fenêtre "Resolve conflicts before Merge" :
   - Cliquez sur le bouton **"Resolve"** à côté de `db_erp.sqlite3`
   - Choisissez **"Use ours"** (utiliser votre version locale)
   - OU choisissez **"Use theirs"** (utiliser la version distante)
   - Cliquez sur **"Continue merge"**

2. **IMPORTANT** : Après le merge, retirez le fichier du suivi Git :
   - Ouvrez le terminal dans GitHub Desktop
   - Exécutez : `git rm --cached db_erp.sqlite3`
   - Commitez : `git commit -m "Remove db_erp.sqlite3 from version control"`
   - Poussez : `git push`

## Pourquoi retirer le fichier du suivi Git ?

- `db_erp.sqlite3` est une base de données locale qui change à chaque utilisation
- Il est déjà dans `.gitignore` mais était suivi avant d'être ajouté
- Les fichiers de base de données ne doivent pas être versionnés (données sensibles, taille, conflits)

## Vérification

Après avoir retiré le fichier du suivi Git, vérifiez que :
- Le fichier existe toujours localement (il ne sera pas supprimé)
- Git ne le suit plus (il n'apparaîtra plus dans `git status`)
- Les futurs merges ne causeront plus de conflits sur ce fichier

## Commandes complètes (si vous avez Git en ligne de commande)

```bash
# 1. Annuler le merge en cours (si vous choisissez cette option)
git merge --abort

# 2. Retirer le fichier du suivi Git (le fichier reste sur votre disque)
git rm --cached db_erp.sqlite3

# 3. Commiter la suppression du suivi
git commit -m "Remove db_erp.sqlite3 from version control"

# 4. Pousser les changements
git push
```

## Note importante

Le fichier `db_erp.sqlite3` restera sur votre disque local. La commande `git rm --cached` retire seulement le suivi Git, elle ne supprime pas le fichier physique.
