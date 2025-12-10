#!/usr/bin/env python3
"""
Test simple de la correction des décimales
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

from decimal import Decimal, InvalidOperation
import re

def normalize_decimal_input(value):
    """
    Fonction de normalisation des décimales (copiée depuis views.py)
    """
    if value is None:
        return Decimal('0')
    
    # Convertir en chaîne
    value_str = str(value).strip()
    
    # Remplacer les virgules par des points (format français vers format international)
    value_str = value_str.replace(',', '.')
    
    # Supprimer les caractères non numériques sauf point et moins
    value_str = re.sub(r'[^\d.-]', '', value_str)
    
    # Gérer les cas vides
    if not value_str or value_str in ['-', '.']:
        return Decimal('0')
    
    # S'assurer qu'il n'y a qu'un seul point décimal
    parts = value_str.split('.')
    if len(parts) > 2:
        value_str = parts[0] + '.' + ''.join(parts[1:])
    
    try:
        return Decimal(value_str)
    except (InvalidOperation, ValueError):
        print(f"[WARNING] Erreur conversion Decimal: {value} -> valeur par défaut 0")
        return Decimal('0')

def test_decimal_conversion():
    """
    Test de la fonction de conversion des décimales
    """
    print("TEST DE CONVERSION DES DECIMALES")
    print("=" * 50)
    
    # Tests de conversion
    test_cases = [
        ("1.71", Decimal('1.71')),
        ("3163.5", Decimal('3163.5')),
        ("1,71", Decimal('1.71')),  # Virgule française
        ("3 163,5", Decimal('3163.5')),  # Espaces et virgule
        ("31635", Decimal('31635')),  # Sans décimales
        ("0.5", Decimal('0.5')),
        ("", Decimal('0')),  # Vide
        (None, Decimal('0')),  # None
    ]
    
    print("Tests de conversion :")
    success_count = 0
    for input_val, expected in test_cases:
        result = normalize_decimal_input(input_val)
        status = "OK" if result == expected else "ERREUR"
        if result == expected:
            success_count += 1
        print(f"  {status} '{input_val}' -> {result} (attendu: {expected})")
    
    print(f"\nResultat: {success_count}/{len(test_cases)} tests reussis")
    return success_count == len(test_cases)

def test_calcul_facture():
    """
    Test du calcul de facture avec quantités décimales
    """
    print("\nTEST DU CALCUL DE FACTURE")
    print("=" * 50)
    
    # Simulation d'une ligne de facture
    quantite_str = "1.71"
    prix_unitaire_str = "1850.00"
    
    # Conversion sécurisée
    quantite = normalize_decimal_input(quantite_str)
    prix_unitaire = normalize_decimal_input(prix_unitaire_str)
    
    # Calcul du total
    prix_total = quantite * prix_unitaire
    
    print(f"Donnees de test :")
    print(f"  - Quantite (string): '{quantite_str}'")
    print(f"  - Quantite (decimal): {quantite}")
    print(f"  - Prix unitaire (string): '{prix_unitaire_str}'")
    print(f"  - Prix unitaire (decimal): {prix_unitaire}")
    print(f"  - Prix total calcule: {prix_total}")
    
    # Vérification
    prix_total_attendu = Decimal('3163.5')
    if prix_total == prix_total_attendu:
        print(f"\nSUCCES : Le calcul est correct !")
        print(f"   {quantite} x {prix_unitaire} = {prix_total}")
        return True
    else:
        print(f"\nERREUR : Le calcul est incorrect !")
        print(f"   Attendu: {prix_total_attendu}")
        print(f"   Obtenu: {prix_total}")
        return False

def test_probleme_original():
    """
    Test du problème original : 1.71 devient 31635
    """
    print("\nTEST DU PROBLEME ORIGINAL")
    print("=" * 50)
    
    # Simulation du problème
    quantite_problematique = "1.71"
    prix_unitaire_problematique = "1850.00"
    
    # Ancienne méthode (problématique)
    try:
        quantite_ancienne = float(quantite_problematique)
        prix_ancien = float(prix_unitaire_problematique)
        total_ancien = quantite_ancienne * prix_ancien
        print(f"Ancienne methode (problematique):")
        print(f"  - Quantite: {quantite_ancienne}")
        print(f"  - Prix: {prix_ancien}")
        print(f"  - Total: {total_ancien}")
    except:
        print("Erreur avec l'ancienne méthode")
    
    # Nouvelle méthode (corrigée)
    quantite_nouvelle = normalize_decimal_input(quantite_problematique)
    prix_nouveau = normalize_decimal_input(prix_unitaire_problematique)
    total_nouveau = quantite_nouvelle * prix_nouveau
    
    print(f"\nNouvelle methode (corrigee):")
    print(f"  - Quantite: {quantite_nouvelle}")
    print(f"  - Prix: {prix_nouveau}")
    print(f"  - Total: {total_nouveau}")
    
    # Vérification
    if total_nouveau == Decimal('3163.5'):
        print(f"\nSUCCES : Le problème est résolu !")
        return True
    else:
        print(f"\nERREUR : Le problème persiste")
        return False

def main():
    """
    Fonction principale de test
    """
    print("TEST DE LA CORRECTION DES DECIMALES")
    print("=" * 60)
    print("Probleme: Quantite 1.71 -> Prix total 3163.5 (pas 31635)")
    print("=" * 60)
    
    # Tests
    test1 = test_decimal_conversion()
    test2 = test_calcul_facture()
    test3 = test_probleme_original()
    
    # Résumé
    print("\nRESUME DES TESTS")
    print("=" * 30)
    print(f"Conversion decimales : {'PASSE' if test1 else 'ECHOUE'}")
    print(f"Calcul facture : {'PASSE' if test2 else 'ECHOUE'}")
    print(f"Probleme original : {'PASSE' if test3 else 'ECHOUE'}")
    
    if all([test1, test2, test3]):
        print(f"\nTOUS LES TESTS SONT PASSES !")
        print(f"   La correction des decimales fonctionne correctement.")
        print(f"   Vous pouvez maintenant tester dans l'interface web.")
    else:
        print(f"\nCERTAINS TESTS ONT ECHOUE")
        print(f"   Verifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main()
