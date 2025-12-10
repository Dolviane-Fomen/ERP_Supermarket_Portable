from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction


class Command(BaseCommand):
    help = 'Corriger les mots de passe des comptes de test'

    def handle(self, *args, **options):
        self.stdout.write('🔐 CORRECTION DES MOTS DE PASSE')
        self.stdout.write('='*40)
        
        # Mots de passe à définir
        passwords = {
            'admin': 'admin',
            'caissier_1': 'caissier123',
            'caissier_2': 'caissier123',
            'vendeur_1': 'vendeur123',
            'vendeur_2': 'vendeur123',
        }
        
        with transaction.atomic():
            for username, password in passwords.items():
                try:
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    self.stdout.write(f'✅ Mot de passe mis à jour pour: {username}')
                except User.DoesNotExist:
                    self.stdout.write(f'❌ Utilisateur non trouvé: {username}')
        
        self.stdout.write('\n' + '='*40)
        self.stdout.write('🏁 CORRECTION TERMINÉE')
        self.stdout.write('\n📋 COMPTES DISPONIBLES:')
        self.stdout.write('   admin / admin')
        self.stdout.write('   caissier_1 / caissier123')
        self.stdout.write('   caissier_2 / caissier123')
        self.stdout.write('   vendeur_1 / vendeur123')
        self.stdout.write('   vendeur_2 / vendeur123')


