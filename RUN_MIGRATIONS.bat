@echo off
title Initialisation base ERP (migrate)
setlocal
color 0B

echo ===============================================
echo   EXECUTION DES MIGRATIONS DJANGO (ERP)
echo ===============================================
echo.

REM Se placer dans le dossier du script
cd /d "%~dp0"

REM Vérifier que Python est disponible
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python (py) n'est pas disponible sur ce poste.
    echo Installez Python puis relancez ce script.
    pause
    exit /b 1
)

echo [INFO] Lancement du script Python RUN_MIGRATIONS.py ...
echo.
py RUN_MIGRATIONS.py
set "EXIT_CODE=%ERRORLEVEL%"

if "%EXIT_CODE%"=="0" (
    echo.
    echo [SUCCES] La base de donnees est à jour.
) else (
    echo.
    echo [ERREUR] L'execution des migrations a echoue (code %EXIT_CODE%).
)

echo.
pause
endlocal







