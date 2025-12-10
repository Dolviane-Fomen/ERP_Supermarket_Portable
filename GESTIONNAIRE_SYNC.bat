@echo off
title Gestionnaire Synchronisation ERP_Launcher
color 0E
cls

:menu_loop
echo.
echo ========================================
echo.
echo    GESTIONNAIRE SYNCHRONISATION
echo    ERP_Launcher avec réseau
echo.
echo ========================================
echo.
echo [1] Démarrer ERP_Launcher avec sync
echo [2] Démarrer ERP_Launcher sans sync
echo [3] Vérifier statut synchronisation
echo [4] Tester connexions réseau
echo [5] Arrêter synchronisation
echo [6] Configuration réseau
echo [7] Restaurer ERP_Launcher original
echo [8] Aide
echo [0] Quitter
echo.
set /p choice="Votre choix (0-8): "

if "%choice%"=="1" goto :start_with_sync
if "%choice%"=="2" goto :start_without_sync
if "%choice%"=="3" goto :check_sync_status
if "%choice%"=="4" goto :test_network
if "%choice%"=="5" goto :stop_sync
if "%choice%"=="6" goto :config_network
if "%choice%"=="7" goto :restore_original
if "%choice%"=="8" goto :help
if "%choice%"=="0" exit

goto :menu_loop

:start_with_sync
echo.
echo Démarrage d'ERP_Launcher avec synchronisation...
call "ERP_Launcher.bat"
goto :menu_loop

:start_without_sync
echo.
echo Démarrage d'ERP_Launcher sans synchronisation...
call "ERP_Launcher_ORIGINAL.bat"
goto :menu_loop

:check_sync_status
echo.
echo ========================================
echo       STATUT SYNCHRONISATION
echo ========================================
echo.
echo Vérification des processus de synchronisation...
tasklist | findstr python
echo.
echo Vérification des connexions réseau...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"Adresse IPv4"') do (
    set "LOCAL_IP=%%a"
    set "LOCAL_IP=!LOCAL_IP: =!"
    goto :ip_found
)
:ip_found
echo Adresse IP locale: %LOCAL_IP%
echo.
echo Test des connexions ERP_Launcher...
ping -n 1 192.168.1.100 >nul 2>&1 && echo ✅ PC1 (192.168.1.100) - Accessible || echo ❌ PC1 (192.168.1.100) - Inaccessible
ping -n 1 192.168.1.101 >nul 2>&1 && echo ✅ PC2 (192.168.1.101) - Accessible || echo ❌ PC2 (192.168.1.101) - Inaccessible
ping -n 1 192.168.1.102 >nul 2>&1 && echo ✅ PC3 (192.168.1.102) - Accessible || echo ❌ PC3 (192.168.1.102) - Inaccessible
ping -n 1 192.168.1.103 >nul 2>&1 && echo ✅ PC4 (192.168.1.103) - Accessible || echo ❌ PC4 (192.168.1.103) - Inaccessible
echo.
pause
goto :menu_loop

:test_network
echo.
echo ========================================
echo       TEST RÉSEAU ERP_LAUNCHER
echo ========================================
echo.
echo Test de connectivité avec les autres PC...
echo.
echo Test des ports 8000 (ERP_Launcher)...
netstat -an | findstr :8000
echo.
echo Test de synchronisation...
py ERP_LAUNCHER_SYNC.py
echo.
pause
goto :menu_loop

:stop_sync
echo.
echo Arrêt de la synchronisation...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM py.exe /T >nul 2>&1
echo Synchronisation arrêtée.
pause
goto :menu_loop

:config_network
echo.
echo ========================================
echo       CONFIGURATION RÉSEAU
echo ========================================
echo.
echo Configuration actuelle:
type erp_sync\erp_launcher_config.json
echo.
echo Pour modifier la configuration, éditez le fichier:
echo erp_sync\erp_launcher_config.json
echo.
pause
goto :menu_loop

:restore_original
echo.
echo Restauration d'ERP_Launcher original...
if exist "ERP_Launcher_ORIGINAL.bat" (
    copy "ERP_Launcher_ORIGINAL.bat" "ERP_Launcher.bat" >nul
    echo ERP_Launcher restauré à sa version originale.
) else (
    echo Fichier original non trouvé.
)
pause
goto :menu_loop

:help
echo.
echo ========================================
echo       AIDE SYNCHRONISATION ERP_LAUNCHER
echo ========================================
echo.
echo FONCTIONNEMENT:
echo - Tous les PC utilisent ERP_Launcher.bat
echo - Synchronisation automatique des données
echo - Communication via réseau local
echo.
echo CONFIGURATION:
echo - PC1: 192.168.1.100:8000
echo - PC2: 192.168.1.101:8000
echo - PC3: 192.168.1.102:8000
echo - PC4: 192.168.1.103:8000
echo.
echo SYNCHRONISATION:
echo - Automatique toutes les 15 secondes
echo - Toutes les données synchronisées
echo - Chaque PC garde sa base locale
echo.
echo UTILISATION:
echo - Utilisez ERP_Launcher.bat normalement
echo - La synchronisation se fait en arrière-plan
echo - Pas de changement dans l'utilisation
echo.
pause
goto :menu_loop
