#!/usr/bin/env python3
"""
Script pour ajouter les fonctions de défacturation à la fin du fichier views.py
"""

def fix_defacturation():
    """Ajoute les fonctions de défacturation à la fin du fichier views.py"""
    
    # Code des fonctions de défacturation
    defacturation_code = '''

# ==================== DÉFACTURATION ====================

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
        
        # Utiliser une transaction pour s'assurer de la cohérence
        from django.db import transaction
        
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
            
            # 3. Supprimer la facture et ses lignes
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
'''
    
    # Lire le fichier views.py
    try:
        with open('views.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier si les fonctions existent déjà
        if 'def defacturer_vente(' in content:
            print("❌ Les fonctions de défacturation existent déjà dans views.py")
            return False
        
        # Ajouter le code à la fin du fichier
        new_content = content + defacturation_code
        
        # Écrire le fichier modifié
        with open('views.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Fonctions de défacturation ajoutées avec succès à views.py")
        return True
        
    except FileNotFoundError:
        print("❌ Fichier views.py non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des fonctions: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Ajout des fonctions de défacturation...")
    success = fix_defacturation()
    
    if success:
        print("\n✅ Fonctions ajoutées avec succès !")
        print("\n🔧 Test de la configuration Django...")
        
        # Tester la configuration Django
        import subprocess
        try:
            result = subprocess.run(['py', 'manage.py', 'check'], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ Configuration Django OK - Le serveur peut démarrer")
            else:
                print("❌ Erreur de configuration Django:")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
    else:
        print("\n❌ Échec de l'ajout des fonctions")

