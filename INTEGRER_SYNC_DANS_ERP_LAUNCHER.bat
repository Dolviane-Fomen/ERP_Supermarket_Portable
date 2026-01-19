@echo off
REM Modifier ERP_Launcher.bat pour démarrer automatiquement la synchronisation

echo ========================================
echo INTEGRATION SYNC DANS ERP_LAUNCHER
echo ========================================
echo.
echo Ce script modifie ERP_Launcher.bat pour démarrer
echo automatiquement la synchronisation en arrière-plan.
echo.

REM Vérifier que ERP_Launcher.bat existe
if not exist "ERP_Launcher.bat" (
    echo [ERREUR] ERP_Launcher.bat introuvable
    pause
    exit /b 1
)

REM Créer une sauvegarde
if not exist "ERP_Launcher.bat.backup" (
    copy "ERP_Launcher.bat" "ERP_Launcher.bat.backup" >nul
    echo [OK] Sauvegarde créée: ERP_Launcher.bat.backup
)

echo.
echo Voulez-vous:
echo   1. Démarrer la sync automatique avec ERP_Launcher
echo   2. Annuler
echo.
set /p choix="Votre choix (1-2): "

if "%choix%"=="1" (
    echo.
    echo Modification de ERP_Launcher.bat...
    
    REM Ajouter le démarrage de la sync au début du script
    powershell -Command "$content = Get-Content 'ERP_Launcher.bat' -Raw; $syncCmd = '@echo off`r`nREM Démarrer la synchronisation automatique en arrière-plan`r`nstart /B py SYNC_AUTOMATIQUE_EN_ARRIERE_PLAN.py`r`n`r`n'; if ($content -notmatch 'SYNC_AUTOMATIQUE_EN_ARRIERE_PLAN') { $content = $syncCmd + $content; Set-Content 'ERP_Launcher.bat' -Value $content -NoNewline }"
    
    echo [OK] ERP_Launcher.bat modifié
    echo.
    echo La synchronisation démarrera automatiquement avec ERP_Launcher
    echo.
) else (
    echo.
    echo Opération annulée
)

pause
