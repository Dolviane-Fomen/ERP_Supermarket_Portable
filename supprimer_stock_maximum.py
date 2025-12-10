#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour supprimer la ligne stock_maximum du modèle Article
"""

import os

def supprimer_stock_maximum():
    """Supprime la ligne stock_maximum du fichier models.py"""
    
    fichier_models = "supermarket/models.py"
    
    if not os.path.exists(fichier_models):
        print(f"ERREUR: Le fichier {fichier_models} n'existe pas")
        return False
    
    # Lire le fichier
    with open(fichier_models, 'r', encoding='utf-8') as f:
        lignes = f.readlines()
    
    # Filtrer les lignes qui contiennent stock_maximum
    nouvelles_lignes = []
    for ligne in lignes:
        if 'stock_maximum' not in ligne:
            nouvelles_lignes.append(ligne)
        else:
            print(f"Ligne supprimée: {ligne.strip()}")
    
    # Écrire le fichier modifié
    with open(fichier_models, 'w', encoding='utf-8') as f:
        f.writelines(nouvelles_lignes)
    
    print("✅ Ligne stock_maximum supprimée avec succès")
    return True

if __name__ == "__main__":
    supprimer_stock_maximum()
