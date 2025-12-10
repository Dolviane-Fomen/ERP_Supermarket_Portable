#!/usr/bin/env python
"""
Script pour créer des raccourcis bureau pour chaque ERP
"""
import os
import sys
from pathlib import Path

print("🖥️ CRÉATION DES RACCOURCIS BUREAU")
print("=" * 50)

# Chemin du bureau
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
current_dir = os.getcwd()

print(f"📁 Dossier actuel: {current_dir}")
print(f"🖥️ Bureau: {desktop_path}")

# Liste des ERPs à créer
erps = [
    {
        "name": "ERP_PC1",
        "file": "ERP_PC1.bat",
        "port": 8001,
        "description": "ERP Supermarket - PC1 (Port 8001)"
    },
    {
        "name": "ERP_PC2", 
        "file": "ERP_PC2.bat",
        "port": 8002,
        "description": "ERP Supermarket - PC2 (Port 8002)"
    },
    {
        "name": "ERP_PC3",
        "file": "ERP_PC3.bat", 
        "port": 8003,
        "description": "ERP Supermarket - PC3 (Port 8003)"
    },
    {
        "name": "ERP_PC4",
        "file": "ERP_PC4.bat",
        "port": 8004, 
        "description": "ERP Supermarket - PC4 (Port 8004)"
    }
]

print(f"\n📋 Création de {len(erps)} raccourcis bureau...")

# Créer les raccourcis
for i, erp in enumerate(erps, 1):
    print(f"\n[{i}/{len(erps)}] Création du raccourci: {erp['name']}")
    
    # Vérifier que le fichier .bat existe
    if not os.path.exists(erp['file']):
        print(f"   ❌ Fichier {erp['file']} non trouvé - Ignoré")
        continue
    
    # Créer le raccourci .bat sur le bureau
    shortcut_path = os.path.join(desktop_path, f"{erp['name']}.bat")
    
    shortcut_content = f'''@echo off
title {erp['description']}
color 0B
cls

echo.
echo ========================================
echo.
echo    {erp['description']}
echo.
echo ========================================
echo.
echo Démarrage en cours...
echo.

:: Se déplacer dans le dossier ERP
cd /d "{current_dir}"

:: Exécuter le lanceur
call "{erp['file']}"

pause
'''
    
    try:
        with open(shortcut_path, 'w', encoding='utf-8') as f:
            f.write(shortcut_content)
        print(f"   ✅ Raccourci créé: {shortcut_path}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

# Créer aussi un raccourci pour le lanceur principal
print(f"\n[Bonus] Création du raccourci principal...")
main_shortcut_path = os.path.join(desktop_path, "ERP_Principal.bat")

main_shortcut_content = f'''@echo off
title ERP Supermarket - Lanceur Principal
color 0A
cls

echo.
echo ========================================
echo.
echo       ERP SUPERMARKET
echo    Lanceur Principal
echo.
echo ========================================
echo.
echo Sélectionnez votre PC:
echo.
echo [1] PC1 - Port 8001
echo [2] PC2 - Port 8002  
echo [3] PC3 - Port 8003
echo [4] PC4 - Port 8004
echo [0] Quitter
echo.
set /p choice="Votre choix (0-4): "

if "%choice%"=="1" call "{current_dir}\\ERP_PC1.bat"
if "%choice%"=="2" call "{current_dir}\\ERP_PC2.bat"
if "%choice%"=="3" call "{current_dir}\\ERP_PC3.bat"
if "%choice%"=="4" call "{current_dir}\\ERP_PC4.bat"
if "%choice%"=="0" exit

pause
'''

try:
    with open(main_shortcut_path, 'w', encoding='utf-8') as f:
        f.write(main_shortcut_content)
    print(f"   ✅ Lanceur principal créé: {main_shortcut_path}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print("\n" + "=" * 50)
print("✅ RACCOURCIS BUREAU CRÉÉS !")
print("=" * 50)
print("\n🎯 RÉSULTAT:")
print("📁 Sur votre bureau, vous avez maintenant:")
print("   • ERP_PC1.bat - Lance ERP PC1 (Port 8001)")
print("   • ERP_PC2.bat - Lance ERP PC2 (Port 8002)")
print("   • ERP_PC3.bat - Lance ERP PC3 (Port 8003)")
print("   • ERP_PC4.bat - Lance ERP PC4 (Port 8004)")
print("   • ERP_Principal.bat - Menu de sélection")
print("\n💡 UTILISATION:")
print("   • Double-cliquez sur le raccourci de votre choix")
print("   • Ou utilisez ERP_Principal.bat pour un menu")
print("   • Chaque raccourci lance l'ERP correspondant")
print("\n🔄 SYNCHRONISATION:")
print("   • Les données se synchronisent automatiquement")
print("   • Chaque PC peut travailler indépendamment")
print("   • Aucune dépendance entre les PC")


