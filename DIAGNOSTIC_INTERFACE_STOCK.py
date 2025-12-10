#!/usr/bin/env python3
"""
Script de diagnostic pour identifier pourquoi le stock ne se met pas à jour dans l'interface
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, MouvementStock, Agence, Fournisseur
from django.utils import timezone

def diagnostic_interface_stock():
    """
    Diagnostic spécifique pour l'interface utilisateur
    """
    print("🔍 DIAGNOSTIC INTERFACE UTILISATEUR - STOCK")
    print("=" * 60)
    
    try:
        # 1. Vérifier l'état actuel des articles
        agence = Agence.objects.first()
        articles = Article.objects.filter(agence=agence)
        
        print(f"📦 ARTICLES ACTUELS:")
        for article in articles:
            print(f"   - {article.designation}: {article.stock_actuel} unités")
        
        # 2. Vérifier les factures d'achat récentes
        factures_recentes = FactureAchat.objects.filter(agence=agence).order_by('-date_creation')[:3]
        print(f"\n📄 FACTURES D'ACHAT RÉCENTES:")
        
        for facture in factures_recentes:
            print(f"   - {facture.reference_achat} ({facture.date_creation})")
            lignes = LigneFactureAchat.objects.filter(facture_achat=facture)
            for ligne in lignes:
                print(f"     * {ligne.designation}: +{ligne.quantite} unités")
        
        # 3. Vérifier les mouvements de stock récents
        mouvements_recents = MouvementStock.objects.filter(agence=agence).order_by('-date_mouvement')[:5]
        print(f"\n📊 MOUVEMENTS RÉCENTS:")
        
        for mouvement in mouvements_recents:
            print(f"   - {mouvement.get_type_mouvement_display()} {mouvement.article.designation}: {mouvement.quantite} ({mouvement.date_mouvement})")
        
        # 4. Test de création d'une facture d'achat complète
        print(f"\n🧪 TEST COMPLET DE FACTURE D'ACHAT")
        print("-" * 40)
        
        # Créer un fournisseur
        fournisseur, created = Fournisseur.objects.get_or_create(
            intitule="Test Interface",
            defaults={'agence': agence}
        )
        
        # Créer une facture
        facture = FactureAchat.objects.create(
            numero_fournisseur="INTERFACE_TEST",
            date_achat=timezone.now().date(),
            heure=timezone.now().time(),
            reference_achat=f"INTERFACE_{int(timezone.now().timestamp())}",
            prix_total_global=1000.00,
            statut='validee',
            fournisseur=fournisseur,
            agence=agence
        )
        
        print(f"✅ Facture créée: {facture.reference_achat}")
        
        # Traiter chaque article
        for article in articles:
            stock_avant = article.stock_actuel
            quantite_ajoutee = 3
            
            # Créer la ligne
            ligne = LigneFactureAchat.objects.create(
                facture_achat=facture,
                article=article,
                reference_article=article.reference_article,
                designation=article.designation,
                prix_unitaire=100.00,
                quantite=quantite_ajoutee,
                prix_total_article=300.00
            )
            
            # Mettre à jour le stock
            article.stock_actuel += quantite_ajoutee
            article.save()
            
            # Créer le mouvement
            MouvementStock.objects.create(
                article=article,
                agence=agence,
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
                commentaire=f"Test Interface - {facture.reference_achat}"
            )
            
            print(f"   ✅ {article.designation}: {stock_avant} → {article.stock_actuel} (+{quantite_ajoutee})")
        
        # 5. Vérifier le résultat final
        print(f"\n🔍 VÉRIFICATION FINALE:")
        articles.refresh_from_db()
        for article in articles:
            print(f"   - {article.designation}: {article.stock_actuel} unités")
        
        # 6. Nettoyer
        facture.delete()
        fournisseur.delete()
        print(f"\n🧹 Données de test supprimées")
        
        print(f"\n🎯 DIAGNOSTIC TERMINÉ")
        print("Si le stock ne se met pas à jour dans l'interface:")
        print("1. Vérifiez que vous utilisez la bonne agence")
        print("2. Rafraîchissez la page (F5)")
        print("3. Vérifiez les mouvements de stock")
        print("4. Redémarrez le navigateur")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    diagnostic_interface_stock()



