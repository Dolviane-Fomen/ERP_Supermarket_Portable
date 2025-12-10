#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rapport final de vérification complète du module commandes"""

import re
from pathlib import Path

urls_file = Path('supermarket/urls.py')
views_file = Path('supermarket/views.py')
models_file = Path('supermarket/models.py')
templates_dir = Path('supermarket/templates/supermarket/commandes')

urls_content = urls_file.read_text(encoding='utf-8')
views_content = views_file.read_text(encoding='utf-8')
models_content = models_file.read_text(encoding='utf-8')

# Extraire toutes les URLs commandes
commande_urls = re.findall(r"path\('commandes/[^']+', views\.(\w+), name='(\w+)'", urls_content)

# Extraire toutes les fonctions définies
view_functions = set(re.findall(r'^def (\w+)\(', views_content, re.MULTILINE))

# Extraire tous les templates référencés
template_refs = re.findall(r"render\(request, 'supermarket/commandes/([^']+)'", views_content)

# Lister les templates existants
if templates_dir.exists():
    existing_templates = {f.name for f in templates_dir.glob('*.html')}
else:
    existing_templates = set()

print("=" * 70)
print("RAPPORT FINAL - MODULE COMMANDES")
print("=" * 70)

# 1. Vérification URLs vs Fonctions
print("\n1️⃣  VÉRIFICATION URLs → FONCTIONS")
print("-" * 70)
missing_funcs = []
for func_name, url_name in commande_urls:
    if func_name not in view_functions:
        missing_funcs.append((func_name, url_name))

if missing_funcs:
    print(f"❌ {len(missing_funcs)} fonction(s) manquante(s):")
    for func, url in missing_funcs:
        print(f"   - {func} (URL: {url})")
else:
    print(f"✅ Toutes les {len(commande_urls)} fonctions sont présentes!")

# 2. Vérification Templates
print("\n2️⃣  VÉRIFICATION TEMPLATES")
print("-" * 70)
missing_templates = []
for template in set(template_refs):
    if template not in existing_templates:
        missing_templates.append(template)

if missing_templates:
    print(f"❌ {len(missing_templates)} template(s) manquant(s):")
    for template in missing_templates:
        print(f"   - {template}")
else:
    print(f"✅ Tous les {len(set(template_refs))} templates sont présents!")

# 3. Vérification Modèle Commande
print("\n3️⃣  VÉRIFICATION MODÈLE COMMANDE")
print("-" * 70)
required_fields = ['quantite', 'quantite_totale', 'prix_total', 'date', 'heure', 'etat_commande', 'client', 'article', 'agence']
commande_model_match = re.search(r'class Commande\(models\.Model\):.*?def __str__', models_content, re.DOTALL)
if commande_model_match:
    commande_model = commande_model_match.group(0)
    missing_fields = []
    for field in required_fields:
        if field not in commande_model:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Champs manquants dans Commande: {', '.join(missing_fields)}")
    else:
        print(f"✅ Tous les champs requis sont présents dans le modèle Commande!")
else:
    print("⚠️  Modèle Commande non trouvé")

# 4. Liste des templates créés
print("\n4️⃣  TEMPLATES CRÉÉS")
print("-" * 70)
print(f"Total: {len(existing_templates)} templates")
for template in sorted(existing_templates):
    print(f"   ✅ {template}")

# 5. Résumé final
print("\n" + "=" * 70)
print("RÉSUMÉ FINAL")
print("=" * 70)
print(f"✅ URLs définies: {len(commande_urls)}")
print(f"✅ Fonctions présentes: {len([f for f, _ in commande_urls if f in view_functions])}/{len(commande_urls)}")
print(f"✅ Templates présents: {len(existing_templates)}")
print(f"✅ Templates référencés: {len(set(template_refs))}")

if not missing_funcs and not missing_templates:
    print("\n🎉 TOUS LES ACCÈS SONT COMPLETS!")
    print("\n⚠️  IMPORTANT: N'oubliez pas de:")
    print("   1. Vider le cache: VIDER_CACHE_PYTHON_DJANGO.bat")
    print("   2. Créer les migrations: py manage.py makemigrations")
    print("   3. Appliquer les migrations: py manage.py migrate")
    print("   4. Relancer l'ERP: ERP_Launcher.bat")
else:
    print("\n⚠️  Des éléments manquent - voir détails ci-dessus")

print("=" * 70)

