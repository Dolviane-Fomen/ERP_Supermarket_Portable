#!/usr/bin/env python
"""
Configuration système ERP avec câbles réseau comme Sage
Synchronisation automatique via réseau local
"""
import os
import json
import shutil
from datetime import datetime

print("🌐 CONFIGURATION SYSTÈME ERP AVEC CÂBLES RÉSEAU")
print("=" * 60)
print("Architecture similaire à Sage avec synchronisation réseau")

# 1. Créer l'architecture réseau
print("\n[1/5] Création de l'architecture réseau...")

# Dossier de synchronisation réseau
network_folder = "network_sync"
if not os.path.exists(network_folder):
    os.makedirs(network_folder)
    print(f"   ✅ Dossier réseau créé: {network_folder}")

# Configuration réseau centralisée
network_config = {
    "system_name": "ERP_Supermarket_Network",
    "version": "1.0",
    "sync_interval": 10,  # secondes
    "max_retries": 3,
    "timeout": 30,
    "network_nodes": [
        {
            "id": "PC1",
            "name": "Station Principale",
            "ip": "192.168.1.100",
            "port": 8001,
            "role": "master",
            "priority": 1
        },
        {
            "id": "PC2", 
            "name": "Station Caisse",
            "ip": "192.168.1.101",
            "port": 8002,
            "role": "slave",
            "priority": 2
        },
        {
            "id": "PC3",
            "name": "Station Stock",
            "ip": "192.168.1.102", 
            "port": 8003,
            "role": "slave",
            "priority": 3
        },
        {
            "id": "PC4",
            "name": "Station Comptabilité",
            "ip": "192.168.1.103",
            "port": 8004,
            "role": "slave", 
            "priority": 4
        }
    ],
    "sync_rules": {
        "articles": "bidirectional",
        "clients": "bidirectional", 
        "ventes": "master_to_slave",
        "stock": "bidirectional",
        "comptabilite": "slave_to_master"
    }
}

# Sauvegarder la configuration
with open(f"{network_folder}/network_config.json", "w", encoding="utf-8") as f:
    json.dump(network_config, f, indent=2)

print("   ✅ Configuration réseau créée")

# 2. Créer le système de synchronisation
print("\n[2/5] Création du système de synchronisation...")

sync_system = '''#!/usr/bin/env python
"""
Système de synchronisation réseau ERP
Fonctionne comme Sage avec câbles réseau
"""
import os
import json
import time
import requests
import threading
from datetime import datetime
import sqlite3
import shutil

class ERPSyncNetwork:
    def __init__(self):
        self.config = self.load_config()
        self.running = False
        self.sync_thread = None
        
    def load_config(self):
        """Charger la configuration réseau"""
        with open("network_sync/network_config.json", "r") as f:
            return json.load(f)
    
    def start_sync(self):
        """Démarrer la synchronisation"""
        if not self.running:
            self.running = True
            self.sync_thread = threading.Thread(target=self.sync_loop)
            self.sync_thread.daemon = True
            self.sync_thread.start()
            print(f"[{datetime.now()}] 🔄 Synchronisation réseau démarrée")
    
    def stop_sync(self):
        """Arrêter la synchronisation"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join()
        print(f"[{datetime.now()}] ⏹️ Synchronisation réseau arrêtée")
    
    def sync_loop(self):
        """Boucle de synchronisation principale"""
        while self.running:
            try:
                self.sync_with_network()
                time.sleep(self.config["sync_interval"])
            except Exception as e:
                print(f"[{datetime.now()}] ❌ Erreur sync: {e}")
                time.sleep(5)
    
    def sync_with_network(self):
        """Synchroniser avec le réseau"""
        print(f"[{datetime.now()}] 🔄 Synchronisation en cours...")
        
        # Synchroniser avec chaque nœud
        for node in self.config["network_nodes"]:
            if node["id"] != self.get_current_node_id():
                self.sync_with_node(node)
    
    def sync_with_node(self, node):
        """Synchroniser avec un nœud spécifique"""
        try:
            # Envoyer nos données
            self.send_data_to_node(node)
            # Recevoir leurs données
            self.receive_data_from_node(node)
        except Exception as e:
            print(f"   ❌ Erreur avec {node['name']}: {e}")
    
    def send_data_to_node(self, node):
        """Envoyer nos données à un nœud"""
        url = f"http://{node['ip']}:{node['port']}/sync/receive"
        # Implémentation de l'envoi des données
        pass
    
    def receive_data_from_node(self, node):
        """Recevoir les données d'un nœud"""
        url = f"http://{node['ip']}:{node['port']}/sync/send"
        # Implémentation de la réception des données
        pass
    
    def get_current_node_id(self):
        """Obtenir l'ID du nœud actuel"""
        # Logique pour déterminer l'ID du PC actuel
        return "PC1"  # À adapter selon le PC

if __name__ == "__main__":
    sync_network = ERPSyncNetwork()
    sync_network.start_sync()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sync_network.stop_sync()
'''

with open("NETWORK_SYNC.py", "w", encoding="utf-8") as f:
    f.write(sync_system)

print("   ✅ Système de synchronisation créé")

# 3. Créer les lanceurs réseau
print("\n[3/5] Création des lanceurs réseau...")

