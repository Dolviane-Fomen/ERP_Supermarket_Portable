@echo off
title ERP Supermarket - Launcher
color 0B
cls

echo.
echo ========================================
echo.
echo          ERP SUPERMARKET
echo        Systeme de Gestion
echo.
echo ========================================
echo.
echo Demarrage en cours...
echo.

:: Se déplacer dans le dossier
cd /d "%~dp0"

:: Trouver Python
set "PYTHON_CMD=py"
python --version >nul 2>&1
if %errorlevel% equ 0 set "PYTHON_CMD=python"

:: Arrêter les anciens serveurs
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM py.exe /T >nul 2>&1
timeout /t 1 >nul

:: Supprimer le cache
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc >nul 2>&1

:: Variables anti-cache
set PYTHONDONTWRITEBYTECODE=1
set PYTHONUNBUFFERED=1

echo Serveur demarre avec succes !
echo.
echo ========================================
echo.
echo   Ouverture automatique du navigateur
echo   dans 3 secondes...
echo.
echo   URL: http://127.0.0.1:8000
echo.
echo ========================================
echo.

:: Ouvrir le navigateur après 3 secondes
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:8000"

:: Démarrer la synchronisation automatique avec le serveur OVH en arrière-plan
if exist "SYNC_AUTOMATIQUE_EN_ARRIERE_PLAN.py" (
    echo Demarrage de la synchronisation automatique...
    start /B %PYTHON_CMD% SYNC_AUTOMATIQUE_EN_ARRIERE_PLAN.py
    echo Synchronisation automatique active (toutes les 5 minutes)
    echo.
)

:: Démarrer la synchronisation réseau en arrière-plan (optionnel, pour sync locale)
if exist "ERP_LAUNCHER_SYNC.py" (
    start /B %PYTHON_CMD% ERP_LAUNCHER_SYNC.py
)

:: Lancer le serveur (cette fenêtre reste ouverte)
%PYTHON_CMD% -B -u manage.py runserver 127.0.0.1:8000 --settings=erp_project.settings_standalone --noreload

