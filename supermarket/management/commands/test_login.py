from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from supermarket.models import Compte


class Command(BaseCommand):
    help = 'Tester la connexion des comptes de test'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nom d\'utilisateur à tester',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Mot de passe à tester',
        )

    def handle(self, *args, **options):
        self.stdout.write('🔐 TEST DE CONNEXION')
        self.stdout.write('='*40)
        
        # Comptes de test à vérifier
        test_accounts = [
            {'username': 'admin', 'password': 'admin'},
            {'username': 'caissier_1', 'password': 'caissier123'},
            {'username': 'caissier_2', 'password': 'caissier123'},
            {'username': 'vendeur_1', 'password': 'vendeur123'},
            {'username': 'vendeur_2', 'password': 'vendeur123'},
        ]
        
        # Si un utilisateur spécifique est demandé
        if options['username'] and options['password']:
            test_accounts = [
                {'username': options['username'], 'password': options['password']}
            ]
        
        for account in test_accounts:
            self.test_account(account['username'], account['password'])
        
        self.stdout.write('\n' + '='*40)
        self.stdout.write('🏁 TEST TERMINÉ')

    def test_account(self, username, password):
        """Tester un compte spécifique"""
        self.stdout.write(f'\n🧪 Test du compte: {username}')
        self.stdout.write('-' * 30)
        
        # Étape 1: Vérifier si l'utilisateur Django existe
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f'✅ Utilisateur Django trouvé: {user.get_full_name()}')
            self.stdout.write(f'   Actif: {"✅" if user.is_active else "❌"}')
            self.stdout.write(f'   Staff: {"✅" if user.is_staff else "❌"}')
        except User.DoesNotExist:
            self.stdout.write(f'❌ Utilisateur Django non trouvé: {username}')
            return
        
        # Étape 2: Tester l'authentification Django
        user_auth = authenticate(username=username, password=password)
        if user_auth:
            self.stdout.write(f'✅ Authentification Django réussie')
        else:
            self.stdout.write(f'❌ Échec de l\'authentification Django')
            self.stdout.write('   Vérifiez le mot de passe ou l\'état du compte')
            return
        
        # Étape 3: Vérifier le compte dans notre système
        try:
            compte = Compte.objects.get(user=user)
            self.stdout.write(f'✅ Compte trouvé: {compte.nom_complet}')
            self.stdout.write(f'   Type: {compte.get_type_compte_display()}')
            self.stdout.write(f'   Numéro: {compte.numero_compte}')
            self.stdout.write(f'   Actif: {"✅" if compte.actif else "❌"}')
            
            if compte.actif:
                self.stdout.write(f'✅ Compte actif - Connexion possible')
            else:
                self.stdout.write(f'❌ Compte inactif - Connexion impossible')
                return
                
        except Compte.DoesNotExist:
            self.stdout.write(f'❌ Compte non trouvé pour l\'utilisateur {username}')
            self.stdout.write('   Créez un compte lié à cet utilisateur')
            return
        
        # Étape 4: Vérifier l'agence
        if compte.agence:
            self.stdout.write(f'✅ Agence associée: {compte.agence.nom_agence}')
            self.stdout.write(f'   ID Agence: {compte.agence.id_agence}')
            self.stdout.write(f'✅ Connexion à la caisse possible')
        else:
            self.stdout.write(f'❌ Aucune agence associée - Connexion impossible')
            self.stdout.write('   Associez une agence à ce compte')
            return
        
        # Étape 5: Vérifier l'employé si applicable
        try:
            employe = compte.employe
            self.stdout.write(f'✅ Employé associé: {employe.numero_employe}')
            self.stdout.write(f'   Poste: {employe.poste}')
            self.stdout.write(f'   Département: {employe.get_departement_display()}')
        except:
            if compte.type_compte == 'admin':
                self.stdout.write(f'ℹ️  Pas d\'employé associé (normal pour admin)')
            else:
                self.stdout.write(f'⚠️  Aucun employé associé pour {compte.get_type_compte_display()}')
        
        # Résumé
        self.stdout.write(f'🎯 RÉSULTAT: {"✅ CONNEXION POSSIBLE" if compte.actif and compte.agence else "❌ CONNEXION IMPOSSIBLE"}')


