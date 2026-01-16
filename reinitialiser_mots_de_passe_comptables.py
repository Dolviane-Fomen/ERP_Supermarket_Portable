#!/usr/bin/env python
"""
Script pour reinitialiser les mots de passe des comptables
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from django.contrib.auth.models import User
from supermarket.models import Compte

def reinitialiser_mots_de_passe_comptables():
    """Reinitialiser les mots de passe des comptables avec des mots de passe par defaut"""
    
    print("=" * 80)
    print("REINITIALISATION DES MOTS DE PASSE - COMPTABLES")
    print("=" * 80)
    
    # Types de comptes autorises pour le module comptabilite
    types_autorises = ['comptable', 'assistant_comptable', 'admin']
    
    # Chercher tous les comptes avec ces types
    comptes = Compte.objects.filter(
        type_compte__in=types_autorises,
        actif=True
    ).select_related('user', 'agence')
    
    if not comptes.exists():
        print("\nAUCUN COMPTE TROUVE!")
        return
    
    print(f"\n{comptes.count()} compte(s) trouve(s).\n")
    print("Mots de passe par defaut proposes:")
    print("  - Pour les comptables: comptable123")
    print("  - Pour les admins: admin123")
    print()
    
    # Reinitialiser les mots de passe
    for compte in comptes:
        if compte.type_compte == 'admin':
            nouveau_mdp = 'admin123'
        elif compte.type_compte in ['comptable', 'assistant_comptable']:
            nouveau_mdp = 'comptable123'
        else:
            nouveau_mdp = 'password123'
        
        compte.user.set_password(nouveau_mdp)
        compte.user.save()
        
        print(f"OK - {compte.user.username} ({compte.type_compte})")
        print(f"   Mot de passe reinitialise: {nouveau_mdp}")
        print(f"   Agence: {compte.agence.nom_agence if compte.agence else 'Aucune'}")
        print()
    
    print("=" * 80)
    print("RESUME DES COMPTES:")
    print("=" * 80)
    print("\nADMINS:")
    for compte in comptes.filter(type_compte='admin'):
        print(f"  - {compte.user.username} / admin123")
    
    print("\nCOMPTABLES:")
    for compte in comptes.filter(type_compte='comptable'):
        print(f"  - {compte.user.username} / comptable123")
        print(f"    Agence: {compte.agence.nom_agence if compte.agence else 'Aucune'}")
    
    print("\nASSISTANTS COMPTABLES:")
    for compte in comptes.filter(type_compte='assistant_comptable'):
        print(f"  - {compte.user.username} / comptable123")
        print(f"    Agence: {compte.agence.nom_agence if compte.agence else 'Aucune'}")
    
    print("\n" + "=" * 80)
    print("Vous pouvez maintenant vous connecter au module comptabilite avec ces identifiants.")
    print("=" * 80)

if __name__ == '__main__':
    reinitialiser_mots_de_passe_comptables()
