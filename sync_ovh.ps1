# Script de Synchronisation ERP avec OVH
# Usage: .\sync_ovh.ps1 [push|pull|deploy|status]

param(
    [string]$Action = "push"
)

# Couleurs pour les messages
$GREEN = "`e[32m"
$YELLOW = "`e[33m"
$RED = "`e[31m"
$BLUE = "`e[34m"
$RESET = "`e[0m"

# Fonction pour afficher les messages
function Write-ColorMessage {
    param(
        [string]$Message,
        [string]$Color = $RESET
    )
    Write-Host "$Color$Message$RESET"
}

function Write-Success { param([string]$msg) Write-ColorMessage $msg $GREEN }
function Write-Warning { param([string]$msg) Write-ColorMessage $msg $YELLOW }
function Write-Error { param([string]$msg) Write-ColorMessage $msg $RED }
function Write-Info { param([string]$msg) Write-ColorMessage $msg $BLUE }

# Vérifier si Git est installé
function Test-GitInstalled {
    try {
        $null = git --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
    } catch {
        # Continuer pour chercher dans d'autres chemins
    }
    
    # Chercher Git dans les chemins courants de GitHub Desktop
    $possiblePaths = @(
        "$env:LOCALAPPDATA\GitHubDesktop\app-*\resources\app\git\cmd\git.exe",
        "$env:ProgramFiles\Git\cmd\git.exe",
        "$env:ProgramFiles(x86)\Git\cmd\git.exe",
        "C:\Program Files\Git\cmd\git.exe",
        "C:\Program Files (x86)\Git\cmd\git.exe"
    )
    
    foreach ($path in $possiblePaths) {
        $found = Get-ChildItem $path -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            $env:PATH += ";$($found.DirectoryName)"
            Write-Info "Git trouve dans: $($found.DirectoryName)"
            return $true
        }
    }
    
    return $false
}

