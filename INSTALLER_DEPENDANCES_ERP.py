#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'installation automatique des dépendances ERP
Installe openpyxl et reportlab sur d'autres PC
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def print_banner():
    """Affiche la bannière du script"""
    print("=" * 60)
    print("🚀 INSTALLATION DÉPENDANCES ERP")
    print("=" * 60)
    print("📦 Installation automatique de openpyxl et reportlab")
    print("=" * 60)

def check_python():
    """Vérifie que Python est installé"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Python détecté : {result.stdout.strip()}")
            return True
        else:
            print("❌ Python non détecté")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification Python : {e}")
        return False

def install_package(package_name):
    """Installe un package Python"""
    print(f"\n📦 Installation de {package_name}...")
    try:
        # Essayer d'abord avec pip
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", package_name, "--upgrade"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {package_name} installé avec succès")
            return True
        else:
            print(f"⚠️ Installation avec pip échouée, tentative avec easy_install...")
            # Essayer avec easy_install
            result = subprocess.run([
                sys.executable, "-m", "easy_install", package_name
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ {package_name} installé avec easy_install")
                return True
            else:
                print(f"❌ Échec de l'installation de {package_name}")
                print(f"Erreur : {result.stderr}")
                return False
                
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout lors de l'installation de {package_name}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'installation de {package_name} : {e}")
        return False

def verify_installation(package_name):
    """Vérifie qu'un package est bien installé"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} vérifié et fonctionnel")
        return True
    except ImportError:
        print(f"❌ {package_name} non trouvé après installation")
        return False

def install_offline_packages():
    """Installe les packages depuis le dossier packages_offline"""
    print("\n📦 Installation des packages offline...")
    
    # Vérifier si le dossier existe
    offline_dir = Path("packages_offline")
    if not offline_dir.exists():
        print("❌ Dossier packages_offline non trouvé")
        return False
    
    # Packages à installer
    packages = [
        "openpyxl-3.1.5-py2.py3-none-any.whl",
        "reportlab-4.4.4-py3-none-any.whl"
    ]
    
    for package in packages:
        package_path = offline_dir / package
        if package_path.exists():
            print(f"📦 Installation de {package}...")
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", str(package_path)
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"✅ {package} installé avec succès")
                else:
                    print(f"❌ Échec de l'installation de {package}")
                    print(f"Erreur : {result.stderr}")
            except Exception as e:
                print(f"❌ Erreur lors de l'installation de {package} : {e}")
        else:
            print(f"⚠️ Package {package} non trouvé dans packages_offline")

def create_requirements_file():
    """Crée un fichier requirements.txt"""
    print("\n📝 Création du fichier requirements.txt...")
    
    requirements = [
        "openpyxl>=3.1.5",
        "reportlab>=4.4.4",
        "django>=5.2.7",
        "pillow>=11.3.0"
    ]
    
    try:
        with open("requirements.txt", "w", encoding="utf-8") as f:
            for req in requirements:
                f.write(f"{req}\n")
        print("✅ Fichier requirements.txt créé")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création de requirements.txt : {e}")
        return False

def install_from_requirements():
    """Installe les packages depuis requirements.txt"""
    print("\n📦 Installation depuis requirements.txt...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Tous les packages installés depuis requirements.txt")
            return True
        else:
            print("❌ Échec de l'installation depuis requirements.txt")
            print(f"Erreur : {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'installation depuis requirements.txt : {e}")
        return False

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifier Python
    if not check_python():
        print("\n❌ Python requis pour continuer")
        input("Appuyez sur Entrée pour quitter...")
        return
    
    print("\n🚀 Début de l'installation des dépendances...")
    
    # Créer requirements.txt
    create_requirements_file()
    
    # Essayer d'abord l'installation offline
    if Path("packages_offline").exists():
        print("\n📦 Installation offline détectée...")
        install_offline_packages()
    else:
        print("\n📦 Installation online...")
        # Installer openpyxl
        install_package("openpyxl")
        # Installer reportlab
        install_package("reportlab")
    
    # Vérifier les installations
    print("\n🔍 Vérification des installations...")
    openpyxl_ok = verify_installation("openpyxl")
    reportlab_ok = verify_installation("reportlab")
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE L'INSTALLATION")
    print("=" * 60)
    print(f"✅ openpyxl : {'Installé' if openpyxl_ok else 'Échec'}")
    print(f"✅ reportlab : {'Installé' if reportlab_ok else 'Échec'}")
    
    if openpyxl_ok and reportlab_ok:
        print("\n🎉 Toutes les dépendances sont installées avec succès !")
        print("🚀 Votre ERP est prêt à fonctionner")
    else:
        print("\n⚠️ Certaines dépendances n'ont pas pu être installées")
        print("💡 Vérifiez votre connexion internet ou utilisez les packages offline")
    
    print("\n" + "=" * 60)
    input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()


