@echo off
REM Script pour copier uniquement les fichiers de synchronisation
REM A utiliser si les autres PCs ont deja l'ERP installe

setlocal enabledelayedexpansion

echo ========================================
echo COPIE DES FICHIERS DE SYNCHRONISATION
echo ========================================
echo.
echo Ce script copie uniquement les fichiers necessaires
echo pour la synchronisation, pas tout le projet ERP.
echo.

REM Demander le chemin de destination
set /p DEST_PATH="Entrez le chemin du dossier ERP sur l'autre PC (ex: C:\ERP_Supermarket_Portable): "

if not exist "!DEST_PATH!" (
    echo.
    echo [ERREUR] Le chemin specifie n'existe pas: !DEST_PATH!
    pause
    exit /b 1
)

echo.
echo Copie des fichiers de synchronisation vers: !DEST_PATH!
echo.

REM Liste des fichiers a copier
set FICHIERS_SYNC=SYNC_LOCAL_ONLINE.py
set FICHIERS_SYNC=!FICHIERS_SYNC! SYNC_LOCAL_ONLINE.bat
set FICHIERS_SYNC=!FICHIERS_SYNC! SYNC_DONNEES_BIDIRECTIONNEL.bat
set FICHIERS_SYNC=!FICHIERS_SYNC! sync_donnees_bidirectionnel.ps1
set FICHIERS_SYNC=!FICHIERS_SYNC! CONFIGURER_SYNC_AUTOMATIQUE.bat
set FICHIERS_SYNC=!FICHIERS_SYNC! CONFIGURER_SYNC_AUTOMATIQUE.ps1
set FICHIERS_SYNC=!FICHIERS_SYNC! CONFIGURER_SYNC_AUTOMATIQUE_TOUS_PC.bat

REM Copier les fichiers
for %%f in (!FICHIERS_SYNC!) do (
    if exist "%%f" (
        copy "%%f" "!DEST_PATH!\" >nul
        if !ERRORLEVEL! EQU 0 (
            echo [OK] Copie: %%f
        ) else (
            echo [ERREUR] Echec copie: %%f
        )
    ) else (
        echo [ATTENTION] Fichier introuvable: %%f
    )
)

REM Copier .ovh_config.json si existe
if exist ".ovh_config.json" (
    copy ".ovh_config.json" "!DEST_PATH!\" >nul
    if !ERRORLEVEL! EQU 0 (
        echo [OK] Copie: .ovh_config.json
    )
)

REM Copier .ovh_config.example.json si existe
if exist ".ovh_config.example.json" (
    copy ".ovh_config.example.json" "!DEST_PATH!\" >nul
    if !ERRORLEVEL! EQU 0 (
        echo [OK] Copie: .ovh_config.example.json
    )
)

echo.
echo ========================================
echo COPIE TERMINEE
echo ========================================
echo.
echo Fichiers copies vers: !DEST_PATH!
echo.
echo Sur l'autre PC, executez:
echo   CONFIGURER_SYNC_AUTOMATIQUE_TOUS_PC.bat
echo.
pause
