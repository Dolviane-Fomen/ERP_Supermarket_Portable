@echo off
title REDEMARRAGE EXPRESS - ERP Supermarket
color 0A
cls

echo.
echo ========================================
echo.
echo       REDEMARRAGE EXPRESS
echo    ERP Supermarket - Modifications
echo.
echo ========================================
echo.

:: Se deplacer dans le dossier
cd /d "%~dp0"

:: Arreter rapidement tous les processus
echo Arret des processus...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM py.exe /T >nul 2>&1

:: Supprimer le cache rapidement
echo Nettoyage du cache...
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc >nul 2>&1

:: Attendre 1 seconde
timeout /t 1 >nul

:: Relancer immediatement
echo Redemarrage...
start "" "ERP_Launcher.bat"

echo.
echo REDEMARRAGE EXPRESS TERMINE !
echo.
pause
