@echo off
title FORCER REDEMARRAGE LAUNCHER - ERP Supermarket
color 0C
cls

echo.
echo ========================================
echo.
echo    FORCER REDEMARRAGE LAUNCHER
echo    ERP Supermarket - Systeme de Gestion
echo.
echo ========================================
echo.
echo Arret de tous les processus en cours...
echo.

:: Se deplacer dans le dossier
cd /d "%~dp0"

:: Arreter TOUS les processus Python/Django
echo [1/6] Arret des processus Python...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM py.exe /T >nul 2>&1
taskkill /F /IM manage.py /T >nul 2>&1
taskkill /F /IM runserver /T >nul 2>&1

:: Arreter les processus Django specifiques
echo [2/6] Arret des processus Django...
for /f "tokens=2" %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| find "manage.py"') do taskkill /F /PID %%i >nul 2>&1

:: Attendre que tous les processus soient arretes
echo [3/6] Attente de l'arret complet...
timeout /t 3 >nul

:: Supprimer TOUT le cache Python
echo [4/6] Suppression du cache Python...
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc >nul 2>&1
del /s /q *.pyo >nul 2>&1

:: Supprimer les fichiers temporaires
echo [5/6] Nettoyage des fichiers temporaires...
del /q *.log >nul 2>&1
del /q *.tmp >nul 2>&1

:: Variables anti-cache
set PYTHONDONTWRITEBYTECODE=1
set PYTHONUNBUFFERED=1
set DJANGO_SETTINGS_MODULE=erp_project.settings

echo [6/6] Redemarrage du launcher...
echo.
echo ========================================
echo.
echo   REDEMARRAGE FORCE TERMINE !
echo.
echo   Le launcher va maintenant redemarrer
echo   avec toutes les modifications prises
echo   en compte.
echo.
echo ========================================
echo.

:: Attendre 2 secondes avant de relancer
timeout /t 2 >nul

:: Relancer le launcher principal
echo Lancement du launcher principal...
start "" "ERP_Launcher.bat"

echo.
echo Le launcher a ete relance avec succes !
echo Toutes les modifications sont maintenant
echo prises en compte.
echo.
pause
