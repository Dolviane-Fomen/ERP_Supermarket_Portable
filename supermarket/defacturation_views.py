"""
Vues pour la défacturation des ventes
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from django.conf import settings
from decimal import Decimal
from .models import FactureVente, LigneFactureVente, MouvementStock, Article
from .views import get_user_agence


@login_required
def defacturer_vente(request, facture_id):
    """Vue pour défacturer (annuler) une vente"""
    try:
        agence = get_user_agence(request)
    except:
        messages.error(request, 'Agence non trouvée.')
        return redirect('detail_factures')
    
    try:
        # Récupérer la facture
        facture = FactureVente.objects.get(id=facture_id, agence=agence)
        
        # Vérifier que la facture n'est pas déjà annulée
        if hasattr(facture, 'annulee') and facture.annulee:
            messages.error(request, 'Cette facture est déjà annulée.')
            return redirect('detail_factures')
        
        # Utiliser une transaction pour s'assurer de la cohérence
        with transaction.atomic():
            print(f"[DÉFACTURATION] Début de la défacturation de la facture {facture.numero_ticket}")
            
            # 1. Récupérer toutes les lignes de la facture
            lignes = LigneFactureVente.objects.filter(facture_vente=facture)
            print(f"[DÉFACTURATION] {lignes.count()} lignes à traiter")
            
            # 2. Remettre les produits en stock et créer des mouvements inversés
            for ligne in lignes:
                article = ligne.article
                quantite_a_remettre = ligne.quantite
                
                print(f"[DÉFACTURATION] Traitement de {article.designation} - Quantité: {quantite_a_remettre}")
                
                # Sauvegarder l'ancien stock
                ancien_stock = article.stock_actuel
                
                # Remettre en stock
                article.stock_actuel += quantite_a_remettre
                # Le suivi de stock est toujours activé automatiquement lors de toute modification du stock
                article.suivi_stock = True
                article.save()
                
                print(f"[DÉFACTURATION] Stock remis: {ancien_stock} → {article.stock_actuel} (+{quantite_a_remettre})")
                
                # Créer un mouvement de stock inverse (entrée)
                MouvementStock.objects.create(
                    article=article,
                    agence=agence,
                    type_mouvement='retour',  # Type spécial pour les retours
                    date_mouvement=timezone.now(),
                    numero_piece=f"RETOUR-{facture.numero_ticket}",
                    quantite_stock=article.stock_actuel,
                    stock_initial=ancien_stock,
                    solde=article.stock_actuel,
                    quantite=quantite_a_remettre,
                    cout_moyen_pondere=float(article.prix_achat),
                    stock_permanent=float(article.stock_actuel * article.prix_achat),
                    facture_vente=facture,  # Référence à la facture annulée
                    commentaire=f"Défacturation - Retour stock pour facture {facture.numero_ticket}"
                )
                
                print(f"[DÉFACTURATION] Mouvement de retour créé pour {article.designation}")
            
            # 3. Marquer la facture comme annulée (au lieu de la supprimer pour l'historique)
            # Option 1: Ajouter un champ 'annulee' au modèle (recommandé)
            # Option 2: Créer un modèle d'historique des annulations
            
            # Pour l'instant, on va supprimer la facture et ses lignes
            # mais on garde les mouvements de stock pour la traçabilité
            
            # Supprimer les lignes de facture
            lignes.delete()
            print(f"[DÉFACTURATION] Lignes de facture supprimées")
            
            # Supprimer la facture
            numero_ticket = facture.numero_ticket
            facture.delete()
            print(f"[DÉFACTURATION] Facture {numero_ticket} supprimée")
            
            messages.success(request, f'Facture {numero_ticket} défacturée avec succès. Les produits ont été remis en stock.')
            
    except FactureVente.DoesNotExist:
        messages.error(request, 'Facture non trouvée.')
        return redirect('detail_factures')
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la défacturation: {e}")
        import traceback
        traceback.print_exc()
        messages.error(request, f'Erreur lors de la défacturation: {str(e)}')
        return redirect('detail_factures')
    
    return redirect('detail_factures')


@login_required
def defacturer_ligne_vente(request, facture_id, ligne_id):
    """Défacturer un article spécifique d'une facture de vente"""
    print(f"[DÉFACTURATION PARTIELLE] Début - facture_id: {facture_id}, ligne_id: {ligne_id}")
    
    if request.method != 'POST':
        messages.error(request, 'Méthode non autorisée.')
        return redirect('detail_factures')
    
    try:
        agence = get_user_agence(request)
    except:
        messages.error(request, 'Agence non trouvée.')
        return redirect('detail_factures')
    
    try:
        facture = FactureVente.objects.get(id=facture_id, agence=agence)
        print(f"[DÉFACTURATION PARTIELLE] Facture trouvée: {facture.numero_ticket}")
        
        ligne = LigneFactureVente.objects.get(id=ligne_id, facture_vente=facture)
        print(f"[DÉFACTURATION PARTIELLE] Ligne trouvée: {ligne.id} - {ligne.designation} - Quantité: {ligne.quantite}")
        
        # Vérifier qu'il y a bien plusieurs lignes (sinon on ne devrait pas être ici)
        total_lignes = LigneFactureVente.objects.filter(facture_vente=facture).count()
        print(f"[DÉFACTURATION PARTIELLE] Nombre total de lignes dans la facture: {total_lignes}")
        
    except FactureVente.DoesNotExist:
        messages.error(request, 'Facture non trouvée.')
        return redirect('detail_factures')
    except LigneFactureVente.DoesNotExist:
        messages.error(request, f"Ligne de facture introuvable (ID: {ligne_id}).")
        return redirect('detail_factures')
    
    try:
        with transaction.atomic():
            article = ligne.article
            quantite = Decimal(ligne.quantite)
            ligne_designation = ligne.designation
            
            if article:
                ancien_stock = article.stock_actuel
                article.stock_actuel += quantite
                # Le suivi de stock est toujours activé automatiquement lors de toute modification du stock
                article.suivi_stock = True
                article.save()
                
                MouvementStock.objects.create(
                    article=article,
                    agence=agence,
                    type_mouvement='retour',
                    date_mouvement=timezone.now(),
                    numero_piece=f"RETOUR-{facture.numero_ticket}",
                    quantite_stock=article.stock_actuel,
                    stock_initial=ancien_stock,
                    solde=article.stock_actuel,
                    quantite=quantite,
                    cout_moyen_pondere=float(article.prix_achat),
                    stock_permanent=float(article.stock_actuel * article.prix_achat),
                    facture_vente=facture,
                    commentaire=f"Défacturation partielle - {article.designation if article else ligne_designation}"
                )
            
            ligne.delete()
            print(f"[DÉFACTURATION PARTIELLE] Ligne {ligne_id} supprimée avec succès")
            
            lignes_restantes = LigneFactureVente.objects.filter(facture_vente=facture)
            print(f"[DÉFACTURATION PARTIELLE] Lignes restantes après suppression: {lignes_restantes.count()}")
            
            if not lignes_restantes.exists():
                numero_ticket = facture.numero_ticket
                facture.delete()
                messages.success(
                    request,
                    f'Toutes les lignes ont été défacturées. La facture {numero_ticket} a été annulée.'
                )
                return redirect('detail_factures')
            
            total_rest = lignes_restantes.aggregate(total=Sum('prix_total'))['total'] or Decimal('0')
            remise = Decimal(str(facture.remise or 0))
            nouvelle_nette = max(Decimal('0'), total_rest - remise)
            facture.nette_a_payer = nouvelle_nette
            if facture.montant_regler is not None:
                facture.rendu = max(Decimal('0'), Decimal(str(facture.montant_regler)) - nouvelle_nette)
            facture.save()
            
            messages.success(
                request,
                f'L\'article "{ligne_designation}" a été défacturé. La facture est mise à jour.'
            )
            return redirect('detail_factures')
    
    except Exception as e:
        print(f"[ERREUR] Défacturation partielle: {e}")
        messages.error(request, f'Erreur lors de la défacturation de la ligne: {str(e)}')
        return redirect('defacturer_confirmation', facture_id=facture_id)


