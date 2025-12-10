#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Vérifier les redirections et templates manquants dans le module commandes"""

import re
from pathlib import Path

views_file = Path('supermarket/views.py')
views_content = views_file.read_text(encoding='utf-8')

# Trouver toutes les fonctions qui font des render vers commandes
render_pattern = r"render\(request, 'supermarket/commandes/([^']+)'"
renders = re.findall(render_pattern, views_content)

# Trouver toutes les redirections vers des URLs commandes
redirect_pattern = r"redirect\('([^']+)'\)"
redirects = re.findall(redirect_pattern, views_content)

# Trouver les fonctions qui devraient afficher un template mais qui redirigent
functions_with_redirects = {}
for func_match in re.finditer(r'def (\w+)\([^)]*\):.*?(?=def |\Z)', views_content, re.DOTALL):
    func_name = func_match.group(1)
    func_body = func_match.group(0)
    
    # Vérifier si c'est une fonction commandes
    if 'commande' in func_name.lower() or 'livraison' in func_name.lower() or 'client' in func_name.lower() or 'livreur' in func_name.lower():
        has_render = bool(re.search(render_pattern, func_body))
        has_redirect = bool(re.search(redirect_pattern, func_body))
        
        if has_redirect and not has_render:
            # Trouver vers où ça redirige
            redirect_targets = re.findall(redirect_pattern, func_body)
            functions_with_redirects[func_name] = redirect_targets

print("=" * 70)
print("VÉRIFICATION DES REDIRECTIONS - MODULE COMMANDES")
print("=" * 70)

print(f"\n📄 Templates référencés: {len(set(renders))}")
print(f"🔀 Redirections trouvées: {len(set(redirects))}")

if functions_with_redirects:
    print(f"\n⚠️  Fonctions qui redirigent sans afficher de template ({len(functions_with_redirects)}):")
    for func, targets in functions_with_redirects.items():
        print(f"   - {func} -> {', '.join(targets)}")
else:
    print("\n✅ Toutes les fonctions affichent des templates ou redirigent correctement")

print("\n" + "=" * 70)

