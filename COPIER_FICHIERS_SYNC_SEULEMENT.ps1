# Script PowerShell pour copier uniquement les fichiers de synchronisation
# A utiliser si les autres PCs ont deja l'ERP installe

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COPIE DES FICHIERS DE SYNCHRONISATION" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ce script copie uniquement les fichiers necessaires" -ForegroundColor Yellow
Write-Host "pour la synchronisation, pas tout le projet ERP." -ForegroundColor Yellow
Write-Host ""

# Demander le chemin de destination
$destPath = Read-Host "Entrez le chemin du dossier ERP sur l'autre PC (ex: C:\ERP_Supermarket_Portable)"

if (-not (Test-Path $destPath)) {
    Write-Host ""
    Write-Host "[ERREUR] Le chemin specifie n'existe pas: $destPath" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Copie des fichiers de synchronisation vers: $destPath" -ForegroundColor Yellow
Write-Host ""

# Liste des fichiers a copier
$filesToCopy = @(
    "SYNC_LOCAL_ONLINE.py",
    "SYNC_LOCAL_ONLINE.bat",
    "SYNC_DONNEES_BIDIRECTIONNEL.bat",
    "sync_donnees_bidirectionnel.ps1",
    "CONFIGURER_SYNC_AUTOMATIQUE.bat",
    "CONFIGURER_SYNC_AUTOMATIQUE.ps1",
    "CONFIGURER_SYNC_AUTOMATIQUE_TOUS_PC.bat"
)

# Fichiers optionnels de configuration
$configFiles = @(
    ".ovh_config.json",
    ".ovh_config.example.json"
)

# Copier les fichiers principaux
$copied = 0
$failed = 0

foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        try {
            Copy-Item $file $destPath -Force
            Write-Host "[OK] Copie: $file" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "[ERREUR] Echec copie: $file" -ForegroundColor Red
            $failed++
        }
    } else {
        Write-Host "[ATTENTION] Fichier introuvable: $file" -ForegroundColor Yellow
    }
}

# Copier les fichiers de configuration
foreach ($file in $configFiles) {
    if (Test-Path $file) {
        try {
            Copy-Item $file $destPath -Force
            Write-Host "[OK] Copie: $file" -ForegroundColor Green
            $copied++
        } catch {
            Write-Host "[ERREUR] Echec copie: $file" -ForegroundColor Red
            $failed++
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COPIE TERMINEE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Fichiers copies: $copied" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "Fichiers en echec: $failed" -ForegroundColor Red
}
Write-Host ""
Write-Host "Fichiers copies vers: $destPath" -ForegroundColor Yellow
Write-Host ""
Write-Host "Sur l'autre PC, executez:" -ForegroundColor Cyan
Write-Host "  CONFIGURER_SYNC_AUTOMATIQUE_TOUS_PC.bat" -ForegroundColor White
Write-Host ""
pause
