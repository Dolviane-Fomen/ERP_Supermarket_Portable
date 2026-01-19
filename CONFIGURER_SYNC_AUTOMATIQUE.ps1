# Configuration automatique de la synchronisation sur tous les PCs
# Script PowerShell plus avancé

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CONFIGURATION AUTOMATIQUE SYNCHRONISATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# ========================================
# ETAPE 1: Configuration .ovh_config.json
# ========================================
Write-Host "[1/5] Configuration du fichier .ovh_config.json..." -ForegroundColor Yellow

$ovhConfig = @{
    git_branch = "main"
    deployment_method = "git"
    ovh_project_path = "/home/ubuntu/erp_project"
    ovh_host = "51.68.124.152"
    git_remote = "origin"
    ovh_user = "ubuntu"
    shared_db_host = "51.68.124.152"
    shared_db_port = "5432"
    shared_db_name = "erp_db"
    shared_db_user = "erp_user"
}

if (Test-Path ".ovh_config.json") {
    Write-Host "  Fichier .ovh_config.json existe deja" -ForegroundColor Gray
    $recreate = Read-Host "  Voulez-vous le recreer? (O/N)"
    if ($recreate -ne "O" -and $recreate -ne "o") {
        Write-Host "  Conservation du fichier existant" -ForegroundColor Gray
    } else {
        $ovhConfig | ConvertTo-Json | Set-Content ".ovh_config.json" -Encoding UTF8
        Write-Host "  [OK] Fichier .ovh_config.json recree" -ForegroundColor Green
    }
} else {
    $ovhConfig | ConvertTo-Json | Set-Content ".ovh_config.json" -Encoding UTF8
    Write-Host "  [OK] Fichier .ovh_config.json cree" -ForegroundColor Green
}

# ========================================
# ETAPE 2: Configuration manage.py pour SQLite local
# ========================================
Write-Host ""
Write-Host "[2/5] Configuration de manage.py pour SQLite local..." -ForegroundColor Yellow

if (Test-Path "manage.py") {
    $manageContent = Get-Content "manage.py" -Raw
    
    if ($manageContent -match "settings_shared_db") {
        Write-Host "  Modification de manage.py pour utiliser SQLite local..." -ForegroundColor Gray
        $manageContent = $manageContent -replace "settings_shared_db", "settings"
        Set-Content "manage.py" -Value $manageContent -NoNewline
        Write-Host "  [OK] manage.py configure pour SQLite local" -ForegroundColor Green
    } elseif ($manageContent -match "settings['\""]") {
        Write-Host "  [OK] manage.py utilise deja SQLite local" -ForegroundColor Green
    } else {
        Write-Host "  [ATTENTION] Configuration de manage.py non detectee" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [ERREUR] manage.py introuvable!" -ForegroundColor Red
}

# ========================================
# ETAPE 3: Verification des dependances
# ========================================
Write-Host ""
Write-Host "[3/5] Verification des dependances..." -ForegroundColor Yellow

# Verifier Python
$pythonCmd = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
    Write-Host "  [OK] Python est installe (py)" -ForegroundColor Green
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
    Write-Host "  [OK] Python est installe (python)" -ForegroundColor Green
} else {
    Write-Host "  [ERREUR] Python n'est pas installe!" -ForegroundColor Red
    Write-Host "  Installez Python avant de continuer." -ForegroundColor Red
    pause
    exit 1
}

# Verifier Django
try {
    $djangoVersion = & $pythonCmd -c "import django; print(django.get_version())" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Django est installe (version $djangoVersion)" -ForegroundColor Green
    } else {
        throw "Django non trouve"
    }
} catch {
    Write-Host "  [ATTENTION] Django n'est pas installe" -ForegroundColor Yellow
    $install = Read-Host "  Voulez-vous l'installer maintenant? (O/N)"
    if ($install -eq "O" -or $install -eq "o") {
        Write-Host "  Installation de Django..." -ForegroundColor Gray
        & $pythonCmd -m pip install django
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Django installe" -ForegroundColor Green
        } else {
            Write-Host "  [ERREUR] Echec de l'installation de Django" -ForegroundColor Red
        }
    }
}

