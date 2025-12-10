#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script pour vérifier que tous les templates référencés dans les vues existent"""

import re
from pathlib import Path

views_file = Path('supermarket/views.py')
templates_dir = Path('supermarket/templates/supermarket/commandes')

views_content = views_file.read_text(encoding='utf-8')

# Extraire tous les templates référencés pour le module commandes
template_refs = re.findall(r"render\(request, 'supermarket/commandes/([^']+)'", views_content)

# Lister tous les templates existants
if templates_dir.exists():
    existing_templates = {f.name for f in templates_dir.glob('*.html')}
else:
    existing_templates = set()

# Vérifier les templates manquants
missing_templates = []
for template in template_refs:
    if template not in existing_templates:
        missing_templates.append(template)

print("=" * 60)
print("VÉRIFICATION DES TEMPLATES MODULE COMMANDES")
print("=" * 60)
print(f"\nTotal templates référencés: {len(template_refs)}")
print(f"Total templates existants: {len(existing_templates)}")

if missing_templates:
    print(f"\n❌ TEMPLATES MANQUANTS ({len(missing_templates)}):")
    for template in missing_templates:
        print(f"   - {template}")
else:
    print("\n✅ TOUS LES TEMPLATES SONT PRÉSENTS!")

print(f"\n📄 Templates référencés:")
for template in sorted(set(template_refs)):
    status = "✅" if template in existing_templates else "❌"
    print(f"   {status} {template}")

print("\n" + "=" * 60)

