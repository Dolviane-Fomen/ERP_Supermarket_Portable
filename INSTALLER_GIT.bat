@echo off
REM Script pour installer Git automatiquement sur Windows

echo ========================================
echo Installation de Git pour Windows
echo ========================================
echo.

REM Verifier si Git est deja installe
git --version >nul 2>&1
if not errorlevel 1 (
    echo.
    echo OK: Git est deja installe!
    git --version
    echo.
    pause
    exit /b 0
)

echo Git n'est pas installe sur ce PC.
echo.
echo Options d'installation:
echo.
echo 1. Installer Git automatiquement (Telechargement et installation)
echo 2. Ouvrir la page de telechargement de Git
echo 3. Installer GitHub Desktop (qui installe Git automatiquement)
echo.
set /p choix="Votre choix (1/2/3): "

if "%choix%"=="1" (
    echo.
    echo Telechargement de Git...
    echo.
    echo IMPORTANT: Cette option ouvre le site de telechargement.
    echo Vous devrez telecharger et installer Git manuellement.
    echo.
    start https://git-scm.com/download/win
    echo.
    echo Apres installation, fermez cette fenetre et relancez CONFIGURER_NOUVEAU_PC.bat
    pause
) else if "%choix%"=="2" (
    echo.
    echo Ouverture du site de telechargement Git...
    start https://git-scm.com/download/win
    echo.
    echo Apres installation, relancez CONFIGURER_NOUVEAU_PC.bat
    pause
) else if "%choix%"=="3" (
    echo.
    echo Ouverture du site de telechargement GitHub Desktop...
    start https://desktop.github.com/
    echo.
    echo GitHub Desktop installe Git automatiquement.
    echo Apres installation, relancez CONFIGURER_NOUVEAU_PC.bat
    pause
) else (
    echo.
    echo Choix invalide
    pause
)




