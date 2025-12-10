"""
Script pour lister les agences disponibles avec leurs IDs
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
print("LISTE DES AGENCES DISPONIBLES")
print("=" * 60)
print()

agences = Agence.objects.all().order_by('id_agence')

if not agences.exists():
    print("⚠️  Aucune agence trouvée dans la base de données.")
    print()
    sys.exit(0)

print("ID  | Nom de l'Agence")
print("-" * 60)

for agence in agences:
    print(f"{agence.id_agence:3d} | {agence.nom_agence}")

print("-" * 60)
print()










