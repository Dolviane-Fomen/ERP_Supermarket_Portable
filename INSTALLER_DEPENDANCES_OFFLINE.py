#!/usr/bin/env python3
"""
Script d'installation des dépendances en mode offline
ERP Supermarket - Installation hors ligne
"""

import subprocess
import sys
from pathlib import Path

def installer_dependances_offline():
    """Installer les dépendances à partir des fichiers téléchargés"""
    
    print("=" * 60)
    print("    INSTALLATION DES DEPENDANCES OFFLINE")
    print("    ERP SUPERMARKET - MODE HORS LIGNE")
    print("=" * 60)
    print()
    
    # Dossier contenant les packages
    script_dir = Path(__file__).parent
    packages_dir = script_dir / "packages_offline"
    
    if not packages_dir.exists():
        print("❌ ERREUR: Dossier packages_offline non trouvé!")
        print("   Exécutez d'abord TELECHARGER_DEPENDANCES_OFFLINE.bat")
        return False
    
    print(f"✅ Dossier packages trouvé: {packages_dir}")
    print()
    
    # Compter les packages
    packages_files = list(packages_dir.glob("*.whl")) + list(packages_dir.glob("*.tar.gz"))
    
    if len(packages_files) == 0:
        print("❌ ERREUR: Aucun package trouvé dans packages_offline!")
        return False
    
    print(f"📦 {len(packages_files)} packages à installer")
    print()
    
    # Installer tous les packages
    print("📥 Installation en cours...")
    print("   (Cela peut prendre quelques minutes)")
    print()
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install",
            "--no-index",
            "--find-links", str(packages_dir),
            "Django", "Pillow", "openpyxl", "reportlab"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Installation réussie!")
        else:
            print(f"❌ Erreur lors de l'installation: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors de l'installation")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    # Vérifier les installations
    print()
    print("🔍 Vérification des installations...")
    print()
    
    verif_ok = True
    
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except ImportError:
        print("❌ Django non installé")
        verif_ok = False
    
    try:
        import openpyxl
        print(f"✅ openpyxl {openpyxl.__version__}")
    except ImportError:
        print("❌ openpyxl non installé")
        verif_ok = False
    
    try:
        import reportlab
        print(f"✅ reportlab {reportlab.Version}")
    except ImportError:
        print("❌ reportlab non installé")
        verif_ok = False
    
    try:
        import PIL
        print(f"✅ Pillow {PIL.__version__}")
    except ImportError:
        print("❌ Pillow non installé")
        verif_ok = False
    
    print()
    if verif_ok:
        print("=" * 60)
        print("    INSTALLATION TERMINEE AVEC SUCCES!")
        print("=" * 60)
        print()
        print("🎉 Toutes les dépendances sont installées!")
        print("✅ L'ERP peut maintenant fonctionner normalement")
        print()
        print("🚀 UTILISATION:")
        print("1. Lancez ERP_Launcher.bat")
        print("2. Connectez-vous à l'ERP")
        print("3. Toutes les fonctionnalités sont disponibles")
        return True
    else:
        print("⚠️  Certaines dépendances n'ont pas été installées")
        return False

if __name__ == "__main__":
    installer_dependances_offline()
    input("\nAppuyez sur Entrée pour fermer...")
