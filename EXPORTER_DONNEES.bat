@echo off
REM ============================================
REM Script d'export des données ERP
REM Utilise EXPORT_DONNEES_STANDALONE.py
REM ============================================

echo.
echo ============================================
echo   EXPORT DES DONNEES ERP
echo ============================================
echo.

REM Vérifier si Python est installé
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python ou ajouter Python au PATH systeme
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Vérifier si le script Python existe
if not exist "EXPORT_DONNEES_STANDALONE.py" (
    echo [ERREUR] Le fichier EXPORT_DONNEES_STANDALONE.py est introuvable
    echo.
    echo Assurez-vous que le fichier est dans le meme repertoire que ce script .bat
    echo.
    pause
    exit /b 1
)

echo [OK] Script Python trouve
echo.

REM Afficher la liste des agences disponibles
echo ============================================
echo   Liste des Agences Disponibles
echo ============================================
echo.
py LISTER_AGENCES.py
if errorlevel 1 (
    echo.
    echo [AVERTISSEMENT] Impossible de lister les agences. Continuons quand meme...
    echo.
)

echo ============================================
echo   Demarrage de l'export...
echo ============================================
echo.

REM Demander l'ID de l'agence (optionnel)
set /p AGENCE_ID="Entrez l'ID de l'agence a exporter (ou appuyez sur Entree pour toutes les agences): "

REM Exécuter le script Python
if "%AGENCE_ID%"=="" (
    py EXPORT_DONNEES_STANDALONE.py
) else (
    py EXPORT_DONNEES_STANDALONE.py --agence-id %AGENCE_ID%
)

REM Vérifier si l'export a réussi
if errorlevel 1 (
    echo.
    echo ============================================
    echo   [ERREUR] L'export a echoue
    echo ============================================
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Export termine avec succes!
echo ============================================
echo.
echo Le fichier JSON a ete cree dans le repertoire actuel.
echo Vous pouvez maintenant l'importer dans la nouvelle version.
echo.
pause

