@echo off
title ERP Supermarket - Gestionnaire Réseau
color 0E
cls

:menu_loop
echo.
echo ========================================
echo.
echo       GESTIONNAIRE RÉSEAU ERP
echo       Système avec câbles réseau
echo.
echo ========================================
echo.
echo [1] Démarrer Station Principale (PC1)
echo [2] Démarrer Station Caisse (PC2)
echo [3] Démarrer Station Stock (PC3)
echo [4] Démarrer Station Comptabilité (PC4)
echo [5] Vérifier statut réseau
echo [6] Tester synchronisation
echo [7] Arrêter tous les serveurs
echo [8] Configuration réseau
echo [9] Aide
echo [0] Quitter
echo.
set /p choice="Votre choix (0-9): "

if "%choice%"=="1" call "ERP_PC1.bat"
if "%choice%"=="2" call "ERP_PC2.bat"
if "%choice%"=="3" call "ERP_PC3.bat"
if "%choice%"=="4" call "ERP_PC4.bat"
if "%choice%"=="5" goto :check_status
if "%choice%"=="6" goto :test_sync
if "%choice%"=="7" goto :stop_all
if "%choice%"=="8" goto :config_network
if "%choice%"=="9" goto :help
if "%choice%"=="0" exit

goto :menu_loop

:check_status
echo.
echo ========================================
echo       VÉRIFICATION STATUT RÉSEAU
echo ========================================
echo.
echo Vérification des connexions réseau...
echo.
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"Adresse IPv4"') do (
    set "LOCAL_IP=%%a"
    set "LOCAL_IP=!LOCAL_IP: =!"
    goto :ip_found
)
:ip_found
echo Adresse IP locale: %LOCAL_IP%
echo.
echo Test des ports réseau...
netstat -an | findstr :800
echo.
echo Test de connectivité...
ping -n 1 192.168.1.100 >nul 2>&1 && echo ✅ PC1 (192.168.1.100) - Accessible || echo ❌ PC1 (192.168.1.100) - Inaccessible
ping -n 1 192.168.1.101 >nul 2>&1 && echo ✅ PC2 (192.168.1.101) - Accessible || echo ❌ PC2 (192.168.1.101) - Inaccessible
ping -n 1 192.168.1.102 >nul 2>&1 && echo ✅ PC3 (192.168.1.102) - Accessible || echo ❌ PC3 (192.168.1.102) - Inaccessible
ping -n 1 192.168.1.103 >nul 2>&1 && echo ✅ PC4 (192.168.1.103) - Accessible || echo ❌ PC4 (192.168.1.103) - Inaccessible
echo.
pause
goto :menu_loop

:test_sync
echo.
echo ========================================
echo       TEST DE SYNCHRONISATION
echo ========================================
echo.
echo Test de synchronisation en cours...
echo.
py NETWORK_SYNC.py
echo.
pause
goto :menu_loop

:stop_all
echo.
echo Arrêt de tous les serveurs réseau...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM py.exe /T >nul 2>&1
echo Tous les serveurs arrêtés.
pause
goto :menu_loop

:config_network
echo.
echo ========================================
echo       CONFIGURATION RÉSEAU
echo ========================================
echo.
echo Configuration actuelle:
type network_sync\network_config.json
echo.
echo Pour modifier la configuration, éditez le fichier:
echo network_sync\network_config.json
echo.
pause
goto :menu_loop

:help
echo.
echo ========================================
echo       AIDE SYSTÈME RÉSEAU ERP
echo ========================================
echo.
echo ARCHITECTURE:
echo - Système distribué avec câbles réseau
echo - Synchronisation automatique des données
echo - Rôles: Master (PC1) et Slaves (PC2-4)
echo.
echo CONNEXIONS:
echo - PC1 (Master): 192.168.1.100:8001
echo - PC2 (Caisse): 192.168.1.101:8002
echo - PC3 (Stock): 192.168.1.102:8003
echo - PC4 (Compta): 192.168.1.103:8004
echo.
echo SYNCHRONISATION:
echo - Automatique toutes les 10 secondes
echo - Bidirectionnelle pour articles/stock
echo - Master vers Slave pour ventes
echo - Slave vers Master pour comptabilité
echo.
echo RÉSEAU:
echo - Utilise les câbles réseau existants
echo - Pas de serveur central requis
echo - Chaque station fonctionne indépendamment
echo.
pause
goto :menu_loop
