# Script de Synchronisation AUTOMATIQUE des Donnees entre Local et OVH
# Usage: .\sync_data_ovh.ps1 [push|pull|sync]

param(
    [string]$Action = "sync"  # "push" (local vers OVH), "pull" (OVH vers local), "sync" (bidirectionnel)
)

# Couleurs
$GREEN = "`e[32m"
$YELLOW = "`e[33m"
$RED = "`e[31m"
$BLUE = "`e[34m"
$RESET = "`e[0m"

function Write-Success { param([string]$msg) Write-Host "$GREEN$msg$RESET" }
function Write-Warning { param([string]$msg) Write-Host "$YELLOW$msg$RESET" }
function Write-Error { param([string]$msg) Write-Host "$RED$msg$RESET" }
function Write-Info { param([string]$msg) Write-Host "$BLUE$msg$RESET" }

# Charger la configuration
function Get-OvhConfig {
    $configFile = ".ovh_config.json"
    if (Test-Path $configFile) {
        try {
            $config = Get-Content $configFile -Encoding UTF8 | ConvertFrom-Json
            return $config
        } catch {
            Write-Error "ERREUR: Erreur lors de la lecture de .ovh_config.json"
            return $null
        }
    } else {
        Write-Error "ERREUR: Fichier .ovh_config.json introuvable!"
        Write-Info "ASTUCE: Exécutez d'abord SYNC_OVH.bat pour créer le fichier de configuration"
        return $null
    }
}

# Activer l'environnement virtuel
function Activate-Venv {
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
        return $true
    } elseif (Test-Path "env\Scripts\Activate.ps1") {
        & .\env\Scripts\Activate.ps1
        return $true
    }
    return $false
}

# Exporter les données locales
function Export-LocalData {
    Write-Info "`nExport des donnees locales..."
    
    if (-not (Activate-Venv)) {
        Write-Warning "ATTENTION: Environnement virtuel non trouve, continuons quand meme..."
    }
    
    # Nom du fichier d'export avec timestamp
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $exportFile = "export_data_local_$timestamp.json"
    
    Write-Info "Fichier d'export: $exportFile"
    
    # Exporter les donnees (exclure les sessions et contenttypes)
    try {
        python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry --exclude auth.permission > $exportFile 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            $fileSize = (Get-Item $exportFile).Length / 1MB
            Write-Success "OK: Donnees exportees avec succes! (Taille: $([math]::Round($fileSize, 2)) MB)"
            return $exportFile
        } else {
            Write-Error "ERREUR: Erreur lors de l'export"
            return $null
        }
    } catch {
        Write-Error "ERREUR: $_"
        return $null
    }
}

# Importer les données depuis OVH
function Pull-FromOvh {
    param($config)
    
    Write-Info "`nRecuperation des donnees depuis OVH..."
    
    $ovhHost = "$($config.ovh_user)@$($config.ovh_host)"
    $remotePath = "$($config.ovh_project_path)"
    
    # Exporter sur le serveur OVH
    Write-Info "Export des donnees sur le serveur OVH..."
    $exportCmd = "ssh $ovhHost 'cd $remotePath && source venv/bin/activate && python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry --exclude auth.permission > export_data_ovh_`$(date +%Y%m%d_%H%M%S).json && ls -t export_data_ovh_*.json | head -1'"
    
    $result = Invoke-Expression $exportCmd 2>&1
    $remoteFile = $result -split "`n" | Select-Object -First 1
    
    if ([string]::IsNullOrWhiteSpace($remoteFile)) {
        Write-Error "ERREUR: Impossible d'exporter depuis OVH"
        return $null
    }
    
    $remoteFile = $remoteFile.Trim()
    
    # Télécharger le fichier
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $localFile = "export_data_ovh_$timestamp.json"
    
    Write-Info "Telechargement du fichier depuis OVH..."
    scp "${ovhHost}:${remotePath}/${remoteFile}" $localFile 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "OK: Fichier telecharge: $localFile"
        return $localFile
    } else {
        Write-Error "ERREUR: Impossible de telecharger le fichier"
        return $null
    }
}