# Verifier psycopg2 (optionnel)
try {
    & $pythonCmd -m pip show psycopg2-binary | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] psycopg2-binary est installe (pour base partagee optionnelle)" -ForegroundColor Green
    }
} catch {
    Write-Host "  [INFO] psycopg2-binary n'est pas installe (optionnel)" -ForegroundColor Gray
}

# ========================================
# ETAPE 4: Configuration SSH
# ========================================
Write-Host ""
Write-Host "[4/5] Configuration SSH pour la synchronisation..." -ForegroundColor Yellow

if (Get-Command ssh -ErrorAction SilentlyContinue) {
    Write-Host "  [OK] SSH est disponible" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "  Test de connexion au serveur OVH..." -ForegroundColor Gray
    Write-Host "  (Vous devrez peut-etre entrer le mot de passe)" -ForegroundColor Gray
    Write-Host ""
    
    # Test de connexion avec timeout
    $testResult = ssh -o ConnectTimeout=5 -o BatchMode=yes ubuntu@51.68.124.152 "echo 'Connexion OK'" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Connexion SSH fonctionne (avec cles SSH)" -ForegroundColor Green
    } else {
        Write-Host "  [INFO] Connexion SSH necessitera un mot de passe" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  Pour eviter de taper le mot de passe a chaque fois:" -ForegroundColor Cyan
        Write-Host "    1. Generez une cle SSH: ssh-keygen -t rsa" -ForegroundColor White
        Write-Host "    2. Copiez-la sur le serveur: ssh-copy-id ubuntu@51.68.124.152" -ForegroundColor White
        Write-Host ""
        
        $setupSSH = Read-Host "  Voulez-vous configurer SSH maintenant? (O/N)"
        if ($setupSSH -eq "O" -or $setupSSH -eq "o") {
            Write-Host "  Generation de la cle SSH..." -ForegroundColor Gray
            ssh-keygen -t rsa -f "$env:USERPROFILE\.ssh\id_rsa" -N '""'
            
            Write-Host "  Copie de la cle sur le serveur..." -ForegroundColor Gray
            Write-Host "  (Vous devrez entrer le mot de passe une fois)" -ForegroundColor Yellow
            ssh-copy-id ubuntu@51.68.124.152
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  [OK] Cle SSH configuree!" -ForegroundColor Green
            }
        }
    }
} else {
    Write-Host "  [ATTENTION] SSH n'est pas dans le PATH" -ForegroundColor Yellow
    Write-Host "  Installez Git for Windows ou OpenSSH" -ForegroundColor Yellow
    Write-Host "  SSH est necessaire pour la synchronisation" -ForegroundColor Yellow
}

# ========================================
# ETAPE 5: Creation des dossiers necessaires
# ========================================
Write-Host ""
Write-Host "[5/5] Creation des dossiers necessaires..." -ForegroundColor Yellow

$folders = @("backups", "sync_data")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "  [OK] Dossier $folder cree" -ForegroundColor Green
    } else {
        Write-Host "  [OK] Dossier $folder existe deja" -ForegroundColor Green
    }
}

# ========================================
# RESUME
# ========================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CONFIGURATION TERMINEE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Fichiers configures:" -ForegroundColor Yellow
Write-Host "  [OK] .ovh_config.json" -ForegroundColor Green
Write-Host "  [OK] manage.py (SQLite local)" -ForegroundColor Green
Write-Host ""
Write-Host "Pour utiliser la synchronisation:" -ForegroundColor Yellow
Write-Host "  1. SYNC_LOCAL_ONLINE.bat pull  - Telecharger depuis serveur" -ForegroundColor White
Write-Host "  2. SYNC_LOCAL_ONLINE.bat push  - Envoyer vers serveur" -ForegroundColor White
Write-Host "  3. SYNC_LOCAL_ONLINE.bat sync  - Synchronisation bidirectionnelle" -ForegroundColor White
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Yellow
Write-Host "  - Travaillez en local avec SQLite (hors ligne OK)" -ForegroundColor White
Write-Host "  - Synchronisez quand vous avez Internet" -ForegroundColor White
Write-Host "  - Faites un PULL avant de commencer a travailler" -ForegroundColor White
Write-Host "  - Faites un PUSH apres avoir termine" -ForegroundColor White
Write-Host ""
pause
