@echo off
chcp 65001 >nul
title Suppression des Articles d'une Agence

echo ============================================================
echo   SUPPRESSION DES ARTICLES D'UNE AGENCE
echo ============================================================
echo.

REM Vérifier que Python est installé
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo.
    pause
    exit /b 1
)

REM Vérifier que le script Python existe
if not exist "SUPPRIMER_ARTICLES_AGENCE.py" (
    echo [ERREUR] Le fichier SUPPRIMER_ARTICLES_AGENCE.py est introuvable
    echo.
    pause
    exit /b 1
)

REM Exécuter le script Python
echo Exécution du script...
echo.
py SUPPRIMER_ARTICLES_AGENCE.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Une erreur s'est produite lors de l'exécution
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Opération terminée
echo ============================================================
pause









