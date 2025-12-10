from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from supermarket.models import Compte, Agence, Caisse


class Command(BaseCommand):
    help = 'Vérifier que le système de connexion fonctionne correctement'

    def handle(self, *args, **options):
        self.stdout.write('🔍 VÉRIFICATION DU SYSTÈME DE CONNEXION')
        self.stdout.write('='*50)
        
        # Test des comptes
        test_accounts = [
            {'username': 'admin', 'password': 'admin', 'expected_agence': 'Super Market Principal'},
            {'username': 'caissier_1', 'password': 'caissier123', 'expected_agence': 'Super Market Principal'},
            {'username': 'caissier_2', 'password': 'caissier123', 'expected_agence': 'Agence Principale'},
            {'username': 'vendeur_1', 'password': 'vendeur123', 'expected_agence': 'Super Market Principal'},
            {'username': 'vendeur_2', 'password': 'vendeur123', 'expected_agence': 'Agence Principale'},
        ]
        
        all_good = True
        
        for account in test_accounts:
            self.stdout.write(f'\n🧪 Test: {account["username"]}')
            self.stdout.write('-' * 30)
            
            # Test d'authentification
            user = authenticate(username=account['username'], password=account['password'])
            if not user:
                self.stdout.write(f'❌ Échec de l\'authentification')
                all_good = False
                continue
            
            # Test du compte
            try:
                compte = Compte.objects.get(user=user, actif=True)
                if compte.agence.nom_agence != account['expected_agence']:
                    self.stdout.write(f'⚠️  Agence incorrecte: {compte.agence.nom_agence} (attendu: {account["expected_agence"]})')
                else:
                    self.stdout.write(f'✅ Agence correcte: {compte.agence.nom_agence}')
                
                # Vérifier qu'il y a des caisses pour cette agence
                caisses = Caisse.objects.filter(agence=compte.agence)
                if caisses.exists():
                    self.stdout.write(f'✅ {caisses.count()} caisse(s) disponible(s) pour cette agence')
                else:
                    self.stdout.write(f'❌ Aucune caisse disponible pour cette agence')
                    all_good = False
                
            except Compte.DoesNotExist:
                self.stdout.write(f'❌ Compte non trouvé ou inactif')
                all_good = False
        
        # Résumé final
        self.stdout.write('\n' + '='*50)
        if all_good:
            self.stdout.write('🎉 SYSTÈME DE CONNEXION FONCTIONNEL!')
            self.stdout.write('✅ Tous les comptes de test sont opérationnels')
            self.stdout.write('✅ Les agences sont correctement liées')
            self.stdout.write('✅ Les caisses sont disponibles')
            self.stdout.write('\n📋 Vous pouvez maintenant vous connecter avec:')
            for account in test_accounts:
                self.stdout.write(f'   {account["username"]} / {account["password"]} → {account["expected_agence"]}')
        else:
            self.stdout.write('❌ PROBLÈMES DÉTECTÉS!')
            self.stdout.write('Vérifiez les erreurs ci-dessus et corrigez-les.')
        
        self.stdout.write('='*50)










