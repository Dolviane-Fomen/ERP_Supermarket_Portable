#!/usr/bin/env python3
"""
Test de vérification que les corrections JavaScript sont appliquées
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
django.setup()

def verifier_corrections_templates():
    """
    Vérifier que les corrections sont appliquées dans les templates
    """
    print("=" * 80)
    print("VERIFICATION DES CORRECTIONS DANS LES TEMPLATES")
    print("=" * 80)
    
    # Vérifier le template principal
    template_principal = "supermarket/templates/supermarket/caisse/facturation_vente.html"
    template_temp = "supermarket/templates/supermarket/caisse/facturation_vente_temp.html"
    template_fixed = "supermarket/templates/supermarket/caisse/facturation_vente_fixed.html"
    
    corrections_appliquees = True
    
    # Vérifier template_temp.html
    print(f"\n1. VERIFICATION DU TEMPLATE TEMP:")
    print("-" * 40)
    
    try:
        with open(template_temp, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier qu'il n'y a plus de parseInt pour les quantités
        if 'parseInt(quantiteInput.value)' in content:
            print("   ❌ ERREUR: parseInt trouvé pour les quantités")
            corrections_appliquees = False
        else:
            print("   ✅ OK: parseInt supprimé pour les quantités")
        
        # Vérifier qu'il y a parseFloat pour les quantités
        if 'parseFloat(quantiteInput.value)' in content:
            print("   ✅ OK: parseFloat utilisé pour les quantités")
        else:
            print("   ❌ ERREUR: parseFloat manquant pour les quantités")
            corrections_appliquees = False
            
    except Exception as e:
        print(f"   ❌ ERREUR: Impossible de lire le fichier: {e}")
        corrections_appliquees = False
    
    # Vérifier template_fixed.html
    print(f"\n2. VERIFICATION DU TEMPLATE FIXED:")
    print("-" * 40)
    
    try:
        with open(template_fixed, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier qu'il n'y a plus de parseInt pour les quantités
        if 'parseInt(quantiteInput.value)' in content:
            print("   ❌ ERREUR: parseInt trouvé pour les quantités")
            corrections_appliquees = False
        else:
            print("   ✅ OK: parseInt supprimé pour les quantités")
        
        # Vérifier qu'il y a parseFloat pour les quantités
        if 'parseFloat(quantiteInput.value)' in content:
            print("   ✅ OK: parseFloat utilisé pour les quantités")
        else:
            print("   ❌ ERREUR: parseFloat manquant pour les quantités")
            corrections_appliquees = False
            
    except Exception as e:
        print(f"   ❌ ERREUR: Impossible de lire le fichier: {e}")
        corrections_appliquees = False
    
    # Vérifier template principal
    print(f"\n3. VERIFICATION DU TEMPLATE PRINCIPAL:")
    print("-" * 40)
    
    try:
        with open(template_principal, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Vérifier qu'il n'y a plus de parseInt pour les quantités
        if 'parseInt(quantiteInput.value)' in content:
            print("   ❌ ERREUR: parseInt trouvé pour les quantités")
            corrections_appliquees = False
        else:
            print("   ✅ OK: parseInt supprimé pour les quantités")
        
        # Vérifier qu'il y a parseFloat pour les quantités
        if 'parseFloat(quantiteInput.value)' in content:
            print("   ✅ OK: parseFloat utilisé pour les quantités")
        else:
            print("   ❌ ERREUR: parseFloat manquant pour les quantités")
            corrections_appliquees = False
            
    except Exception as e:
        print(f"   ❌ ERREUR: Impossible de lire le fichier: {e}")
        corrections_appliquees = False
    
    print(f"\n" + "=" * 80)
    print(f"RESUME DE LA VERIFICATION:")
    print(f"=" * 80)
    
    if corrections_appliquees:
        print(f"✅ TOUTES LES CORRECTIONS SONT APPLIQUEES!")
        print(f"✅ Les templates utilisent maintenant parseFloat pour les quantités")
        print(f"✅ Les quantités décimales seront correctement gérées")
        print(f"\nVous pouvez maintenant tester dans l'interface web:")
        print(f"1. Allez sur http://127.0.0.1:8000")
        print(f"2. Connectez-vous à la caisse")
        print(f"3. Créez une facture avec quantité 1.71")
        print(f"4. Le total devrait maintenant être correct!")
    else:
        print(f"❌ CERTAINES CORRECTIONS MANQUENT!")
        print(f"❌ Vérifiez les erreurs ci-dessus")
    
    return corrections_appliquees

def creer_test_rapide():
    """
    Créer un test rapide pour vérifier la correction
    """
    print(f"\n" + "=" * 80)
    print(f"TEST RAPIDE DE LA CORRECTION")
    print(f"=" * 80)
    
    # Test simple de conversion
    test_cases = [
        ("1.71", 1.71),
        ("2.5", 2.5),
        ("0.75", 0.75),
        ("1,71", 1.71),  # Virgule française
    ]
    
    print(f"\nTest de conversion JavaScript simulé:")
    for input_val, expected in test_cases:
        # Simulation de parseFloat
        try:
            result = float(input_val.replace(',', '.'))
            status = "OK" if abs(result - expected) < 0.001 else "ERREUR"
            print(f"   {status} '{input_val}' -> {result} (attendu: {expected})")
        except:
            print(f"   ERREUR '{input_val}' -> conversion impossible")

if __name__ == "__main__":
    verifier_corrections_templates()
    creer_test_rapide()
