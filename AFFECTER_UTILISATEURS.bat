@echo off
title Affectation Utilisateurs aux Agences - ERP Supermarket
color 0B
cls

echo.
echo ========================================
echo   AFFECTATION UTILISATEURS AUX AGENCES
echo ========================================
echo.
echo Ce script va configurer les utilisateurs suivants :
echo.
echo GESTION CAISSE:
echo   - Constantine (caisseire1)  → MARCHE HUITIEME
echo   - Irene (caissier2)         → MARCHE ESSOS
echo   - Estelle (caisseire3)      → MARCHE VOTGBI
echo   - Marceline (caisier4)      → POISSONNERIE SANGAH
echo.
echo GESTION STOCK:
echo   - Brayan (comptable1)       → MARCHE HUITIEME
echo   - Gabriel (comptable2)      → MARCHE ESSOS
echo   - Michelle (comptable3)     → MARCHE VOTGBI
echo   - Brayan1 (comptable4)      → POISSONNERIE SANGAH
echo.
echo ========================================
echo.
pause

cd /d "%~dp0"

:: Trouver Python
set "PYTHON_CMD=py"
python --version >nul 2>&1
if %errorlevel% equ 0 set "PYTHON_CMD=python"

echo.
echo Lancement du script d'affectation...
echo.

%PYTHON_CMD% AFFECTER_UTILISATEURS_AGENCES.py

echo.
echo ========================================
echo.
pause




