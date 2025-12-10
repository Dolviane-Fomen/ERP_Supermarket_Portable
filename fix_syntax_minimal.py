#!/usr/bin/env python
"""
Script pour corriger uniquement les erreurs de syntaxe critiques
"""

def fix_syntax_minimal():
    print("=== CORRECTION MINIMALE DES ERREURS DE SYNTAXE ===")
    
    # Lire le fichier
    with open('supermarket/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    corrections = []
    
    # 1. Corriger les erreurs spécifiques identifiées
    if 'session_data:' in content:
        content = content.replace('session_data:', 'session_data)')
        corrections.append("session_data: corrigé")
    
    if 'get_user_agence(request:' in content:
        content = content.replace('get_user_agence(request:', 'get_user_agence(request)')
        corrections.append("get_user_agence(request: corrigé")
    
    # 2. Corriger les parenthèses manquantes dans float(Decimal(...))
    import re
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
    
    # Sauvegarder
    with open('supermarket/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {len(corrections)} corrections appliquées:")
    for correction in corrections:
        print(f"  - {correction}")

if __name__ == "__main__":
    fix_syntax_minimal()