@login_required
def defacturer_vente_confirmation(request, facture_id):
    """Vue pour confirmer la défacturation d'une vente"""
    try:
        agence = get_user_agence(request)
    except:
        messages.error(request, 'Agence non trouvée.')
        return redirect('login_stock')
    
    try:
        facture = FactureVente.objects.get(id=facture_id, agence=agence)
        lignes = LigneFactureVente.objects.filter(facture_vente=facture)
        
        context = {
            'facture': facture,
            'lignes': lignes,
            'agence': agence,
        }
        
        return render(request, 'supermarket/stock/defacturation_confirmation.html', context)
        
    except FactureVente.DoesNotExist:
        messages.error(request, 'Facture non trouvée.')
        return redirect('detail_factures')




@login_required
def liste_factures_defacturation(request):
    """Vue pour lister les factures pouvant être défacturées"""
    try:
        agence = get_user_agence(request)
    except:
        messages.error(request, 'Agence non trouvée.')
        return redirect('login_stock')
    
    # Récupérer les factures récentes (par exemple, des 7 derniers jours)
    from datetime import datetime, timedelta
    date_limite = datetime.now().date() - timedelta(days=7)
    
    factures = FactureVente.objects.filter(
        agence=agence,
        date__gte=date_limite
    ).order_by('-date', '-heure')
    
    context = {
        'factures': factures,
        'agence': agence,
    }
    
    return render(request, 'supermarket/stock/liste_defacturation.html', context)
