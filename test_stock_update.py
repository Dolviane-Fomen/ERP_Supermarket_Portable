#!/usr/bin/env python3
"""
Script de test pour vérifier la mise à jour du stock lors des factures d'achat
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, MouvementStock, Agence, Fournisseur
from django.utils import timezone

def test_stock_update():
    """
    Test pour vérifier que le stock se met à jour correctement
    """
    print("🧪 TEST DE MISE À JOUR DU STOCK")
    print("=" * 50)
    
    try:
        # Récupérer la première agence
        agence = Agence.objects.first()
        if not agence:
            print("❌ Aucune agence trouvée")
            return
        
        print(f"📍 Agence: {agence.nom_agence}")
        
        # Récupérer le premier article
        article = Article.objects.filter(agence=agence).first()
        if not article:
            print("❌ Aucun article trouvé")
            return
        
        print(f"📦 Article: {article.designation}")
        print(f"📊 Stock initial: {article.stock_actuel}")
        
        # Créer un fournisseur de test
        fournisseur, created = Fournisseur.objects.get_or_create(
            intitule="Fournisseur Test",
            defaults={'agence': agence}
        )
        
        # Créer une facture d'achat de test
        facture = FactureAchat.objects.create(
            numero_fournisseur="TEST001",
            date_achat=timezone.now().date(),
            heure=timezone.now().time(),
            reference_achat=f"TEST_{int(timezone.now().timestamp())}",
            prix_total_global=1000.00,
            statut='validee',
            fournisseur=fournisseur,
            agence=agence
        )
        
        print(f"📄 Facture créée: {facture.reference_achat}")
        
        # Créer une ligne de facture
        quantite_ajoutee = 5
        ligne = LigneFactureAchat.objects.create(
            facture_achat=facture,
            article=article,
            reference_article=article.reference_article,
            designation=article.designation,
            prix_unitaire=200.00,
            quantite=quantite_ajoutee,
            prix_total_article=1000.00
        )
        
        print(f"📝 Ligne créée: {ligne.designation} - Quantité: {quantite_ajoutee}")
        
        # Mettre à jour le stock
        ancien_stock = article.stock_actuel
        article.stock_actuel += quantite_ajoutee
        article.save()
        
        print(f"📈 Stock mis à jour: {ancien_stock} → {article.stock_actuel}")
        
        # Créer un mouvement de stock
        MouvementStock.objects.create(
            article=article,
            agence=agence,
            type_mouvement='entree',
            date_mouvement=timezone.now(),
            numero_piece=facture.reference_achat,
            quantite_stock=article.stock_actuel,
            stock_initial=ancien_stock,
            solde=article.stock_actuel,
            quantite=quantite_ajoutee,
            cout_moyen_pondere=float(article.prix_achat),
            stock_permanent=float(article.stock_actuel * article.prix_achat),
            facture_achat=facture,
            fournisseur=fournisseur,
            commentaire=f"Test - Facture {facture.reference_achat}"
        )
        
        print("✅ Mouvement de stock créé")
        
        # Vérifier le résultat
        article.refresh_from_db()
        print(f"🔍 Stock final vérifié: {article.stock_actuel}")
        
        if article.stock_actuel == ancien_stock + quantite_ajoutee:
            print("✅ SUCCÈS: Le stock a été correctement mis à jour!")
        else:
            print("❌ ÉCHEC: Le stock n'a pas été mis à jour correctement")
        
        # Nettoyer les données de test
        facture.delete()
        print("🧹 Données de test supprimées")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_stock_update()



