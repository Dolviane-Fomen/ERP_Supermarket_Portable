#!/usr/bin/env python
"""
Script de test pour vérifier la logique de modification des factures d'achat
Teste que le stock augmente avec la DIFFÉRENCE et non la quantité totale
"""
import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
django.setup()

from supermarket.models import (
    Agence, FactureAchat, LigneFactureAchat, Article, MouvementStock
)
from django.db import transaction
from django.utils import timezone
from datetime import date, time

def test_modification_facture_achat():
    """Test de modification d'une facture d'achat avec augmentation de quantité"""
    
    print("=" * 80)
    print("TEST DE MODIFICATION FACTURE D'ACHAT")
    print("=" * 80)
    print()
    
    # 1. Trouver l'agence "Marche Huitieme"
    try:
        agence = Agence.objects.filter(nom_agence__icontains='huitieme').first()
        if not agence:
            # Essayer avec d'autres variantes
            agence = Agence.objects.filter(nom_agence__icontains='8').first()
        if not agence:
            print("❌ ERREUR: Agence 'Marche Huitieme' non trouvée")
            print("Agences disponibles:")
            for a in Agence.objects.all()[:10]:
                print(f"  - {a.nom_agence} (ID: {a.id_agence})")
            return False
        print(f"✅ Agence trouvée: {agence.nom_agence} (ID: {agence.id_agence})")
    except Exception as e:
        print(f"❌ ERREUR lors de la recherche de l'agence: {e}")
        return False
    
    # 2. Trouver une facture d'achat existante pour cette agence
    try:
        facture = FactureAchat.objects.filter(agence=agence).first()
        if not facture:
            print("❌ ERREUR: Aucune facture d'achat trouvée pour cette agence")
            print("   Création d'une facture de test...")
            
            # Créer une facture de test
            from supermarket.models import Fournisseur
            fournisseur, _ = Fournisseur.objects.get_or_create(
                intitule="Fournisseur Test",
                defaults={'agence': agence}
            )
            
            facture = FactureAchat.objects.create(
                numero_fournisseur="TEST001",
                date_achat=date.today(),
                heure=time.now(),
                reference_achat=f"TEST-{int(timezone.now().timestamp())}",
                prix_total_global=Decimal('1000.00'),
                statut='validee',
                fournisseur=fournisseur,
                agence=agence
            )
            
            # Trouver un article existant ou en créer un
            article = Article.objects.filter(agence=agence).first()
            if not article:
                print("❌ ERREUR: Aucun article trouvé pour créer une ligne de test")
                return False
            
            # Créer une ligne de facture
            LigneFactureAchat.objects.create(
                facture_achat=facture,
                article=article,
                reference_article=article.reference_article,
                designation=article.designation,
                prix_unitaire=Decimal('100.00'),
                quantite=Decimal('10.0'),
                prix_total_article=Decimal('1000.00')
            )
            
            print(f"✅ Facture de test créée: {facture.reference_achat}")
        else:
            print(f"✅ Facture trouvée: {facture.reference_achat}")
    except Exception as e:
        print(f"❌ ERREUR lors de la recherche/création de la facture: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 3. Récupérer une ligne de facture avec un article
    try:
        ligne = LigneFactureAchat.objects.filter(facture_achat=facture).select_related('article').first()
        if not ligne or not ligne.article:
            print("❌ ERREUR: Aucune ligne de facture avec article trouvée")
            return False
        
        article = ligne.article
        quantite_ancienne = Decimal(str(ligne.quantite))
        
        print(f"✅ Ligne de facture trouvée:")
        print(f"   Article: {article.designation} (ID: {article.id})")
        print(f"   Quantité actuelle dans la facture: {quantite_ancienne}")
        print(f"   Stock actuel de l'article: {article.stock_actuel}")
    except Exception as e:
        print(f"❌ ERREUR lors de la récupération de la ligne: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. Enregistrer l'état initial
    stock_initial = Decimal(str(article.stock_actuel))
    quantite_ancienne = Decimal(str(ligne.quantite))
    
    print()
    print("-" * 80)
    print("ÉTAT INITIAL")
    print("-" * 80)
    print(f"Stock actuel de l'article: {stock_initial}")
    print(f"Quantité dans la facture: {quantite_ancienne}")
    print()
    
    # 5. Définir la nouvelle quantité (plus grande)
    quantite_nouvelle = quantite_ancienne + Decimal('20')  # Augmenter de 20
    difference_attendue = quantite_nouvelle - quantite_ancienne
    
    print("-" * 80)
    print("MODIFICATION")
    print("-" * 80)
    print(f"Ancienne quantité: {quantite_ancienne}")
    print(f"Nouvelle quantité: {quantite_nouvelle}")
    print(f"Différence attendue: {difference_attendue}")
    print(f"Stock attendu après modification: {stock_initial + difference_attendue}")
    print()
    
    # 6. Simuler la modification de la facture (comme dans modifier_facture_achat)
    try:
        with transaction.atomic():
            # Récupérer les anciennes quantités
            lignes_existantes = LigneFactureAchat.objects.select_related('article').filter(facture_achat=facture)
            anciennes_quantites = {}
            for l in lignes_existantes:
                if l.article:
                    anciennes_quantites[l.article.id] = Decimal(str(l.quantite))
            
            print(f"[DEBUG] Anciennes quantités récupérées: {anciennes_quantites}")
            
            # Supprimer les anciennes lignes
            LigneFactureAchat.objects.filter(facture_achat=facture).delete()
            print("[DEBUG] Anciennes lignes supprimées")
            
            # Créer la nouvelle ligne avec la nouvelle quantité
            quantite_nouvelle_decimal = Decimal(str(quantite_nouvelle))
            prix_unitaire = Decimal(str(ligne.prix_unitaire))
            
            nouvelle_ligne = LigneFactureAchat.objects.create(
                facture_achat=facture,
                article=article,
                reference_article=article.reference_article,
                designation=article.designation,
                prix_unitaire=float(prix_unitaire),
                quantite=int(quantite_nouvelle_decimal),
                prix_total_article=float(prix_unitaire * quantite_nouvelle_decimal)
            )
            print(f"[DEBUG] Nouvelle ligne créée avec quantité: {quantite_nouvelle_decimal}")
            
            # Recharger l'article depuis la base de données
            article.refresh_from_db()
            stock_avant_modification = Decimal(str(article.stock_actuel))
            
            # Calculer la différence
            quantite_ancienne_recuperee = anciennes_quantites.get(article.id, Decimal('0'))
            difference = quantite_nouvelle_decimal - quantite_ancienne_recuperee
            
            print(f"[DEBUG] Stock avant modification: {stock_avant_modification}")
            print(f"[DEBUG] Quantité ancienne récupérée: {quantite_ancienne_recuperee}")
            print(f"[DEBUG] Quantité nouvelle: {quantite_nouvelle_decimal}")
            print(f"[DEBUG] Différence calculée: {difference}")
            
            # Calculer le stock final
            stock_final = stock_avant_modification + difference
            
            print(f"[DEBUG] Stock final calculé: {stock_final} = {stock_avant_modification} + {difference}")
            
            # Mettre à jour le stock
            article.stock_actuel = stock_final
            article.save()
            
            print(f"[DEBUG] Stock mis à jour dans la base de données")
            
            # Créer un mouvement de stock
            if difference > 0:
                type_mouvement = 'entree'
                quantite_mouvement = difference
            elif difference < 0:
                type_mouvement = 'sortie'
                quantite_mouvement = abs(difference)
            else:
                type_mouvement = 'ajustement'
                quantite_mouvement = Decimal('0')
            
            if quantite_mouvement > 0:
                MouvementStock.objects.create(
                    article=article,
                    agence=agence,
                    type_mouvement=type_mouvement,
                    date_mouvement=timezone.now(),
                    numero_piece=facture.reference_achat,
                    quantite_stock=article.stock_actuel,
                    stock_initial=stock_avant_modification,
                    solde=stock_final,
                    quantite=quantite_mouvement,
                    cout_moyen_pondere=float(article.prix_achat),
                    stock_permanent=float(article.stock_actuel * article.prix_achat),
                    facture_achat=facture,
                    fournisseur=facture.fournisseur,
                    commentaire=f"Test modification - {facture.reference_achat} (modification: {quantite_ancienne_recuperee}→{quantite_nouvelle_decimal}, {type_mouvement} {quantite_mouvement})"
                )
                print(f"[DEBUG] Mouvement de stock créé: {type_mouvement} de {quantite_mouvement}")
        
        # Recharger l'article pour vérifier
        article.refresh_from_db()
        stock_final_reel = Decimal(str(article.stock_actuel))
        
        print()
        print("-" * 80)
        print("RÉSULTAT")
        print("-" * 80)
        print(f"Stock initial: {stock_initial}")
        print(f"Stock final réel: {stock_final_reel}")
        print(f"Différence de stock: {stock_final_reel - stock_initial}")
        print(f"Différence attendue: {difference_attendue}")
        print()
        
        # Vérification
        if abs(stock_final_reel - (stock_initial + difference_attendue)) < Decimal('0.01'):
            print("✅ SUCCÈS: Le stock a augmenté avec la DIFFÉRENCE!")
            print(f"   Stock final = {stock_initial} + {difference_attendue} = {stock_final_reel}")
            return True
        else:
            print("❌ ÉCHEC: Le stock n'a PAS augmenté avec la différence!")
            print(f"   Attendu: {stock_initial} + {difference_attendue} = {stock_initial + difference_attendue}")
            print(f"   Obtenu: {stock_final_reel}")
            print(f"   Différence: {stock_final_reel - (stock_initial + difference_attendue)}")
            
            # Vérifier si le stock a augmenté avec la quantité totale au lieu de la différence
            if abs(stock_final_reel - (stock_initial + quantite_nouvelle)) < Decimal('0.01'):
                print()
                print("⚠️  PROBLÈME DÉTECTÉ: Le stock a augmenté avec la QUANTITÉ TOTALE au lieu de la DIFFÉRENCE!")
                print(f"   Stock final = {stock_initial} + {quantite_nouvelle} (quantité totale) = {stock_final_reel}")
                print(f"   Au lieu de: {stock_initial} + {difference_attendue} (différence) = {stock_initial + difference_attendue}")
            
            return False
            
    except Exception as e:
        print(f"❌ ERREUR lors de la modification: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    try:
        print()
        print("🔍 DÉMARRAGE DU TEST DE MODIFICATION FACTURE D'ACHAT")
        print()
        
        success = test_modification_facture_achat()
        
        print()
        print("=" * 80)
        if success:
            print("✅ TEST RÉUSSI")
        else:
            print("❌ TEST ÉCHOUÉ")
        print("=" * 80)
        print()
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

