# 🔄 Comment Fonctionne la Synchronisation Local ↔ En Ligne

## 📋 Vue d'ensemble

La synchronisation garantit que **toutes vos données sont identiques** entre votre PC local et le serveur en ligne.

### ✅ Ce qui est synchronisé :

1. **📄 Factures de vente** (`FactureVente`, `LigneFactureVente`)
   - Quand la caissière crée une facture localement → Elle apparaît en ligne
   - Le chiffre d'affaires est mis à jour automatiquement

2. **📦 Stock** (`Article.quantite_stock`, `MouvementStock`)
   - Si le stock passe de 40 à 30 localement → Il devient 30 en ligne aussi
   - Les mouvements de stock sont synchronisés

3. **📊 Statistiques** (`StatistiqueVente`, `ChiffreAffaire`)
   - Les statistiques de ventes sont synchronisées
   - Le chiffre d'affaires est à jour en ligne

4. **👥 Clients, Fournisseurs, Articles**
   - Toutes les données sont synchronisées dans les deux sens

---

## 🔄 Processus de Synchronisation

### Mode Bidirectionnel (`sync`)

Le script `SYNC_LOCAL_ONLINE.py` fonctionne en **2 étapes** :

#### Étape 1 : 📥 PULL (Télécharger depuis le serveur)
```
Serveur en ligne → PC Local
```
- Récupère les dernières données du serveur
- Met à jour votre base locale avec les données en ligne

#### Étape 2 : 📤 PUSH (Envoyer vers le serveur)
```
PC Local → Serveur en ligne
```
- **IMPORTANT** : Cette étape envoie TOUJOURS vos données locales
- Même si l'étape 1 a échoué, vos factures sont envoyées
- Le stock local est synchronisé avec le serveur

### ⏱️ Fréquence de Synchronisation

**Actuellement configuré : Toutes les 1 minute**

Le script `SYNC_AUTOMATIQUE_EN_ARRIERE_PLAN.py` s'exécute automatiquement :
- ✅ Démarre avec `ERP_Launcher.bat`
- ✅ Synchronise toutes les 60 secondes (1 minute)
- ✅ Fonctionne en arrière-plan sans intervention

---

## 📝 Exemple Concret

### Scénario : La caissière crée une facture

1. **10:00:00** - La caissière crée une facture locale
   - Facture #123 créée
   - Stock de l'article A passe de 40 → 30

2. **10:00:30** - Synchronisation automatique (dans 30 secondes max)
   - ✅ La facture #123 est envoyée au serveur
   - ✅ Le stock de l'article A devient 30 en ligne aussi
   - ✅ Les statistiques sont mises à jour

3. **10:01:00** - Vous consultez en ligne
   - ✅ Vous voyez la facture #123
   - ✅ Le stock affiche 30
   - ✅ Le chiffre d'affaires est à jour

---

## 🛠️ Commandes Manuelles

Si vous voulez synchroniser manuellement :

### Envoyer les données locales vers le serveur (PUSH)
```bash
py SYNC_LOCAL_ONLINE.py --mode push --merge
```
**Utilisez ceci quand :**
- La caissière vient de créer des factures
- Vous voulez que les données locales apparaissent en ligne immédiatement

### Télécharger les données du serveur (PULL)
```bash
py SYNC_LOCAL_ONLINE.py --mode pull --merge
```
**Utilisez ceci quand :**
- Vous voulez récupérer les dernières données du serveur
- Vous avez modifié des données en ligne et voulez les avoir localement

### Synchronisation bidirectionnelle (SYNC)
```bash
py SYNC_LOCAL_ONLINE.py --mode sync --merge
```
**Utilisez ceci pour :**
- Synchroniser dans les deux sens
- C'est ce que fait la synchronisation automatique

---

## ⚙️ Configuration

### Modifier la fréquence de synchronisation

Éditez `SYNC_AUTOMATIQUE_EN_ARRIERE_PLAN.py` :

```python
SYNC_INTERVAL = 60  # Secondes (60 = 1 minute, 300 = 5 minutes)
```

### Vérifier que la synchronisation fonctionne

1. Créez une facture localement
2. Attendez 1-2 minutes
3. Vérifiez en ligne que la facture apparaît

---

## 🔍 Vérification

### Comment savoir si la synchronisation fonctionne ?

1. **Vérifiez les logs** :
   - Ouvrez la console où `SYNC_AUTOMATIQUE_EN_ARRIERE_PLAN.py` s'exécute
   - Vous devriez voir des messages toutes les minutes

2. **Testez manuellement** :
   ```bash
   py SYNC_LOCAL_ONLINE.py --mode push --merge
   ```
   - Si ça fonctionne, vous verrez "✅ Synchronisation réussie"

3. **Vérifiez en ligne** :
   - Créez une facture locale
   - Attendez 1-2 minutes
   - Vérifiez que la facture apparaît en ligne

---

## ⚠️ Important

### Le stock est synchronisé dans les DEUX sens

- ✅ Si vous modifiez le stock localement → Il change en ligne
- ✅ Si vous modifiez le stock en ligne → Il change localement
- ⚠️ **Attention** : La dernière modification gagne en cas de conflit

### Les factures sont toujours envoyées

Même si la synchronisation automatique rencontre un problème :
- ✅ Les factures locales sont **toujours** envoyées au serveur
- ✅ Le stock local est **toujours** synchronisé
- ✅ Vous pouvez toujours synchroniser manuellement avec `--mode push`

---

## 🚨 Dépannage

### La synchronisation ne fonctionne pas ?

1. **Vérifiez la connexion Internet**
   - Le script vérifie automatiquement Internet
   - Si pas d'Internet, la synchronisation est annulée

2. **Vérifiez SSH**
   - Testez : `ssh ubuntu@51.68.124.152`
   - Si ça demande un mot de passe, exécutez `CONFIGURER_SSH_SANS_MOT_DE_PASSE.bat`

3. **Synchronisez manuellement**
   ```bash
   py SYNC_LOCAL_ONLINE.py --mode push --merge
   ```

4. **Vérifiez les logs**
   - Regardez les messages d'erreur dans la console
   - Ils indiquent généralement le problème

---

## 📞 Support

Si vous avez des questions ou des problèmes :
1. Vérifiez ce document
2. Testez la synchronisation manuelle
3. Consultez les logs d'erreur
