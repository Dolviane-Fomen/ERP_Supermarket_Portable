@echo off
REM Script de synchronisation Local <-> En ligne
REM Usage: SYNC_LOCAL_ONLINE.bat [pull|push|sync]

setlocal enabledelayedexpansion

echo ================================================
echo    SYNCHRONISATION LOCAL ^<^-> EN LIGNE
echo ================================================
echo.

if "%1"=="" (
    echo Mode d'utilisation:
    echo   SYNC_LOCAL_ONLINE.bat pull  - Télécharger depuis le serveur en ligne
    echo   SYNC_LOCAL_ONLINE.bat push  - Envoyer vers le serveur en ligne
    echo   SYNC_LOCAL_ONLINE.bat sync  - Synchronisation bidirectionnelle
    echo.
    echo Exemple: SYNC_LOCAL_ONLINE.bat pull
    exit /b 1
)

set MODE=%1

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

REM Changer vers le répertoire du script
cd /d "%~dp0"

REM Exécuter le script Python
echo Mode sélectionné: %MODE%
echo.

if "%MODE%"=="pull" (
    python SYNC_LOCAL_ONLINE.py --mode pull --merge
) else if "%MODE%"=="push" (
    python SYNC_LOCAL_ONLINE.py --mode push --merge
) else if "%MODE%"=="sync" (
    python SYNC_LOCAL_ONLINE.py --mode sync --merge
) else (
    echo [ERREUR] Mode invalide: %MODE%
    echo Utilisez: pull, push ou sync
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo [ERREUR] La synchronisation a échoué
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCES] Synchronisation terminée
    pause
)




