@echo off
REM Script pour configurer la synchronisation sur un nouveau PC

echo ========================================
echo Configuration Synchronisation OVH
echo ========================================
echo.

REM Verifier si on est dans le bon dossier
if not exist "sync_ovh.ps1" (
    echo ERREUR: Ce script doit etre execute dans le dossier ERP_Supermarket_Portable
    echo.
    pause
    exit /b 1
)

REM Creer le fichier .ovh_config.json depuis l'exemple
if exist ".ovh_config.example.json" (
    if not exist ".ovh_config.json" (
        copy ".ovh_config.example.json" ".ovh_config.json" >nul
        echo OK: Fichier .ovh_config.json cree!
        echo.
        echo Veuillez maintenant:
        echo 1. Ouvrir .ovh_config.json
        echo 2. Verifier que les informations sont correctes
        echo    (IP, utilisateur, chemin du projet)
        echo.
    ) else (
        echo ATTENTION: .ovh_config.json existe deja
        echo Voulez-vous le remplacer? (o/n)
        set /p replace="> "
        if /i "%replace%"=="o" (
            copy ".ovh_config.example.json" ".ovh_config.json" >nul
            echo OK: Fichier .ovh_config.json mis a jour!
        )
    )
) else (
    echo ERREUR: Fichier .ovh_config.example.json introuvable
)

echo.
echo ========================================
echo Configuration terminee!
echo ========================================
echo.
echo Vous pouvez maintenant utiliser SYNC_OVH.bat pour synchroniser
echo.
pause




