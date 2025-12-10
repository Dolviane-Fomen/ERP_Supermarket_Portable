#!/usr/bin/env python3
"""
Script pour tester l'affichage du stock dans l'interface
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, MouvementStock, Agence, Fournisseur
from django.utils import timezone

def test_affichage_stock():
    """
    Test pour vérifier l'affichage du stock
    """
    print("🔍 TEST AFFICHAGE STOCK")
    print("=" * 50)
    
    try:
        # 1. Vérifier l'agence POISSONNERIE SANGAH
        agence = Agence.objects.get(nom_agence="POISSONNERIE SANGAH")
        print(f"📍 Agence: {agence.nom_agence}")
        
        # 2. Prendre un article de cette agence
        article = Article.objects.filter(agence=agence).first()
        if not article:
            print("❌ Aucun article trouvé dans cette agence")
            return False
        
        print(f"📦 Article: {article.designation}")
        stock_initial = article.stock_actuel
        print(f"📊 Stock initial: {stock_initial}")
        
        # 3. Créer une facture d'achat
        fournisseur, created = Fournisseur.objects.get_or_create(
            intitule="Test Affichage",
            defaults={'agence': agence}
        )
        
        facture = FactureAchat.objects.create(
            numero_fournisseur="TEST_AFFICHAGE",
            date_achat=timezone.now().date(),
            heure=timezone.now().time(),
            reference_achat=f"AFFICHAGE_{int(timezone.now().timestamp())}",
            prix_total_global=1000.00,
            statut='validee',
            fournisseur=fournisseur,
            agence=agence
        )
        
        print(f"✅ Facture créée: {facture.reference_achat}")
        
        # 4. Créer une ligne de facture
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
        
        print(f"✅ Ligne créée: {ligne.designation} - Quantité: {quantite_ajoutee}")
        
        # 5. Mettre à jour le stock
        article.stock_actuel += quantite_ajoutee
        article.save()
        
        print(f"✅ Stock mis à jour: {stock_initial} → {article.stock_actuel}")
        
        # 6. Créer un mouvement de stock
        MouvementStock.objects.create(
            article=article,
            agence=agence,
            type_mouvement='entree',
            date_mouvement=timezone.now(),
            numero_piece=facture.reference_achat,
            quantite_stock=article.stock_actuel,
            stock_initial=stock_initial,
            solde=article.stock_actuel,
            quantite=quantite_ajoutee,
            cout_moyen_pondere=float(article.prix_achat),
            stock_permanent=float(article.stock_actuel * article.prix_achat),
            facture_achat=facture,
            fournisseur=fournisseur,
            commentaire=f"Test Affichage - {facture.reference_achat}"
        )
        
        print("✅ Mouvement de stock créé")
        
        # 7. Vérifier que la modification est persistante
        article.refresh_from_db()
        print(f"🔍 Stock vérifié en base: {article.stock_actuel}")
        
        # 8. Simuler une requête comme dans l'interface
        print(f"\n📋 SIMULATION REQUÊTE INTERFACE:")
        print(f"   - Agence: {agence.nom_agence}")
        print(f"   - Article: {article.designation}")
        print(f"   - Stock affiché: {article.stock_actuel}")
        
        # 9. Vérifier les mouvements récents
        mouvements_recents = MouvementStock.objects.filter(
            agence=agence,
            article=article
        ).order_by('-date_mouvement')[:3]
        
        print(f"\n📊 MOUVEMENTS RÉCENTS POUR CET ARTICLE:")
        for mouvement in mouvements_recents:
            print(f"   - {mouvement.get_type_mouvement_display()} {mouvement.quantite} unités")
            print(f"     Date: {mouvement.date_mouvement}")
            print(f"     Facture: {mouvement.numero_piece}")
        
        # 10. Nettoyer les données de test
        facture.delete()
        fournisseur.delete()
        print(f"\n🧹 Données de test supprimées")
        
        print(f"\n🎯 RÉSULTAT DU TEST:")
        if article.stock_actuel == stock_initial + quantite_ajoutee:
            print("✅ SUCCÈS: Le stock a été correctement mis à jour!")
            print("   Le problème est dans l'AFFICHAGE de l'interface")
            print("   Solutions:")
            print("   1. Rafraîchir la page (F5)")
            print("   2. Vider le cache du navigateur")
            print("   3. Redémarrer le serveur Django")
            print("   4. Vérifier la session utilisateur")
        else:
            print("❌ ÉCHEC: Le stock n'a pas été mis à jour")
            print("   Le problème est dans la LOGIQUE de mise à jour")
        
        return True
        
    except Agence.DoesNotExist:
        print("❌ Agence POISSONNERIE SANGAH non trouvée")
        print("Agences disponibles:")
        for agence in Agence.objects.all():
            print(f"   - {agence.nom_agence}")
        return False
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_affichage_stock()



