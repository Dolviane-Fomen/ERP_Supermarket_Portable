from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from supermarket.models import Agence, Compte, Employe, Caisse


class Command(BaseCommand):
    help = 'Vérifier l\'état des comptes et données dans la base'

    def handle(self, *args, **options):
        self.stdout.write('🔍 DIAGNOSTIC DE LA BASE DE DONNÉES')
        self.stdout.write('='*50)
        
        # Vérifier les agences
        self.check_agences()
        
        # Vérifier les utilisateurs
        self.check_users()
        
        # Vérifier les comptes
        self.check_comptes()
        
        # Vérifier les employés
        self.check_employes()
        
        # Vérifier les caisses
        self.check_caisses()
        
        # Vérifier les liens
        self.check_links()

    def check_agences(self):
        """Vérifier les agences"""
        self.stdout.write('\n📁 AGGENCES:')
        agences = Agence.objects.all()
        if agences.exists():
            for agence in agences:
                self.stdout.write(f'  ✅ {agence.nom_agence} (ID: {agence.id_agence})')
        else:
            self.stdout.write('  ❌ Aucune agence trouvée!')
        self.stdout.write(f'  Total: {agences.count()} agences')

    def check_users(self):
        """Vérifier les utilisateurs Django"""
        self.stdout.write('\n👥 UTILISATEURS DJANGO:')
        users = User.objects.all()
        if users.exists():
            for user in users:
                status = '✅' if user.is_active else '❌'
                self.stdout.write(f'  {status} {user.username} - {user.get_full_name()} (Actif: {user.is_active})')
        else:
            self.stdout.write('  ❌ Aucun utilisateur trouvé!')
        self.stdout.write(f'  Total: {users.count()} utilisateurs')

    def check_comptes(self):
        """Vérifier les comptes"""
        self.stdout.write('\n👤 COMPTES:')
        comptes = Compte.objects.select_related('user', 'agence').all()
        if comptes.exists():
            for compte in comptes:
                status = '✅' if compte.actif else '❌'
                agence_info = compte.agence.nom_agence if compte.agence else 'AUCUNE AGENCE'
                self.stdout.write(f'  {status} {compte.user.username} - {compte.nom_complet}')
                self.stdout.write(f'      Type: {compte.get_type_compte_display()}')
                self.stdout.write(f'      Agence: {agence_info}')
                self.stdout.write(f'      Actif: {compte.actif}')
        else:
            self.stdout.write('  ❌ Aucun compte trouvé!')
        self.stdout.write(f'  Total: {comptes.count()} comptes')

    def check_employes(self):
        """Vérifier les employés"""
        self.stdout.write('\n💼 EMPLOYÉS:')
        employes = Employe.objects.select_related('compte__user', 'compte__agence').all()
        if employes.exists():
            for employe in employes:
                self.stdout.write(f'  ✅ {employe.numero_employe} - {employe.compte.nom_complet}')
                self.stdout.write(f'      Poste: {employe.poste}')
                self.stdout.write(f'      Département: {employe.get_departement_display()}')
                self.stdout.write(f'      Agence: {employe.compte.agence.nom_agence if employe.compte.agence else "AUCUNE"}')
        else:
            self.stdout.write('  ❌ Aucun employé trouvé!')
        self.stdout.write(f'  Total: {employes.count()} employés')

    def check_caisses(self):
        """Vérifier les caisses"""
        self.stdout.write('\n💰 CAISSES:')
        caisses = Caisse.objects.select_related('agence').all()
        if caisses.exists():
            for caisse in caisses:
                status_icon = '🟢' if caisse.statut == 'ouverte' else '🔴'
                self.stdout.write(f'  {status_icon} {caisse.numero_caisse} - {caisse.nom_caisse}')
                self.stdout.write(f'      Agence: {caisse.agence.nom_agence}')
                self.stdout.write(f'      Statut: {caisse.get_statut_display()}')
                self.stdout.write(f'      Solde: {caisse.solde_actuel} FCFA')
        else:
            self.stdout.write('  ❌ Aucune caisse trouvée!')
        self.stdout.write(f'  Total: {caisses.count()} caisses')

    def check_links(self):
        """Vérifier les liens entre les entités"""
        self.stdout.write('\n🔗 VÉRIFICATION DES LIENS:')
        
        # Vérifier les comptes sans agence
        comptes_sans_agence = Compte.objects.filter(agence__isnull=True)
        if comptes_sans_agence.exists():
            self.stdout.write('  ⚠️  Comptes sans agence:')
            for compte in comptes_sans_agence:
                self.stdout.write(f'      - {compte.user.username}')
        else:
            self.stdout.write('  ✅ Tous les comptes ont une agence')
        
        # Vérifier les utilisateurs sans compte
        users_sans_compte = User.objects.filter(compte__isnull=True)
        if users_sans_compte.exists():
            self.stdout.write('  ⚠️  Utilisateurs sans compte:')
            for user in users_sans_compte:
                self.stdout.write(f'      - {user.username}')
        else:
            self.stdout.write('  ✅ Tous les utilisateurs ont un compte')
        
        # Vérifier les comptes sans employé
        comptes_sans_employe = Compte.objects.filter(employe__isnull=True)
        if comptes_sans_employe.exists():
            self.stdout.write('  ⚠️  Comptes sans employé (normal pour admin):')
            for compte in comptes_sans_employe:
                if compte.type_compte != 'admin':
                    self.stdout.write(f'      - {compte.user.username} ({compte.get_type_compte_display()})')
        
        # Vérifier les caisses sans agence
        caisses_sans_agence = Caisse.objects.filter(agence__isnull=True)
        if caisses_sans_agence.exists():
            self.stdout.write('  ⚠️  Caisses sans agence:')
            for caisse in caisses_sans_agence:
                self.stdout.write(f'      - {caisse.numero_caisse}')
        else:
            self.stdout.write('  ✅ Toutes les caisses ont une agence')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('🏁 DIAGNOSTIC TERMINÉ')