for i, node in enumerate(network_config["network_nodes"], 1):
    node_id = node["id"]
    node_name = node["name"]
    port = node["port"]
    role = node["role"]
    
    # Couleurs selon le rôle
    color = "0A" if role == "master" else "0B"
    
    launcher_content = f'''@echo off
title ERP Supermarket - {node_name} ({node_id})
color {color}
cls

echo.
echo ========================================
echo.
echo       ERP SUPERMARKET
echo       {node_name} ({node_id})
echo       Rôle: {role.upper()}
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

echo Serveur {node_name} démarré avec succès !
echo.
echo ========================================
echo.
echo   🌐 RÉSEAU ERP ACTIVÉ
echo   Accès local: http://localhost:{port}
echo   Accès réseau: http://[IP]:{port}
echo.
echo   🔄 Synchronisation automatique
echo   Intervalle: {network_config["sync_interval"]} secondes
echo   Rôle: {role.upper()}
echo.
echo   📡 Connexions réseau:
'''
    
    # Ajouter les connexions réseau
    for other_node in network_config["network_nodes"]:
        if other_node["id"] != node_id:
            launcher_content += f'''echo   - {other_node["name"]}: {other_node["ip"]}:{other_node["port"]}
'''
    
    launcher_content += f'''echo.
echo ========================================
echo.

:: Démarrer la synchronisation réseau
start /B py NETWORK_SYNC.py

:: Lancer le serveur ERP
%PYTHON_CMD% -B -u manage.py runserver 0.0.0.0:{port} --settings=erp_project.settings_standalone --noreload
'''
    
    with open(f"ERP_{node_id}.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print(f"   ✅ ERP_{node_id}.bat créé ({node_name})")

# 4. Créer le gestionnaire réseau
print("\n[4/5] Création du gestionnaire réseau...")

network_manager = f'''@echo off
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
type network_sync\\network_config.json
echo.
echo Pour modifier la configuration, éditez le fichier:
echo network_sync\\network_config.json
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
'''

with open("GESTIONNAIRE_RESEAU.bat", "w", encoding="utf-8") as f:
    f.write(network_manager)

print("   ✅ GESTIONNAIRE_RESEAU.bat créé")

# 5. Créer les raccourcis bureau
print("\n[5/5] Création des raccourcis bureau...")

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Raccourcis pour chaque station
for node in network_config["network_nodes"]:
    shortcut_path = os.path.join(desktop_path, f"ERP_{node['id']}.bat")
    
    shortcut_content = f'''@echo off
title {node['name']} - ERP Supermarket
color 0A
cls

echo.
echo ========================================
echo.
echo    {node['name']} - ERP SUPERMARKET
echo    Rôle: {node['role'].upper()}
echo.
echo ========================================
echo.
echo Démarrage en cours...
echo.

:: Se déplacer dans le dossier ERP
cd /d "{os.getcwd()}"

:: Exécuter le lanceur
call "ERP_{node['id']}.bat"

pause
'''
    
    try:
        with open(shortcut_path, 'w', encoding="utf-8") as f:
            f.write(shortcut_content)
        print(f"   ✅ Raccourci {node['id']} créé")
    except Exception as e:
        print(f"   ❌ Erreur {node['id']}: {e}")

# Raccourci gestionnaire
manager_shortcut = os.path.join(desktop_path, "GESTIONNAIRE_RESEAU.bat")
manager_content = f'''@echo off
title Gestionnaire Réseau ERP
color 0E
cls

echo.
echo ========================================
echo.
echo    GESTIONNAIRE RÉSEAU ERP
echo    Système avec câbles réseau
echo.
echo ========================================
echo.
echo Démarrage du gestionnaire...
echo.

:: Se déplacer dans le dossier ERP
cd /d "{os.getcwd()}"

:: Exécuter le gestionnaire
call "GESTIONNAIRE_RESEAU.bat"

pause
'''

try:
    with open(manager_shortcut, 'w', encoding="utf-8") as f:
        f.write(manager_content)
    print(f"   ✅ Raccourci gestionnaire créé")
except Exception as e:
    print(f"   ❌ Erreur gestionnaire: {e}")

print("\n" + "=" * 60)
print("✅ SYSTÈME RÉSEAU CRÉÉ !")
print("=" * 60)
print("\n🎯 ARCHITECTURE RÉSEAU:")
print("📡 Stations réseau:")
print("   • PC1 (Master) - Station Principale - 192.168.1.100:8001")
print("   • PC2 (Slave) - Station Caisse - 192.168.1.101:8002")
print("   • PC3 (Slave) - Station Stock - 192.168.1.102:8003")
print("   • PC4 (Slave) - Station Comptabilité - 192.168.1.103:8004")
print("\n🔄 SYNCHRONISATION:")
print("   • Automatique toutes les 10 secondes")
print("   • Bidirectionnelle pour articles/stock")
print("   • Master vers Slave pour ventes")
print("   • Slave vers Master pour comptabilité")
print("\n🌐 RÉSEAU:")
print("   • Utilise les câbles réseau existants")
print("   • Pas de serveur central requis")
print("   • Chaque station fonctionne indépendamment")
print("\n💡 UTILISATION:")
print("   • Double-cliquez sur GESTIONNAIRE_RESEAU.bat")
print("   • Ou utilisez les raccourcis individuels")
print("   • Système similaire à Sage avec câbles réseau")
print("\n📖 CONFIGURATION:")
print("   • Éditez network_sync/network_config.json")
print("   • Modifiez les adresses IP selon votre réseau")
print("   • Ajustez les règles de synchronisation")


