@echo off
REM Script pour vérifier que les factures sont bien synchronisées sur le serveur
REM Usage: VERIFIER_SYNCHRONISATION.bat

echo ========================================
echo    VERIFICATION DE LA SYNCHRONISATION
echo    Agence: MARCHE HUITIEME
echo ========================================
echo.
echo Ce script compare les factures locales de l'agence MARCHE HUITIEME
echo avec celles du serveur pour verifier que la synchronisation fonctionne.
echo.
pause

cd /d "%~dp0"

REM Détecter Python
set "PYTHON_CMD=py"
python --version >nul 2>&1
if %errorlevel% equ 0 set "PYTHON_CMD=python"

echo.
echo Verification en cours pour l'agence MARCHE HUITIEME...
echo.

%PYTHON_CMD% VERIFIER_SYNCHRONISATION.py --agence "MARCHE HUITIEME"

if errorlevel 1 (
    echo.
    echo [ATTENTION] Certaines factures ne sont pas encore synchronisees
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCES] Toutes les factures sont synchronisees!
    pause
)
