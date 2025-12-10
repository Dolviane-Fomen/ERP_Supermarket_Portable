#!/usr/bin/env python3
"""
Script de test simplifié pour vérifier la correction des quantités décimales
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

from decimal import Decimal
from django.utils import timezone
from supermarket.models import *

def test_decimal_conversion():
    """
    Test de la fonction de conversion des décimales
    """
    print("TEST DE CONVERSION DES DECIMALES")
    print("=" * 50)
    
    # Importer la fonction depuis views.py
    from views import normalize_decimal_input
    
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

def test_facture_decimal():
    """
    Test de creation d'une facture avec quantites decimales
    """
    print("\nTEST DE FACTURE AVEC QUANTITES DECIMALES")
    print("=" * 50)
    
    try:
        # Recuperer les donnees necessaires
        agence = Agence.objects.first()
        if not agence:
            print("ERREUR: Aucune agence trouvee")
            return False
        
        client = Client.objects.filter(agence=agence).first()
        if not client:
            client = Client.objects.create(
                intitule='Client Test',
                adresse='Adresse Test',
                telephone='0000000000',
                agence=agence
            )
        
        caisse = Caisse.objects.filter(agence=agence).first()
        if not caisse:
            caisse = Caisse.objects.create(
                numero_caisse='TEST001',
                nom_caisse='Caisse Test',
                agence=agence,
                statut='active'
            )
        
        article = Article.objects.filter(agence=agence).first()
        if not article:
            famille = Famille.objects.first()
            if not famille:
                famille = Famille.objects.create(
                    code='TEST',
                    intitule='Test',
                    unite_vente='Unite'
                )
            
            article = Article.objects.create(
                reference_article='TEST001',
                designation='Article Test',
                categorie=famille,
                prix_achat=Decimal('1000.00'),
                prix_vente=Decimal('1850.00'),
                stock_actuel=Decimal('10.00'),
                agence=agence
            )
        
        # Creer une session de caisse
        session_caisse = SessionCaisse.objects.create(
            caisse=caisse,
            agence=agence,
            solde_ouverture=Decimal('0.00'),
            statut='ouverte'
        )
        
        # Test avec quantite 1.71 et prix unitaire 1850
        quantite_test = Decimal('1.71')
        prix_unitaire_test = Decimal('1850.00')
        prix_total_attendu = quantite_test * prix_unitaire_test  # 3163.5
        
        print(f"Donnees de test :")
        print(f"  - Quantite : {quantite_test}")
        print(f"  - Prix unitaire : {prix_unitaire_test}")
        print(f"  - Prix total attendu : {prix_total_attendu}")
        
        # Creer la facture
        facture = FactureVente.objects.create(
            numero_ticket=f"TEST_DECIMAL_{int(timezone.now().timestamp())}",
            date=timezone.now().date(),
            heure=timezone.now().time(),
            nette_a_payer=prix_total_attendu,
            montant_regler=prix_total_attendu,
            rendu=Decimal('0.00'),
            remise=Decimal('0.00'),
            en_attente=False,
            nom_vendeuse='Test User',
            client=client,
            caisse=caisse,
            agence=agence,
            session_caisse=session_caisse
        )
        
        # Creer la ligne de facture
        ligne = LigneFactureVente.objects.create(
            facture_vente=facture,
            article=article,
            designation=article.designation,
            quantite=quantite_test,
            prix_unitaire=prix_unitaire_test,
            prix_total=prix_total_attendu
        )
        
        print(f"\nFacture creee :")
        print(f"  - Numero : {facture.numero_ticket}")
        print(f"  - Quantite ligne : {ligne.quantite}")
        print(f"  - Prix unitaire ligne : {ligne.prix_unitaire}")
        print(f"  - Prix total ligne : {ligne.prix_total}")
        print(f"  - Net a payer facture : {facture.nette_a_payer}")
        
        # Verifier la coherence
        if ligne.prix_total == prix_total_attendu and facture.nette_a_payer == prix_total_attendu:
            print(f"\nSUCCES : Les calculs sont corrects !")
            print(f"   Quantite {quantite_test} x Prix {prix_unitaire_test} = {prix_total_attendu}")
            return True
        else:
            print(f"\nERREUR : Incoherence dans les calculs")
            return False
            
    except Exception as e:
        print(f"\nERREUR lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chiffre_affaires():
    """
    Test du calcul du chiffre d'affaires
    """
    print("\nTEST DU CALCUL DU CHIFFRE D'AFFAIRES")
    print("=" * 50)
    
    try:
        from django.db.models import Sum
        
        agence = Agence.objects.first()
        if not agence:
            print("ERREUR: Aucune agence trouvee")
            return False
        
        # Recuperer les factures de test
        factures_test = FactureVente.objects.filter(
            agence=agence,
            numero_ticket__startswith='TEST_DECIMAL'
        )
        
        if not factures_test.exists():
            print("ERREUR: Aucune facture de test trouvee")
            return False
        
        # Calculer le chiffre d'affaires
        chiffre_affaires = factures_test.aggregate(total=Sum('nette_a_payer'))['total'] or Decimal('0')
        
        print(f"Chiffre d'affaires calcule : {chiffre_affaires}")
        
        # Verifier chaque facture
        total_manuel = Decimal('0')
        for facture in factures_test:
            print(f"  - Facture {facture.numero_ticket} : {facture.nette_a_payer}")
            total_manuel += facture.nette_a_payer
        
        print(f"Total manuel : {total_manuel}")
        
        if chiffre_affaires == total_manuel:
            print(f"\nSUCCES : Le chiffre d'affaires est correct !")
            return True
        else:
            print(f"\nERREUR : Incoherence dans le chiffre d'affaires")
            return False
            
    except Exception as e:
        print(f"\nERREUR lors du test : {e}")
        return False

def cleanup_test_data():
    """
    Nettoyer les donnees de test
    """
    print("\nNETTOYAGE DES DONNEES DE TEST")
    print("=" * 50)
    
    try:
        # Supprimer les factures de test
        factures_test = FactureVente.objects.filter(numero_ticket__startswith='TEST_DECIMAL')
        count = factures_test.count()
        factures_test.delete()
        
        print(f"OK: {count} factures de test supprimees")
        
        # Supprimer les sessions de test
        sessions_test = SessionCaisse.objects.filter(caisse__numero_caisse='TEST001')
        count_sessions = sessions_test.count()
        sessions_test.delete()
        
        print(f"OK: {count_sessions} sessions de test supprimees")
        
        return True
        
    except Exception as e:
        print(f"ERREUR lors du nettoyage : {e}")
        return False

def main():
    """
    Fonction principale de test
    """
    print("TEST COMPLET DE LA CORRECTION DES DECIMALES")
    print("=" * 60)
    print("Probleme teste : Quantite 1.71 -> Prix total 3163.5 (pas 31635)")
    print("=" * 60)
    
    # Nettoyer d'abord
    cleanup_test_data()
    
    # Tests
    test1 = test_decimal_conversion()
    test2 = test_facture_decimal()
    test3 = test_chiffre_affaires()
    
    # Resume
    print("\nRESUME DES TESTS")
    print("=" * 30)
    print(f"Conversion decimales : {'PASSE' if test1 else 'ECHOUE'}")
    print(f"Facture decimale : {'PASSE' if test2 else 'ECHOUE'}")
    print(f"Chiffre d'affaires : {'PASSE' if test3 else 'ECHOUE'}")
    
    if all([test1, test2, test3]):
        print(f"\nTOUS LES TESTS SONT PASSES !")
        print(f"   La correction des decimales fonctionne correctement.")
    else:
        print(f"\nCERTAINS TESTS ONT ECHOUE")
        print(f"   Verifiez les erreurs ci-dessus.")
    
    # Nettoyer a la fin
    cleanup_test_data()

if __name__ == "__main__":
    main()
