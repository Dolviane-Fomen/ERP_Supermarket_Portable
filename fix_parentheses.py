#!/usr/bin/env python
"""
Script pour corriger les erreurs de parenthèses
"""

def fix_parentheses():
    print("=== CORRECTION DES ERREURS DE PARENTHÈSES ===")
    
    # Lire le fichier
    with open('supermarket/views.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    corrections = []
    
    # Parcourir les lignes et corriger les erreurs
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Corriger les erreurs spécifiques
        if "'session_caisse') session_caisse" in line:
            lines[i] = line.replace("'session_caisse') session_caisse", "'session_caisse': session_caisse")
            corrections.append(f"Ligne {line_num}: session_caisse corrigé")
        
        # Corriger les parenthèses mal fermées
        if line.count('(') != line.count(')'):
            # Essayer de corriger automatiquement
            open_count = line.count('(')
            close_count = line.count(')')
            if open_count > close_count:
                lines[i] = line.rstrip() + ')' * (open_count - close_count) + '\n'
                corrections.append(f"Ligne {line_num}: Parenthèses ajoutées")
    
    # Sauvegarder
    with open('supermarket/views.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ {len(corrections)} corrections appliquées:")
    for correction in corrections:
        print(f"  - {correction}")

if __name__ == "__main__":
    fix_parentheses()
