@echo off
REM Script pour verifier que la configuration Git est correcte apres copie

echo ========================================
echo Verification Configuration Git
echo ========================================
echo.

REM Verifier si Git est installe
git --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installe!
    echo Installez Git ou GitHub Desktop
    pause
    exit /b 1
)

echo OK: Git est installe
echo.

REM Verifier si on est dans un depot Git
if not exist ".git" (
    echo ERREUR: Ce dossier n'est pas un depot Git!
    echo.
    echo Solutions:
    echo 1. Cloner depuis GitHub (recommandee)
    echo    git clone https://github.com/Dolviane-Fomen/ERP_Supermarket_Portable.git
    echo.
    echo 2. Ou initialiser Git manuellement:
    echo    git init
    echo    git remote add origin https://github.com/Dolviane-Fomen/ERP_Supermarket_Portable.git
    echo.
    pause
    exit /b 1
)

echo OK: Dossier Git detecte
echo.

REM Verifier le remote GitHub
echo Verification du remote GitHub...
git remote -v
echo.

git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ATTENTION: Remote 'origin' non configure!
    echo.
    echo Ajoutez-le avec:
    echo git remote add origin https://github.com/Dolviane-Fomen/ERP_Supermarket_Portable.git
    echo.
) else (
    echo OK: Remote GitHub configure
    echo.
)

REM Verifier si .ovh_config.json existe
if not exist ".ovh_config.json" (
    echo ATTENTION: Fichier .ovh_config.json manquant!
    echo Executez CONFIGURER_NOUVEAU_PC.bat
    echo.
) else (
    echo OK: Fichier .ovh_config.json present
    echo.
)

REM Verifier les fichiers de synchronisation
if not exist "SYNC_OVH.bat" (
    echo ERREUR: SYNC_OVH.bat manquant!
) else (
    echo OK: SYNC_OVH.bat present
)

if not exist "sync_ovh.ps1" (
    echo ERREUR: sync_ovh.ps1 manquant!
) else (
    echo OK: sync_ovh.ps1 present
)

echo.
echo ========================================
echo Verification terminee
echo ========================================
echo.
pause

