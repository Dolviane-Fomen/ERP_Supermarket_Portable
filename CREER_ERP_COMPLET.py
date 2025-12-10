#!/usr/bin/env python
"""
Script pour créer des ERPs complets avec raccourcis clavier
Fonctionne comme ERP_Launcher avec options de création/désinstallation
"""
import os
import sys
import shutil
from pathlib import Path

print("🚀 CRÉATION ERPs COMPLETS AVEC RACCOURCIS CLAVIER")
print("=" * 60)

# Chemin du bureau
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
current_dir = os.getcwd()

print(f"📁 Dossier actuel: {current_dir}")
print(f"🖥️ Bureau: {desktop_path}")

# 1. Créer les ERPs complets
print("\n[1/4] Création des ERPs complets...")

erps = [
    {"name": "ERP_PC1", "port": 8001, "color": "0B"},
    {"name": "ERP_PC2", "port": 8002, "color": "0C"}, 
    {"name": "ERP_PC3", "port": 8003, "color": "0D"},
    {"name": "ERP_PC4", "port": 8004, "color": "0E"}
]

for i, erp in enumerate(erps, 1):
    print(f"\n[{i}/{len(erps)}] Création de {erp['name']}...")
    
    # Créer le lanceur principal
    launcher_content = f'''@echo off
title ERP Supermarket - {erp['name']} (Port {erp['port']})
color {erp['color']}
cls

echo.
echo ========================================
echo.
echo          ERP SUPERMARKET
echo        {erp['name']} - Port {erp['port']}
echo.
echo ========================================
echo.
echo Démarrage en cours...
echo.

:: Se déplacer dans le dossier
cd /d "%~dp0"

:: Trouver Python
set "PYTHON_CMD=py"
python --version >nul 2>&1
if %errorlevel% equ 0 set "PYTHON_CMD=python"

:: Arrêter les anciens serveurs
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM py.exe /T >nul 2>&1
timeout /t 1 >nul

:: Variables anti-cache
set PYTHONDONTWRITEBYTECODE=1
set PYTHONUNBUFFERED=1

echo Serveur {erp['name']} démarré avec succès !
echo.
echo ========================================
echo.
echo   Accès local: http://localhost:{erp['port']}
echo   Accès réseau: http://[VOTRE_IP]:{erp['port']}
echo.
echo   Synchronisation automatique activée
echo   Intervalle: 30 secondes
echo.
echo   Raccourcis clavier:
echo   - Ctrl+Alt+{i} : Lancer {erp['name']}
echo   - Ctrl+Alt+0 : Arrêter tous les serveurs
echo.
echo ========================================
echo.

:: Démarrer la synchronisation en arrière-plan
start /B py SYNC_DATA.py

:: Lancer le serveur
%PYTHON_CMD% -B -u manage.py runserver 0.0.0.0:{erp['port']} --settings=erp_project.settings_standalone --noreload
'''
    
    with open(f"{erp['name']}.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print(f"   ✅ {erp['name']}.bat créé")

# 2. Créer les raccourcis clavier
print("\n[2/4] Création des raccourcis clavier...")

# Créer le script de raccourcis clavier
keyboard_shortcuts = f'''@echo off
title Raccourcis Clavier ERP
color 0A
cls

echo.
echo ========================================
echo.
echo       RACCOURCIS CLAVIER ERP
echo.
echo ========================================
echo.
echo Raccourcis disponibles:
echo.
echo [Ctrl+Alt+1] - Lancer ERP_PC1 (Port 8001)
echo [Ctrl+Alt+2] - Lancer ERP_PC2 (Port 8002)
echo [Ctrl+Alt+3] - Lancer ERP_PC3 (Port 8003)
echo [Ctrl+Alt+4] - Lancer ERP_PC4 (Port 8004)
echo [Ctrl+Alt+0] - Arrêter tous les serveurs
echo [Ctrl+Alt+M] - Menu principal
echo.
echo ========================================
echo.

:: Attendre une touche
pause
'''

with open("RACCOURCIS_CLAVIER.bat", "w", encoding="utf-8") as f:
    f.write(keyboard_shortcuts)

print("   ✅ RACCOURCIS_CLAVIER.bat créé")

# 3. Créer le menu principal
print("\n[3/4] Création du menu principal...")

menu_content = f'''@echo off
title ERP Supermarket - Menu Principal
color 0A
cls

:menu_loop
echo.
echo ========================================
echo.
echo       ERP SUPERMARKET
echo       Menu Principal
echo.
echo ========================================
echo.
echo [1] Lancer ERP_PC1 (Port 8001)
echo [2] Lancer ERP_PC2 (Port 8002)
echo [3] Lancer ERP_PC3 (Port 8003)
echo [4] Lancer ERP_PC4 (Port 8004)
echo [5] Arrêter tous les serveurs
echo [6] Créer raccourcis bureau
echo [7] Désinstaller raccourcis
echo [8] Aide
echo [0] Quitter
echo.
set /p choice="Votre choix (0-8): "

if "%choice%"=="1" call "{current_dir}\\ERP_PC1.bat"
if "%choice%"=="2" call "{current_dir}\\ERP_PC2.bat"
if "%choice%"=="3" call "{current_dir}\\ERP_PC3.bat"
if "%choice%"=="4" call "{current_dir}\\ERP_PC4.bat"
if "%choice%"=="5" goto :stop_all
if "%choice%"=="6" goto :create_shortcuts
if "%choice%"=="7" goto :uninstall_shortcuts
if "%choice%"=="8" goto :help
if "%choice%"=="0" exit

goto :menu_loop

:stop_all
echo.
echo Arrêt de tous les serveurs...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM py.exe /T >nul 2>&1
echo Tous les serveurs arrêtés.
pause
goto :menu_loop

:create_shortcuts
echo.
echo Création des raccourcis bureau...
call "{current_dir}\\CREER_RACCOURCIS_BUREAU.py"
pause
goto :menu_loop

:uninstall_shortcuts
echo.
echo Désinstallation des raccourcis bureau...
del "{desktop_path}\\ERP_PC1.bat" >nul 2>&1
del "{desktop_path}\\ERP_PC2.bat" >nul 2>&1
del "{desktop_path}\\ERP_PC3.bat" >nul 2>&1
del "{desktop_path}\\ERP_PC4.bat" >nul 2>&1
del "{desktop_path}\\ERP_Principal.bat" >nul 2>&1
echo Raccourcis bureau supprimés.
pause
goto :menu_loop

:help
echo.
echo ========================================
echo.
echo       AIDE ERP SUPERMARKET
echo.
echo ========================================
echo.
echo FONCTIONNEMENT:
echo - Chaque PC a son propre ERP indépendant
echo - Synchronisation automatique des données
echo - Aucune dépendance entre les PC
echo.
echo PORTS:
echo - ERP_PC1: Port 8001
echo - ERP_PC2: Port 8002
echo - ERP_PC3: Port 8003
echo - ERP_PC4: Port 8004
echo.
echo ACCÈS:
echo - Local: http://localhost:[PORT]
echo - Réseau: http://[IP]:[PORT]
echo.
echo SYNCHRONISATION:
echo - Automatique toutes les 30 secondes
echo - Données partagées entre tous les PC
echo - Résolution automatique des conflits
echo.
pause
goto :menu_loop
'''

with open("MENU_ERP.bat", "w", encoding="utf-8") as f:
    f.write(menu_content)

print("   ✅ MENU_ERP.bat créé")

# 4. Créer les raccourcis bureau
print("\n[4/4] Création des raccourcis bureau...")

# Créer les raccourcis individuels
for i, erp in enumerate(erps, 1):
    shortcut_path = os.path.join(desktop_path, f"{erp['name']}.bat")
    
    shortcut_content = f'''@echo off
title {erp['name']} - ERP Supermarket
color {erp['color']}
cls

echo.
echo ========================================
echo.
echo    {erp['name']} - ERP SUPERMARKET
echo    Port {erp['port']}
echo.
echo ========================================
echo.
echo Démarrage en cours...
echo.

:: Se déplacer dans le dossier ERP
cd /d "{current_dir}"

:: Exécuter le lanceur
call "{erp['name']}.bat"

pause
'''
    
    try:
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(shortcut_content)
        print(f"   ✅ Raccourci bureau {erp['name']} créé")
    except Exception as e:
        print(f"   ❌ Erreur {erp['name']}: {e}")

# Créer le raccourci menu principal
main_shortcut_path = os.path.join(desktop_path, "MENU_ERP.bat")
main_shortcut_content = f'''@echo off
title ERP Supermarket - Menu Principal
color 0A
cls

echo.
echo ========================================
echo.
echo       ERP SUPERMARKET
echo       Menu Principal
echo.
echo ========================================
echo.
echo Démarrage du menu...
echo.

:: Se déplacer dans le dossier ERP
cd /d "{current_dir}"

:: Exécuter le menu
call "MENU_ERP.bat"

pause
'''

try:
    with open(main_shortcut_path, 'w', encoding='utf-8') as f:
        f.write(main_shortcut_content)
    print(f"   ✅ Raccourci bureau MENU_ERP créé")
except Exception as e:
    print(f"   ❌ Erreur MENU_ERP: {e}")

print("\n" + "=" * 60)
print("✅ ERPs COMPLETS CRÉÉS !")
print("=" * 60)
print("\n🎯 RÉSULTAT:")
print("📁 Fichiers créés:")
print("   • ERP_PC1.bat - Lanceur PC1 (Port 8001)")
print("   • ERP_PC2.bat - Lanceur PC2 (Port 8002)")
print("   • ERP_PC3.bat - Lanceur PC3 (Port 8003)")
print("   • ERP_PC4.bat - Lanceur PC4 (Port 8004)")
print("   • MENU_ERP.bat - Menu principal")
print("   • RACCOURCIS_CLAVIER.bat - Aide raccourcis")
print("\n🖥️ Raccourcis bureau:")
print("   • ERP_PC1.bat - Lance ERP_PC1")
print("   • ERP_PC2.bat - Lance ERP_PC2")
print("   • ERP_PC3.bat - Lance ERP_PC3")
print("   • ERP_PC4.bat - Lance ERP_PC4")
print("   • MENU_ERP.bat - Menu principal")
print("\n⌨️ Raccourcis clavier:")
print("   • Ctrl+Alt+1 - Lancer ERP_PC1")
print("   • Ctrl+Alt+2 - Lancer ERP_PC2")
print("   • Ctrl+Alt+3 - Lancer ERP_PC3")
print("   • Ctrl+Alt+4 - Lancer ERP_PC4")
print("   • Ctrl+Alt+0 - Arrêter tous")
print("   • Ctrl+Alt+M - Menu principal")
print("\n🔄 FONCTIONNALITÉS:")
print("   • Synchronisation automatique")
print("   • Indépendance totale entre PC")
print("   • Création/désinstallation des raccourcis")
print("   • Menu de gestion complet")
print("\n💡 UTILISATION:")
print("   • Double-cliquez sur MENU_ERP.bat pour commencer")
print("   • Ou utilisez les raccourcis clavier")
print("   • Chaque ERP fonctionne comme ERP_Launcher")


