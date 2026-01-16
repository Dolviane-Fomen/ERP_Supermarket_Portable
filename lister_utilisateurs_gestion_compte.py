#!/usr/bin/env python
"""
Script pour lister tous les utilisateurs ayant accès au module Gestion des Comptes
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

def lister_utilisateurs_gestion_compte():
    """Lister tous les utilisateurs ayant accès au module Gestion des Comptes"""
    
    print("=" * 80)
    print("LISTE DES UTILISATEURS - MODULE GESTION DES COMPTES")
    print("=" * 80)
    
    # Le module gestion des comptes est accessible uniquement aux administrateurs
    types_autorises = ['admin']
    
    # Chercher tous les comptes administrateurs actifs
    comptes = Compte.objects.filter(
        type_compte__in=types_autorises,
        actif=True
    ).select_related('user', 'agence').order_by('nom', 'prenom')
    
    if not comptes.exists():
        print("\nAUCUN UTILISATEUR TROUVE avec acces au module Gestion des Comptes!")
        print("\nType de compte autorise: Administrateur (admin)")
        return
    
    print(f"\n{comptes.count()} utilisateur(s) trouve(s) avec acces au module Gestion des Comptes:\n")
    
    for index, compte in enumerate(comptes, 1):
        print("-" * 80)
        print(f"UTILISATEUR #{index}")
        print("-" * 80)
        print(f"Nom complet: {compte.nom_complet}")
        print(f"Numero compte: {compte.numero_compte}")
        print(f"Type compte: {compte.get_type_compte_display()} ({compte.type_compte})")
        print(f"Agence: {compte.agence.nom_agence if compte.agence else 'Aucune'}")
        print(f"Email: {compte.email}")
        print(f"Telephone: {compte.telephone}")
        print(f"Username Django: {compte.user.username}")
        print(f"Email Django: {compte.user.email}")
        print(f"Compte actif: {'Oui' if compte.actif else 'Non'}")
        print(f"Date creation: {compte.date_creation}")
        if compte.date_derniere_connexion:
            print(f"Derniere connexion: {compte.date_derniere_connexion}")
        else:
            print(f"Derniere connexion: Jamais connecte")
        
        # Vérifier si l'utilisateur Django est actif
        print(f"Utilisateur Django actif: {'Oui' if compte.user.is_active else 'Non'}")
        print(f"Superutilisateur Django: {'Oui' if compte.user.is_superuser else 'Non'}")
        print(f"Staff Django: {'Oui' if compte.user.is_staff else 'Non'}")
        
        # Note: Les mots de passe Django sont hashés, on ne peut pas les récupérer
        print(f"\nNOTE - MOT DE PASSE: Les mots de passe sont cryptes dans Django.")
        print(f"   Pour reinitialiser le mot de passe, utilisez:")
        print(f"   py manage.py changepassword {compte.user.username}")
        print("-" * 80)
        print()
    
    # Statistiques
    print("\n" + "=" * 80)
    print("STATISTIQUES")
    print("=" * 80)
    print(f"Total utilisateurs avec acces: {comptes.count()}")
    
    # Par agence
    agences_dict = {}
    for compte in comptes:
        agence_nom = compte.agence.nom_agence if compte.agence else "Aucune agence"
        if agence_nom not in agences_dict:
            agences_dict[agence_nom] = 0
        agences_dict[agence_nom] += 1
    
    if agences_dict:
        print("\nRepartition par agence:")
        for agence_nom, count in sorted(agences_dict.items()):
            print(f"  - {agence_nom}: {count} utilisateur(s)")
    
    # Utilisateurs actifs vs inactifs Django
    actifs_django = sum(1 for c in comptes if c.user.is_active)
    inactifs_django = comptes.count() - actifs_django
    print(f"\nUtilisateurs Django actifs: {actifs_django}")
    print(f"Utilisateurs Django inactifs: {inactifs_django}")
    
    print("\n" + "=" * 80)
    print("INFORMATIONS IMPORTANTES")
    print("=" * 80)
    print("\n1. Les mots de passe sont cryptes (hash) dans Django et ne peuvent pas")
    print("   etre recuperes en clair.")
    print("\n2. Pour reinitialiser un mot de passe:")
    print("   py manage.py changepassword <username>")
    print("\n3. Pour creer un nouveau compte administrateur:")
    print("   - Creer un User Django: py manage.py createsuperuser")
    print("   - Puis creer un Compte avec type_compte='admin'")
    print("\n4. Type de compte autorise pour le module Gestion des Comptes:")
    print("   - Administrateur (admin)")
    print("\n5. Le module Gestion des Comptes permet de:")
    print("   - Creer, modifier et supprimer des comptes utilisateurs")
    print("   - Gerer les permissions et les types de comptes")
    print("   - Consulter l'historique des comptes")
    print("\n" + "=" * 80)

if __name__ == '__main__':
    lister_utilisateurs_gestion_compte()
