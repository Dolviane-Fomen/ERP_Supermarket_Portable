from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from supermarket.models import (
    Agence, Compte, Employe, Client, Fournisseur, Famille, Article,
    Caisse, SessionCaisse, FactureVente, LigneFactureVente
)

class Command(BaseCommand):
    help = 'Vérifier les données existantes dans la base'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Vérification des données existantes...'))

        # Vérifier les agences
        agences = Agence.objects.all()
        self.stdout.write(f'📊 Agences: {agences.count()}')
        for agence in agences:
            self.stdout.write(f'  - {agence.nom_agence}')

        # Vérifier les utilisateurs
        users = User.objects.all()
        self.stdout.write(f'👥 Utilisateurs: {users.count()}')
        for user in users:
            self.stdout.write(f'  - {user.username} ({user.email})')

        # Vérifier les comptes
        comptes = Compte.objects.all()
        self.stdout.write(f'💼 Comptes: {comptes.count()}')
        for compte in comptes:
            self.stdout.write(f'  - {compte.nom} {compte.prenom} ({compte.numero_compte})')

        # Vérifier les employés
        employes = Employe.objects.all()
        self.stdout.write(f'👨‍💼 Employés: {employes.count()}')
        for employe in employes:
            self.stdout.write(f'  - {employe.compte.nom} ({employe.poste})')

        # Vérifier les clients
        clients = Client.objects.all()
        self.stdout.write(f'🛒 Clients: {clients.count()}')
        for client in clients:
            self.stdout.write(f'  - {client.intitule} ({client.numero_compte_tiers})')

        # Vérifier les fournisseurs
        fournisseurs = Fournisseur.objects.all()
        self.stdout.write(f'🚚 Fournisseurs: {fournisseurs.count()}')
        for fournisseur in fournisseurs:
            self.stdout.write(f'  - {fournisseur.intitule} ({fournisseur.numero_compte_tiers})')

        # Vérifier les familles
        familles = Famille.objects.all()
        self.stdout.write(f'📦 Familles: {familles.count()}')
        for famille in familles:
            self.stdout.write(f'  - {famille.intitule} ({famille.code})')

        # Vérifier les articles
        articles = Article.objects.all()
        self.stdout.write(f'🛍️ Articles: {articles.count()}')
        for article in articles:
            self.stdout.write(f'  - {article.designation} ({article.reference_article})')

        # Vérifier les caisses
        caisses = Caisse.objects.all()
        self.stdout.write(f'💰 Caisses: {caisses.count()}')
        for caisse in caisses:
            self.stdout.write(f'  - {caisse.nom_caisse} (Solde: {caisse.solde_actuel} FCFA)')

        # Vérifier les sessions
        sessions = SessionCaisse.objects.all()
        self.stdout.write(f'🕐 Sessions: {sessions.count()}')
        for session in sessions:
            self.stdout.write(f'  - {session.caisse.nom_caisse} - {session.statut} ({session.date_ouverture})')

        # Vérifier les factures
        factures = FactureVente.objects.all()
        self.stdout.write(f'🧾 Factures: {factures.count()}')
        for facture in factures:
            self.stdout.write(f'  - {facture.numero_ticket} - {facture.nette_a_payer} FCFA ({facture.date})')

        self.stdout.write(self.style.SUCCESS('\n✅ Vérification terminée!'))
        self.stdout.write(self.style.SUCCESS('🔗 Interface d\'administration: http://127.0.0.1:8000/admin/'))
        self.stdout.write(self.style.SUCCESS('👤 Identifiants: admin / admin123'))









