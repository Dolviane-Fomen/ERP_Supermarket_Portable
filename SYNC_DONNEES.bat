@echo off
REM Script de synchronisation des DONNEES (stock, clients, commandes, etc.)
REM Double-cliquez sur ce fichier pour synchroniser les donnees

echo ========================================
echo Synchronisation des DONNEES ERP
echo ========================================
echo.

REM Verifier si PowerShell est disponible
powershell.exe -Command "& {Get-Host}" >nul 2>&1
if errorlevel 1 (
    echo Erreur: PowerShell n'est pas disponible
    pause
    exit /b 1
)

REM Executer le script PowerShell
powershell.exe -ExecutionPolicy Bypass -File "%~dp0sync_data_ovh.ps1"

echo.
echo ========================================
pause




