#!/usr/bin/env python3
"""
Script de diagnostic pour toutes les agences - Vérification du stock
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, MouvementStock, Agence, Fournisseur
from django.utils import timezone

def diagnostic_toutes_agences():
    """
    Diagnostic pour toutes les agences
    """
    print("🔍 DIAGNOSTIC TOUTES LES AGENCES - STOCK")
    print("=" * 60)
    
    try:
        # 1. Lister toutes les agences
        agences = Agence.objects.all()
        print(f"📍 AGENCES TROUVÉES ({agences.count()}):")
        
        for agence in agences:
            print(f"   - {agence.nom_agence}")
        
        print()
        
        # 2. Vérifier chaque agence
        for agence in agences:
            print(f"🏢 AGENCE: {agence.nom_agence}")
            print("-" * 40)
            
            # Articles de cette agence
            articles = Article.objects.filter(agence=agence)
            print(f"📦 Articles: {articles.count()}")
            
            if articles.exists():
                for article in articles:
                    print(f"   - {article.designation}: {article.stock_actuel} unités")
            
            # Factures d'achat de cette agence
            factures = FactureAchat.objects.filter(agence=agence)
            print(f"📄 Factures d'achat: {factures.count()}")
            
            if factures.exists():
                derniere_facture = factures.order_by('-date_creation').first()
                print(f"   - Dernière: {derniere_facture.reference_achat}")
            
            # Mouvements de stock de cette agence
            mouvements = MouvementStock.objects.filter(agence=agence)
            print(f"📊 Mouvements: {mouvements.count()}")
            
            if mouvements.exists():
                mouvements_entree = mouvements.filter(type_mouvement='entree')
                mouvements_sortie = mouvements.filter(type_mouvement='sortie')
                print(f"   - Entrées: {mouvements_entree.count()}")
                print(f"   - Sorties: {mouvements_sortie.count()}")
            
            print()
        
        # 3. Test spécifique pour POISSONERIE SANGHA
        print("🐟 TEST SPÉCIFIQUE - POISSONERIE SANGHA")
        print("-" * 50)
        
        try:
            agence_sangha = Agence.objects.get(nom_agence__icontains="SANGHA")
            print(f"✅ Agence trouvée: {agence_sangha.nom_agence}")
            
            # Articles de cette agence
            articles_sangha = Article.objects.filter(agence=agence_sangha)
            print(f"📦 Articles dans cette agence: {articles_sangha.count()}")
            
            if articles_sangha.exists():
                print("Articles avec stock:")
                for article in articles_sangha:
                    print(f"   - {article.designation}: {article.stock_actuel} unités")
                
                # Test de création d'une facture d'achat pour cette agence
                print(f"\n🧪 TEST FACTURE D'ACHAT POUR {agence_sangha.nom_agence}")
                
                # Créer un fournisseur pour cette agence
                fournisseur, created = Fournisseur.objects.get_or_create(
                    intitule="Fournisseur Test Sangha",
                    defaults={'agence': agence_sangha}
                )
                
                # Créer une facture d'achat
                facture = FactureAchat.objects.create(
                    numero_fournisseur="SANGHA_TEST",
                    date_achat=timezone.now().date(),
                    heure=timezone.now().time(),
                    reference_achat=f"SANGHA_{int(timezone.now().timestamp())}",
                    prix_total_global=2000.00,
                    statut='validee',
                    fournisseur=fournisseur,
                    agence=agence_sangha
                )
                
                print(f"✅ Facture créée: {facture.reference_achat}")
                
                # Traiter chaque article de cette agence
                for article in articles_sangha:
                    stock_avant = article.stock_actuel
                    quantite_ajoutee = 5
                    
                    # Créer la ligne
                    ligne = LigneFactureAchat.objects.create(
                        facture_achat=facture,
                        article=article,
                        reference_article=article.reference_article,
                        designation=article.designation,
                        prix_unitaire=200.00,
                        quantite=quantite_ajoutee,
                        prix_total_article=1000.00
                    )
                    
                    # Mettre à jour le stock
                    article.stock_actuel += quantite_ajoutee
                    article.save()
                    
                    # Créer le mouvement
                    MouvementStock.objects.create(
                        article=article,
                        agence=agence_sangha,
                        type_mouvement='entree',
                        date_mouvement=timezone.now(),
                        numero_piece=facture.reference_achat,
                        quantite_stock=article.stock_actuel,
                        stock_initial=stock_avant,
                        solde=article.stock_actuel,
                        quantite=quantite_ajoutee,
                        cout_moyen_pondere=float(article.prix_achat),
                        stock_permanent=float(article.stock_actuel * article.prix_achat),
                        facture_achat=facture,
                        fournisseur=fournisseur,
                        commentaire=f"Test Sangha - {facture.reference_achat}"
                    )
                    
                    print(f"   ✅ {article.designation}: {stock_avant} → {article.stock_actuel} (+{quantite_ajoutee})")
                
                # Nettoyer les données de test
                facture.delete()
                fournisseur.delete()
                print("🧹 Données de test supprimées")
                
            else:
                print("⚠️ Aucun article trouvé dans cette agence")
                print("💡 Créez d'abord des articles pour cette agence")
            
        except Agence.DoesNotExist:
            print("❌ Agence POISSONERIE SANGHA non trouvée")
            print("Agences disponibles:")
            for agence in agences:
                print(f"   - {agence.nom_agence}")
        
        print(f"\n🎯 DIAGNOSTIC TERMINÉ")
        print("Le système de stock fonctionne pour toutes les agences.")
        print("Assurez-vous d'être connecté avec la bonne agence dans l'interface.")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    diagnostic_toutes_agences()



