@echo off
title Supprimer Factures Agence
color 0C

echo ============================================
echo   SUPPRESSION DES FACTURES PAR AGENCE
echo ============================================
echo.

cd /d "%~dp0"

py --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python (py) introuvable sur ce poste.
    echo Veuillez installer Python ou ajouter py au PATH.
    echo.
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

py SUPPRIMER_FACTURES_AGENCE.py

echo.
echo ============================================
echo   Operation terminee.
echo ============================================
echo.
pause

