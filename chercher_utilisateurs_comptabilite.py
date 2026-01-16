#!/usr/bin/env python
"""
Script pour chercher les utilisateurs ayant accès au module gestion financière (comptabilité)
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from django.contrib.auth.models import User
from supermarket.models import Compte, Agence

def chercher_utilisateurs_comptabilite():
    """Chercher les utilisateurs ayant accès au module comptabilité"""
    
    print("=" * 80)
    print("RECHERCHE DES UTILISATEURS - MODULE GESTION FINANCIERE (COMPTABILITE)")
    print("=" * 80)
    
    # Types de comptes autorisés pour le module comptabilité
    types_autorises = ['comptable', 'assistant_comptable', 'admin']
    
    # Chercher tous les comptes avec ces types
    comptes = Compte.objects.filter(
        type_compte__in=types_autorises,
        actif=True
    ).select_related('user', 'agence')
    
    if not comptes.exists():
        print("\nAUCUN UTILISATEUR TROUVE avec acces au module comptabilite!")
        print("\nTypes de comptes autorises:")
        for t in types_autorises:
            print(f"  - {t}")
        return
    
    print(f"\n{comptes.count()} utilisateur(s) trouve(s) avec acces au module comptabilite:\n")
    
    for compte in comptes:
        print("-" * 80)
        print(f"Nom complet: {compte.nom_complet}")
        print(f"Numero compte: {compte.numero_compte}")
        print(f"Type compte: {compte.type_compte}")
        print(f"Agence: {compte.agence.nom_agence if compte.agence else 'Aucune'}")
        print(f"Email: {compte.email}")
        print(f"Telephone: {compte.telephone}")
        print(f"Username Django: {compte.user.username}")
        print(f"Email Django: {compte.user.email}")
        print(f"Compte actif: {'Oui' if compte.actif else 'Non'}")
        print(f"Date creation: {compte.date_creation}")
        
        # Note: Les mots de passe Django sont hashés, on ne peut pas les récupérer
        print(f"\nATTENTION - MOT DE PASSE: Les mots de passe sont cryptes dans Django.")
        print(f"   Pour reinitialiser le mot de passe, utilisez:")
        print(f"   py manage.py changepassword {compte.user.username}")
        print("-" * 80)
        print()
    
    print("\n" + "=" * 80)
    print("INFORMATIONS IMPORTANTES:")
    print("=" * 80)
    print("\n1. Les mots de passe sont cryptes (hash) dans Django et ne peuvent pas")
    print("   etre recuperes en clair.")
    print("\n2. Pour reinitialiser un mot de passe:")
    print("   py manage.py changepassword <username>")
    print("\n3. Pour creer un nouveau compte comptable:")
    print("   - Creer un User Django: py manage.py createsuperuser")
    print("   - Puis creer un Compte avec type_compte='comptable'")
    print("\n4. Types de comptes autorises pour le module comptabilite:")
    for t in types_autorises:
        print(f"   - {t}")
    print("\n" + "=" * 80)

if __name__ == '__main__':
    chercher_utilisateurs_comptabilite()
