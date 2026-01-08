# ÉTAPE 2 : Configurer les Secrets GitHub

## Instructions

1. **Allez sur GitHub :**
   - Ouvrez : https://github.com/Dolviane-Fomen/ERP_Supermarket_Portable/settings/secrets/actions

2. **Ajoutez les 4 secrets un par un :**

### Secret 1 : OVH_HOST
- Cliquez sur **"New repository secret"**
- **Name:** `OVH_HOST`
- **Secret:** `51.68.124.152`
- Cliquez sur **"Add secret"**

### Secret 2 : OVH_USER
- Cliquez sur **"New repository secret"**
- **Name:** `OVH_USER`
- **Secret:** `ubuntu`
- Cliquez sur **"Add secret"**

### Secret 3 : OVH_PROJECT_PATH
- Cliquez sur **"New repository secret"**
- **Name:** `OVH_PROJECT_PATH`
- **Secret:** `/home/ubuntu/erp_project`
- Cliquez sur **"Add secret"**

### Secret 4 : OVH_SSH_KEY
- Cliquez sur **"New repository secret"**
- **Name:** `OVH_SSH_KEY`
- **Secret:** Collez la clé privée complète que vous avez copiée à l'ÉTAPE 1
  - Doit commencer par `-----BEGIN OPENSSH PRIVATE KEY-----`
  - Doit se terminer par `-----END OPENSSH PRIVATE KEY-----`
- Cliquez sur **"Add secret"**

## Vérification

Après avoir ajouté les 4 secrets, vous devriez voir :
- ✅ OVH_HOST
- ✅ OVH_USER
- ✅ OVH_PROJECT_PATH
- ✅ OVH_SSH_KEY

## Prochaine étape

Une fois les 4 secrets ajoutés, passez à **ETAPE3_TESTER.bat**

