import os
import sys
import django

# Ajouter le répertoire du projet au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Compte, Agence

# Trouver l'agence MARCHE HUITIEME
agence = Agence.objects.filter(nom_agence__icontains='huitieme').first()

if agence:
    print(f"Agence trouvée: {agence.nom_agence} (ID: {agence.id_agence})")
    print(f"Adresse: {agence.adresse}")
    print("\n" + "="*60)
    
    # Récupérer tous les comptes de cette agence
    comptes = Compte.objects.filter(agence=agence, actif=True).select_related('user')
    
    print(f"\nNombre d'utilisateurs actifs: {comptes.count()}")
    print("\n" + "-"*60)
    print("LISTE DES UTILISATEURS:")
    print("-"*60)
    
    for compte in comptes:
        print(f"\nUsername: {compte.user.username}")
        print(f"  Nom complet: {compte.nom_complet}")
        print(f"  Type de compte: {compte.type_compte}")
        print(f"  Numéro compte: {compte.numero_compte}")
        print(f"  Email: {compte.email}")
        print(f"  Téléphone: {compte.telephone}")
        print(f"  Actif: {compte.actif}")
else:
    print("❌ Agence 'MARCHE HUITIEME' non trouvée!")
    print("\nAgences disponibles:")
    for ag in Agence.objects.all():
        print(f"  - {ag.nom_agence}")

