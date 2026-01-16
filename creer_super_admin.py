#!/usr/bin/env python
"""
Script pour créer un compte super admin avec accès à tous les modules
Username: admin
Password: admin123
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

def creer_super_admin():
    """Créer un compte super admin avec accès à tous les modules"""
    
    print("=" * 80)
    print("CREATION DU COMPTE SUPER ADMIN")
    print("=" * 80)
    
    username = 'admin'
    password = 'admin123'
    email = 'admin@erp.local'
    
    # Vérifier si l'utilisateur existe déjà
    try:
        user_existant = User.objects.get(username=username)
        print(f"\nATTENTION: L'utilisateur '{username}' existe deja!")
        print("Voulez-vous le mettre a jour? (suppression et recreation)")
        
        # Supprimer le compte et l'utilisateur existant
        try:
            compte_existant = Compte.objects.get(user=user_existant)
            print(f"  - Suppression du compte: {compte_existant.numero_compte}")
            compte_existant.delete()
        except Compte.DoesNotExist:
            print("  - Aucun compte associe trouve")
        
        print(f"  - Suppression de l'utilisateur Django: {username}")
        user_existant.delete()
        print("  - Utilisateur et compte supprimes avec succes\n")
        
    except User.DoesNotExist:
        print(f"\nL'utilisateur '{username}' n'existe pas encore. Creation en cours...\n")
    
    # Récupérer la première agence disponible (ou créer une agence par défaut si aucune n'existe)
    try:
        agence = Agence.objects.first()
        if not agence:
            print("ERREUR: Aucune agence trouvee dans la base de donnees!")
            print("Veuillez creer au moins une agence avant de creer un compte admin.")
            return
        print(f"Agence selectionnee: {agence.nom_agence} (ID: {agence.id_agence})")
    except Exception as e:
        print(f"ERREUR lors de la recuperation de l'agence: {e}")
        return
    
    try:
        # Créer l'utilisateur Django
        print(f"\nCreation de l'utilisateur Django...")
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=True,  # Accès à l'interface d'administration Django
            is_superuser=True  # Super utilisateur Django
        )
        print(f"  [OK] Utilisateur Django cree: {user.username}")
        
        # Générer un numéro de compte unique
        numero_compte = 'ADMIN_SUPER'
        compteur = 1
        while Compte.objects.filter(numero_compte=numero_compte).exists():
            numero_compte = f'ADMIN_SUPER_{compteur}'
            compteur += 1
        
        # Créer le compte
        print(f"\nCreation du compte ERP...")
        compte = Compte.objects.create(
            user=user,
            numero_compte=numero_compte,
            type_compte='admin',  # Type admin pour accès à tous les modules
            nom='Super',
            prenom='Admin',
            telephone='0000000000',
            email=email,
            agence=agence,
            actif=True
        )
        print(f"  [OK] Compte ERP cree: {compte.numero_compte}")
        print(f"  [OK] Type de compte: {compte.get_type_compte_display()}")
        print(f"  [OK] Agence: {compte.agence.nom_agence}")
        
        print("\n" + "=" * 80)
        print("COMPTE SUPER ADMIN CREE AVEC SUCCES!")
        print("=" * 80)
        print(f"\nInformations de connexion:")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Email: {email}")
        print(f"\nNom complet: {compte.nom_complet}")
        print(f"Numero compte: {compte.numero_compte}")
        print(f"Type compte: {compte.get_type_compte_display()}")
        print(f"Agence: {compte.agence.nom_agence}")
        print(f"\nACCES AUX MODULES:")
        print("  [OK] Tous les modules et fonctionnalites de l'ERP")
        print("  [OK] Interface d'administration Django (is_staff=True)")
        print("  [OK] Super utilisateur Django (is_superuser=True)")
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\nERREUR lors de la creation du compte: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == '__main__':
    creer_super_admin()
