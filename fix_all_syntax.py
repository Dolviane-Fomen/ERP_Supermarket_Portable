#!/usr/bin/env python
"""
Script pour corriger toutes les erreurs de syntaxe
"""

import re

def fix_all_syntax():
    print("=== CORRECTION TOUTES LES ERREURS DE SYNTAXE ===")
    
    # Lire le fichier
    with open('supermarket/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    corrections = []
    
    # 1. Corriger les appels de fonction avec : au lieu de )
    content = re.sub(
        r'(\w+)\(([^)]*):',
        r'\1(\2)',
        content
    )
    corrections.append("Appels de fonction avec : corrigés")
    
    # 2. Corriger les parenthèses mal fermées
    content = re.sub(
        r'float\(Decimal\(str\(([^)]+)\)\)',
        r'float(Decimal(str(\1)))',
        content
    )
    corrections.append("Parenthèses dans float(Decimal(...)) corrigées")
    
    # 3. Corriger les conditions if malformées
    content = re.sub(
        r'if\s+([^:]+)\s*\)\s*$',
        r'if \1:',
        content,
        flags=re.MULTILINE
    )
    corrections.append("Conditions if corrigées")
    
    # 4. Corriger les erreurs spécifiques
    content = content.replace('agence = get_user_agence(request:', 'agence = get_user_agence(request)')
    corrections.append("Erreur get_user_agence corrigée")
    
    # Sauvegarder
    with open('supermarket/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {len(corrections)} corrections appliquées:")
    for correction in corrections:
        print(f"  - {correction}")

if __name__ == "__main__":
    fix_all_syntax()
