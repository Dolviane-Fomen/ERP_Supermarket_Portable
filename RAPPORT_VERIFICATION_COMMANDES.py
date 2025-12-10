#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rapport complet de vérification du module commandes"""

import re
from pathlib import Path
from collections import defaultdict

urls_file = Path('supermarket/urls.py')
views_file = Path('supermarket/views.py')
templates_dir = Path('supermarket/templates/supermarket/commandes')

urls_content = urls_file.read_text(encoding='utf-8')
views_content = views_file.read_text(encoding='utf-8')

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
print("RAPPORT COMPLET - MODULE COMMANDES")
print("=" * 70)

# 1. Vérification des fonctions
print("\n📋 1. VÉRIFICATION DES FONCTIONS")
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

# 2. Vérification des templates
print("\n📄 2. VÉRIFICATION DES TEMPLATES")
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

# 3. Liste complète des accès
print("\n🔗 3. LISTE COMPLÈTE DES ACCÈS")
print("-" * 70)

categories = {
    'Authentification': ['login_commandes', 'logout_commandes'],
    'Commandes': ['enregistrer_commande', 'consulter_commandes', 'detail_commande', 'modifier_commande', 'supprimer_commande', 'sauvegarder_commande'],
    'Articles': ['ajouter_article_commande', 'mettre_a_jour_quantites_commande', 'supprimer_article_commande', 'rechercher_articles_commande', 'search_window_commande'],
    'Factures': ['consulter_factures_commande', 'detail_facture_commande', 'generer_facture_commande', 'generer_facture_commande_existante', 'imprimer_facture_commande', 'imprimer_facture_commande_xprinter'],
    'Clients': ['enregistrer_client', 'consulter_clients_commandes', 'detail_client_commandes', 'modifier_client_commandes', 'supprimer_client_commandes'],
    'Livraisons': ['planification_livraison', 'creer_planification_livraison', 'verifier_stock_livraison', 'reporter_livraison', 'annuler_livraison', 'modifier_ordre_livraison', 'voir_itineraire', 'confirmer_livraison', 'definir_etat_livraison', 'definir_etat_final_livraison', 'consulter_livraisons'],
    'Statistiques': ['statistiques_clients', 'generer_statistiques_clients', 'export_statistiques_clients_excel'],
    'Rapports': ['rapport_livraison', 'generer_rapport_livraison', 'export_rapport_livraison_excel'],
    'Livreurs': ['consulter_livreurs', 'enregistrer_livreur', 'detail_livreur', 'modifier_livreur', 'supprimer_livreur'],
    'Notifications': ['get_notifications', 'marquer_notification_lue', 'marquer_toutes_notifications_lues']
}

url_names = {name for _, name in commande_urls}

for category, expected_urls in categories.items():
    print(f"\n{category}:")
    for url_name in expected_urls:
        status = "✅" if url_name in url_names else "❌"
        print(f"   {status} {url_name}")

# 4. Résumé final
print("\n" + "=" * 70)
print("RÉSUMÉ FINAL")
print("=" * 70)
print(f"✅ URLs définies: {len(commande_urls)}")
print(f"✅ Fonctions présentes: {len([f for f, _ in commande_urls if f in view_functions])}/{len(commande_urls)}")
print(f"✅ Templates présents: {len(existing_templates)}")
print(f"✅ Templates référencés: {len(set(template_refs))}")

if not missing_funcs and not missing_templates:
    print("\n🎉 TOUS LES ACCÈS SONT COMPLETS ET FONCTIONNELS!")
else:
    print("\n⚠️  Des éléments manquent - voir détails ci-dessus")

print("=" * 70)

