#!/usr/bin/env python
"""
Script pour créer la migration des modèles MargePersonnalisee et AssignationMargeArticle
"""

import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from django.core.management import call_command

print("=" * 80)
print("CREATION DE LA MIGRATION POUR LES MARGES PERSONNALISEES")
print("=" * 80)
print()

try:
    call_command('makemigrations', 'supermarket', name='add_marges_personnalisees', verbosity=2)
    print()
    print("[OK] Migration creee avec succes!")
    print()
    print("Pour appliquer la migration, executez:")
    print("  py manage.py migrate supermarket")
    print()
except Exception as e:
    print(f"[ERREUR] {e}")
    import traceback
    traceback.print_exc()
