#!/usr/bin/env python3
"""
Script pour vérifier si le stock change réellement en base de données
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, MouvementStock, Agence, Fournisseur
from django.utils import timezone

def verifier_stock_base_donnees():
    """
    Vérifier si le stock change réellement en base de données
    """
    print("🔍 VÉRIFICATION STOCK EN BASE DE DONNÉES")
    print("=" * 60)
    
    try:
        # 1. Vérifier toutes les agences
        agences = Agence.objects.all()
        print(f"📍 AGENCES TROUVÉES ({agences.count()}):")
        
        for agence in agences:
            print(f"   - {agence.nom_agence}")
        
        print()
        
        # 2. Vérifier chaque agence en détail
        for agence in agences:
            print(f"🏢 AGENCE: {agence.nom_agence}")
            print("-" * 50)
            
            # Articles de cette agence
            articles = Article.objects.filter(agence=agence)
            print(f"📦 Articles: {articles.count()}")
            
            if articles.exists():
                print("   Articles avec stock actuel:")
                for article in articles:
                    print(f"   - {article.designation}: {article.stock_actuel} unités")
            
            # Factures d'achat de cette agence
            factures = FactureAchat.objects.filter(agence=agence).order_by('-date_creation')
            print(f"📄 Factures d'achat: {factures.count()}")
            
            if factures.exists():
                print("   Dernières factures:")
                for facture in factures[:3]:  # 3 dernières
                    print(f"   - {facture.reference_achat} ({facture.date_creation})")
                    lignes = LigneFactureAchat.objects.filter(facture_achat=facture)
                    for ligne in lignes:
                        print(f"     * {ligne.designation}: +{ligne.quantite} unités")
            
            # Mouvements de stock de cette agence
            mouvements = MouvementStock.objects.filter(agence=agence).order_by('-date_mouvement')
            print(f"📊 Mouvements de stock: {mouvements.count()}")
            
            if mouvements.exists():
                mouvements_entree = mouvements.filter(type_mouvement='entree')
                mouvements_sortie = mouvements.filter(type_mouvement='sortie')
                print(f"   - Entrées: {mouvements_entree.count()}")
                print(f"   - Sorties: {mouvements_sortie.count()}")
                
                print("   Derniers mouvements:")
                for mouvement in mouvements[:5]:  # 5 derniers
                    print(f"   - {mouvement.get_type_mouvement_display()} {mouvement.article.designation}")
                    print(f"     Quantité: {mouvement.quantite}")
                    print(f"     Date: {mouvement.date_mouvement}")
                    print(f"     Facture: {mouvement.numero_piece}")
                    print()
            
            print()
        
        # 3. Test de création d'une facture d'achat pour vérifier
        print("🧪 TEST DE CRÉATION FACTURE D'ACHAT")
        print("-" * 40)
        
        # Prendre la première agence
        agence_test = agences.first()
        print(f"Agence de test: {agence_test.nom_agence}")
        
        # Prendre le premier article de cette agence
        article_test = Article.objects.filter(agence=agence_test).first()
        if not article_test:
            print("❌ Aucun article trouvé dans cette agence")
            return False
        
        print(f"Article de test: {article_test.designation}")
        stock_initial = article_test.stock_actuel
        print(f"Stock initial: {stock_initial}")
        
        # Créer un fournisseur de test
        fournisseur_test, created = Fournisseur.objects.get_or_create(
            intitule="Test Vérification Stock",
            defaults={'agence': agence_test}
        )
        
        # Créer une facture d'achat
        facture_test = FactureAchat.objects.create(
            numero_fournisseur="TEST_VERIF",
            date_achat=timezone.now().date(),
            heure=timezone.now().time(),
            reference_achat=f"VERIF_{int(timezone.now().timestamp())}",
            prix_total_global=500.00,
            statut='validee',
            fournisseur=fournisseur_test,
            agence=agence_test
        )
        
        print(f"✅ Facture créée: {facture_test.reference_achat}")
        
        # Créer une ligne de facture
        quantite_ajoutee = 10
        ligne_test = LigneFactureAchat.objects.create(
            facture_achat=facture_test,
            article=article_test,
            reference_article=article_test.reference_article,
            designation=article_test.designation,
            prix_unitaire=50.00,
            quantite=quantite_ajoutee,
            prix_total_article=500.00
        )
        
        print(f"✅ Ligne créée: {ligne_test.designation} - Quantité: {quantite_ajoutee}")
        
        # Mettre à jour le stock
        article_test.stock_actuel += quantite_ajoutee
        article_test.save()
        
        print(f"✅ Stock mis à jour: {stock_initial} → {article_test.stock_actuel}")
        
        # Créer un mouvement de stock
        MouvementStock.objects.create(
            article=article_test,
            agence=agence_test,
            type_mouvement='entree',
            date_mouvement=timezone.now(),
            numero_piece=facture_test.reference_achat,
            quantite_stock=article_test.stock_actuel,
            stock_initial=stock_initial,
            solde=article_test.stock_actuel,
            quantite=quantite_ajoutee,
            cout_moyen_pondere=float(article_test.prix_achat),
            stock_permanent=float(article_test.stock_actuel * article_test.prix_achat),
            facture_achat=facture_test,
            fournisseur=fournisseur_test,
            commentaire=f"Test Vérification - {facture_test.reference_achat}"
        )
        
        print("✅ Mouvement de stock créé")
        
        # Vérifier que la modification est persistante
        article_test.refresh_from_db()
        print(f"🔍 Stock vérifié en base: {article_test.stock_actuel}")
        
        if article_test.stock_actuel == stock_initial + quantite_ajoutee:
            print("✅ SUCCÈS: Le stock a été correctement mis à jour en base de données!")
            print("   Le problème est dans l'AFFICHAGE VISUEL de l'interface")
        else:
            print("❌ ÉCHEC: Le stock n'a pas été mis à jour en base de données")
            print("   Le problème est dans la LOGIQUE DE MISE À JOUR")
        
        # Nettoyer les données de test
        facture_test.delete()
        fournisseur_test.delete()
        print("🧹 Données de test supprimées")
        
        print(f"\n🎯 DIAGNOSTIC TERMINÉ")
        print("Si le stock change en base mais pas dans l'interface:")
        print("1. Problème d'affichage dans l'interface")
        print("2. Cache du navigateur")
        print("3. Problème de session utilisateur")
        print("4. Problème de requête dans la vue")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verifier_stock_base_donnees()



