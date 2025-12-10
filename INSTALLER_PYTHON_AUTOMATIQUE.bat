@echo off
title Installation Automatique Python pour ERP Supermarket
color 0A
setlocal enabledelayedexpansion

echo ========================================
echo    INSTALLATION AUTOMATIQUE PYTHON
echo    ERP SUPERMARKET - CONFIGURATION COMPLETE
echo ========================================
echo.

set "SCRIPT_DIR=%~dp0"
set "PYTHON_INSTALLER=%TEMP%\python-installer.exe"
set "PYTHON_INSTALLED=false"
set "PYTHON_VERSION="
set "PYTHON_URL="

echo [INFO] Installation automatique de Python pour ERP Supermarket
echo [INFO] Ce script va installer Python et le configurer automatiquement
echo.

:: ========================================
:: VERIFICATION PYTHON EXISTANT
:: ========================================
echo [ETAPE 1/6] Verification de Python existant...

python --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Python deja installe
    python --version
    set "PYTHON_INSTALLED=true"
    goto :check_dependencies
)

py --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Python deja installe via py
    py --version
    set "PYTHON_INSTALLED=true"
    goto :check_dependencies
)

echo [INFO] Python non detecte - Installation necessaire
echo.

:: ========================================
:: DETECTION SYSTEME ET VERSION PYTHON
:: ========================================
echo [ETAPE 2/6] Detection du systeme et selection de Python...

:: Detection de l'architecture (32-bit ou 64-bit)
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set "ARCH=amd64"
    echo [INFO] Systeme 64-bit detecte
) else if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    set "ARCH=win32"
    echo [INFO] Systeme 32-bit detecte
) else (
    set "ARCH=amd64"
    echo [INFO] Architecture par defaut: 64-bit
)

:: Detection de la version Windows
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo [INFO] Version Windows detectee: %VERSION%

:: Selection de la version Python appropriee
if "%VERSION%"=="10.0" (
    set "PYTHON_VERSION=3.11.8"
    echo [INFO] Windows 10 detecte - Python 3.11.8 recommande
) else if "%VERSION%"=="6.3" (
    set "PYTHON_VERSION=3.9.18"
    echo [INFO] Windows 8.1 detecte - Python 3.9.18 compatible
) else if "%VERSION%"=="6.1" (
    set "PYTHON_VERSION=3.9.18"
    echo [INFO] Windows 7 detecte - Python 3.9.18 compatible
) else (
    set "PYTHON_VERSION=3.11.8"
    echo [INFO] Version Windows non reconnue - Python 3.11.8 par defaut
)

:: Construction de l'URL de telechargement
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-%ARCH%.exe"
echo [INFO] Version Python selectionnee: %PYTHON_VERSION%
echo [INFO] Architecture: %ARCH%
echo [INFO] URL de telechargement: %PYTHON_URL%
echo.

:: ========================================
:: TELECHARGEMENT PYTHON
:: ========================================
echo [ETAPE 3/6] Telechargement de Python...

echo [INFO] Telechargement de Python %PYTHON_VERSION%...
echo [INFO] URL: %PYTHON_URL%
echo [INFO] Destination: %PYTHON_INSTALLER%
echo.

:: Utiliser PowerShell pour telecharger
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}" >nul 2>&1

if not exist "%PYTHON_INSTALLER%" (
    echo [ERREUR] Impossible de telecharger Python
    echo [INFO] Telechargement manuel necessaire
    echo [INFO] Allez sur: https://python.org/downloads/
    echo [INFO] Telechargez Python 3.11.8 ou plus recent
    echo [INFO] Installez avec "Add Python to PATH" coche
    pause
    exit /b 1
) else (
    echo [OK] Python telecharge avec succes
)

echo [OK] Telechargement termine
echo.

:: ========================================
:: INSTALLATION PYTHON
:: ========================================
echo [ETAPE 4/6] Installation de Python...

echo [INFO] Lancement de l'installation Python...
echo [INFO] Configuration automatique en cours...
echo.

