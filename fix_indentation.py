#!/usr/bin/env python
"""
Script pour corriger les erreurs d'indentation
"""

def fix_indentation():
    print("=== CORRECTION DES ERREURS D'INDENTATION ===")
    
    # Lire le fichier
    with open('supermarket/views.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    corrections = []
    
    # Parcourir les lignes et corriger les erreurs d'indentation
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Supprimer les lignes vides avec des espaces
        if line.strip() == '' and line != '\n':
            lines[i] = '\n'
            corrections.append(f"Ligne {line_num}: Ligne vide avec espaces nettoyée")
        
        # Corriger les erreurs d'indentation spécifiques
        if line.strip().startswith('agence=agence,') and line.startswith(' '):
            lines[i] = '            agence=agence,\n'
            corrections.append(f"Ligne {line_num}: Indentation corrigée")
    
    # Sauvegarder
    with open('supermarket/views.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ {len(corrections)} corrections appliquées:")
    for correction in corrections:
        print(f"  - {correction}")

if __name__ == "__main__":
    fix_indentation()