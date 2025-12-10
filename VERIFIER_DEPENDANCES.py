#!/usr/bin/env python3
"""
Script de vérification des dépendances ERP - VERSION OPTIMISEE
Affichage détaillé de toutes les dépendances installées
"""

import sys
from pathlib import Path

def verifier_dependances():
    """Vérifier que toutes les dépendances sont installées avec détails"""
    print("=" * 70)
    print("    VERIFICATION DES DEPENDANCES - VERSION OPTIMISEE")
    print("    ERP SUPERMARKET")
    print("=" * 70)
    print()
    
    # Informations Python
    print("🐍 INFORMATIONS PYTHON:")
    print("-" * 70)
    print(f"   Version: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"   Exécutable: {sys.executable}")
    print(f"   Plateforme: {sys.platform}")
    print()
    
    # Vérifier chaque dépendance avec détails
    print("=" * 70)
    print("📦 DEPENDANCES INSTALLEES:")
    print("=" * 70)
    print()
    
    dependances_info = []
    verif_ok = True
    
    # Django
    print("1. DJANGO:")
    print("-" * 70)
    try:
        import django
        version = django.get_version()
        location = Path(django.__file__).parent
        print(f"   ✅ Installé: OUI")
        print(f"   📌 Version: {version}")
        print(f"   📍 Emplacement: {location}")
        dependances_info.append(("Django", version, "✅ INSTALLE", True))
    except ImportError as e:
        print(f"   ❌ Installé: NON")
        print(f"   ⚠️  Erreur: {e}")
        dependances_info.append(("Django", "N/A", "❌ MANQUANT", False))
        verif_ok = False
    print()
    
    # openpyxl
    print("2. OPENPYXL (Excel):")
    print("-" * 70)
    try:
        import openpyxl
        version = openpyxl.__version__
        location = Path(openpyxl.__file__).parent
        print(f"   ✅ Installé: OUI")
        print(f"   📌 Version: {version}")
        print(f"   📍 Emplacement: {location}")
        print(f"   💡 Fonction: Export et import de fichiers Excel (.xlsx)")
        dependances_info.append(("openpyxl", version, "✅ INSTALLE", True))
    except ImportError as e:
        print(f"   ❌ Installé: NON")
        print(f"   ⚠️  Erreur: {e}")
        print(f"   💡 Fonction: Export et import de fichiers Excel (.xlsx)")
        dependances_info.append(("openpyxl", "N/A", "❌ MANQUANT", False))
        verif_ok = False
    print()
    
    # reportlab
    print("3. REPORTLAB (PDF):")
    print("-" * 70)
    try:
        import reportlab
        version = reportlab.Version
        location = Path(reportlab.__file__).parent
        print(f"   ✅ Installé: OUI")
        print(f"   📌 Version: {version}")
        print(f"   📍 Emplacement: {location}")
        print(f"   💡 Fonction: Génération de rapports et documents PDF")
        dependances_info.append(("reportlab", version, "✅ INSTALLE", True))
    except ImportError as e:
        print(f"   ❌ Installé: NON")
        print(f"   ⚠️  Erreur: {e}")
        print(f"   💡 Fonction: Génération de rapports et documents PDF")
        dependances_info.append(("reportlab", "N/A", "❌ MANQUANT", False))
        verif_ok = False
    print()
    
    # Pillow
    print("4. PILLOW (Images):")
    print("-" * 70)
    try:
        import PIL
        version = PIL.__version__
        location = Path(PIL.__file__).parent
        print(f"   ✅ Installé: OUI")
        print(f"   📌 Version: {version}")
        print(f"   📍 Emplacement: {location}")
        print(f"   💡 Fonction: Traitement et manipulation d'images")
        dependances_info.append(("Pillow", version, "✅ INSTALLE", True))
    except ImportError as e:
        print(f"   ❌ Installé: NON")
        print(f"   ⚠️  Erreur: {e}")
        print(f"   💡 Fonction: Traitement et manipulation d'images")
        dependances_info.append(("Pillow", "N/A", "❌ MANQUANT", False))
        verif_ok = False
    print()
    
    # Résumé final
    print("=" * 70)
    print("📊 RESUME DES DEPENDANCES:")
    print("=" * 70)
    print()
    print(f"{'Package':<15} {'Version':<20} {'Statut':<15}")
    print("-" * 70)
    for nom, version, statut, installe in dependances_info:
        print(f"{nom:<15} {version:<20} {statut:<15}")
    print()
    
    # Statistiques
    total = len(dependances_info)
    installes = sum(1 for _, _, _, installe in dependances_info if installe)
    manquants = total - installes
    
    print(f"📈 STATISTIQUES:")
    print(f"   Total: {total} dépendances")
    print(f"   Installées: {installes} / {total}")
    print(f"   Manquantes: {manquants} / {total}")
    print()
    
    # Conclusion
    if verif_ok:
        print("=" * 70)
        print("    ✅ TOUTES LES DEPENDANCES SONT INSTALLEES!")
        print("=" * 70)
        print()
        print("🎉 L'ERP peut fonctionner normalement avec toutes les fonctionnalités:")
        print("   ✅ Framework Django")
        print("   ✅ Export/Import Excel (.xlsx)")
        print("   ✅ Génération de rapports PDF")
        print("   ✅ Traitement d'images")
        print()
        print("🚀 Vous pouvez maintenant:")
        print("1. Lancer l'ERP: ERP_Launcher.bat")
        print("2. Utiliser toutes les fonctionnalités")
        print("3. Exporter des données en Excel")
        print("4. Générer des rapports PDF")
        return True
    else:
        print("=" * 70)
        print("    ⚠️  DEPENDANCES MANQUANTES DETECTEES!")
        print("=" * 70)
        print()
        print(f"❌ {manquants} dépendance(s) manquante(s) sur {total}")
        print()
        print("🔧 SOLUTION:")
        print("1. Exécutez: INSTALLER_DEPENDANCES_OFFLINE.bat")
        print("2. Ou installez manuellement les packages manquants")
        print("3. Puis vérifiez à nouveau avec ce script")
        print()
        print("💡 COMMANDE MANUELLE:")
        print("   python -m pip install Django Pillow openpyxl reportlab")
        return False

if __name__ == "__main__":
    verifier_dependances()
    print()
    input("Appuyez sur Entrée pour fermer...")


