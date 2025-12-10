#!/usr/bin/env python3
"""
AFFECTER_UTILISATEURS_AGENCES.py
Script pour affecter correctement les utilisateurs aux agences
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
django.setup()

from django.contrib.auth.models import User
from supermarket.models import Agence, Compte, Employe

def log(message):
    """Afficher un message avec formatage"""
    print(f"[INFO] {message}")

def affecter_utilisateurs():
    """Affecter les utilisateurs aux bonnes agences"""
    
    print("=" * 70)
    print("  AFFECTATION DES UTILISATEURS AUX AGENCES")
    print("=" * 70)
    print()
    
    # Définition des utilisateurs
    utilisateurs_caisse = [
        {
            'prenom': 'Constantine',
            'nom': 'Constantine',
            'username': 'caisseire1',
            'password': 'caisse1',
            'agence_nom': 'MARCHE HUITIEME',
            'type_compte': 'caissier',
            'email': 'constantine@erp.local',
            'telephone': '0000000001'
        },
        {
            'prenom': 'Irene',
            'nom': 'Irene',
            'username': 'caissier2',
            'password': 'caisse2',
            'agence_nom': 'MARCHE ESSOS',
            'type_compte': 'caissier',
            'email': 'irene@erp.local',
            'telephone': '0000000002'
        },
        {
            'prenom': 'Estelle',
            'nom': 'Estelle',
            'username': 'caisseire3',
            'password': 'caisse3',
            'agence_nom': 'MARCHE VOTGBI',
            'type_compte': 'caissier',
            'email': 'estelle@erp.local',
            'telephone': '0000000003'
        },
        {
            'prenom': 'Marceline',
            'nom': 'Marceline',
            'username': 'caisier4',
            'password': 'caisse4',
            'agence_nom': 'POISSONNERIE SANGAH',
            'type_compte': 'caissier',
            'email': 'marceline@erp.local',
            'telephone': '0000000004'
        },
    ]
    
    utilisateurs_stock = [
        {
            'prenom': 'Brayan',
            'nom': 'Brayan',
            'username': 'comptable1',
            'password': 'compt1',
            'agence_nom': 'MARCHE HUITIEME',
            'type_compte': 'comptable',
            'email': 'brayan@erp.local',
            'telephone': '0000000005'
        },
        {
            'prenom': 'Gabriel',
            'nom': 'Gabriel',
            'username': 'comptable2',
            'password': 'compt2',
            'agence_nom': 'MARCHE ESSOS',
            'type_compte': 'comptable',
            'email': 'gabriel@erp.local',
            'telephone': '0000000006'
        },
        {
            'prenom': 'Michelle',
            'nom': 'Michelle',
            'username': 'comptable3',
            'password': 'compt3',
            'agence_nom': 'MARCHE VOTGBI',
            'type_compte': 'comptable',
            'email': 'michelle@erp.local',
            'telephone': '0000000007'
        },
        {
            'prenom': 'Brayan',
            'nom': 'Brayan1',
            'username': 'comptable4',
            'password': 'compt4',
            'agence_nom': 'POISSONNERIE SANGAH',
            'type_compte': 'comptable',
            'email': 'brayan1@erp.local',
            'telephone': '0000000008'
        },
    ]
    
    tous_utilisateurs = utilisateurs_caisse + utilisateurs_stock
    
    # Statistiques
    stats = {
        'utilisateurs_crees': 0,
        'utilisateurs_mis_a_jour': 0,
        'comptes_crees': 0,
        'comptes_mis_a_jour': 0,
        'employes_crees': 0,
        'erreurs': 0
    }
    
    print("📋 TRAITEMENT DES UTILISATEURS")
    print()
    
    for user_data in tous_utilisateurs:
        try:
            username = user_data['username']
            agence_nom = user_data['agence_nom']
            
            print(f"→ {user_data['prenom']} ({username}) - {agence_nom}")
            
            # Rechercher l'agence
            try:
                agence = Agence.objects.get(nom_agence__icontains=agence_nom)
                log(f"  Agence trouvée: {agence.nom_agence}")
            except Agence.DoesNotExist:
                print(f"  ❌ ERREUR: Agence '{agence_nom}' non trouvée")
                stats['erreurs'] += 1
                continue
            
            # Créer ou mettre à jour l'utilisateur Django
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': user_data['prenom'],
                    'last_name': user_data['nom'],
                    'email': user_data['email'],
                    'is_active': True,
                }
            )
            
            if user_created:
                user.set_password(user_data['password'])
                user.save()
                log(f"  ✅ Utilisateur créé: {username}")
                stats['utilisateurs_crees'] += 1
            else:
                # Mettre à jour le mot de passe
                user.set_password(user_data['password'])
                user.first_name = user_data['prenom']
                user.last_name = user_data['nom']
                user.email = user_data['email']
                user.save()
                log(f"  ✅ Utilisateur mis à jour: {username}")
                stats['utilisateurs_mis_a_jour'] += 1
            
            # Créer ou mettre à jour le Compte
            compte, compte_created = Compte.objects.get_or_create(
                user=user,
                defaults={
                    'numero_compte': f"CPT_{username.upper()}",
                    'type_compte': user_data['type_compte'],
                    'nom': user_data['nom'],
                    'prenom': user_data['prenom'],
                    'telephone': user_data['telephone'],
                    'email': user_data['email'],
                    'actif': True,
                    'agence': agence
                }
            )
            
            if compte_created:
                log(f"  ✅ Compte créé pour {user_data['prenom']}")
                stats['comptes_crees'] += 1
            else:
                # Mettre à jour l'agence et les infos
                compte.agence = agence
                compte.type_compte = user_data['type_compte']
                compte.nom = user_data['nom']
                compte.prenom = user_data['prenom']
                compte.telephone = user_data['telephone']
                compte.email = user_data['email']
                compte.actif = True
                compte.save()
                log(f"  ✅ Compte mis à jour: {user_data['prenom']} → {agence.nom_agence}")
                stats['comptes_mis_a_jour'] += 1
            
            # Créer l'Employé si nécessaire
            employe, employe_created = Employe.objects.get_or_create(
                compte=compte,
                defaults={
                    'numero_employe': f"EMP_{username.upper()}",
                    'poste': 'Caissier(ère)' if user_data['type_compte'] == 'caissier' else 'Comptable',
                    'departement': 'caisse' if user_data['type_compte'] == 'caissier' else 'comptabilite',
                    'statut': 'actif'
                }
            )
            
            if employe_created:
                log(f"  ✅ Employé créé pour {user_data['prenom']}")
                stats['employes_crees'] += 1
            
            print()
            
        except Exception as e:
            print(f"  ❌ ERREUR pour {user_data['username']}: {e}")
            stats['erreurs'] += 1
            print()
    
    # Afficher les statistiques
    print("=" * 70)
    print("  RÉSUMÉ DES OPÉRATIONS")
    print("=" * 70)
    print()
    print(f"📊 Utilisateurs créés       : {stats['utilisateurs_crees']}")
    print(f"📊 Utilisateurs mis à jour  : {stats['utilisateurs_mis_a_jour']}")
    print(f"📊 Comptes créés            : {stats['comptes_crees']}")
    print(f"📊 Comptes mis à jour       : {stats['comptes_mis_a_jour']}")
    print(f"📊 Employés créés           : {stats['employes_crees']}")
    print(f"❌ Erreurs                  : {stats['erreurs']}")
    print()
    
    # Afficher les affectations finales
    print("=" * 70)
    print("  AFFECTATIONS FINALES")
    print("=" * 70)
    print()
    
    print("🏪 GESTION CAISSE:")
    for user_data in utilisateurs_caisse:
        try:
            user = User.objects.get(username=user_data['username'])
            compte = Compte.objects.get(user=user)
            print(f"  ✅ {compte.prenom} ({user.username}) → {compte.agence.nom_agence}")
        except:
            print(f"  ❌ {user_data['username']} - Non configuré")
    
    print()
    print("📦 GESTION STOCK:")
    for user_data in utilisateurs_stock:
        try:
            user = User.objects.get(username=user_data['username'])
            compte = Compte.objects.get(user=user)
            print(f"  ✅ {compte.prenom} ({user.username}) → {compte.agence.nom_agence}")
        except:
            print(f"  ❌ {user_data['username']} - Non configuré")
    
    print()
    print("=" * 70)
    print("  ✅ AFFECTATION TERMINÉE")
    print("=" * 70)
    print()
    
    print("📋 INFORMATIONS DE CONNEXION:")
    print()
    print("GESTION CAISSE:")
    for user_data in utilisateurs_caisse:
        print(f"  • {user_data['prenom']:15} - {user_data['username']:15} / {user_data['password']:10} - {user_data['agence_nom']}")
    
    print()
    print("GESTION STOCK:")
    for user_data in utilisateurs_stock:
        print(f"  • {user_data['prenom']:15} - {user_data['username']:15} / {user_data['password']:10} - {user_data['agence_nom']}")
    
    print()
    print("=" * 70)

if __name__ == '__main__':
    try:
        affecter_utilisateurs()
        sys.exit(0)
    except Exception as e:
        print(f"❌ ERREUR GLOBALE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




