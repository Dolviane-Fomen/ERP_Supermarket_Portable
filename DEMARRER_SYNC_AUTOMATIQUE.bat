@echo off
REM Démarrer la synchronisation automatique en arrière-plan

echo ========================================
echo DEMARRAGE SYNCHRONISATION AUTOMATIQUE
echo ========================================
echo.
echo La synchronisation se fera automatiquement toutes les 5 minutes
echo Appuyez sur Ctrl+C pour arrêter
echo.

REM Changer vers le répertoire du script
cd /d "%~dp0"

REM Vérifier Python
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py
) else (
    python --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=python
    ) else (
        echo [ERREUR] Python n'est pas installé
        pause
        exit /b 1
    )
)

REM Démarrer la synchronisation automatique
echo Démarrage du service...
%PYTHON_CMD% SYNC_AUTOMATIQUE_EN_ARRIERE_PLAN.py

pause
