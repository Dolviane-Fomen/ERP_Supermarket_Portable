@echo off
REM Script pour configurer l'authentification Git avec GitHub Desktop

echo ========================================
echo Configuration Authentification Git
echo ========================================
echo.

REM Verifier si Git est installe
git --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installe!
    pause
    exit /b 1
)

echo Configuration de Git pour utiliser GitHub Desktop...
echo.

REM Configurer Git Credential Manager pour utiliser GitHub Desktop
git config --global credential.helper manager

echo.
echo OK: Git est maintenant configure pour utiliser GitHub Desktop
echo.
echo Prochaines etapes:
echo 1. Quand Git demandera une authentification
echo 2. Choisissez "Sign in with your browser"
echo 3. Ou utilisez votre token GitHub
echo.
echo Pour tester, essayez: git push origin main
echo.

pause

