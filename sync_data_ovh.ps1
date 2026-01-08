# Script de Synchronisation des Données entre Local et OVH
# Usage: .\sync_data_ovh.ps1 [export|import|backup]

param(
    [string]$Action = "export",
    [string]$Direction = "local_to_ovh"  # "local_to_ovh" ou "ovh_to_local"
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
            return Get-Content $configFile | ConvertFrom-Json
        } catch {
            Write-Error "❌ Erreur lors de la lecture de .ovh_config.json"
            return $null
        }
    } else {
        Write-Error "❌ Fichier .ovh_config.json introuvable!"
        Write-Info "💡 Exécutez d'abord sync_ovh.ps1 pour créer le fichier de configuration"
        return $null
    }
}

# Exporter les données depuis la base locale
function Export-LocalData {
    Write-Info "`n📤 Export des données locales..."
    
    # Activer l'environnement virtuel si il existe
    if (Test-Path "venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
    } elseif (Test-Path "env\Scripts\Activate.ps1") {
        & .\env\Scripts\Activate.ps1
    }
    
    # Nom du fichier d'export avec timestamp
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $exportFile = "export_data_$timestamp.json"
    
    Write-Info "📁 Fichier d'export: $exportFile"
    
    # Exporter les données
    try {
        python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry --exclude auth.permission > $exportFile
        if ($LASTEXITCODE -eq 0) {
            $fileSize = (Get-Item $exportFile).Length / 1MB
            Write-Success "✅ Données exportées avec succès! (Taille: $([math]::Round($fileSize, 2)) MB)"
            return $exportFile
        } else {
            Write-Error "❌ Erreur lors de l'export"
            return $null
        }
    } catch {
        Write-Error "❌ Erreur: $_"
        return $null
    }
}

# Importer les données depuis OVH
function Import-FromOvh {
    param($config, $localFile)
    
    Write-Info "`n📥 Transfert du fichier vers OVH..."
    
    $ovhHost = "$($config.ovh_user)@$($config.ovh_host)"
    $remotePath = "$($config.ovh_project_path)/export_data.json"
    
    # Transférer le fichier via SCP
    try {
        Write-Info "🔌 Connexion à OVH..."
        scp $localFile "${ovhHost}:${remotePath}"
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Fichier transféré vers OVH!"
            
            # Importer sur le serveur
            Write-Info "📥 Import des données sur le serveur OVH..."
            $importCmd = "ssh $ovhHost 'cd $($config.ovh_project_path) && source venv/bin/activate && python manage.py loaddata export_data.json --settings=erp_project.settings_production'"
            
            Write-Warning "⚠️  ATTENTION: Cette opération va écraser les données existantes sur OVH!"
            $confirm = Read-Host "Voulez-vous continuer? (oui/non)"
            
            if ($confirm -eq "oui") {
                Invoke-Expression $importCmd
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "✅ Données importées sur OVH avec succès!"
                } else {
                    Write-Error "❌ Erreur lors de l'import sur OVH"
                }
            } else {
                Write-Warning "❌ Opération annulée"
            }
        } else {
            Write-Error "❌ Erreur lors du transfert"
        }
    } catch {
        Write-Error "❌ Erreur: $_"
        Write-Info "💡 Assurez-vous que SSH/SCP est configuré correctement"
    }
}

# Sauvegarder les données OVH vers local
function Backup-FromOvh {
    param($config)
    
    Write-Info "`n📥 Sauvegarde des données depuis OVH..."
    
    $ovhHost = "$($config.ovh_user)@$($config.ovh_host)"
    $remotePath = "$($config.ovh_project_path)"
    
    # Exporter sur le serveur OVH
    Write-Info "📤 Export des données sur OVH..."
    $exportCmd = "ssh $ovhHost 'cd $remotePath && source venv/bin/activate && python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry --exclude auth.permission > backup_ovh_$(date +%Y%m%d_%H%M%S).json && ls -lh backup_ovh_*.json | tail -1'"
    
    Invoke-Expression $exportCmd
    
    # Télécharger le fichier
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $localFile = "backup_ovh_$timestamp.json"
    
    Write-Info "📥 Téléchargement du fichier..."
    $latestBackup = "ssh $ovhHost 'cd $remotePath && ls -t backup_ovh_*.json | head -1'"
    $backupName = Invoke-Expression $latestBackup
    
    if ($backupName) {
        scp "${ovhHost}:${remotePath}/${backupName}" $localFile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Sauvegarde téléchargée: $localFile"
            return $localFile
        } else {
            Write-Error "❌ Erreur lors du téléchargement"
        }
    }
    
    return $null
}

# Fonction principale
function Main {
    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "🔄 Synchronisation des Données ERP" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Yellow
    
    $config = Get-OvhConfig
    if ($null -eq $config) {
        exit 1
    }
    
    switch ($Action.ToLower()) {
        "export" {
            if ($Direction -eq "local_to_ovh") {
                $exportFile = Export-LocalData
                if ($exportFile) {
                    Import-FromOvh -config $config -localFile $exportFile
                }
            } else {
                Write-Error "❌ Direction non supportée pour export"
            }
        }
        "backup" {
            Backup-FromOvh -config $config
        }
        default {
            Write-Error "❌ Action inconnue: $Action"
            Write-Info "Usage: .\sync_data_ovh.ps1 [export|backup] [local_to_ovh|ovh_to_local]"
        }
    }
    
    Write-Success "`n✅ Opération terminée!"
}

Main

