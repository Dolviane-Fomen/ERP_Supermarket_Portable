@echo off
title Installation Python Rapide - ERP Supermarket
color 0A
setlocal enabledelayedexpansion

echo ========================================
echo    INSTALLATION PYTHON RAPIDE
echo    ERP SUPERMARKET - RECUPERATION
echo ========================================
echo.

set "PYTHON_INSTALLED=false"
set "PYTHON_CMD="

echo [INFO] Installation rapide de Python pour ERP Supermarket
echo [INFO] Ce script utilise des methodes alternatives
echo.

:: ========================================
:: VERIFICATION PYTHON EXISTANT
:: ========================================
echo [ETAPE 1/4] Verification de Python existant...

python --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Python deja installe
    python --version
    set "PYTHON_CMD=python"
    set "PYTHON_INSTALLED=true"
    goto :install_dependencies
)

py --version >nul 2>&1
if !errorlevel! equ 0 (
    echo [OK] Python deja installe via py
    py --version
    set "PYTHON_CMD=py"
    set "PYTHON_INSTALLED=true"
    goto :install_dependencies
)

echo [INFO] Python non detecte - Installation manuelle necessaire
echo.

:: ========================================
:: INSTALLATION MANUELLE GUIDE
:: ========================================
echo [ETAPE 2/4] Installation manuelle de Python...
echo.
echo [GUIDE] Installation manuelle de Python:
echo.
echo 1. Ouvrez votre navigateur
echo 2. Allez sur: https://python.org/downloads/
echo 3. Cliquez sur "Download Python 3.11.8"
echo 4. IMPORTANT: Cochez "Add Python to PATH"
echo 5. Cliquez sur "Install Now"
echo 6. Attendez la fin de l'installation
echo 7. Redemarrez cette fenetre
echo.
echo [INFO] Ou utilisez le Microsoft Store:
echo - Ouvrez Microsoft Store
echo - Recherchez "Python 3.11"
echo - Installez Python 3.11
echo.
echo Voulez-vous ouvrir le site de telechargement maintenant?
set /p choice="(O/N): "
if /i "%choice%"=="O" (
    start https://python.org/downloads/
)

echo.
echo [INFO] Apres l'installation, relancez ce script
pause
exit /b 0

:install_dependencies
echo [OK] Python fonctionnel detecte
echo.

:: ========================================
:: INSTALLATION DEPENDANCES
:: ========================================
echo [ETAPE 3/4] Installation des dependances ERP...

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
echo [ETAPE 4/4] Verification finale du systeme...

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
:: RESULTAT FINAL
:: ========================================
echo ========================================
echo    INSTALLATION TERMINEE AVEC SUCCES!
echo ========================================
echo.
echo Python installe et configure:
%PYTHON_CMD% --version
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





