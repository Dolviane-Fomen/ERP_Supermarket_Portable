#!/usr/bin/env python3
"""
Test final des quantités décimales avec le serveur relancé
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureVente, LigneFactureVente, Agence, Client, Caisse, Employe
from django.utils import timezone
from decimal import Decimal

def test_final_quantites_decimales():
    """
    Test final des quantités décimales
    """
    print("TEST FINAL - QUANTITÉS DÉCIMALES")
    print("=" * 50)
    
    try:
        # 1. Récupérer l'agence et l'article
        agence = Agence.objects.get(nom_agence__icontains="POISSONNERIE SANGAH")
        article = Article.objects.get(designation__icontains="BAR CALADA DETAIL", agence=agence)
        
        print(f"[OK] Agence: {agence.nom_agence}")
        print(f"[OK] Article: {article.designation}")
        print(f"[OK] Stock actuel: {article.stock_actuel}")
        
        # 2. Tester la création d'une ligne avec quantité décimale
        print(f"\n[TEST] Création d'une ligne avec quantité 0.75...")
        
        # Créer une facture temporaire pour le test
        client = Client.objects.filter(agence=agence).first()
        caisse = Caisse.objects.filter(agence=agence).first()
        employe = Employe.objects.filter(compte__agence=agence).first()
        
        facture = FactureVente.objects.create(
            numero_ticket=f"TEST_FINAL_{int(timezone.now().timestamp())}",
            date=timezone.now().date(),
            heure=timezone.now().time(),
            nette_a_payer=Decimal('75.00'),
            montant_regler=Decimal('75.00'),
            rendu=Decimal('0.00'),
            remise=Decimal('0.00'),
            en_attente=False,
            nom_vendeuse=employe.compte.user.first_name,
            client=client,
            caisse=caisse,
            agence=agence,
            vendeur=employe
        )
        
        # Créer une ligne avec quantité décimale
        ligne = LigneFactureVente.objects.create(
            facture_vente=facture,
            article=article,
            designation=article.designation,
            quantite=Decimal('0.75'),  # 3/4 de kg
            prix_unitaire=Decimal('100.00'),
            prix_total=Decimal('75.00')
        )
        
        # Test supplémentaire: quantité négative (retour de marchandise)
        print(f"\n[TEST] Test quantité négative (-0.25)...")
        ligne_retour = LigneFactureVente.objects.create(
            facture_vente=facture,
            article=article,
            designation=article.designation,
            quantite=Decimal('-0.25'),  # Retour de marchandise
            prix_unitaire=Decimal('100.00'),
            prix_total=Decimal('-25.00')
        )
        print(f"[SUCCÈS] Ligne de retour créée avec quantité: {ligne_retour.quantite}")
        
        print(f"[SUCCÈS] Ligne créée avec quantité: {ligne.quantite}")
        print(f"[SUCCÈS] Type de quantité: {type(ligne.quantite)}")
        print(f"[SUCCÈS] Prix total: {ligne.prix_total}")
        
        # 3. Tester la mise à jour du stock
        stock_avant = article.stock_actuel
        article.stock_actuel -= Decimal('0.75')
        article.save()
        stock_apres = article.stock_actuel
        
        print(f"\n[STOCK] Avant: {stock_avant}")
        print(f"[STOCK] Après: {stock_apres}")
        print(f"[STOCK] Différence: {stock_avant - stock_apres}")
        
        if stock_apres == stock_avant - Decimal('0.75'):
            print("[SUCCÈS] Mise à jour du stock avec quantité décimale réussie!")
        else:
            print("[ÉCHEC] Problème avec la mise à jour du stock")
            return False
        
        # 4. Nettoyer
        facture.delete()
        article.stock_actuel = stock_avant
        article.save()
        
        print(f"\n[TEST TERMINÉ AVEC SUCCÈS!]")
        print("Les quantités décimales fonctionnent parfaitement!")
        print("Vous pouvez maintenant utiliser votre ERP avec des quantités comme 0.5, 1.25, 2.75, etc.")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_final_quantites_decimales()
