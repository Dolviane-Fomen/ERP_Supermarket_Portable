@echo off
title Nettoyage cache Python/Django
color 0B
setlocal

echo ===============================================
echo   NETTOYAGE CACHE PYTHON / DJANGO
echo ===============================================
echo.

REM Se placer dans le dossier du script
cd /d "%~dp0"

REM Vérifier Python
py --version >NUL 2>&1
if errorlevel 1 (
    echo [ERREUR] Python (py.exe) est introuvable sur ce poste.
    echo Installez Python ou ajoutez-le au PATH, puis relancez.
    pause
    exit /b 1
)

echo [INFO] Lancement de VIDER_CACHE_PYTHON_DJANGO.py ...
echo.
py VIDER_CACHE_PYTHON_DJANGO.py
set EXITCODE=%ERRORLEVEL%

if "%EXITCODE%"=="0" (
    echo.
    echo [SUCCES] Nettoyage terminé. Relancez ERP_Launcher.bat.
) else (
    echo.
    echo [ERREUR] Le script s'est terminé avec le code %EXITCODE%.
)

echo.
pause
endlocal







