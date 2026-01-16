#!/usr/bin/env python
"""
Script pour lister les utilisateurs ayant accès aux modules:
- Gestion Compte (comptable)
- Analyse Financière
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

def afficher_compte(compte, module_name):
    """Afficher les informations d'un compte"""
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
    print(f"Module(s) d'acces: {module_name}")
    print("-" * 80)
    print()

def chercher_utilisateurs_modules():
    """Chercher les utilisateurs ayant accès aux modules Gestion Compte et Analyse Financière"""
    
    print("=" * 80)
    print("LISTE DES UTILISATEURS - MODULES GESTION COMPTE ET ANALYSE FINANCIERE")
    print("=" * 80)
    
    # Types de comptes autorisés pour le module Gestion Compte (comptable)
    types_gestion_compte = ['comptable', 'assistant_comptable', 'admin']
    
    # Types de comptes autorisés pour le module Analyse Financière
    types_analyse_financiere = ['analyste_financiere', 'admin']
    
    # Chercher tous les comptes pour le module Gestion Compte
    comptes_gestion = Compte.objects.filter(
        type_compte__in=types_gestion_compte,
        actif=True
    ).select_related('user', 'agence').order_by('type_compte', 'nom', 'prenom')
    
    # Chercher tous les comptes pour le module Analyse Financière
    comptes_analyse = Compte.objects.filter(
        type_compte__in=types_analyse_financiere,
        actif=True
    ).select_related('user', 'agence').order_by('type_compte', 'nom', 'prenom')
    
    # ===== MODULE GESTION COMPTE =====
    print("\n" + "=" * 80)
    print("MODULE: GESTION COMPTE (COMPTABLE)")
    print("=" * 80)
    print(f"\nTypes de comptes autorises: {', '.join(types_gestion_compte)}")
    
    if not comptes_gestion.exists():
        print("\nAUCUN UTILISATEUR TROUVE avec acces au module Gestion Compte!")
    else:
        print(f"\n{comptes_gestion.count()} utilisateur(s) trouve(s):\n")
        for compte in comptes_gestion:
            modules = []
            if compte.type_compte in types_gestion_compte:
                modules.append("Gestion Compte")
            if compte.type_compte in types_analyse_financiere:
                modules.append("Analyse Financière")
            afficher_compte(compte, ", ".join(modules))
    
    # ===== MODULE ANALYSE FINANCIERE =====
    print("\n" + "=" * 80)
    print("MODULE: ANALYSE FINANCIERE")
    print("=" * 80)
    print(f"\nTypes de comptes autorises: {', '.join(types_analyse_financiere)}")
    
    if not comptes_analyse.exists():
        print("\nAUCUN UTILISATEUR TROUVE avec acces au module Analyse Financiere!")
    else:
        print(f"\n{comptes_analyse.count()} utilisateur(s) trouve(s):\n")
        for compte in comptes_analyse:
            modules = []
            if compte.type_compte in types_gestion_compte:
                modules.append("Gestion Compte")
            if compte.type_compte in types_analyse_financiere:
                modules.append("Analyse Financière")
            afficher_compte(compte, ", ".join(modules))
    
    # ===== RESUME =====
    print("\n" + "=" * 80)
    print("RESUME")
    print("=" * 80)
    
    # Comptes uniques (pour éviter les doublons admin)
    tous_comptes_ids = set()
    tous_comptes_ids.update(comptes_gestion.values_list('id', flat=True))
    tous_comptes_ids.update(comptes_analyse.values_list('id', flat=True))
    
    print(f"\nTotal utilisateurs uniques avec acces aux modules: {len(tous_comptes_ids)}")
    print(f"  - Module Gestion Compte uniquement: {comptes_gestion.exclude(id__in=comptes_analyse.values_list('id', flat=True)).count()}")
    print(f"  - Module Analyse Financiere uniquement: {comptes_analyse.exclude(id__in=comptes_gestion.values_list('id', flat=True)).count()}")
    print(f"  - Acces aux deux modules: {comptes_gestion.filter(id__in=comptes_analyse.values_list('id', flat=True)).count()}")
    
    # ===== INFORMATIONS IMPORTANTES =====
    print("\n" + "=" * 80)
    print("INFORMATIONS IMPORTANTES:")
    print("=" * 80)
    print("\n1. Les mots de passe sont cryptes (hash) dans Django et ne peuvent pas")
    print("   etre recuperes en clair.")
    print("\n2. Pour reinitialiser un mot de passe:")
    print("   py manage.py changepassword <username>")
    print("\n3. Types de comptes par module:")
    print("   - Module Gestion Compte: comptable, assistant_comptable, admin")
    print("   - Module Analyse Financiere: analyste_financiere, admin")
    print("\n" + "=" * 80)

if __name__ == '__main__':
    chercher_utilisateurs_modules()
