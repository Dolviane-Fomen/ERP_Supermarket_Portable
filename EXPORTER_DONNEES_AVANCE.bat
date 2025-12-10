@echo off
REM ============================================
REM Script d'export des données ERP (Version Avancée)
REM Utilise EXPORT_DONNEES_STANDALONE.py
REM ============================================

chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

title Export des Donnees ERP

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║         EXPORT DES DONNEES ERP - VERSION STANDALONE     ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Vérifier si Python est installé
echo [1/3] Vérification de Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Solutions possibles:
    echo   1. Installer Python depuis https://www.python.org/
    echo   2. Ajouter Python au PATH système
    echo   3. Utiliser le chemin complet vers python.exe
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    ✓ Python !PYTHON_VERSION! détecté
echo.

REM Vérifier si le script Python existe
echo [2/3] Vérification du script d'export...
if not exist "EXPORT_DONNEES_STANDALONE.py" (
    echo.
    echo ❌ [ERREUR] Le fichier EXPORT_DONNEES_STANDALONE.py est introuvable
    echo.
    echo Assurez-vous que le fichier est dans le même répertoire que ce script .bat
    echo.
    echo Répertoire actuel: %CD%
    echo.
    pause
    exit /b 1
)
echo    ✓ Script Python trouvé
echo.

REM Vérifier si manage.py existe (pour s'assurer qu'on est dans le bon répertoire)
echo [3/3] Vérification de l'environnement Django...
if not exist "manage.py" (
    echo    ⚠ Avertissement: manage.py non trouvé
    echo    Le script peut quand même fonctionner si Django est configuré
    echo.
) else (
    echo    ✓ Environnement Django détecté
    echo.
)

echo ═══════════════════════════════════════════════════════════
echo   Démarrage de l'export des données...
echo ═══════════════════════════════════════════════════════════
echo.

REM Afficher la liste des agences disponibles
echo.
echo ═══════════════════════════════════════════════════════════
echo   📋 LISTE DES AGENCES DISPONIBLES
echo ═══════════════════════════════════════════════════════════
echo.
py LISTER_AGENCES.py
if errorlevel 1 (
    echo.
    echo ⚠️  Impossible de lister les agences. Continuons quand même...
    echo.
)

REM Demander l'ID de l'agence (optionnel)
echo.
set /p AGENCE_ID="Entrez l'ID de l'agence à exporter (ou appuyez sur Entrée pour toutes les agences): "

REM Exécuter le script Python
if "%AGENCE_ID%"=="" (
    py EXPORT_DONNEES_STANDALONE.py
) else (
    py EXPORT_DONNEES_STANDALONE.py --agence-id %AGENCE_ID%
)

REM Vérifier si l'export a réussi
set EXPORT_STATUS=%errorlevel%
if %EXPORT_STATUS% neq 0 (
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo   ❌ ERREUR: L'export a échoué (Code: %EXPORT_STATUS%)
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo Vérifiez:
    echo   - Que la base de données est accessible
    echo   - Que Django est correctement configuré
    echo   - Les messages d'erreur ci-dessus
    echo.
    pause
    exit /b %EXPORT_STATUS%
)

echo.
echo ═══════════════════════════════════════════════════════════
echo   ✅ EXPORT TERMINÉ AVEC SUCCÈS!
echo ═══════════════════════════════════════════════════════════
echo.

REM Chercher le fichier JSON créé
set JSON_FILE=
for /f "delims=" %%i in ('dir /b export_erp_standalone_*.json 2^>nul') do set JSON_FILE=%%i

if defined JSON_FILE (
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo   📁 FICHIER CRÉÉ
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo Nom du fichier: %JSON_FILE%
    echo.
    for %%A in ("%JSON_FILE%") do (
        set SIZE=%%~zA
        set /a SIZE_MB=!SIZE! / 1048576
        set /a SIZE_KB=(!SIZE! %% 1048576) / 1024
        echo Taille: !SIZE_MB! MB !SIZE_KB! KB
    )
    echo.
    echo 📍 Emplacement complet:
    echo    %CD%\%JSON_FILE%
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo.
) else (
    echo.
    echo ⚠ Avertissement: Fichier JSON non trouvé dans le répertoire actuel
    echo    Répertoire: %CD%
    echo.
)

echo ═══════════════════════════════════════════════════════════
echo   PROCHAINES ÉTAPES:
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Installer la nouvelle version avec fonctionnalité export/import
echo 2. Démarrer le serveur de la nouvelle version
echo 3. Aller sur: http://127.0.0.1:8000/supermarket/export-import/
echo 4. Cliquer sur "Importer des Données"
echo 5. Sélectionner le fichier JSON exporté
echo.
echo ═══════════════════════════════════════════════════════════
echo.

pause

