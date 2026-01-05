#!/usr/bin/env python
"""
Script de test pour simuler exactement ce qui se passe dans le formulaire web
lors de la modification d'une facture d'achat
"""
import os
import sys
import django
from decimal import Decimal
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
django.setup()

from supermarket.models import (
    Agence, FactureAchat, LigneFactureAchat, Article, MouvementStock
)
from django.db import transaction
from django.utils import timezone
from datetime import date, time

def test_modification_comme_formulaire():
    """Test de modification simulant exactement le formulaire web"""
    
    print("=" * 80)
    print("TEST DE MODIFICATION FACTURE D'ACHAT (SIMULATION FORMULAIRE WEB)")
    print("=" * 80)
    print()
    
    # 1. Trouver l'agence "Marche Huitieme"
    try:
        agence = Agence.objects.filter(nom_agence__icontains='huitieme').first()
        if not agence:
            agence = Agence.objects.filter(nom_agence__icontains='8').first()
        if not agence:
            print("❌ ERREUR: Agence 'Marche Huitieme' non trouvée")
            return False
        print(f"✅ Agence trouvée: {agence.nom_agence} (ID: {agence.id_agence})")
    except Exception as e:
        print(f"❌ ERREUR lors de la recherche de l'agence: {e}")
        return False
    
    # 2. Trouver une facture d'achat existante
    try:
        facture = FactureAchat.objects.filter(agence=agence, statut='validee').first()
        if not facture:
            print("❌ ERREUR: Aucune facture d'achat validée trouvée")
            return False
        print(f"✅ Facture trouvée: {facture.reference_achat}")
    except Exception as e:
        print(f"❌ ERREUR lors de la recherche de la facture: {e}")
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
    print("MODIFICATION (SIMULATION FORMULAIRE WEB)")
    print("-" * 80)
    print(f"Ancienne quantité: {quantite_ancienne}")
    print(f"Nouvelle quantité: {quantite_nouvelle}")
    print(f"Différence attendue: {difference_attendue}")
    print(f"Stock attendu après modification: {stock_initial + difference_attendue}")
    print()
    
    # 6. Simuler exactement ce qui se passe dans modifier_facture_achat
    try:
        with transaction.atomic():
            # Étape 1: Récupérer les anciennes quantités (comme dans la vue)
            lignes_existantes = LigneFactureAchat.objects.select_related('article').filter(facture_achat=facture)
            anciennes_quantites = {}
            
            print(f"[SIMULATION] Récupération des anciennes lignes: {lignes_existantes.count()} lignes trouvées")
            for l in lignes_existantes:
                if l.article:
                    article_id = l.article.id
                    anciennes_quantites[article_id] = Decimal(str(l.quantite))
                    print(f"  [SIMULATION] Ancienne ligne - Article ID: {article_id}, Quantité: {l.quantite}")
            
            # Étape 2: Supprimer toutes les anciennes lignes
            LigneFactureAchat.objects.filter(facture_achat=facture).delete()
            print("[SIMULATION] Anciennes lignes supprimées")
            
            # Étape 3: Créer la nouvelle ligne (simulant articles_data du formulaire)
            # Simuler le JSON qui vient du formulaire
            articles_data_json = json.dumps([{
                'id': article.id,
                'quantite': float(quantite_nouvelle),
                'prix_achat': float(ligne.prix_unitaire)
            }])
            
            print(f"[SIMULATION] Articles data (JSON): {articles_data_json}")
            
            articles = json.loads(articles_data_json)
            for a in articles:
                article_id = a.get('id')
                quantite_nouvelle_decimal = Decimal(str(a.get('quantite', 0)))
                prix_achat_nouveau = Decimal(str(a.get('prix_achat', 0)))
                
                # Recharger l'article depuis la base
                article.refresh_from_db()
                stock_avant_modification = Decimal(str(article.stock_actuel))
                
                # Calculer la différence
                quantite_ancienne_recuperee = anciennes_quantites.get(article_id, Decimal('0'))
                difference = quantite_nouvelle_decimal - quantite_ancienne_recuperee
                
                print(f"[SIMULATION] Stock avant modification: {stock_avant_modification}")
                print(f"[SIMULATION] Quantité ancienne récupérée: {quantite_ancienne_recuperee}")
                print(f"[SIMULATION] Quantité nouvelle: {quantite_nouvelle_decimal}")
                print(f"[SIMULATION] Différence calculée: {difference}")
                
                # Calculer le stock final
                stock_final = stock_avant_modification + difference
                print(f"[SIMULATION] Stock final calculé: {stock_final} = {stock_avant_modification} + {difference}")
                
                # Créer la nouvelle ligne
                nouvelle_ligne = LigneFactureAchat.objects.create(
                    facture_achat=facture,
                    article=article,
                    reference_article=article.reference_article,
                    designation=article.designation,
                    prix_unitaire=float(prix_achat_nouveau),
                    quantite=int(quantite_nouvelle_decimal),
                    prix_total_article=float(prix_achat_nouveau * quantite_nouvelle_decimal)
                )
                print(f"[SIMULATION] Nouvelle ligne créée avec quantité: {quantite_nouvelle_decimal}")
                
                # Mettre à jour le stock
                article.stock_actuel = stock_final
                article.save()
                print(f"[SIMULATION] Stock mis à jour: {stock_avant_modification} → {stock_final}")
                
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
                        commentaire=f"Test modification formulaire - {facture.reference_achat} (modification: {quantite_ancienne_recuperee}→{quantite_nouvelle_decimal}, {type_mouvement} {quantite_mouvement})"
                    )
                    print(f"[SIMULATION] Mouvement de stock créé: {type_mouvement} de {quantite_mouvement}")
                
                # ⚠️ POINT CRITIQUE: Simuler ce qui pourrait se passer si facture.save() est appelé
                # (comme cela pourrait arriver dans le formulaire web)
                print()
                print("[SIMULATION] ⚠️  Vérification: Si facture.save() était appelé maintenant...")
                
                # Recharger la facture
                facture.refresh_from_db()
                
                # Vérifier si mettre_a_jour_stock() serait appelé
                # (Dans le modèle, cela se produit si statut == 'validee' et si c'est nouveau ou si le statut vient de changer)
                print(f"[SIMULATION] Statut de la facture: {facture.statut}")
                print(f"[SIMULATION] Nombre de mouvements existants pour cette facture et cet article: {MouvementStock.objects.filter(facture_achat=facture, article=article).count()}")
        
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
    print()
    print("🔍 DÉMARRAGE DU TEST DE MODIFICATION (SIMULATION FORMULAIRE WEB)")
    print()
    
    success = test_modification_comme_formulaire()
    
    print()
    print("=" * 80)
    if success:
        print("✅ TEST RÉUSSI")
    else:
        print("❌ TEST ÉCHOUÉ")
    print("=" * 80)
    print()


