from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from supermarket.models import Agence, Compte, Employe, Famille, Article, Client, Caisse
from decimal import Decimal


class Command(BaseCommand):
    help = 'Créer les comptes de test et les données nécessaires pour le système de caisse'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Supprimer et recréer toutes les données de test',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Suppression des données existantes...')
            self.reset_data()

        self.stdout.write('Création des données de test...')
        
        with transaction.atomic():
            # Créer les agences
            agences = self.create_agences()
            
            # Créer les familles d'articles
            familles = self.create_familles()
            
            # Créer les articles
            self.create_articles(agences, familles)
            
            # Créer les clients
            self.create_clients(agences)
            
            # Créer les caisses
            self.create_caisses(agences)
            
            # Créer les comptes utilisateurs
            self.create_test_accounts(agences)
            
        self.stdout.write(
            self.style.SUCCESS('✅ Données de test créées avec succès!')
        )
        self.print_test_accounts()

    def reset_data(self):
        """Supprimer toutes les données de test"""
        # Supprimer dans l'ordre inverse des dépendances
        Article.objects.all().delete()
        Famille.objects.all().delete()
        Client.objects.all().delete()
        Caisse.objects.all().delete()
        Employe.objects.all().delete()
        Compte.objects.all().delete()
        Agence.objects.all().delete()
        
        # Supprimer les utilisateurs de test
        User.objects.filter(username__startswith='test_').delete()
        User.objects.filter(username__in=[
            'admin', 'caissier_1', 'caissier_2', 'vendeur_1', 'vendeur_2'
        ]).delete()

    def create_agences(self):
        """Créer les agences de test"""
        agences_data = [
            {
                'nom_agence': 'Agence Centre',
                'adresse': '123 Avenue de la République, Centre-ville'
            },
            {
                'nom_agence': 'Agence Banlieue',
                'adresse': '456 Route de la Banlieue, Quartier Est'
            }
        ]
        
        agences = []
        for data in agences_data:
            agence, created = Agence.objects.get_or_create(
                nom_agence=data['nom_agence'],
                defaults={'adresse': data['adresse']}
            )
            agences.append(agence)
            if created:
                self.stdout.write(f'  ✅ Agence créée: {agence.nom_agence}')
            else:
                self.stdout.write(f'  ℹ️  Agence existante: {agence.nom_agence}')
        
        return agences

    def create_familles(self):
        """Créer les familles d'articles"""
        familles_data = [
            {'code': 'BOI', 'intitule': 'Boissons', 'unite_vente': 'Unité'},
            {'code': 'ALI', 'intitule': 'Alimentation', 'unite_vente': 'Unité'},
            {'code': 'HYG', 'intitule': 'Hygiène', 'unite_vente': 'Unité'},
            {'code': 'MEN', 'intitule': 'Ménage', 'unite_vente': 'Unité'},
        ]
        
        familles = []
        for data in familles_data:
            famille, created = Famille.objects.get_or_create(
                code=data['code'],
                defaults={
                    'intitule': data['intitule'],
                    'unite_vente': data['unite_vente'],
                    'suivi_stock': True
                }
            )
            familles.append(famille)
            if created:
                self.stdout.write(f'  ✅ Famille créée: {famille.intitule}')
        
        return familles

    def create_articles(self, agences, familles):
        """Créer les articles de test"""
        articles_data = [
            {'reference': 'ART001', 'designation': 'Coca Cola 33cl', 'prix_vente': 500, 'famille': 'BOI'},
            {'reference': 'ART002', 'designation': 'Pain de mie', 'prix_vente': 1000, 'famille': 'ALI'},
            {'reference': 'ART003', 'designation': 'Savon de Marseille', 'prix_vente': 400, 'famille': 'HYG'},
            {'reference': 'ART004', 'designation': 'Riz 5kg', 'prix_vente': 3000, 'famille': 'ALI'},
            {'reference': 'ART005', 'designation': 'Eau minérale 1.5L', 'prix_vente': 300, 'famille': 'BOI'},
            {'reference': 'ART006', 'designation': 'Détergent liquide', 'prix_vente': 800, 'famille': 'MEN'},
            {'reference': 'ART007', 'designation': 'Pommes', 'prix_vente': 1200, 'famille': 'ALI'},
            {'reference': 'ART008', 'designation': 'Jus d\'orange 1L', 'prix_vente': 600, 'famille': 'BOI'},
        ]
        
        famille_map = {f.code: f for f in familles}
        
        for agence in agences:
            for data in articles_data:
                article, created = Article.objects.get_or_create(
                    reference_article=data['reference'],
                    agence=agence,
                    defaults={
                        'designation': data['designation'],
                        'categorie': famille_map[data['famille']],
                        'prix_vente': Decimal(data['prix_vente']),
                        'prix_achat': Decimal(data['prix_vente'] * 0.7),  # Prix d'achat = 70% du prix de vente
                        'dernier_prix_achat': Decimal(data['prix_vente'] * 0.7),
                        'stock_actuel': 100,
                        'stock_minimum': 10,
                        'conditionnement': 'Unité',
                        'unite_vente': 'Unité',
                        'suivi_stock': True
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Article créé: {article.designation} ({agence.nom_agence})')

    def create_clients(self, agences):
        """Créer les clients de test"""
        clients_data = [
            {'intitule': 'Client Général', 'adresse': 'Adresse générale', 'telephone': '0000000000'},
            {'intitule': 'Marie Dupont', 'adresse': '123 Rue des Lilas', 'telephone': '0123456789'},
            {'intitule': 'Jean Martin', 'adresse': '456 Avenue des Roses', 'telephone': '0987654321'},
        ]
        
        for agence in agences:
            for data in clients_data:
                client, created = Client.objects.get_or_create(
                    intitule=data['intitule'],
                    agence=agence,
                    defaults={
                        'adresse': data['adresse'],
                        'telephone': data['telephone'],
                        'email': ''
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Client créé: {client.intitule} ({agence.nom_agence})')

    def create_caisses(self, agences):
        """Créer les caisses de test"""
        for i, agence in enumerate(agences, 1):
            caisse, created = Caisse.objects.get_or_create(
                numero_caisse=f'CAISSE00{i}',
                agence=agence,
                defaults={
                    'nom_caisse': f'Caisse Principale {agence.nom_agence}',
                    'solde_initial': Decimal('10000.00'),
                    'solde_actuel': Decimal('10000.00'),
                    'statut': 'fermee'
                }
            )
            if created:
                self.stdout.write(f'  ✅ Caisse créée: {caisse.nom_caisse}')

    def create_test_accounts(self, agences):
        """Créer les comptes utilisateurs de test"""
        accounts_data = [
            # Admin principal
            {
                'username': 'admin',
                'password': 'admin',
                'email': 'admin@supermarket.com',
                'first_name': 'Admin',
                'last_name': 'Principal',
                'type_compte': 'admin',
                'agence': agences[0]  # Première agence
            },
            # Caissiers
            {
                'username': 'caissier_1',
                'password': 'caissier123',
                'email': 'caissier1@supermarket.com',
                'first_name': 'Pierre',
                'last_name': 'Caissier',
                'type_compte': 'caissier',
                'agence': agences[0],
                'numero_employe': 'EMP001',
                'poste': 'Caissier',
                'departement': 'caisse'
            },
            {
                'username': 'caissier_2',
                'password': 'caissier123',
                'email': 'caissier2@supermarket.com',
                'first_name': 'Sophie',
                'last_name': 'Caissier',
                'type_compte': 'caissier',
                'agence': agences[1],
                'numero_employe': 'EMP002',
                'poste': 'Caissier',
                'departement': 'caisse'
            },
            # Vendeurs
            {
                'username': 'vendeur_1',
                'password': 'vendeur123',
                'email': 'vendeur1@supermarket.com',
                'first_name': 'Marc',
                'last_name': 'Vendeur',
                'type_compte': 'vendeur',
                'agence': agences[0],
                'numero_employe': 'EMP003',
                'poste': 'Vendeur',
                'departement': 'vente'
            },
            {
                'username': 'vendeur_2',
                'password': 'vendeur123',
                'email': 'vendeur2@supermarket.com',
                'first_name': 'Julie',
                'last_name': 'Vendeur',
                'type_compte': 'vendeur',
                'agence': agences[1],
                'numero_employe': 'EMP004',
                'poste': 'Vendeur',
                'departement': 'vente'
            }
        ]
        
        for data in accounts_data:
            # Créer l'utilisateur Django
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'is_active': True,
                    'is_staff': data['type_compte'] == 'admin'
                }
            )
            
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(f'  ✅ Utilisateur créé: {user.username}')
            else:
                self.stdout.write(f'  ℹ️  Utilisateur existant: {user.username}')
            
            # Créer le compte
            compte, created = Compte.objects.get_or_create(
                user=user,
                defaults={
                    'numero_compte': f'COMPTE_{data["username"].upper()}',
                    'type_compte': data['type_compte'],
                    'nom': data['last_name'],
                    'prenom': data['first_name'],
                    'telephone': '0000000000',
                    'email': data['email'],
                    'agence': data['agence'],
                    'actif': True
                }
            )
            
            if created:
                self.stdout.write(f'  ✅ Compte créé: {compte.nom_complet} ({data["agence"].nom_agence})')
            
            # Créer l'employé si nécessaire
            if 'numero_employe' in data:
                employe, created = Employe.objects.get_or_create(
                    compte=compte,
                    defaults={
                        'numero_employe': data['numero_employe'],
                        'poste': data['poste'],
                        'departement': data['departement'],
                        'date_embauche': '2024-01-01'
                    }
                )
                if created:
                    self.stdout.write(f'  ✅ Employé créé: {employe}')

    def print_test_accounts(self):
        """Afficher les comptes de test créés"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write('📋 COMPTES DE TEST CRÉÉS')
        self.stdout.write('='*60)
        
        comptes = Compte.objects.select_related('user', 'agence').all()
        for compte in comptes:
            self.stdout.write(f'👤 {compte.user.username}')
            self.stdout.write(f'   Nom: {compte.nom_complet}')
            self.stdout.write(f'   Type: {compte.get_type_compte_display()}')
            self.stdout.write(f'   Agence: {compte.agence.nom_agence}')
            self.stdout.write(f'   Actif: {"✅" if compte.actif else "❌"}')
            self.stdout.write('')
        
        self.stdout.write('🔑 INFORMATIONS DE CONNEXION:')
        self.stdout.write('   Admin Principal: admin / admin')
        self.stdout.write('   Caissier Agence 1: caissier_1 / caissier123')
        self.stdout.write('   Caissier Agence 2: caissier_2 / caissier123')
        self.stdout.write('   Vendeur Agence 1: vendeur_1 / vendeur123')
        self.stdout.write('   Vendeur Agence 2: vendeur_2 / vendeur123')
        self.stdout.write('='*60)


