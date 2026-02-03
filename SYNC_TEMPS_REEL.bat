@echo off
REM Script pour synchroniser en temps réel (seulement l'envoi des données locales)
REM Usage: SYNC_TEMPS_REEL.bat

echo ========================================
echo    SYNCHRONISATION TEMPS REEL
echo    (Envoi Local -^> Serveur)
echo ========================================
echo.
echo Ce script envoie vos données locales vers le serveur
echo sans télécharger les données du serveur.
echo.
echo Utile pour:
echo   - Envoyer les factures créées localement
echo   - Synchroniser le stock en temps réel
echo   - Mettre à jour les statistiques
echo.
pause

cd /d "%~dp0"

REM Détecter Python
set "PYTHON_CMD=py"
python --version >nul 2>&1
if %errorlevel% equ 0 set "PYTHON_CMD=python"

echo.
echo Envoi des données locales vers le serveur...
echo.

%PYTHON_CMD% SYNC_LOCAL_ONLINE.py --mode push --merge

if errorlevel 1 (
    echo.
    echo [ERREUR] L'envoi a echoue
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCES] Donnees locales envoyees au serveur
    pause
)
