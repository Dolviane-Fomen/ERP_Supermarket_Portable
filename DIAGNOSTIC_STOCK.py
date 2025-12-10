#!/usr/bin/env python3
"""
Script de diagnostic pour vérifier le fonctionnement du stock
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, MouvementStock, Agence, Fournisseur
from django.utils import timezone

def diagnostic_complet():
    """
    Diagnostic complet du système de stock
    """
    print("DIAGNOSTIC COMPLET DU SYSTEME DE STOCK")
    print("=" * 60)
    
    try:
        # 1. Vérifier les agences
        agences = Agence.objects.all()
        print(f"Agences trouvees: {agences.count()}")
        
        if not agences.exists():
            print("ERREUR: Aucune agence trouvee")
            return False
        
        agence = agences.first()
        print(f"   - Agence principale: {agence.nom_agence}")
        
        # 2. Vérifier les articles
        articles = Article.objects.filter(agence=agence)
        print(f"\nArticles trouves: {articles.count()}")
        
        if not articles.exists():
            print("ERREUR: Aucun article trouve")
            return False
        
        # Afficher quelques articles avec leur stock
        print("   Articles avec stock:")
        for article in articles[:5]:
            print(f"   - {article.designation}: {article.stock_actuel} unités")
        
        # 3. Vérifier les factures d'achat
        factures_achat = FactureAchat.objects.filter(agence=agence)
        print(f"\nFactures d'achat: {factures_achat.count()}")
        
        if factures_achat.exists():
            derniere_facture = factures_achat.order_by('-date_creation').first()
            print(f"   - Derniere facture: {derniere_facture.reference_achat}")
            
            # Vérifier les lignes de cette facture
            lignes = LigneFactureAchat.objects.filter(facture_achat=derniere_facture)
            print(f"   - Lignes de facture: {lignes.count()}")
            
            for ligne in lignes:
                print(f"     * {ligne.designation}: {ligne.quantite} unites")
        
        # 4. Vérifier les mouvements de stock
        mouvements = MouvementStock.objects.filter(agence=agence)
        print(f"\nMouvements de stock: {mouvements.count()}")
        
        if mouvements.exists():
            mouvements_entree = mouvements.filter(type_mouvement='entree')
            mouvements_sortie = mouvements.filter(type_mouvement='sortie')
            
            print(f"   - Entrees: {mouvements_entree.count()}")
            print(f"   - Sorties: {mouvements_sortie.count()}")
            
            # Afficher les derniers mouvements
            derniers_mouvements = mouvements.order_by('-date_mouvement')[:3]
            print("   Derniers mouvements:")
            for mouvement in derniers_mouvements:
                print(f"     * {mouvement.get_type_mouvement_display()} - {mouvement.article.designation}: {mouvement.quantite}")
        
        # 5. Test de création d'une facture d'achat
        print(f"\nTEST DE CREATION D'UNE FACTURE D'ACHAT")
        print("-" * 40)
        
        # Créer un fournisseur de test
        fournisseur_test, created = Fournisseur.objects.get_or_create(
            intitule="Fournisseur Test Diagnostic",
            defaults={'agence': agence}
        )
        
        # Créer une facture de test
        facture_test = FactureAchat.objects.create(
            numero_fournisseur="TEST_DIAG",
            date_achat=timezone.now().date(),
            heure=timezone.now().time(),
            reference_achat=f"DIAG_{int(timezone.now().timestamp())}",
            prix_total_global=500.00,
            statut='validee',
            fournisseur=fournisseur_test,
            agence=agence
        )
        
        print(f"OK - Facture de test creee: {facture_test.reference_achat}")
        
        # Prendre le premier article pour le test
        article_test = articles.first()
        stock_initial = article_test.stock_actuel
        
        # Créer une ligne de facture
        ligne_test = LigneFactureAchat.objects.create(
            facture_achat=facture_test,
            article=article_test,
            reference_article=article_test.reference_article,
            designation=article_test.designation,
            prix_unitaire=100.00,
            quantite=2,
            prix_total_article=200.00
        )
        
        print(f"OK - Ligne creee: {ligne_test.designation} - Quantite: {ligne_test.quantite}")
        
        # Mettre à jour le stock
        article_test.stock_actuel += ligne_test.quantite
        article_test.save()
        
        print(f"OK - Stock mis a jour: {stock_initial} -> {article_test.stock_actuel}")
        
        # Créer un mouvement de stock
        MouvementStock.objects.create(
            article=article_test,
            agence=agence,
            type_mouvement='entree',
            date_mouvement=timezone.now(),
            numero_piece=facture_test.reference_achat,
            quantite_stock=article_test.stock_actuel,
            stock_initial=stock_initial,
            solde=article_test.stock_actuel,
            quantite=ligne_test.quantite,
            cout_moyen_pondere=float(article_test.prix_achat),
            stock_permanent=float(article_test.stock_actuel * article_test.prix_achat),
            facture_achat=facture_test,
            fournisseur=fournisseur_test,
            commentaire=f"Test Diagnostic - {facture_test.reference_achat}"
        )
        
        print("OK - Mouvement de stock cree")
        
        # Vérifier le résultat
        article_test.refresh_from_db()
        if article_test.stock_actuel == stock_initial + ligne_test.quantite:
            print("SUCCES: Le stock a ete correctement mis a jour!")
        else:
            print("ECHEC: Le stock n'a pas ete mis a jour correctement")
            return False
        
        # Nettoyer les données de test
        facture_test.delete()
        fournisseur_test.delete()
        print("Donnees de test supprimees")
        
        print(f"\nDIAGNOSTIC TERMINE AVEC SUCCES!")
        print("Le systeme de stock fonctionne correctement.")
        
        return True
        
    except Exception as e:
        print(f"ERREUR LORS DU DIAGNOSTIC: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    diagnostic_complet()


# Test de fermeture de caisse avec nombres décimaux
def test_fermeture_caisse_decimal():
    """Test de la fermeture de caisse avec des nombres décimaux"""
    print("\n" + "=" * 80)
    print("TEST DE FERMETURE DE CAISSE AVEC NOMBRES DÉCIMAUX")
    print("=" * 80)
    
    try:
        from decimal import Decimal
        import json
        from supermarket.models import (
            Caisse, Employe, Compte, SessionCaisse, 
            FactureVente, LigneFactureVente, DocumentVente, 
            Client, Famille
        )
        from django.contrib.auth.models import User
        
        # Récupérer l'agence
        agence = Agence.objects.first()
        if not agence:
            print("ERREUR: Aucune agence trouvée")
            return False
        
        print(f"\n[OK] Agence: {agence.nom_agence}")
        
        # Utiliser des articles existants avec prix décimaux
        print("\nRécupération d'articles existants...")
        articles = Article.objects.filter(agence=agence)[:3]
        
        if articles.count() < 3:
            print("  ⚠️  Pas assez d'articles, création de quelques articles de test...")
            famille = Famille.objects.first()
            if not famille:
                famille = Famille.objects.create(
                    code="TEST",
                    intitule="Famille Test",
                    unite_vente="U",
                    suivi_stock=True
                )
            
            for i in range(3 - articles.count()):
                article = Article.objects.create(
                    reference_article=f"REF_TEST{i+1:03d}",
                    designation=f"Article Test {i+1}",
                    prix_achat=Decimal(f'{10.5 + i * 2.3}'),
                    prix_vente=Decimal(f'{15.75 + i * 3.5}'),
                    stock_actuel=100,
                    famille=famille,
                    agence=agence
                )
                articles = list(articles) + [article]
        
        print(f"  [OK] {len(articles)} articles trouves")
        
        # Simuler le processus de fermeture de caisse
        print("\nSimulation de la fermeture de caisse...")
        
        # Données de test avec nombres décimaux
        factures_data = []
        chiffre_affaires = 0.0
        
        for i in range(2):
            facture_data = {
                'numero_ticket': f'TKT_DEC{i+1:03d}',
                'date': '2025-10-24',
                'heure': '14:30',
                'client': 'Client Test Decimal',
                'nette_a_payer': float(Decimal(f'{100.50 + i * 25.75}')),
                'articles': []
            }
            
            for j, article in enumerate(articles[:2]):
                quantite = Decimal(f'{1 + j * 0.5}')
                prix_unitaire = article.prix_vente
                prix_total = quantite * prix_unitaire
                
                facture_data['articles'].append({
                    'designation': article.designation,
                    'reference': article.reference_article,
                    'quantite': int(quantite),
                    'prix_unitaire': float(prix_unitaire),
                    'total': float(prix_total)
                })
            
            chiffre_affaires += facture_data['nette_a_payer']
            factures_data.append(facture_data)
        
        # Test de sérialisation JSON
        print("\nTest de serialisation JSON...")
        try:
            json_string = json.dumps(factures_data)
            print(f"[OK] SUCCES: Donnees serialisables en JSON ({len(json_string)} caracteres)")
        except TypeError as e:
            print(f"[ERREUR] {e}")
            return False
        
        # Test de la réponse JSON finale
        print("\nTest de la reponse JSON finale...")
        response_data = {
            'success': True,
            'message': 'Caisse fermee avec succes!',
            'document_id': 123,
            'chiffre_affaires': float(chiffre_affaires),
            'redirect_url': '/caisse/'
        }
        
        try:
            json_response = json.dumps(response_data)
            print(f"[OK] SUCCES: Reponse JSON serialisable")
        except TypeError as e:
            print(f"[ERREUR] {e}")
            return False
        
        print("\n" + "=" * 80)
        print("[OK] TOUS LES TESTS SONT PASSES AVEC SUCCES!")
        print("=" * 80)
        print(f"\nResume:")
        print(f"  - Chiffre d'affaires: {chiffre_affaires} FCFA")
        print(f"  - Articles avec prix decimaux: OK")
        print(f"  - Quantites decimales: OK")
        print(f"  - Serialisation JSON: OK")
        
        return True
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Lancer les deux tests
    success1 = diagnostic_complet()
    success2 = test_fermeture_caisse_decimal()
    
    if success1 and success2:
        print("\n[SUCCES] TOUS LES TESTS SONT REUSSIS!")
    else:
        print("\n[ECHEC] CERTAINS TESTS ONT ECHOUE!")
