"""
Script pour ajouter l'agence "Poissonnerie Sangah" dans la base de données
"""
import os
import sys
import django

# Configuration du chemin Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Agence

print("\n" + "=" * 60)
print("AJOUT DE L'AGENCE 'POISSONNERIE SANGAH'")
print("=" * 60)
print()

# Vérifier si l'agence existe déjà
nom_agence = "Poissonnerie Sangah"
agence_existante = Agence.objects.filter(nom_agence__iexact=nom_agence).first()

if agence_existante:
    print(f"⚠️  L'agence '{nom_agence}' existe déjà !")
    print(f"   ID: {agence_existante.id_agence}")
    print(f"   Nom: {agence_existante.nom_agence}")
    print(f"   Adresse: {agence_existante.adresse}")
    print()
    sys.exit(0)

# Créer la nouvelle agence
try:
    nouvelle_agence = Agence.objects.create(
        nom_agence=nom_agence,
        adresse="Sangah, Yaoundé"
    )
    
    print(f"✅ Agence créée avec succès !")
    print(f"   ID: {nouvelle_agence.id_agence}")
    print(f"   Nom: {nouvelle_agence.nom_agence}")
    print(f"   Adresse: {nouvelle_agence.adresse}")
    print()
    print("L'agence est maintenant disponible dans le module Suivi Statistique.")
    print()
    
except Exception as e:
    print(f"❌ Erreur lors de la création de l'agence: {e}")
    print()
    sys.exit(1)
