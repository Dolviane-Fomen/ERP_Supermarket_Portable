# Configuration GitHub Actions pour Déploiement Automatique OVH

## Étapes de Configuration

### 1. Générer une clé SSH sur le serveur OVH

Connectez-vous à votre serveur OVH :
```bash
ssh ubuntu@51.68.124.152
```

Générez une clé SSH dédiée pour GitHub Actions :
```bash
ssh-keygen -t ed25519 -C "github-actions@ovh" -f ~/.ssh/github_actions_key
```

**Important :** Ne mettez PAS de mot de passe (appuyez juste sur Entrée).

Affichez la clé privée (vous en aurez besoin pour GitHub) :
```bash
cat ~/.ssh/github_actions_key
```

Copiez TOUT le contenu affiché (de `-----BEGIN OPENSSH PRIVATE KEY-----` jusqu'à `-----END OPENSSH PRIVATE KEY-----`).

### 2. Autoriser la clé publique sur le serveur

```bash
cat ~/.ssh/github_actions_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 3. Configurer les Secrets GitHub

1. Allez sur GitHub : https://github.com/Dolviane-Fomen/ERP_Supermarket_Portable
2. Cliquez sur **Settings** (Paramètres)
3. Dans le menu gauche, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**

Ajoutez ces 4 secrets :

#### Secret 1 : OVH_HOST
- **Name:** `OVH_HOST`
- **Value:** `51.68.124.152`

#### Secret 2 : OVH_USER
- **Name:** `OVH_USER`
- **Value:** `ubuntu`

#### Secret 3 : OVH_PROJECT_PATH
- **Name:** `OVH_PROJECT_PATH`
- **Value:** `/home/ubuntu/erp_project`

#### Secret 4 : OVH_SSH_KEY
- **Name:** `OVH_SSH_KEY`
- **Value:** Collez la clé privée complète que vous avez copiée à l'étape 1

### 4. Tester le déploiement

Une fois les secrets configurés :

1. Faites une petite modification dans votre projet local
2. Double-cliquez sur `SYNC_OVH.bat` pour pousser vers GitHub
3. Allez sur GitHub → **Actions** dans votre dépôt
4. Vous verrez le workflow se lancer automatiquement
5. Attendez quelques secondes/minutes
6. Si c'est vert ✅, le déploiement a réussi !

## Vérification

Pour vérifier que tout fonctionne :
```bash
# Sur le serveur OVH
ssh ubuntu@51.68.124.152
cd /home/ubuntu/erp_project
git log -1  # Doit afficher votre dernier commit
```

## Résolution des problèmes

### Le workflow échoue avec "Permission denied"
- Vérifiez que la clé SSH privée est bien collée dans `OVH_SSH_KEY`
- Vérifiez que la clé publique est dans `~/.ssh/authorized_keys` sur le serveur

### Le workflow échoue avec "command not found"
- Vérifiez que le chemin `OVH_PROJECT_PATH` est correct
- Vérifiez que l'environnement virtuel existe : `ls -la /home/ubuntu/erp_project/venv`

### Le service systemd n'existe pas
- C'est normal si vous n'avez pas encore configuré le service systemd
- Le workflow continuera quand même
- Configurez le service plus tard si nécessaire




