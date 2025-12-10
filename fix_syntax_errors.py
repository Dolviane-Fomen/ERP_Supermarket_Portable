#!/usr/bin/env python
"""
Script pour corriger les erreurs de syntaxe dans views.py
"""

import re

def fix_syntax_errors():
    print("=== CORRECTION DES ERREURS DE SYNTAXE ===")
    
    # Lire le fichier
    with open('supermarket/views.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corrections spécifiques
    corrections = []
    
    # 1. Corriger les parenthèses manquantes dans les expressions float(Decimal(...))
    content = re.sub(
        r'float\(Decimal\(str\(([^)]+)\)\)',
        r'float(Decimal(str(\1)))',
        content
    )
    corrections.append("Parenthèses manquantes dans float(Decimal(...))")
    
    # 2. Corriger les erreurs de syntaxe dans les conditions
    content = re.sub(
        r'if\s+([^:]+)\s*\)\s*$',
        r'if \1:',
        content,
        flags=re.MULTILINE
    )
    corrections.append("Conditions if malformées")
    
    # 3. Corriger les erreurs d'indentation
    lines = content.split('\n')
    fixed_lines = []
    indent_level = 0
    
    for i, line in enumerate(lines):
        # Détecter les erreurs d'indentation
        if line.strip().startswith('if ') and not line.strip().endswith(':'):
            # Ajouter les deux points manquants
            line = line.rstrip() + ':'
            corrections.append(f"Ligne {i+1}: Ajout de ':' manquant")
        
        # Corriger les parenthèses mal fermées
        if 'float(Decimal(str(' in line and line.count('(') != line.count(')'):
            # Compter les parenthèses et corriger
            open_count = line.count('(')
            close_count = line.count(')')
            if open_count > close_count:
                line += ')' * (open_count - close_count)
                corrections.append(f"Ligne {i+1}: Parenthèses manquantes corrigées")
        
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Sauvegarder
    with open('supermarket/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {len(corrections)} corrections appliquées:")
    for correction in corrections:
        print(f"  - {correction}")
    
    return len(corrections)

if __name__ == "__main__":
    fix_syntax_errors()
