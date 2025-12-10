# Script PowerShell pour forcer le redémarrage complet du launcher ERP
# Auteur: Assistant IA
# Description: Force le redémarrage avec nettoyage complet

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "    FORCER REDEMARRAGE COMPLET" -ForegroundColor Yellow
Write-Host "    ERP Supermarket - Systeme de Gestion" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Se deplacer dans le dossier du script
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

Write-Host "[1/8] Arret de tous les processus Python/Django..." -ForegroundColor Red

# Arreter tous les processus Python
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process -Name "py" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Arreter les processus Django specifiques
Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*manage.py*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*runserver*"} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "[2/8] Attente de l'arret complet..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "[3/8] Suppression du cache Python..." -ForegroundColor Green
# Supprimer tous les dossiers __pycache__
Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | ForEach-Object {
    Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue
}

# Supprimer tous les fichiers .pyc et .pyo
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Recurse -Filter "*.pyo" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[4/8] Nettoyage des fichiers temporaires..." -ForegroundColor Green
# Supprimer les fichiers temporaires
Get-ChildItem -Path . -Filter "*.log" | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Filter "*.tmp" | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "[5/8] Verification des processus restants..." -ForegroundColor Yellow
# Verifier qu'aucun processus Python ne tourne encore
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "ATTENTION: Des processus Python sont encore actifs!" -ForegroundColor Red
    $pythonProcesses | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
}

Write-Host "[6/8] Configuration des variables d'environnement..." -ForegroundColor Green
# Configurer les variables d'environnement
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONUNBUFFERED = "1"
$env:DJANGO_SETTINGS_MODULE = "erp_project.settings"

Write-Host "[7/8] Redemarrage du launcher..." -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "   REDEMARRAGE FORCE TERMINE !" -ForegroundColor Green
Write-Host ""
Write-Host "   Le launcher va maintenant redemarrer" -ForegroundColor White
Write-Host "   avec toutes les modifications prises" -ForegroundColor White
Write-Host "   en compte." -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[8/8] Lancement du launcher principal..." -ForegroundColor Green
Start-Sleep -Seconds 2

# Lancer le launcher principal
if (Test-Path "ERP_Launcher.bat") {
    Start-Process -FilePath "ERP_Launcher.bat" -WindowStyle Normal
    Write-Host ""
    Write-Host "Le launcher a ete relance avec succes !" -ForegroundColor Green
    Write-Host "Toutes les modifications sont maintenant prises en compte." -ForegroundColor Green
} else {
    Write-Host "ERREUR: Le fichier ERP_Launcher.bat n'a pas ete trouve!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Appuyez sur une touche pour continuer..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
