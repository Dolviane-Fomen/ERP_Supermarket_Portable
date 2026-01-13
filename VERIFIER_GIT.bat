@echo off
REM Script pour verifier si Git est installe

echo ========================================
echo Verification de Git
echo ========================================
echo.

REM Verifier Git en ligne de commande
git --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installe!
    echo.
    echo Pour installer Git:
    echo   1. Double-cliquez sur INSTALLER_GIT.bat
    echo   2. Ou telechargez depuis: https://git-scm.com/download/win
    echo   3. Ou installez GitHub Desktop: https://desktop.github.com/
    echo.
    echo GitHub Desktop installe Git automatiquement.
    echo.
    pause
    exit /b 1
) else (
    echo OK: Git est installe!
    echo.
    git --version
    echo.
    echo Vous pouvez maintenant utiliser:
    echo   - SYNC_OVH.bat pour synchroniser
    echo   - RECUPERER_MODIFICATIONS.bat pour recuperer les modifications
    echo   - CONFIGURER_NOUVEAU_PC.bat pour configurer
    echo.
    pause
    exit /b 0
)




