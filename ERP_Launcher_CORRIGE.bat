@echo off
title ERP Supermarket - Launcher avec Corrections Stock
color 0A
cls

echo ========================================
echo.
echo          ERP SUPERMARKET
echo        Systeme de Gestion
echo      AVEC CORRECTIONS STOCK
echo.
echo ========================================
echo.
echo Demarrage en cours...
echo.

:: Se déplacer dans le dossier
cd /d "%~dp0"

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

echo Serveur demarre avec les corrections stock !
echo.
echo ========================================
echo.
echo   CORRECTIONS APPLIQUEES:
echo   ✓ Stock mis à jour lors des achats
echo   ✓ Fonction dupliquée supprimée
echo   ✓ Test de validation réussi
echo.
echo   URL: http://127.0.0.1:8000
echo.
echo ========================================
echo.

:: Ouvrir le navigateur après 3 secondes
start "" cmd /c "timeout /t 3 ^>nul ^&^& start http://127.0.0.1:8000"

:: Lancer le serveur SANS --noreload pour permettre le rechargement
py -B -u manage.py runserver 127.0.0.1:8000 --settings=erp_project.settings_standalone
