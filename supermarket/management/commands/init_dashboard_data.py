from django.core.management.base import BaseCommand
from supermarket.models import Agence, Caisse, Compte, Employe, Client, Article, Famille, TypeVente
from django.contrib.auth.models import User
from decimal import Decimal

class Command(BaseCommand):
    help = 'Initialise les données nécessaires pour le dashboard'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initialisation des données du dashboard...'))
        
        # Créer un utilisateur admin si il n'existe pas
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Utilisateur admin créé'))
        else:
            self.stdout.write(self.style.WARNING('Utilisateur admin existe déjà'))
        
        # Créer une agence
        agence, created = Agence.objects.get_or_create(
            nom_agence='Agence Principale',
            defaults={
                'adresse': '123 Rue de la Paix'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Agence créée'))
        else:
            self.stdout.write(self.style.WARNING('Agence existe déjà'))
        
        # Créer un compte pour l'employé
        compte, created = Compte.objects.get_or_create(
            numero_compte='EMP001',
            defaults={
                'user': user,
                'type_compte': 'caissier',
                'nom': 'Dupont',
                'prenom': 'Marie',
                'email': 'marie.dupont@example.com',
                'telephone': '+237 987 654 321',
                'agence': agence
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Compte employé créé'))
        else:
            self.stdout.write(self.style.WARNING('Compte employé existe déjà'))
        
        # Créer un employé
        employe, created = Employe.objects.get_or_create(
            compte=compte,
            defaults={
                'agence': agence,
                'poste': 'Caissière'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Employé créé'))
        else:
            self.stdout.write(self.style.WARNING('Employé existe déjà'))
        
        # Créer une caisse
        caisse, created = Caisse.objects.get_or_create(
            numero_caisse='CAISSE001',
            defaults={
                'agence': agence,
                'solde_actuel': Decimal('100000.00')
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Caisse créée'))
        else:
            self.stdout.write(self.style.WARNING('Caisse existe déjà'))
        
        # Créer des clients
        clients_data = [
            {'intitule': 'Client 1', 'telephone': '+237 111 111 111'},
            {'intitule': 'Client 2', 'telephone': '+237 222 222 222'},
            {'intitule': 'Client 3', 'telephone': '+237 333 333 333'},
        ]
        
        for client_data in clients_data:
            client, created = Client.objects.get_or_create(
                intitule=client_data['intitule'],
                defaults={
                    'agence': agence,
                    'telephone': client_data['telephone']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Client {client_data["intitule"]} créé'))
        
        # Créer une famille d'articles
        famille, created = Famille.objects.get_or_create(
            intitule='Alimentation',
            defaults={
                'code': 'ALIM001',
                'unite_vente': 'Unité',
                'suivi_stock': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Famille d\'articles créée'))
        
        # Créer des articles
        articles_data = [
            {'reference': 'ART001', 'designation': 'Riz 1kg', 'prix_vente': Decimal('500.00'), 'prix_achat': Decimal('300.00')},
            {'reference': 'ART002', 'designation': 'Huile 1L', 'prix_vente': Decimal('800.00'), 'prix_achat': Decimal('500.00')},
            {'reference': 'ART003', 'designation': 'Sucre 1kg', 'prix_vente': Decimal('600.00'), 'prix_achat': Decimal('400.00')},
            {'reference': 'ART004', 'designation': 'Pain', 'prix_vente': Decimal('200.00'), 'prix_achat': Decimal('100.00')},
            {'reference': 'ART005', 'designation': 'Eau 1.5L', 'prix_vente': Decimal('300.00'), 'prix_achat': Decimal('150.00')},
        ]
        
        for article_data in articles_data:
            article, created = Article.objects.get_or_create(
                reference_article=article_data['reference'],
                defaults={
                    'designation': article_data['designation'],
                    'prix_vente': article_data['prix_vente'],
                    'prix_achat': article_data['prix_achat'],
                    'stock_actuel': 100,
                    'categorie': famille,
                    'agence': agence
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Article {article_data["designation"]} créé'))
                
                # Créer les types de vente pour cet article
                TypeVente.objects.get_or_create(
                    article=article,
                    intitule='Détail',
                    defaults={'prix': article_data['prix_vente']}
                )
                TypeVente.objects.get_or_create(
                    article=article,
                    intitule='Demi-gros',
                    defaults={'prix': article_data['prix_vente'] * Decimal('0.85')}
                )
                TypeVente.objects.get_or_create(
                    article=article,
                    intitule='Gros',
                    defaults={'prix': article_data['prix_vente'] * Decimal('0.70')}
                )
        
        self.stdout.write(self.style.SUCCESS('✅ Données du dashboard initialisées avec succès!'))
        self.stdout.write(self.style.SUCCESS('Vous pouvez maintenant accéder au dashboard avec des données de test.'))
