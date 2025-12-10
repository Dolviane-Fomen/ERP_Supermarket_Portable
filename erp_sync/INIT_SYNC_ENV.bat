@echo off
title Initialisation Sync ERP
color 0A

echo ============================================
echo   INITIALISATION DES DOSSIERS DE SYNC ERP
echo ============================================
echo.

set "SYNC_DIR=C:\erp_sync"
echo [INFO] Création de %SYNC_DIR%
md "%SYNC_DIR%" 2>nul
md "%SYNC_DIR%\entrant" 2>nul
md "%SYNC_DIR%\sortant" 2>nul
md "%SYNC_DIR%\archive" 2>nul
md "%SYNC_DIR%\logs" 2>nul

echo [OK] Dossiers créés.
echo.
echo Merci de partager %SYNC_DIR% sur le réseau
echo (clic droit > Partage > Autoriser lecture/écriture).
echo.
pause








