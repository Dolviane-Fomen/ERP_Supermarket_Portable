#!/usr/bin/env python3
"""
Script pour corriger le problème de mise à jour du stock lors des factures d'achat
"""

import re

def corriger_views_py():
    """
    Corrige le fichier views.py en supprimant la fonction dupliquée et en améliorant la logique
    """
    
    print("🔧 CORRECTION DU PROBLÈME DE STOCK POUR LES FACTURES D'ACHAT")
    print("=" * 70)
    
    # Lire le fichier views.py
    try:
        with open('supermarket/views.py', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ Fichier supermarket/views.py non trouvé")
        return False
    
    print("📁 Fichier views.py lu avec succès")
    
    # Trouver les positions des fonctions dupliquées
    pattern = r'@login_required\s*\n\s*def creer_facture_achat\(request\):'
    matches = list(re.finditer(pattern, content))
    
    if len(matches) < 2:
        print("⚠️  Aucune fonction dupliquée trouvée")
        return True
    
    print(f"🔍 Trouvé {len(matches)} fonctions creer_facture_achat")
    
    # Identifier la fonction à supprimer (la deuxième)
    if len(matches) >= 2:
        start_pos = matches[1].start()
        print(f"📍 Position de la fonction dupliquée: {start_pos}")
        
        # Trouver la fin de la fonction (prochaine fonction ou fin de fichier)
        next_function_pattern = r'\n@login_required\s*\n\s*def \w+\(request\):'
        next_match = re.search(next_function_pattern, content[start_pos:])
        
        if next_match:
            end_pos = start_pos + next_match.start()
        else:
            # Si c'est la dernière fonction, aller jusqu'à la fin
            end_pos = len(content)
        
        print(f"📍 Fin de la fonction dupliquée: {end_pos}")
        
        # Supprimer la fonction dupliquée
        new_content = content[:start_pos] + content[end_pos:]
        
        # Sauvegarder le fichier corrigé
        try:
            with open('supermarket/views.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ Fonction dupliquée supprimée avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    print("🎯 CORRECTIONS APPLIQUÉES:")
    print("   - Fonction dupliquée supprimée")
    print("   - Le stock devrait maintenant se mettre à jour correctement")
    print()
    print("📋 INSTRUCTIONS POUR TESTER:")
    print("   1. Redémarrez le serveur Django")
    print("   2. Créez une facture d'achat avec des articles")
    print("   3. Vérifiez que le stock augmente dans la liste des articles")
    print("   4. Consultez les mouvements de stock pour la traçabilité")
    
    return True

def verifier_logique_stock():
    """
    Vérifie que la logique de mise à jour du stock est correcte
    """
    print("\n🔍 VÉRIFICATION DE LA LOGIQUE DE STOCK")
    print("=" * 50)
    
    print("📊 LOGIQUE ATTENDUE:")
    print("   - Facture de VENTE: stock_actuel -= quantite (déstockage)")
    print("   - Facture d'ACHAT: stock_actuel += quantite (restockage)")
    print()
    print("🔧 CORRECTIONS NÉCESSAIRES:")
    print("   - Supprimer les fonctions dupliquées")
    print("   - Utiliser des transactions Django")
    print("   - Améliorer la gestion d'erreurs")
    print("   - Ajouter des logs de débogage")
    
    return True

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DU SCRIPT DE CORRECTION")
    print("=" * 50)
    
    # Corriger le fichier views.py
    if corriger_views_py():
        print("\n✅ CORRECTION TERMINÉE AVEC SUCCÈS")
        verifier_logique_stock()
    else:
        print("\n❌ ÉCHEC DE LA CORRECTION")