# Pousser les données vers OVH
function Push-ToOvh {
    param($config, $localFile)
    
    Write-Info "`nTransfert des donnees vers OVH..."
    
    $ovhHost = "$($config.ovh_user)@$($config.ovh_host)"
    $remotePath = "$($config.ovh_project_path)"
    
    # Transférer le fichier via SCP
    try {
        Write-Info "Connexion a OVH..."
        $remoteFile = "export_data_import.json"
        scp $localFile "${ovhHost}:${remotePath}/${remoteFile}" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "OK: Fichier transfere vers OVH!"
            
            # Importer sur le serveur
            Write-Info "Import des donnees sur le serveur OVH..."
            Write-Warning "ATTENTION: Cette operation va fusionner les donnees sur OVH"
            
            $importCmd = "ssh $ovhHost 'cd $remotePath && source venv/bin/activate && python manage.py loaddata $remoteFile --settings=erp_project.settings_production 2>&1'"
            
            $importResult = Invoke-Expression $importCmd
            
            if ($LASTEXITCODE -eq 0) {
                Write-Success "OK: Donnees importees sur OVH avec succes!"
                
                # Redemarrer Gunicorn
                Write-Info "Redemarrage de Gunicorn..."
                ssh $ovhHost "sudo systemctl restart erp 2>/dev/null || sudo systemctl restart gunicorn 2>/dev/null || echo 'Service non trouve'"
                
                return $true
            } else {
                Write-Error "ERREUR lors de l'import sur OVH"
                Write-Host $importResult
                return $false
            }
        } else {
            Write-Error "ERREUR lors du transfert"
            return $false
        }
    } catch {
        Write-Error "ERREUR: $_"
        Write-Info "ASTUCE: Assurez-vous que SSH/SCP est configure correctement"
        return $false
    }
}

# Importer localement
function Import-Local {
    param($importFile)
    
    Write-Info "`nImport des donnees dans la base locale..."
    
    if (-not (Activate-Venv)) {
        Write-Warning "ATTENTION: Environnement virtuel non trouve"
    }
    
    Write-Warning "ATTENTION: Cette operation va fusionner les donnees locales"
    $confirm = Read-Host "Voulez-vous continuer? (oui/non)"
    
    if ($confirm -ne "oui") {
        Write-Warning "Operation annulee"
        return $false
    }
    
    try {
        python manage.py loaddata $importFile 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "OK: Donnees importees localement avec succes!"
            return $true
        } else {
            Write-Error "ERREUR lors de l'import local"
            return $false
        }
    } catch {
        Write-Error "ERREUR: $_"
        return $false
    }
}

# Fonction principale
function Main {
    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "Synchronisation des DONNEES ERP" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Yellow
    
    $config = Get-OvhConfig
    if ($null -eq $config) {
        exit 1
    }
    
    switch ($Action.ToLower()) {
        "push" {
            # Local -> OVH
            $exportFile = Export-LocalData
            if ($exportFile) {
                Push-ToOvh -config $config -localFile $exportFile
            }
        }
        "pull" {
            # OVH -> Local
            $importFile = Pull-FromOvh -config $config
            if ($importFile) {
                Import-Local -importFile $importFile
            }
        }
        "sync" {
            # Bidirectionnel: Push puis Pull
            Write-Info "Synchronisation bidirectionnelle..."
            Write-Info "1. Envoi des donnees locales vers OVH..."
            $exportFile = Export-LocalData
            if ($exportFile) {
                Push-ToOvh -config $config -localFile $exportFile
            }
            
            Write-Info "`n2. Recuperation des donnees depuis OVH..."
            $importFile = Pull-FromOvh -config $config
            if ($importFile) {
                Import-Local -importFile $importFile
            }
        }
        default {
            Write-Error "ERREUR: Action inconnue: $Action"
            Write-Info "Usage: .\sync_data_ovh.ps1 [push|pull|sync]"
            Write-Info "  push = Envoyer local -> OVH"
            Write-Info "  pull = Recuperer OVH -> local"
            Write-Info "  sync = Synchronisation bidirectionnelle"
        }
    }
    
    Write-Success "`nOK: Operation terminee!"
}

Main
