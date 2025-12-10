#!/usr/bin/env python3
"""
Script pour vérifier pourquoi le stock ne s'affiche pas correctement dans l'interface
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, MouvementStock, Agence, Fournisseur
from django.utils import timezone

def verifier_interface_stock():
    """
    Vérifier l'état du stock dans l'interface
    """
    print("🔍 VÉRIFICATION INTERFACE STOCK")
    print("=" * 50)
    
    try:
        # 1. Vérifier l'agence
        agence = Agence.objects.first()
        print(f"📍 Agence: {agence.nom_agence}")
        
        # 2. Vérifier les articles et leur stock
        articles = Article.objects.filter(agence=agence)
        print(f"\n📦 ARTICLES ET STOCK ACTUEL:")
        
        for article in articles:
            print(f"   - {article.designation}")
            print(f"     Stock: {article.stock_actuel}")
            print(f"     Prix achat: {article.prix_achat}")
            print(f"     Dernier prix: {article.dernier_prix_achat}")
            print()
        
        # 3. Vérifier les factures d'achat
        factures = FactureAchat.objects.filter(agence=agence).order_by('-date_creation')
        print(f"📄 FACTURES D'ACHAT ({factures.count()}):")
        
        for facture in factures[:3]:  # 3 dernières
            print(f"   - {facture.reference_achat} ({facture.date_creation})")
            lignes = LigneFactureAchat.objects.filter(facture_achat=facture)
            for ligne in lignes:
                print(f"     * {ligne.designation}: {ligne.quantite} unités")
        
        # 4. Vérifier les mouvements de stock
        mouvements = MouvementStock.objects.filter(agence=agence).order_by('-date_mouvement')
        print(f"\n📊 MOUVEMENTS DE STOCK ({mouvements.count()}):")
        
        for mouvement in mouvements[:5]:  # 5 derniers
            print(f"   - {mouvement.get_type_mouvement_display()} {mouvement.article.designation}")
            print(f"     Quantité: {mouvement.quantite}")
            print(f"     Date: {mouvement.date_mouvement}")
            print(f"     Facture: {mouvement.numero_piece}")
            print()
        
        # 5. Test de simulation d'une facture d'achat
        print("🧪 SIMULATION FACTURE D'ACHAT")
        print("-" * 30)
        
        # Prendre le premier article
        article_test = articles.first()
        stock_initial = article_test.stock_actuel
        
        print(f"Article: {article_test.designation}")
        print(f"Stock initial: {stock_initial}")
        
        # Simuler l'ajout de stock
        quantite_ajoutee = 2
        article_test.stock_actuel += quantite_ajoutee
        article_test.save()
        
        print(f"Quantité ajoutée: {quantite_ajoutee}")
        print(f"Stock après ajout: {article_test.stock_actuel}")
        
        # Vérifier que la modification est persistante
        article_test.refresh_from_db()
        print(f"Stock vérifié: {article_test.stock_actuel}")
        
        if article_test.stock_actuel == stock_initial + quantite_ajoutee:
            print("✅ Stock correctement mis à jour en base de données")
        else:
            print("❌ Problème de mise à jour en base de données")
        
        # Remettre le stock à sa valeur initiale
        article_test.stock_actuel = stock_initial
        article_test.save()
        print("🔄 Stock remis à sa valeur initiale")
        
        print(f"\n🎯 DIAGNOSTIC TERMINÉ")
        print("Si le stock ne s'affiche pas dans l'interface:")
        print("1. Vérifiez que vous êtes connecté avec la bonne agence")
        print("2. Rafraîchissez la page (Ctrl+F5)")
        print("3. Vérifiez la console du navigateur pour les erreurs")
        print("4. Redémarrez le serveur Django")
        
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verifier_interface_stock()



