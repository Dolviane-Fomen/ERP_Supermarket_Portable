from django.core.management.base import BaseCommand
from supermarket.models import Agence, Caisse, Compte, User
from decimal import Decimal

class Command(BaseCommand):
    help = 'Corriger la configuration de la caisse'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Vérification et correction de la configuration de la caisse...'))
        
        # Vérifier l'agence
        agence = Agence.objects.first()
        if not agence:
            self.stdout.write(self.style.ERROR('Aucune agence trouvée!'))
            return
        
        self.stdout.write(f'Agence trouvée: {agence.nom_agence}')
        
        # Vérifier la caisse
        caisse = Caisse.objects.filter(agence=agence).first()
        if not caisse:
            self.stdout.write(self.style.WARNING('Aucune caisse trouvée pour cette agence. Création...'))
            
            # Créer une caisse
            caisse = Caisse.objects.create(
                numero_caisse='CAISSE001',
                nom_caisse='Caisse Principale',
                agence=agence,
                solde_initial=Decimal('100000.00'),
                solde_actuel=Decimal('100000.00')
            )
            self.stdout.write(self.style.SUCCESS(f'Caisse créée: {caisse.numero_caisse}'))
        else:
            self.stdout.write(f'Caisse existante: {caisse.numero_caisse}')
        
        # Vérifier l'utilisateur
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin',
                'last_name': 'System',
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Utilisateur admin créé'))
        else:
            self.stdout.write('Utilisateur admin existe déjà')
        
        # Vérifier le compte
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
            self.stdout.write('Compte employé existe déjà')
        
        self.stdout.write(self.style.SUCCESS('✅ Configuration de la caisse corrigée!'))
        self.stdout.write(f'Agence: {agence.nom_agence}')
        self.stdout.write(f'Caisse: {caisse.numero_caisse} (Solde: {caisse.solde_actuel} FCFA)')
        self.stdout.write(f'Utilisateur: {user.username}')




