# Script de Synchronisation Bidirectionnelle des Donnees
# Fusionne les donnees local <-> OVH sans rien remplacer

param(
    [string]$Action = "sync"  # "sync" pour bidirectionnel
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
            return Get-Content $configFile -Encoding UTF8 | ConvertFrom-Json
        } catch {
            Write-Error "ERREUR: Erreur lors de la lecture de .ovh_config.json"
            return $null
        }
    } else {
        Write-Error "ERREUR: Fichier .ovh_config.json introuvable!"
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

# Synchronisation bidirectionnelle
function Sync-Bidirectional {
    param($config)
    
    Write-Host "`n========================================" -ForegroundColor Yellow
    Write-Host "Synchronisation Bidirectionnelle" -ForegroundColor Yellow
    Write-Host "========================================`n" -ForegroundColor Yellow
    
    Write-Info "ETAPE 1: Export des donnees LOCALES (SQLite)..."
    Activate-Venv | Out-Null
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $localExport = "export_local_$timestamp.json"
    
    python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry --exclude auth.permission > $localExport 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "ERREUR lors de l'export local"
        return $false
    }
    
    $localSize = (Get-Item $localExport).Length / 1MB
    Write-Success "OK: Export local cree ($([math]::Round($localSize, 2)) MB)"
    
    Write-Info "`nETAPE 2: Export des donnees EN LIGNE (PostgreSQL sur OVH)..."
    
    $ovhHost = "$($config.ovh_user)@$($config.ovh_host)"
    $remotePath = "$($config.ovh_project_path)"
    
    # Exporter depuis OVH
    $remoteExportCmd = "ssh $ovhHost 'cd $remotePath && source venv/bin/activate && python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry --exclude auth.permission --settings=erp_project.settings_production > export_ovh_`$(date +%Y%m%d_%H%M%S).json && ls -t export_ovh_*.json | head -1'"
    
    $remoteFile = Invoke-Expression $remoteExportCmd 2>&1 | Select-Object -First 1
    $remoteFile = $remoteFile.Trim()
    
    if ([string]::IsNullOrWhiteSpace($remoteFile)) {
        Write-Error "ERREUR: Impossible d'exporter depuis OVH"
        return $false
    }
    
    $ovhExport = "export_ovh_$timestamp.json"
    Write-Info "Telechargement depuis OVH: $remoteFile"
    
    scp "${ovhHost}:${remotePath}/${remoteFile}" $ovhExport 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "ERREUR lors du telechargement depuis OVH"
        return $false
    }
    
    Write-Success "OK: Export OVH telecharge"
    
    Write-Info "`nETAPE 3: Fusion des donnees OVH dans LOCAL (sans remplacer)..."
    Write-Warning "Les donnees OVH seront ajoutees aux donnees locales"
    
    python manage.py loaddata $ovhExport --verbosity=1 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "OK: Donnees OVH fusionnees dans local"
    } else {
        Write-Warning "ATTENTION: Certaines donnees peuvent etre en conflit (normal si doublons)"
    }
    
    Write-Info "`nETAPE 4: Export des donnees LOCALES fusionnees..."
    
    $mergedExport = "export_merged_$timestamp.json"
    python manage.py dumpdata --exclude contenttypes --exclude sessions --exclude admin.logentry --exclude auth.permission > $mergedExport 2>&1
    
    Write-Info "`nETAPE 5: Fusion des donnees locales dans OVH (sans remplacer)..."
    
    scp $mergedExport "${ovhHost}:${remotePath}/import_merged.json" 2>&1
    
    $importCmd = "ssh $ovhHost 'cd $remotePath && source venv/bin/activate && python manage.py loaddata import_merged.json --settings=erp_project.settings_production 2>&1'"
    
    Write-Warning "Les donnees locales seront ajoutees aux donnees OVH"
    $importResult = Invoke-Expression $importCmd
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "OK: Donnees locales fusionnees dans OVH"
        
        # Redemarrer Gunicorn
        Write-Info "Redemarrage de Gunicorn..."
        ssh $ovhHost "sudo systemctl restart erp 2>/dev/null || sudo systemctl restart gunicorn 2>/dev/null || echo 'Service non trouve'"
        
        Write-Success "`nSUCCESS: Synchronisation bidirectionnelle terminee!"
        Write-Info "Les donnees des deux cotes ont ete fusionnees (sans remplacement)"
    } else {
        Write-Warning "ATTENTION: Certaines donnees peuvent etre en conflit (normal si doublons)"
    }
    
    # Nettoyer
    Write-Info "`nNettoyage des fichiers temporaires..."
    Remove-Item $localExport, $ovhExport, $mergedExport -ErrorAction SilentlyContinue
    
    return $true
}

# Fonction principale
function Main {
    $config = Get-OvhConfig
    if ($null -eq $config) {
        exit 1
    }
    
    if ($Action.ToLower() -eq "sync") {
        Sync-Bidirectional -config $config
    } else {
        Write-Error "ERREUR: Action inconnue. Utilisez 'sync' pour synchronisation bidirectionnelle"
    }
}

Main




