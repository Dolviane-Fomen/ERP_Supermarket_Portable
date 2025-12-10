#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script pour créer les migrations pour le module commandes"""

import os
import sys
import django

# Configuration du chemin Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')

try:
    django.setup()
    
    from django.core.management import call_command
    from django.db import connection
    
    print("=" * 70)
    print("CRÉATION DES MIGRATIONS - MODULE COMMANDES")
    print("=" * 70)
    
    # Vérifier si les tables existent
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='supermarket_commande'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            cursor.execute("PRAGMA table_info(supermarket_commande)")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"\n📊 Colonnes existantes dans Commande: {', '.join(columns)}")
            
            required_columns = ['quantite', 'quantite_totale', 'prix_total']
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"\n⚠️  Colonnes manquantes: {', '.join(missing_columns)}")
                print("   → Des migrations sont nécessaires!")
            else:
                print("\n✅ Toutes les colonnes requises sont présentes!")
        else:
            print("\n⚠️  La table Commande n'existe pas encore")
            print("   → Des migrations sont nécessaires!")
    
    print("\n📝 Création des migrations...")
    call_command('makemigrations', verbosity=1)
    
    print("\n🔄 Application des migrations...")
    call_command('migrate', verbosity=1, interactive=False)
    
    print("\n✅ Migrations terminées!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

