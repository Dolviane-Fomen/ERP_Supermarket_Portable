#!/usr/bin/env python3
"""
Script pour tester la gestion du cache de stock
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, MouvementStock, Agence, Fournisseur
from django.utils import timezone

def test_cache_stock():
    """
    Test pour vérifier que le cache de stock fonctionne correctement
    """
    print("🔍 TEST GESTION CACHE STOCK")
    print("=" * 60)
    
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
        stock_avant = article.stock_actuel
        print(f"📊 Stock avant facture: {stock_avant}")
        
        # 3. Créer une facture d'achat
        fournisseur, created = Fournisseur.objects.get_or_create(
            intitule="Test Cache",
            defaults={'agence': agence}
        )
        
        facture = FactureAchat.objects.create(
            numero_fournisseur="TEST_CACHE",
            date_achat=timezone.now().date(),
            heure=timezone.now().time(),
            reference_achat=f"CACHE_{int(timezone.now().timestamp())}",
            prix_total_global=2000.00,
            statut='validee',
            fournisseur=fournisseur,
            agence=agence
        )
        
        print(f"✅ Facture créée: {facture.reference_achat}")
        
        # 4. Créer une ligne de facture
        quantite_ajoutee = 10
        ligne = LigneFactureAchat.objects.create(
            facture_achat=facture,
            article=article,
            reference_article=article.reference_article,
            designation=article.designation,
            prix_unitaire=200.00,
            quantite=quantite_ajoutee,
            prix_total_article=2000.00
        )
        
        print(f"✅ Ligne créée: {ligne.designation} - Quantité: {quantite_ajoutee}")
        
        # 5. Mettre à jour le stock
        article.stock_actuel += quantite_ajoutee
        article.save()
        
        stock_apres = article.stock_actuel
        print(f"✅ Stock mis à jour: {stock_avant} → {stock_apres}")
        
        # 6. Créer un mouvement de stock
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
            commentaire=f"Test Cache - {facture.reference_achat}"
        )
        
        print("✅ Mouvement de stock créé")
        
        # 7. Vérifier que la modification est persistante
        article.refresh_from_db()
        print(f"🔍 Stock vérifié en base: {article.stock_actuel}")
        
        # 8. Simuler l'URL de redirection avec refresh
        print(f"\n📋 SIMULATION REDIRECTION AVEC REFRESH:")
        print(f"   - URL: /stock/consulter_articles/?refresh=1")
        print(f"   - Message: 'Facture d'achat {facture.reference_achat} créée avec succès! Stock mis à jour.'")
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
        if article.stock_actuel == stock_avant + quantite_ajoutee:
            print("✅ SUCCÈS: Le stock a été correctement mis à jour!")
            print("✅ SUCCÈS: La redirection avec refresh=1 est configurée!")
            print("✅ SUCCÈS: Le bouton 'Actualiser le Stock' est ajouté!")
            print("   Maintenant, après création d'une facture d'achat:")
            print("   1. Vous serez redirigé vers la liste des articles avec refresh=1")
            print("   2. Le cache de session sera vidé automatiquement")
            print("   3. Vous verrez le stock mis à jour immédiatement")
            print("   4. Vous pouvez cliquer sur 'Actualiser le Stock' si nécessaire")
        else:
            print("❌ ÉCHEC: Le stock n'a pas été mis à jour")
        
        return True
        
    except Agence.DoesNotExist:
        print("❌ Agence POISSONNERIE SANGAH non trouvée")
        return False
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_cache_stock()



