#!/usr/bin/env python3
"""
Script pour corriger le problème de mise à jour du stock lors des factures d'achat
"""

def corriger_facture_achat():
    """
    Fonction améliorée pour la création de factures d'achat avec gestion correcte du stock
    """
    
    # Code amélioré pour la fonction creer_facture_achat
    code_ameliore = '''
@login_required
def creer_facture_achat(request):
    """Vue pour créer une nouvelle facture d'achat avec gestion correcte du stock"""
    try:
        agence = get_user_agence(request)
    except:
        messages.error(request, 'Agence non trouvée.')
        return redirect('login_stock')
    
    if request.method == 'POST':
        try:
            print("[START] DÉBUT CRÉATION FACTURE D'ACHAT")
            print(f"[LIST] Données POST reçues: {dict(request.POST)}")
            
            # Récupérer les données du formulaire
            numero_fournisseur = request.POST.get('numero_fournisseur')
            date_achat = request.POST.get('date_achat')
            heure = request.POST.get('heure')
            reference_achat = request.POST.get('reference_achat')
            prix_total_global = request.POST.get('prix_total_global')
            statut = request.POST.get('statut')
            commentaire = request.POST.get('commentaire')
            
            # Validation
            if not all([numero_fournisseur, date_achat, heure, reference_achat, prix_total_global]):
                messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
                return redirect('creer_facture_achat')
            
            # Récupérer ou créer le fournisseur
            fournisseur, created = Fournisseur.objects.get_or_create(
                intitule=numero_fournisseur,
                defaults={'agence': agence}
            )
            
            # Vérifier si la référence existe déjà
            if FactureAchat.objects.filter(reference_achat=reference_achat).exists():
                import time
                reference_achat = f"{reference_achat}_{int(time.time())}"
            
            # Créer la facture d'achat
            facture = FactureAchat.objects.create(
                numero_fournisseur=numero_fournisseur,
                date_achat=date_achat,
                heure=heure,
                reference_achat=reference_achat,
                prix_total_global=float(prix_total_global),
                statut=statut,
                commentaire=commentaire,
                fournisseur=fournisseur,
                agence=agence
            )
            
            # Traiter les articles sélectionnés avec transaction
            articles_data = request.POST.get('articles_data', '')
            
            if articles_data:
                import json
                from django.db import transaction
                
                try:
                    articles = json.loads(articles_data)
                    print(f"[PACKAGE] Articles à traiter: {len(articles)}")
                    
                    # Utiliser une transaction pour s'assurer que tout est sauvegardé
                    with transaction.atomic():
                        for i, article_data in enumerate(articles):
                            print(f"[NOTE] Traitement article {i+1}: {article_data}")
                            
                            # Récupérer l'article
                            article = Article.objects.get(id=article_data['id'])
                            print(f"[OK] Article trouvé: {article.designation}")
                            
                            # Créer la ligne de facture
                            ligne = LigneFactureAchat.objects.create(
                                facture_achat=facture,
                                article=article,
                                reference_article=article.reference_article,
                                designation=article.designation,
                                prix_unitaire=float(article_data['prix_achat']),
                                quantite=int(article_data['quantite']),
                                prix_total_article=float(article_data['prix_achat']) * int(article_data['quantite'])
                            )
                            
                            # Mettre à jour le stock de l'article
                            ancien_stock = article.stock_actuel
                            quantite_ajoutee = float(article_data['quantite'])
                            article.stock_actuel += quantite_ajoutee
                            
                            # Mettre à jour le dernier prix d'achat
                            article.dernier_prix_achat = float(article_data['prix_achat'])
                            
                            # Sauvegarder les modifications
                            article.save()
                            
                            print(f"[STOCK] ✅ Stock mis à jour: {ancien_stock} → {article.stock_actuel} (+{quantite_ajoutee})")
                            
                            # Créer un mouvement de stock pour traçabilité
                            try:
                                MouvementStock.objects.create(
                                    article=article,
                                    agence=agence,
                                    type_mouvement='entree',
                                    date_mouvement=timezone.now(),
                                    numero_piece=facture.reference_achat,
                                    quantite_stock=article.stock_actuel,
                                    stock_initial=ancien_stock,
                                    solde=article.stock_actuel,
                                    quantite=int(article_data['quantite']),
                                    cout_moyen_pondere=float(article.prix_achat),
                                    stock_permanent=float(article.stock_actuel * article.prix_achat),
                                    facture_achat=facture,
                                    fournisseur=facture.fournisseur,
                                    commentaire=f"Achat - Facture {facture.reference_achat}"
                                )
                                print(f"[MOUVEMENT] ✅ Entrée enregistrée pour {article.designation}")
                            except Exception as e:
                                print(f"[WARNING] ERREUR MOUVEMENT STOCK: {e}")
                    
                    print(f"[SUCCESS] ✅ Tous les articles ont été traités avec succès!")
                    
                except (json.JSONDecodeError, Article.DoesNotExist, KeyError) as e:
                    print(f"[ERREUR] Erreur lors du traitement des articles: {e}")
                    messages.error(request, f'Erreur lors du traitement des articles: {str(e)}')
            else:
                print("[WARNING] Aucun article sélectionné")
            
            messages.success(request, f'Facture d\'achat "{reference_achat}" créée avec succès!')
            return redirect('creer_facture_achat')
            
        except Exception as e:
            print(f"[ERREUR] Erreur lors de la création de la facture: {e}")
            messages.error(request, f'Erreur lors de la création de la facture: {str(e)}')
            return redirect('creer_facture_achat')
    
    # GET - Afficher le formulaire
    statut_choices = FactureAchat.STATUT_CHOICES
    
    context = {
        'statut_choices': statut_choices,
    }
    return render(request, 'supermarket/stock/creer_facture_achat.html', context)
'''
    
    return code_ameliore

if __name__ == "__main__":
    print("Script de correction du stock pour les factures d'achat")
    print("=" * 60)
    print("PROBLÈME IDENTIFIÉ:")
    print("- Il y a deux fonctions identiques creer_facture_achat")
    print("- Le stock devrait augmenter lors des achats")
    print("- La logique semble correcte mais il peut y avoir des conflits")
    print()
    print("SOLUTION:")
    print("- Supprimer la fonction dupliquée")
    print("- Utiliser des transactions Django")
    print("- Améliorer la gestion d'erreurs")
    print("- Ajouter plus de logs pour le débogage")



