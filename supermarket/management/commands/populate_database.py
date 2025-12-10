from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from supermarket.models import (
    Agence, Compte, Employe, Client, Fournisseur, Article, Caisse, 
    SessionCaisse, FactureVente, LigneFactureVente, Famille
)

class Command(BaseCommand):
    help = 'Remplir la base de données avec des données de test'

    def handle(self, *args, **options):
        self.stdout.write('Début du remplissage de la base de données...')
        
        # Créer une agence
        agence, created = Agence.objects.get_or_create(
            nom_agence="Super Market Principal",
            defaults={
                'adresse': '123 Avenue de la Paix, Yaoundé',
            }
        )
        if created:
            self.stdout.write(f'Agence créée: {agence.nom_agence}')
        
        # Créer un utilisateur admin
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@supermarket.com',
                'first_name': 'Admin',
                'last_name': 'Super Market',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('Utilisateur admin créé')
        
        # Créer un compte pour l'admin
        compte, created = Compte.objects.get_or_create(
            user=user,
            defaults={
                'nom': 'Admin',
                'prenom': 'Super Market',
                'email': 'admin@supermarket.com',
                'telephone': '0123456789',
                'agence': agence,
                'actif': True,
                'numero_compte': 'ADM001',
            }
        )
        if created:
            self.stdout.write('Compte admin créé')
        
        # Créer un employé
        employe, created = Employe.objects.get_or_create(
            compte=compte,
            defaults={
                'poste': 'Gérant',
                'date_embauche': timezone.now().date(),
                'salaire': 500000,
                'agence': agence,
            }
        )
        if created:
            self.stdout.write('Employé créé')
        
        # Créer des clients
        clients_data = [
            {'numero_compte_tiers': 'CLI001', 'intitule': 'Client Particulier', 'telephone': '0123456789'},
            {'numero_compte_tiers': 'CLI002', 'intitule': 'Restaurant Le Bon Goût', 'telephone': '0234567890'},
            {'numero_compte_tiers': 'CLI003', 'intitule': 'Épicerie du Quartier', 'telephone': '0345678901'},
        ]
        
        for client_data in clients_data:
            client, created = Client.objects.get_or_create(
                numero_compte_tiers=client_data['numero_compte_tiers'],
                defaults={
                    'intitule': client_data['intitule'],
                    'telephone': client_data['telephone'],
                    'adresse': 'Adresse client',
                    'agence': agence,
                }
            )
            if created:
                self.stdout.write(f'Client créé: {client.intitule}')
        
        # Créer des fournisseurs
        fournisseurs_data = [
            {'numero_compte_tiers': 'FOUR001', 'intitule': 'Distributeur Central', 'telephone': '0456789012'},
            {'numero_compte_tiers': 'FOUR002', 'intitule': 'Import Export SA', 'telephone': '0567890123'},
        ]
        
        for fournisseur_data in fournisseurs_data:
            fournisseur, created = Fournisseur.objects.get_or_create(
                numero_compte_tiers=fournisseur_data['numero_compte_tiers'],
                defaults={
                    'intitule': fournisseur_data['intitule'],
                    'telephone': fournisseur_data['telephone'],
                    'adresse': 'Adresse fournisseur',
                    'agence': agence,
                }
            )
            if created:
                self.stdout.write(f'Fournisseur créé: {fournisseur.intitule}')
        
        # Créer des familles d'articles
        familles_data = [
            {'intitule': 'Boissons', 'unite_vente': 'Bouteille', 'suivi_stock': True, 'code': 'BOI'},
            {'intitule': 'Alimentaire', 'unite_vente': 'Unité', 'suivi_stock': True, 'code': 'ALI'},
            {'intitule': 'Hygiène', 'unite_vente': 'Unité', 'suivi_stock': True, 'code': 'HYG'},
        ]
        
        for famille_data in familles_data:
            famille, created = Famille.objects.get_or_create(
                code=famille_data['code'],
                defaults=famille_data
            )
            if created:
                self.stdout.write(f'Famille créée: {famille.intitule}')
        
        # Créer des articles
        articles_data = [
            {
                'reference_article': 'ART001', 'designation': 'Coca Cola 33cl', 
                'prix_achat': 400, 'prix_vente': 500, 'stock_actuel': 100,
                'famille': 'BOI'
            },
            {
                'reference_article': 'ART002', 'designation': 'Pain de mie', 
                'prix_achat': 800, 'prix_vente': 1000, 'stock_actuel': 50,
                'famille': 'ALI'
            },
            {
                'reference_article': 'ART003', 'designation': 'Savon de Marseille', 
                'prix_achat': 300, 'prix_vente': 400, 'stock_actuel': 75,
                'famille': 'HYG'
            },
            {
                'reference_article': 'ART004', 'designation': 'Riz 5kg', 
                'prix_achat': 2500, 'prix_vente': 3000, 'stock_actuel': 30,
                'famille': 'ALI'
            },
            {
                'reference_article': 'ART005', 'designation': 'Eau minérale 1.5L', 
                'prix_achat': 200, 'prix_vente': 300, 'stock_actuel': 200,
                'famille': 'BOI'
            },
        ]
        
        for article_data in articles_data:
            famille = Famille.objects.get(code=article_data.pop('famille'))
            article, created = Article.objects.get_or_create(
                reference_article=article_data['reference_article'],
                defaults={
                    **article_data,
                    'categorie': famille,
                    'agence': agence,
                    'suivi_stock': True,
                    'conditionnement': 'Unité',
                    'unite_vente': 'Unité',
                    'type_vente': 'detail',
                    'dernier_prix_achat': article_data['prix_achat'],
                }
            )
            if created:
                self.stdout.write(f'Article créé: {article.designation}')
        
        # Créer une caisse
        caisse, created = Caisse.objects.get_or_create(
            numero_caisse="CAISSE001",
            defaults={
                'nom_caisse': 'Caisse Principale',
                'solde_actuel': 100000,
                'agence': agence,
            }
        )
        if created:
            self.stdout.write(f'Caisse créée: {caisse.nom_caisse}')
        
        # Créer une session de caisse ouverte
        session, created = SessionCaisse.objects.get_or_create(
            caisse=caisse,
            statut='ouverte',
            defaults={
                'utilisateur': user,
                'employe': employe,
                'agence': agence,
                'solde_ouverture': 100000,
                'date_ouverture': timezone.now(),
            }
        )
        if created:
            self.stdout.write(f'Session de caisse créée')
        
        # Créer quelques factures de test
        client = Client.objects.first()
        articles = Article.objects.all()[:3]
        
        for i in range(3):
            facture, created = FactureVente.objects.get_or_create(
                numero_ticket=f"TICKET{str(i+1).zfill(3)}",
                defaults={
                    'nom_vendeuse': f"{employe.compte.nom} {employe.compte.prenom}",
                    'nette_a_payer': 1000 * (i + 1),
                    'montant_regler': 1000 * (i + 1),
                    'rendu': 0,
                    'date': timezone.now().date(),
                    'heure': timezone.now().time(),
                    'type_vente': 'detail',
                    'client': client,
                    'caisse': caisse,
                    'agence': agence,
                    'vendeur': employe,
                }
            )
            
            if created:
                # Ajouter des lignes de facture
                for j, article in enumerate(articles):
                    LigneFactureVente.objects.create(
                        facture_vente=facture,
                        article=article,
                        designation=article.designation,
                        quantite=j + 1,
                        prix_unitaire=article.prix_vente,
                        prix_total=article.prix_vente * (j + 1),
                    )
                self.stdout.write(f'Facture créée: {facture.numero_ticket}')
        
        self.stdout.write(
            self.style.SUCCESS('Base de données remplie avec succès !')
        )
        self.stdout.write('Données créées:')
        self.stdout.write(f'- 1 Agence: {agence.nom_agence}')
        self.stdout.write(f'- 1 Utilisateur: admin (mot de passe: admin123)')
        self.stdout.write(f'- 1 Employé: {employe.compte.nom} {employe.compte.prenom}')
        self.stdout.write(f'- {Client.objects.count()} Clients')
        self.stdout.write(f'- {Fournisseur.objects.count()} Fournisseurs')
        self.stdout.write(f'- {Article.objects.count()} Articles')
        self.stdout.write(f'- 1 Caisse: {caisse.nom_caisse}')
        self.stdout.write(f'- 1 Session de caisse ouverte')
        self.stdout.write(f'- {FactureVente.objects.count()} Factures de test')

