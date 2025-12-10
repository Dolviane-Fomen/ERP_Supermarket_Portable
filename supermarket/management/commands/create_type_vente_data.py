from django.core.management.base import BaseCommand
from supermarket.models import Article, TypeVente, Agence

class Command(BaseCommand):
    help = 'Créer des données de test pour TypeVente'

    def handle(self, *args, **options):
        self.stdout.write('Création des données de test pour TypeVente...')
        
        # Récupérer l'agence
        agence = Agence.objects.first()
        if not agence:
            self.stdout.write(self.style.ERROR('Aucune agence trouvée. Créez d\'abord une agence.'))
            return
        
        # Récupérer tous les articles
        articles = Article.objects.filter(agence=agence)
        
        if not articles.exists():
            self.stdout.write(self.style.ERROR('Aucun article trouvé. Créez d\'abord des articles.'))
            return
        
        # Supprimer les types de vente existants
        TypeVente.objects.all().delete()
        self.stdout.write('Anciens types de vente supprimés.')
        
        created_count = 0
        
        for article in articles:
            # Prix de base (prix_vente de l'article)
            prix_base = float(article.prix_vente)
            
            # Créer les 3 types de vente pour chaque article
            types_vente_data = [
                {
                    'intitule': 'Détail',
                    'prix': prix_base,  # Prix normal
                },
                {
                    'intitule': 'Demi-gros',
                    'prix': round(prix_base * 0.85, 2),  # 15% de réduction
                },
                {
                    'intitule': 'Gros',
                    'prix': round(prix_base * 0.70, 2),  # 30% de réduction
                }
            ]
            
            for type_data in types_vente_data:
                TypeVente.objects.create(
                    intitule=type_data['intitule'],
                    prix=type_data['prix'],
                    article=article
                )
                created_count += 1
            
            self.stdout.write(f'Types de vente créés pour: {article.designation}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ {created_count} types de vente créés avec succès pour {articles.count()} articles!'
            )
        )
        
        # Afficher un exemple
        if articles.exists():
            article_exemple = articles.first()
            types_exemple = TypeVente.objects.filter(article=article_exemple)
            self.stdout.write(f'\nExemple pour "{article_exemple.designation}":')
            for type_vente in types_exemple:
                self.stdout.write(f'  - {type_vente.intitule}: {type_vente.prix} FCFA')