# Charger la configuration OVH
function Get-OvhConfig {
    $configFile = ".ovh_config.json"
    if (Test-Path $configFile) {
        try {
            $config = Get-Content $configFile -Encoding UTF8 | ConvertFrom-Json
            return $config
        } catch {
            Write-Error "ERREUR: Erreur lors de la lecture du fichier de configuration .ovh_config.json"
            return $null
        }
    } else {
        Write-Warning "ATTENTION: Fichier .ovh_config.json introuvable. Creation d'un fichier template..."
        $template = @{
            git_remote = "origin"
            git_branch = "main"
            ovh_host = "VOTRE_IP_OVH"
            ovh_user = "erpuser"
            ovh_project_path = "/home/erpuser/erp_project"
            deployment_method = "git"
        } | ConvertTo-Json -Depth 10
        
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [System.IO.File]::WriteAllLines((Resolve-Path .).Path + "\" + $configFile, $template, $utf8NoBom)
        Write-Info "OK: Fichier .ovh_config.json cree. Veuillez le remplir avec vos informations."
        Write-Info "ATTENTION: Ce fichier est dans .gitignore et ne sera pas versionne."
        return $null
    }
}

# Vérifier l'état Git
function Get-GitStatus {
    Write-Info "`nVerification de l'etat Git..."
    
    # Vérifier si on est dans un dépôt Git
    if (-not (Test-Path ".git")) {
        Write-Error "ERREUR: Ce repertoire n'est pas un depot Git!"
        Write-Info "ASTUCE: Initialisez Git avec: git init"
        return $false
    }
    
    # Vérifier le statut
    $status = git status --short
    if ($status) {
        Write-Warning "ATTENTION: Modifications non commitees detectees:"
        Write-Host $status
        $response = Read-Host "Voulez-vous les commiter maintenant? (o/n)"
        if ($response -eq "o" -or $response -eq "O") {
            $commitMsg = Read-Host "Message de commit"
            if ([string]::IsNullOrWhiteSpace($commitMsg)) {
                $commitMsg = "Mise a jour automatique"
            }
            git add .
            git commit -m $commitMsg
            Write-Success "OK: Modifications commitees"
        }
    } else {
        Write-Success "OK: Aucune modification a commiter"
    }
    
    return $true
}

# Pousser vers GitHub
function Push-ToGitHub {
    param($config)
    
    Write-Info "`nPoussage vers GitHub..."
    
    $remote = $config.git_remote
    $branch = $config.git_branch
    
    Write-Info "Remote: $remote, Branch: $branch"
    
    # Vérifier si le remote existe
    $remotes = git remote
    if ($remotes -notcontains $remote) {
        Write-Error "ERREUR: Le remote '$remote' n'existe pas!"
        Write-Info "ASTUCE: Ajoutez votre remote avec: git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git"
        return $false
    }
    
    # Pousser vers GitHub
    try {
        git push $remote $branch
        if ($LASTEXITCODE -eq 0) {
            Write-Success "OK: Code pousse vers GitHub avec succes!"
            return $true
        } else {
            Write-Error "ERREUR: Erreur lors du push vers GitHub"
            return $false
        }
    } catch {
        Write-Error "ERREUR: $_"
        return $false
    }
}

# Déclencher le déploiement sur OVH
function Deploy-ToOvh {
    param($config)
    
    Write-Info "`nDeclenchement du deploiement sur OVH..."
    
    if ($config.deployment_method -eq "ssh") {
        # Méthode SSH directe
        Write-Info "Connexion SSH a OVH..."
        $sshCmd = "ssh $($config.ovh_user)@$($config.ovh_host) 'cd $($config.ovh_project_path) && ./deploy.sh'"
        Invoke-Expression $sshCmd
    } else {
        # Méthode Git (recommandée)
        Write-Info "Le serveur OVH recuperera automatiquement les modifications via Git"
        Write-Info "ASTUCE: Si vous avez configure GitHub Actions, le deploiement se fera automatiquement"
        Write-Info "ASTUCE: Sinon, connectez-vous manuellement au serveur et executez: ~/deploy.sh"
    }
    
    Write-Success "OK: Deploiement declenche!"
}

# Récupérer depuis GitHub
function Pull-FromGitHub {
    param($config)
    
    Write-Info "`nRecuperation depuis GitHub..."
    
    $remote = $config.git_remote
    $branch = $config.git_branch
    
    try {
        git pull $remote $branch
        if ($LASTEXITCODE -eq 0) {
            Write-Success "OK: Code recupere depuis GitHub avec succes!"
            return $true
        } else {
            Write-Error "ERREUR: Erreur lors du pull depuis GitHub"
            return $false
        }
    } catch {
        Write-Error "ERREUR: $_"
        return $false
    }
}

# Afficher le statut
function Show-Status {
    param($config)
    
    Write-Info "`nStatut de la synchronisation"
    Write-Info "=================================="
    
    # Statut Git local
    Write-Info "`nLocal:"
    $status = git status --short
    if ($status) {
        Write-Warning "Modifications non commitees:"
        Write-Host $status
    } else {
        Write-Success "OK: Aucune modification locale"
    }
    
    # Vérifier si on est à jour avec le remote
    Write-Info "`nRemote:"
    git fetch --dry-run 2>&1 | Out-Null
    $localCommit = git rev-parse HEAD
    $remoteCommit = git rev-parse "$($config.git_remote)/$($config.git_branch)" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        if ($localCommit -eq $remoteCommit) {
            Write-Success "OK: Local a jour avec $($config.git_remote)/$($config.git_branch)"
        } else {
            Write-Warning "ATTENTION: Local et remote ne sont pas synchronises"
            Write-Info "ASTUCE: Utilisez 'pull' pour recuperer ou 'push' pour envoyer"
        }
    } else {
        Write-Warning "ATTENTION: Impossible de verifier le remote"
    }
    
    # Informations OVH
    Write-Info "`nServeur OVH:"
    Write-Info "   Host: $($config.ovh_host)"
    Write-Info "   User: $($config.ovh_user)"
    Write-Info "   Path: $($config.ovh_project_path)"
    Write-Info "   Methode: $($config.deployment_method)"
}

# Fonction principale
function Main {
    Write-ColorMessage "`n========================================" $YELLOW
    Write-ColorMessage "Synchronisation ERP avec OVH" $YELLOW
    Write-ColorMessage "========================================`n" $YELLOW
    
    # Vérifier Git
    if (-not (Test-GitInstalled)) {
        Write-Error "ERREUR: Git n'est pas installe!"
        Write-Info "ASTUCE: Installez Git depuis: https://git-scm.com/download/win"
        exit 1
    }
    
    # Charger la configuration
    $config = Get-OvhConfig
    if ($null -eq $config) {
        exit 1
    }
    
    # Actions
    switch ($Action.ToLower()) {
        "push" {
            if (Get-GitStatus) {
                if (Push-ToGitHub -config $config) {
                    Deploy-ToOvh -config $config
                }
            }
        }
        "pull" {
            Pull-FromGitHub -config $config
        }
        "deploy" {
            Deploy-ToOvh -config $config
        }
        "status" {
            Show-Status -config $config
        }
        default {
            Write-Error "ERREUR: Action inconnue: $Action"
            Write-Info "Usage: .\sync_ovh.ps1 [push|pull|deploy|status]"
            exit 1
        }
    }
    
    Write-Success "`nOK: Operation terminee!"
}

# Exécuter le script
Main
