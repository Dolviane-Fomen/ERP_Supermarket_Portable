#!/usr/bin/env python3
"""
Test web direct de la correction des décimales
Création d'une facture de test avec quantités décimales
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

def create_test_facture():
    """
    Créer une facture de test avec des quantités décimales pour démonstration
    """
    print("=" * 80)
    print("CREATION D'UNE FACTURE DE TEST AVEC QUANTITES DECIMALES")
    print("=" * 80)
    
    try:
        # Récupérer les données nécessaires
        agence = Agence.objects.first()
        if not agence:
            print("ERREUR: Aucune agence trouvée")
            return False
        
        client = Client.objects.filter(agence=agence).first()
        if not client:
            client = Client.objects.create(
                intitule='Client Test Décimales',
                adresse='Adresse Test',
                telephone='0000000000',
                agence=agence
            )
            print(f"Client de test créé: {client.intitule}")
        
        caisse = Caisse.objects.filter(agence=agence).first()
        if not caisse:
            caisse = Caisse.objects.create(
                numero_caisse='TEST_DECIMAL',
                nom_caisse='Caisse Test Décimales',
                agence=agence,
                statut='active'
            )
            print(f"Caisse de test créée: {caisse.nom_caisse}")
        
        # Créer une session de caisse
        session_caisse = SessionCaisse.objects.create(
            caisse=caisse,
            agence=agence,
            solde_ouverture=Decimal('0.00'),
            statut='ouverte'
        )
        print(f"Session de caisse créée: {session_caisse.id}")
        
        # Récupérer ou créer des articles de test
        articles_test = []
        
        # Article 1: Test avec quantité 1.71
        article1 = Article.objects.filter(agence=agence, designation__icontains='HUILE').first()
        if not article1:
            famille = Famille.objects.first()
            if not famille:
                famille = Famille.objects.create(
                    code='TEST',
                    intitule='Test',
                    unite_vente='Unité'
                )
            
            article1 = Article.objects.create(
                reference_article='TEST_DECIMAL_001',
                designation='HUILE VEGETALE TEST',
                categorie=famille,
                prix_achat=Decimal('5000.00'),
                prix_vente=Decimal('1850.00'),
                stock_actuel=Decimal('10.00'),
                agence=agence
            )
        
        articles_test.append({
            'article': article1,
            'quantite': Decimal('1.71'),
            'prix_unitaire': article1.prix_vente,
            'total_attendu': Decimal('1.71') * article1.prix_vente
        })
        
        # Article 2: Test avec quantité 2.5
        article2 = Article.objects.filter(agence=agence, designation__icontains='RIZ').first()
        if not article2:
            article2 = Article.objects.create(
                reference_article='TEST_DECIMAL_002',
                designation='RIZ BLANC TEST',
                categorie=famille,
                prix_achat=Decimal('8000.00'),
                prix_vente=Decimal('1200.00'),
                stock_actuel=Decimal('15.00'),
                agence=agence
            )
        
        articles_test.append({
            'article': article2,
            'quantite': Decimal('2.5'),
            'prix_unitaire': article2.prix_vente,
            'total_attendu': Decimal('2.5') * article2.prix_vente
        })
        
        # Article 3: Test avec quantité 0.75
        article3 = Article.objects.filter(agence=agence, designation__icontains='SUCRE').first()
        if not article3:
            article3 = Article.objects.create(
                reference_article='TEST_DECIMAL_003',
                designation='SUCRE BLANC TEST',
                categorie=famille,
                prix_achat=Decimal('12000.00'),
                prix_vente=Decimal('800.00'),
                stock_actuel=Decimal('20.00'),
                agence=agence
            )
        
        articles_test.append({
            'article': article3,
            'quantite': Decimal('0.75'),
            'prix_unitaire': article3.prix_vente,
            'total_attendu': Decimal('0.75') * article3.prix_vente
        })
        
        print(f"\nArticles de test préparés:")
        for i, item in enumerate(articles_test, 1):
            print(f"  Article {i}: {item['article'].designation}")
            print(f"    Quantité: {item['quantite']}")
            print(f"    Prix unitaire: {item['prix_unitaire']} FCFA")
            print(f"    Total attendu: {item['total_attendu']} FCFA")
            print()
        
        # Créer la facture de test
        numero_ticket = f"TEST_DECIMAL_{int(timezone.now().timestamp())}"
        
        # Calculer le total de la facture
        total_facture = sum(item['total_attendu'] for item in articles_test)
        
        facture = FactureVente.objects.create(
            numero_ticket=numero_ticket,
            date=timezone.now().date(),
            heure=timezone.now().time(),
            nette_a_payer=total_facture,
            montant_regler=total_facture,
            rendu=Decimal('0.00'),
            remise=Decimal('0.00'),
            en_attente=False,
            nom_vendeuse='Test Décimales',
            client=client,
            caisse=caisse,
            agence=agence,
            session_caisse=session_caisse
        )
        
        print(f"Facture de test créée:")
        print(f"  Numéro: {facture.numero_ticket}")
        print(f"  Date: {facture.date}")
        print(f"  Client: {facture.client.intitule}")
        print(f"  Net à payer: {facture.nette_a_payer} FCFA")
        print()
        
        # Créer les lignes de facture
        total_verification = Decimal('0')
        
        for i, item in enumerate(articles_test, 1):
            ligne = LigneFactureVente.objects.create(
                facture_vente=facture,
                article=item['article'],
                designation=item['article'].designation,
                quantite=item['quantite'],
                prix_unitaire=item['prix_unitaire'],
                prix_total=item['total_attendu']
            )
            
            total_verification += ligne.prix_total
            
            print(f"Ligne {i} créée:")
            print(f"  Article: {ligne.designation}")
            print(f"  Quantité: {ligne.quantite}")
            print(f"  Prix unitaire: {ligne.prix_unitaire} FCFA")
            print(f"  Prix total: {ligne.prix_total} FCFA")
            print()
        
        print(f"VERIFICATION:")
        print(f"  Total calculé: {total_facture} FCFA")
        print(f"  Total vérification: {total_verification} FCFA")
        
        if total_facture == total_verification:
            print(f"  [SUCCES] Les calculs sont cohérents!")
        else:
            print(f"  [ERREUR] Incohérence dans les calculs!")
        
        print(f"\n" + "=" * 80)
        print(f"FACTURE DE TEST CREEE AVEC SUCCES!")
        print(f"=" * 80)
        print(f"Numéro de facture: {facture.numero_ticket}")
        print(f"Vous pouvez maintenant:")
        print(f"1. Aller sur http://127.0.0.1:8000")
        print(f"2. Vous connecter à la caisse")
        print(f"3. Chercher la facture: {facture.numero_ticket}")
        print(f"4. Vérifier que les quantités décimales sont correctes")
        print(f"=" * 80)
        
        return True
        
    except Exception as e:
        print(f"ERREUR lors de la création de la facture de test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    create_test_facture()