:: Installation silencieuse avec configuration automatique
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1 Include_tkinter=1 Include_launcher=1

if !errorlevel! neq 0 (
    echo [ERREUR] Installation Python echouee
    echo [INFO] Tentative d'installation manuelle...
    echo [INFO] Lancement de l'installateur Python...
    start "" "%PYTHON_INSTALLER%"
    echo [INFO] Suivez les instructions a l'ecran
    echo [INFO] IMPORTANT: Cochez "Add Python to PATH"
    pause
    exit /b 1
) else (
    echo [OK] Python installe avec succes
)

echo [OK] Installation Python terminee
echo.

:: ========================================
:: VERIFICATION INSTALLATION
:: ========================================
echo [ETAPE 5/6] Verification de l'installation...

:: Attendre que Python soit disponible
echo [INFO] Attente de la disponibilite de Python...
timeout /t 5 /nobreak >nul

python --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Python detecte via python
    python --version
    set "PYTHON_CMD=python"
    goto :check_dependencies
)

py --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Python detecte via py
    py --version
    set "PYTHON_CMD=py"
    goto :check_dependencies
)

echo [WARNING] Python installe mais pas encore dans le PATH
echo [INFO] Redemarrage de l'invite de commande necessaire
echo [INFO] Fermez cette fenetre et relancez ERP_Launcher.bat
pause
exit /b 0

:check_dependencies
echo [OK] Python fonctionnel
echo.

:: ========================================
:: INSTALLATION DEPENDANCES
:: ========================================
echo [ETAPE 6/6] Installation des dependances ERP...

echo [INFO] Installation de Django et Pillow...
%PYTHON_CMD% -m pip install django pillow --quiet --disable-pip-version-check

if !errorlevel! neq 0 (
    echo [WARNING] Certaines dependances n'ont pas pu etre installees
    echo [INFO] Tentative d'installation alternative...
    %PYTHON_CMD% -m pip install --user django pillow
    if !errorlevel! neq 0 (
        echo [ERREUR] Impossible d'installer les dependances
        echo [INFO] Installation manuelle necessaire
        echo [INFO] Executez: %PYTHON_CMD% -m pip install django pillow
        pause
        exit /b 1
    )
) else (
    echo [OK] Dependances installees avec succes
)

echo [OK] Dependances ERP installees
echo.

:: ========================================
:: VERIFICATION FINALE
:: ========================================
echo [ETAPE 7/7] Verification finale du systeme...

%PYTHON_CMD% -c "import django; import PIL" >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERREUR] Le systeme n'est pas pret
    echo [INFO] Verifiez les etapes precedentes
    pause
    exit /b 1
) else (
    echo [OK] Le systeme est pret!
)

echo [OK] Verification finale reussie
echo.

:: ========================================
:: NETTOYAGE
:: ========================================
echo [INFO] Nettoyage des fichiers temporaires...
if exist "%PYTHON_INSTALLER%" (
    del "%PYTHON_INSTALLER%" >nul 2>&1
    echo [OK] Fichier d'installation supprime
)

echo.

:: ========================================
:: RESULTAT FINAL
:: ========================================
echo ========================================
echo    INSTALLATION TERMINEE AVEC SUCCES!
echo ========================================
echo.
echo Python installe et configure:
%PYTHON_CMD% --version
echo.
echo Version Python installee: %PYTHON_VERSION%
echo Architecture: %ARCH%
echo Systeme: Windows %VERSION%
echo.
echo Dependances installees:
echo - Django (framework web)
echo - Pillow (traitement d'images)
echo.
echo Votre ERP Supermarket est maintenant pret!
echo.
echo UTILISATION:
echo 1. Double-clic sur ERP_Launcher.bat
echo 2. L'ERP s'ouvre automatiquement
echo 3. URL: http://127.0.0.1:8000
echo.
echo Comptes par defaut:
echo - Admin: admin / admin123
echo - Caissier: caissier1 / caissier123
echo.
echo ========================================
echo.
pause
