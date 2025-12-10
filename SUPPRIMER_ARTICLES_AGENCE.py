"""
Script pour supprimer tous les articles d'une agence spécifique
"""
import os
import sys
import django

# Configuration du chemin Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
django.setup()

from supermarket.models import Article, Agence

def supprimer_articles_agence(nom_agence):
    """
    Supprime tous les articles d'une agence spécifique
    
    Args:
        nom_agence: Nom de l'agence (ex: "MARCHE ESSOS")
    """
    try:
        # Récupérer l'agence
        try:
            agence = Agence.objects.get(nom_agence=nom_agence)
            print(f"✓ Agence trouvée: {agence.nom_agence} (ID: {agence.id_agence})")
        except Agence.DoesNotExist:
            print(f"✗ Erreur: L'agence '{nom_agence}' n'existe pas.")
            print("\nAgences disponibles:")
            for a in Agence.objects.all().order_by('nom_agence'):
                print(f"  - {a.nom_agence}")
            return False
        
        # Compter les articles
        nombre_articles = Article.objects.filter(agence=agence).count()
        print(f"\n📊 Nombre d'articles dans '{agence.nom_agence}': {nombre_articles}")
        
        if nombre_articles == 0:
            print("✓ Aucun article à supprimer.")
            return True
        
        # Demander confirmation
        print(f"\n⚠️  ATTENTION: Vous êtes sur le point de supprimer {nombre_articles} article(s) de l'agence '{agence.nom_agence}'")
        confirmation = input("Êtes-vous sûr de vouloir continuer ? (tapez 'OUI' pour confirmer): ")
        
        if confirmation != 'OUI':
            print("❌ Opération annulée.")
            return False
        
        # Supprimer les articles
        print(f"\n🗑️  Suppression en cours...")
        articles_supprimes = Article.objects.filter(agence=agence).delete()
        
        print(f"✓ Suppression terminée !")
        print(f"  - Articles supprimés: {articles_supprimes[0]}")
        
        # Vérifier qu'il ne reste plus d'articles
        articles_restants = Article.objects.filter(agence=agence).count()
        if articles_restants == 0:
            print(f"✓ Vérification: Aucun article restant dans '{agence.nom_agence}'")
        else:
            print(f"⚠️  Attention: {articles_restants} article(s) restant(s)")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la suppression: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale"""
    print("=" * 60)
    print("  SUPPRESSION DES ARTICLES D'UNE AGENCE")
    print("=" * 60)
    print()
    
    # Afficher les agences disponibles
    print("Agences disponibles:")
    agences = Agence.objects.all().order_by('nom_agence')
    for i, agence in enumerate(agences, 1):
        nombre_articles = Article.objects.filter(agence=agence).count()
        print(f"  {i}. {agence.nom_agence} ({nombre_articles} articles)")
    print()
    
    # Demander le nom de l'agence
    nom_agence = input("Entrez le nom de l'agence (ou appuyez sur Entrée pour 'MARCHE ESSOS'): ").strip()
    
    if not nom_agence:
        nom_agence = "MARCHE ESSOS"
    
    print()
    supprimer_articles_agence(nom_agence)
    
    print("\n" + "=" * 60)
    input("Appuyez sur Entrée pour quitter...")


if __name__ == '__main__':
    main()









