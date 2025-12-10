#!/usr/bin/env python3
"""
Script de test complet pour vérifier la correction des quantités décimales
Test avec quantité 1.71 et prix total 3163.5
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
    print("🧪 TEST DE CONVERSION DES DÉCIMALES")
    print("=" * 50)
    
    # Importer la fonction depuis views.py
    import sys
    sys.path.append(str(BASE_DIR))
    from views import normalize_decimal_input, safe_quantity_conversion, safe_price_conversion
    
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
    for input_val, expected in test_cases:
        result = normalize_decimal_input(input_val)
        status = "✅" if result == expected else "❌"
        print(f"  {status} '{input_val}' -> {result} (attendu: {expected})")
    
    return True

def test_facture_decimal():
    """
    Test de création d'une facture avec quantités décimales
    """
    print("\n🧪 TEST DE FACTURE AVEC QUANTITÉS DÉCIMALES")
    print("=" * 50)
    
    try:
        # Récupérer les données nécessaires
        agence = Agence.objects.first()
        if not agence:
            print("❌ Aucune agence trouvée")
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
                    unite_vente='Unité'
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
        
        # Créer une session de caisse
        session_caisse = SessionCaisse.objects.create(
            caisse=caisse,
            agence=agence,
            solde_ouverture=Decimal('0.00'),
            statut='ouverte'
        )
        
        # Test avec quantité 1.71 et prix unitaire 1850
        quantite_test = Decimal('1.71')
        prix_unitaire_test = Decimal('1850.00')
        prix_total_attendu = quantite_test * prix_unitaire_test  # 3163.5
        
        print(f"📊 Données de test :")
        print(f"  - Quantité : {quantite_test}")
        print(f"  - Prix unitaire : {prix_unitaire_test}")
        print(f"  - Prix total attendu : {prix_total_attendu}")
        
        # Créer la facture
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
        
        # Créer la ligne de facture
        ligne = LigneFactureVente.objects.create(
            facture_vente=facture,
            article=article,
            designation=article.designation,
            quantite=quantite_test,
            prix_unitaire=prix_unitaire_test,
            prix_total=prix_total_attendu
        )
        
        print(f"\n✅ Facture créée :")
        print(f"  - Numéro : {facture.numero_ticket}")
        print(f"  - Quantité ligne : {ligne.quantite}")
        print(f"  - Prix unitaire ligne : {ligne.prix_unitaire}")
        print(f"  - Prix total ligne : {ligne.prix_total}")
        print(f"  - Net à payer facture : {facture.nette_a_payer}")
        
        # Vérifier la cohérence
        if ligne.prix_total == prix_total_attendu and facture.nette_a_payer == prix_total_attendu:
            print(f"\n🎉 SUCCÈS : Les calculs sont corrects !")
            print(f"   Quantité {quantite_test} × Prix {prix_unitaire_test} = {prix_total_attendu}")
            return True
        else:
            print(f"\n❌ ERREUR : Incohérence dans les calculs")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chiffre_affaires():
    """
    Test du calcul du chiffre d'affaires
    """
    print("\n🧪 TEST DU CALCUL DU CHIFFRE D'AFFAIRES")
    print("=" * 50)
    
    try:
        from django.db.models import Sum
        
        agence = Agence.objects.first()
        if not agence:
            print("❌ Aucune agence trouvée")
            return False
        
        # Récupérer les factures de test
        factures_test = FactureVente.objects.filter(
            agence=agence,
            numero_ticket__startswith='TEST_DECIMAL'
        )
        
        if not factures_test.exists():
            print("❌ Aucune facture de test trouvée")
            return False
        
        # Calculer le chiffre d'affaires
        chiffre_affaires = factures_test.aggregate(total=Sum('nette_a_payer'))['total'] or Decimal('0')
        
        print(f"📊 Chiffre d'affaires calculé : {chiffre_affaires}")
        
        # Vérifier chaque facture
        total_manuel = Decimal('0')
        for facture in factures_test:
            print(f"  - Facture {facture.numero_ticket} : {facture.nette_a_payer}")
            total_manuel += facture.nette_a_payer
        
        print(f"📊 Total manuel : {total_manuel}")
        
        if chiffre_affaires == total_manuel:
            print(f"\n🎉 SUCCÈS : Le chiffre d'affaires est correct !")
            return True
        else:
            print(f"\n❌ ERREUR : Incohérence dans le chiffre d'affaires")
            return False
            
    except Exception as e:
        print(f"\n❌ ERREUR lors du test : {e}")
        return False

def cleanup_test_data():
    """
    Nettoyer les données de test
    """
    print("\n🧹 NETTOYAGE DES DONNÉES DE TEST")
    print("=" * 50)
    
    try:
        # Supprimer les factures de test
        factures_test = FactureVente.objects.filter(numero_ticket__startswith='TEST_DECIMAL')
        count = factures_test.count()
        factures_test.delete()
        
        print(f"✅ {count} factures de test supprimées")
        
        # Supprimer les sessions de test
        sessions_test = SessionCaisse.objects.filter(caisse__numero_caisse='TEST001')
        count_sessions = sessions_test.count()
        sessions_test.delete()
        
        print(f"✅ {count_sessions} sessions de test supprimées")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR lors du nettoyage : {e}")
        return False

def main():
    """
    Fonction principale de test
    """
    print("🚀 TEST COMPLET DE LA CORRECTION DES DÉCIMALES")
    print("=" * 60)
    print("Problème testé : Quantité 1.71 → Prix total 3163.5 (pas 31635)")
    print("=" * 60)
    
    # Nettoyer d'abord
    cleanup_test_data()
    
    # Tests
    test1 = test_decimal_conversion()
    test2 = test_facture_decimal()
    test3 = test_chiffre_affaires()
    
    # Résumé
    print("\n📋 RÉSUMÉ DES TESTS")
    print("=" * 30)
    print(f"Conversion décimales : {'✅ PASSÉ' if test1 else '❌ ÉCHOUÉ'}")
    print(f"Facture décimale : {'✅ PASSÉ' if test2 else '❌ ÉCHOUÉ'}")
    print(f"Chiffre d'affaires : {'✅ PASSÉ' if test3 else '❌ ÉCHOUÉ'}")
    
    if all([test1, test2, test3]):
        print(f"\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print(f"   La correction des décimales fonctionne correctement.")
    else:
        print(f"\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print(f"   Vérifiez les erreurs ci-dessus.")
    
    # Nettoyer à la fin
    cleanup_test_data()

if __name__ == "__main__":
    main()
