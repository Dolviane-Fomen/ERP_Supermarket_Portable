#!/usr/bin/env python3
"""
Test simple pour vérifier la création d'une facture d'achat et la mise à jour du stock
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, Agence, Fournisseur
from django.utils import timezone

def test_facture_simple():
    """
    Test simple de création de facture d'achat
    """
    print("🧪 TEST SIMPLE - CRÉATION FACTURE D'ACHAT")
    print("=" * 50)
    
    try:
        # Récupérer les données
        agence = Agence.objects.first()
        article = Article.objects.filter(agence=agence).first()
        
        if not agence or not article:
            print("❌ Données manquantes")
            return False
        
        print(f"✅ Agence: {agence.nom_agence}")
        print(f"✅ Article: {article.designation}")
        print(f"   Stock AVANT création facture: {article.stock_actuel}")
        
        # Créer un fournisseur de test
        fournisseur_test, created = Fournisseur.objects.get_or_create(
            intitule="Test Simple",
            defaults={'agence': agence}
        )
        
        # Créer une facture d'achat (comme dans l'interface web)
        facture = FactureAchat.objects.create(
            numero_fournisseur="TEST_SIMPLE",
            date_achat=timezone.now().date(),
            heure=timezone.now().time(),
            reference_achat=f"SIMPLE_{int(timezone.now().timestamp())}",
            prix_total_global=150.00,
            statut='validee',  # Statut validée pour déclencher la mise à jour
            fournisseur=fournisseur_test,
            agence=agence
        )
        
        print(f"✅ Facture créée: {facture.reference_achat}")
        print(f"   Statut: {facture.statut}")
        
        # Créer une ligne de facture
        ligne = LigneFactureAchat.objects.create(
            facture_achat=facture,
            article=article,
            reference_article=article.reference_article,
            designation=article.designation,
            prix_unitaire=75.00,
            quantite=2,
            prix_total_article=150.00
        )
        
        print(f"✅ Ligne créée: {ligne.designation} - Quantité: {ligne.quantite}")
        
        # Vérifier le stock après création
        article.refresh_from_db()
        print(f"   Stock APRÈS création facture: {article.stock_actuel}")
        
        # Vérifier qu'un mouvement de stock a été créé
        from supermarket.models import MouvementStock
        mouvements = MouvementStock.objects.filter(facture_achat=facture)
        print(f"✅ Mouvements de stock créés: {mouvements.count()}")
        
        # Nettoyer
        facture.delete()
        fournisseur_test.delete()
        print("🧹 Données de test supprimées")
        
        print("\n🎉 TEST TERMINÉ!")
        return True
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_facture_simple()
