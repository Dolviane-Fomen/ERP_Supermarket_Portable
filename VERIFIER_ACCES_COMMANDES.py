#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script pour vérifier que toutes les URLs du module commandes ont leurs fonctions correspondantes"""

import re
from pathlib import Path

# Lire les fichiers
urls_file = Path('supermarket/urls.py')
views_file = Path('supermarket/views.py')

urls_content = urls_file.read_text(encoding='utf-8')
views_content = views_file.read_text(encoding='utf-8')

# Extraire toutes les fonctions référencées dans les URLs commandes
commande_urls = re.findall(r"path\('commandes/[^']+', views\.(\w+)", urls_content)

# Extraire toutes les fonctions définies dans views.py
view_functions = set(re.findall(r'^def (\w+)\(', views_content, re.MULTILINE))

# Vérifier les fonctions manquantes
missing_functions = []
for func_name in commande_urls:
    if func_name not in view_functions:
        missing_functions.append(func_name)

print("=" * 60)
print("VÉRIFICATION DES ACCÈS MODULE COMMANDES")
print("=" * 60)
print(f"\nTotal URLs commandes: {len(commande_urls)}")
print(f"Total fonctions dans views.py: {len(view_functions)}")

if missing_functions:
    print(f"\n❌ FONCTIONS MANQUANTES ({len(missing_functions)}):")
    for func in missing_functions:
        print(f"   - {func}")
else:
    print("\n✅ TOUTES LES FONCTIONS SONT PRÉSENTES!")

# Vérifier aussi les templates
templates_dir = Path('supermarket/templates/supermarket/commandes')
if templates_dir.exists():
    templates = [f.name for f in templates_dir.glob('*.html')]
    print(f"\n📄 Templates trouvés: {len(templates)}")
    print(f"   {', '.join(templates)}")
else:
    print("\n⚠️  Dossier templates/commandes non trouvé")

print("\n" + "=" * 60)

