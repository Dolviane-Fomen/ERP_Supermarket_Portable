@echo off
REM Script pour recuperer les modifications depuis GitHub

echo ========================================
echo Recuperation des modifications GitHub
echo ========================================
echo.

REM Verifier Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installe!
    pause
    exit /b 1
)

REM Verifier si on est dans un depot Git
if not exist ".git" (
    echo ERREUR: Ce n'est pas un depot Git!
    echo Vous devez d'abord cloner le projet depuis GitHub
    pause
    exit /b 1
)

echo Recuperation des modifications depuis GitHub...
echo.

REM Recuperer les modifications
git pull origin main

if errorlevel 1 (
    echo.
    echo ERREUR: Probleme lors de la recuperation
    echo Verifiez votre connexion internet et vos permissions
) else (
    echo.
    echo ========================================
    echo SUCCESS: Modifications recuperees!
    echo ========================================
)

echo.
pause

