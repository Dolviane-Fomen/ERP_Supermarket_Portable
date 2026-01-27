#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour vérifier les erreurs d'indentation dans views.py
"""

import re
import sys

def verifier_indentation(fichier_path):
    """Vérifier les erreurs d'indentation dans un fichier Python"""
    erreurs = []
    
    try:
        with open(fichier_path, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return erreurs
    
    # États pour suivre le contexte
    niveau_indentation_attendu = 0
    pile_indentation = [0]  # Pile pour suivre les niveaux d'indentation
    
    for num_ligne, ligne in enumerate(lignes, start=1):
        ligne_originale = ligne
        ligne = ligne.rstrip('\n\r')
        
        # Ignorer les lignes vides et les commentaires
        if not ligne.strip() or ligne.strip().startswith('#'):
            continue
        
        # Compter les espaces de début (indentation)
        espaces_debut = len(ligne) - len(ligne.lstrip())
        contenu = ligne.lstrip()
        
        # Vérifier si c'est une ligne de continuation (se termine par \ ou contient des parenthèses non fermées)
        est_continuation = ligne_originale.rstrip().endswith('\\') or ligne_originale.count('(') > ligne_originale.count(')')
        
        # Détecter les mots-clés qui augmentent le niveau d'indentation
        if re.match(r'^\s*(if|elif|else|for|while|def|class|try|except|finally|with)\s', contenu):
            # Vérifier l'indentation
            if espaces_debut != pile_indentation[-1]:
                erreurs.append({
                    'ligne': num_ligne,
                    'contenu': contenu[:80],
                    'indentation_actuelle': espaces_debut,
                    'indentation_attendue': pile_indentation[-1],
                    'type': 'Mauvaise indentation après mot-clé'
                })
            
            # Si c'est un bloc qui s'ouvre, on s'attend à ce que la ligne suivante soit indentée
            if not contenu.endswith(':'):
                # Certains cas spéciaux
                if 'if' in contenu and ':' not in contenu:
                    pass  # Peut être une expression inline
                else:
                    # Vérifier si le ':' manque
                    if re.match(r'^\s*(if|elif|else|for|while|def|class|try|except|finally|with)\s', contenu):
                        if ':' not in contenu:
                            erreurs.append({
                                'ligne': num_ligne,
                                'contenu': contenu[:80],
                                'indentation_actuelle': espaces_debut,
                                'indentation_attendue': pile_indentation[-1],
                                'type': 'Deux-points manquant après mot-clé'
                            })
        
        # Détecter les lignes qui devraient être indentées (après un ':')
        elif num_ligne > 1:
            ligne_precedente = lignes[num_ligne - 2].rstrip('\n\r')
            contenu_precedent = ligne_precedente.lstrip()
            
            # Si la ligne précédente se termine par ':', la ligne actuelle devrait être indentée
            if ligne_precedente.rstrip().endswith(':'):
                indentation_attendue = len(ligne_precedente) - len(contenu_precedent) + 4  # +4 pour l'indentation Python standard
                if espaces_debut != indentation_attendue and contenu and not contenu.startswith('#'):
                    # Vérifier si c'est un else/elif qui devrait être au même niveau
                    if re.match(r'^\s*(elif|else|except|finally)\s', contenu):
                        indentation_attendue = len(ligne_precedente) - len(contenu_precedent)
                    
                    if espaces_debut != indentation_attendue:
                        erreurs.append({
                            'ligne': num_ligne,
                            'contenu': contenu[:80],
                            'indentation_actuelle': espaces_debut,
                            'indentation_attendue': indentation_attendue,
                            'type': 'Mauvaise indentation après deux-points',
                            'ligne_precedente': ligne_precedente[:80]
                        })
        
        # Détecter les problèmes de mélange tabs/espaces
        if '\t' in ligne_originale[:espaces_debut]:
            erreurs.append({
                'ligne': num_ligne,
                'contenu': contenu[:80],
                'indentation_actuelle': espaces_debut,
                'indentation_attendue': None,
                'type': 'Mélange de tabs et espaces détecté'
            })
    
    return erreurs

def main():
    fichier = 'supermarket/views.py'
    
    print("=" * 80)
    print("VÉRIFICATION DES ERREURS D'INDENTATION DANS views.py")
    print("=" * 80)
    print()
    
    erreurs = verifier_indentation(fichier)
    
    if not erreurs:
        print("[OK] Aucune erreur d'indentation detectee!")
        return 0
    
    print(f"[ERREUR] {len(erreurs)} erreur(s) d'indentation trouvee(s):\n")
    
    for i, erreur in enumerate(erreurs, 1):
        print(f"\n{'='*80}")
        print(f"ERREUR #{i} - Ligne {erreur['ligne']}")
        print(f"{'='*80}")
        print(f"Type: {erreur['type']}")
        print(f"Contenu: {erreur['contenu']}")
        if 'indentation_actuelle' in erreur and erreur['indentation_actuelle'] is not None:
            print(f"Indentation actuelle: {erreur['indentation_actuelle']} espaces")
        if 'indentation_attendue' in erreur and erreur['indentation_attendue'] is not None:
            print(f"Indentation attendue: {erreur['indentation_attendue']} espaces")
        if 'ligne_precedente' in erreur:
            print(f"Ligne précédente: {erreur['ligne_precedente']}")
        print()
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {len(erreurs)} erreur(s) trouvée(s)")
    print(f"{'='*80}")
    
    return len(erreurs)

if __name__ == '__main__':
    sys.exit(main())
