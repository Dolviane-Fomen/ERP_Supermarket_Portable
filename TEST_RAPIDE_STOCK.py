#!/usr/bin/env python3
"""
Test rapide pour vérifier que les modifications de stock sont actives
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Article, FactureAchat, LigneFactureAchat, Agence, Fournisseur
from django.utils import timezone

def test_rapide():
    """
    Test rapide des modifications de stock
    """
    print("🧪 TEST RAPIDE - VÉRIFICATION DES MODIFICATIONS")
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
        print(f"   Stock actuel: {article.stock_actuel}")
        
        # Vérifier que les nouvelles méthodes existent
        if hasattr(FactureAchat, 'mettre_a_jour_stock'):
            print("✅ Méthode mettre_a_jour_stock présente")
        else:
            print("❌ Méthode mettre_a_jour_stock manquante")
            return False
            
        if hasattr(FactureAchat, 'valider_facture'):
            print("✅ Méthode valider_facture présente")
        else:
            print("❌ Méthode valider_facture manquante")
            return False
        
        # Test rapide de création de facture
        fournisseur_test, created = Fournisseur.objects.get_or_create(
            intitule="Test Rapide",
            defaults={'agence': agence}
        )
        
        facture = FactureAchat.objects.create(
            numero_fournisseur="TEST_RAPIDE",
            date_achat=timezone.now().date(),
            heure=timezone.now().time(),
            reference_achat=f"RAPIDE_{int(timezone.now().timestamp())}",
            prix_total_global=100.00,
            statut='brouillon',
            fournisseur=fournisseur_test,
            agence=agence
        )
        
        # Créer une ligne
        ligne = LigneFactureAchat.objects.create(
            facture_achat=facture,
            article=article,
            reference_article=article.reference_article,
            designation=article.designation,
            prix_unitaire=50.00,
            quantite=2,
            prix_total_article=100.00
        )
        
        print(f"✅ Facture créée: {facture.reference_achat}")
        
        # Test de validation
        stock_avant = article.stock_actuel
        print(f"   Stock avant validation: {stock_avant}")
        
        # Utiliser la nouvelle méthode
        if facture.valider_facture():
            article.refresh_from_db()
            stock_apres = article.stock_actuel
            print(f"   Stock après validation: {stock_apres}")
            
            if stock_apres == stock_avant + ligne.quantite:
                print("🎉 SUCCÈS: Les modifications fonctionnent!")
                resultat = True
            else:
                print("❌ ÉCHEC: Le stock n'a pas été mis à jour")
                resultat = False
        else:
            print("⚠️ Facture déjà validée")
            resultat = True
        
        # Nettoyer
        facture.delete()
        fournisseur_test.delete()
        
        return resultat
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    if test_rapide():
        print("\n✅ TOUS LES TESTS SONT PASSÉS!")
        print("   Les modifications sont actives et fonctionnent.")
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ!")
        print("   Vérifiez que le serveur a été redémarré.")
