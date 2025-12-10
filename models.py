from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class Agence(models.Model):
    """Modèle pour les agences"""
    id_agence = models.AutoField(primary_key=True, verbose_name="ID Agence")
    nom_agence = models.CharField(max_length=100, verbose_name="Nom agence")
    adresse = models.TextField(verbose_name="Adresse")
    
    class Meta:
        verbose_name = "Agence"
        verbose_name_plural = "Agences"
        ordering = ['nom_agence']
    
    def __str__(self):
        return self.nom_agence

class Famille(models.Model):
    """Modèle pour les familles d'articles"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    intitule = models.CharField(max_length=100, verbose_name="Intitulé")
    unite_vente = models.CharField(max_length=20, verbose_name="Unité de vente")
    suivi_stock = models.BooleanField(default=True, verbose_name="Suivi de stock")
    
    class Meta:
        verbose_name = "Famille"
        verbose_name_plural = "Familles"
        ordering = ['intitule']
    
    def __str__(self):
        return f"{self.code} - {self.intitule}"

class Compte(models.Model):
    """Modèle pour les comptes utilisateurs"""
    # Liaison avec le système d'authentification Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur Django")
    
    # Informations du compte
    numero_compte = models.CharField(max_length=20, unique=True, verbose_name="Numéro de compte")
    type_compte = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrateur'),
            ('gerant', 'Gérant'),
            ('caissier', 'Caissier'),
            ('vendeur', 'Vendeur'),
            ('magasinier', 'Magasinier'),
            ('comptable', 'Comptable'),
        ],
        default='vendeur',
        verbose_name="Type de compte"
    )
    
    # Informations personnelles
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="E-mail")
    
    # Statut et permissions
    actif = models.BooleanField(default=True, verbose_name="Compte actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_derniere_connexion = models.DateTimeField(blank=True, null=True, verbose_name="Dernière connexion")
    
    # Liaison avec l'agence
    agence = models.ForeignKey('Agence', on_delete=models.CASCADE, verbose_name="Agence")
    
    class Meta:
        verbose_name = "Compte"
        verbose_name_plural = "Comptes"
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.numero_compte})"
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

class Employe(models.Model):
    """Modèle pour les employés"""
    # Liaison avec le compte
    compte = models.OneToOneField(Compte, on_delete=models.CASCADE, verbose_name="Compte")
    
    # Informations professionnelles
    numero_employe = models.CharField(max_length=20, unique=True, verbose_name="Numéro employé")
    poste = models.CharField(max_length=100, verbose_name="Poste")
    departement = models.CharField(
        max_length=50,
        choices=[
            ('vente', 'Vente'),
            ('caisse', 'Caisse'),
            ('stock', 'Stock'),
            ('comptabilite', 'Comptabilité'),
            ('administration', 'Administration'),
            ('direction', 'Direction'),
        ],
        default='vente',
        verbose_name="Département"
    )
    
    # Statut
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    # salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Salaire")
    
    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['compte__nom', 'compte__prenom']
    
    def __str__(self):
        return f"{self.compte.prenom} {self.compte.nom} ({self.numero_employe})"

class Client(models.Model):
    """Modèle pour les clients"""
    intitule = models.CharField(max_length=200, verbose_name="Intitulé")
    adresse = models.TextField(verbose_name="Adresse")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    
    # Relations
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['intitule']
    
    def __str__(self):
        return self.intitule

class Fournisseur(models.Model):
    """Modèle pour les fournisseurs"""
    intitule = models.CharField(max_length=200, verbose_name="Intitulé")
    adresse = models.TextField(verbose_name="Adresse")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    
    # Relations
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['intitule']
    
    def __str__(self):
        return self.intitule

class TypeVente(models.Model):
    """Modèle pour les types de vente d'un article"""
    intitule = models.CharField(max_length=100, verbose_name="Intitulé")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='types_vente', verbose_name="Article")
    
    class Meta:
        verbose_name = "Type de vente"
        verbose_name_plural = "Types de vente"
        ordering = ['intitule']
    
    def __str__(self):
        return f"{self.intitule} - {self.article.designation}"

class Article(models.Model):
    """Modèle pour les articles"""
    
    # Choix pour les unités de vente
    UNITE_VENTE_CHOICES = [
        ('Sac', 'Sac'),
        ('Bouteille', 'Bouteille'),
        ('Morceau', 'Morceau'),
        ('Bidon', 'Bidon'),
        ('Kg', 'Kg'),
        ('Litre', 'Litre'),
        ('Paquet', 'Paquet'),
        ('Unité', 'Unité'),
        ('Carton', 'Carton'),
        ('Boîte', 'Boîte'),
    ]
    
    # Choix pour les conditionnements
    CONDITIONNEMENT_CHOICES = [
        ('Sac', 'Sac'),
        ('Sac de 1kg', 'Sac de 1kg'),
        ('Sac de 5kg', 'Sac de 5kg'),
        ('Sac de 10kg', 'Sac de 10kg'),
        ('Sac de 25kg', 'Sac de 25kg'),
        ('Sac de 50kg', 'Sac de 50kg'),
        ('Bouteille', 'Bouteille'),
        ('Bouteille de 0.5L', 'Bouteille de 0.5L'),
        ('Bouteille de 1L', 'Bouteille de 1L'),
        ('Bouteille de 1.5L', 'Bouteille de 1.5L'),
        ('Bouteille de 2L', 'Bouteille de 2L'),
        ('Bouteille de 5L', 'Bouteille de 5L'),
        ('Bidon', 'Bidon'),
        ('Bidon de 5L', 'Bidon de 5L'),
        ('Bidon de 10L', 'Bidon de 10L'),
        ('Bidon de 20L', 'Bidon de 20L'),
        ('Morceau', 'Morceau'),
        ('Morceau unitaire', 'Morceau unitaire'),
        ('Morceau de 500g', 'Morceau de 500g'),
        ('Paquet', 'Paquet'),
        ('Carton', 'Carton'),
        ('Boîte', 'Boîte'),
    ]
    
    reference_article = models.CharField(max_length=50, unique=True, verbose_name="Référence article")
    designation = models.CharField(max_length=200, verbose_name="Désignation")
    categorie = models.ForeignKey(Famille, on_delete=models.CASCADE, verbose_name="Catégorie")
    suivi_stock = models.BooleanField(default=True, verbose_name="Suivi stock")
    conditionnement = models.CharField(max_length=50, choices=CONDITIONNEMENT_CHOICES, verbose_name="Conditionnement")
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix d'achat")
    dernier_prix_achat = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Dernier prix d'achat")
    unite_vente = models.CharField(max_length=20, choices=UNITE_VENTE_CHOICES, verbose_name="Unité de vente")
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix de vente")
    
    # Stock actuel
    stock_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock actuel")
    stock_minimum = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Stock minimum")
    
    # RELATION
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['designation']
    
    def __str__(self):
        return f"{self.reference_article} - {self.designation}"

class Caisse(models.Model):
    """Modèle pour la gestion des caisses"""
    numero_caisse = models.CharField(max_length=20, unique=True, verbose_name="Numéro de caisse")
    nom_caisse = models.CharField(max_length=100, verbose_name="Nom de la caisse")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    solde_initial = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Solde initial")
    solde_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Solde actuel")
    statut = models.CharField(max_length=20, choices=[
        ('ouverte', 'Ouverte'),
        ('fermee', 'Fermée'),
        ('maintenance', 'En maintenance'),
    ], default='fermee', verbose_name="Statut")
    date_ouverture = models.DateTimeField(null=True, blank=True, verbose_name="Date d'ouverture")
    date_fermeture = models.DateTimeField(null=True, blank=True, verbose_name="Date de fermeture")
    
    class Meta:
        verbose_name = "Caisse"
        verbose_name_plural = "Caisses"
        ordering = ['numero_caisse']
    
    def __str__(self):
        return f"{self.numero_caisse} - {self.nom_caisse}"

class SessionCaisse(models.Model):
    """Modèle pour les sessions de caisse"""
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE, verbose_name="Caisse")
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur", null=True, blank=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, verbose_name="Employé", null=True, blank=True)
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    solde_ouverture = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Solde d'ouverture")
    solde_fermeture = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Solde de fermeture")
    date_ouverture = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ouverture")
    date_fermeture = models.DateTimeField(null=True, blank=True, verbose_name="Date de fermeture")
    statut = models.CharField(max_length=20, choices=[
        ('ouverte', 'Ouverte'),
        ('fermee', 'Fermée'),
    ], default='ouverte', verbose_name="Statut")
    
    class Meta:
        verbose_name = "Session de caisse"
        verbose_name_plural = "Sessions de caisse"
        ordering = ['-date_ouverture']
    
    def __str__(self):
        return f"Session {self.caisse.numero_caisse} - {self.utilisateur.username}"

class FactureVente(models.Model):
    """Modèle pour les factures de vente"""
    numero_ticket = models.CharField(max_length=50, unique=True, verbose_name="Numéro de ticket")
    date = models.DateField(verbose_name="Date")
    heure = models.TimeField(verbose_name="Heure")
    nette_a_payer = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Net à payer")
    montant_regler = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Montant réglé")
    rendu = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Rendu")
    remise = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Remise")
    en_attente = models.BooleanField(default=False, verbose_name="En attente")
    nom_vendeuse = models.CharField(max_length=200, verbose_name="Nom de la vendeuse")
    
    # Relations
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    caisse = models.ForeignKey(Caisse, on_delete=models.CASCADE, verbose_name="Caisse")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    vendeur = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vendeur")
    session_caisse = models.ForeignKey('SessionCaisse', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Session de caisse")
    
    class Meta:
        verbose_name = "Facture de vente"
        verbose_name_plural = "Factures de vente"
        ordering = ['-date', '-heure']
    
    def __str__(self):
        return f"Ticket {self.numero_ticket} - {self.client.intitule}"

class LigneFactureVente(models.Model):
    """Modèle pour les lignes de facture de vente (détails des articles)"""
    facture_vente = models.ForeignKey(FactureVente, on_delete=models.CASCADE, related_name='lignes', verbose_name="Facture de vente")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    designation = models.CharField(max_length=200, verbose_name="Désignation")
    quantite = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix total")
    
    class Meta:
        verbose_name = "Ligne de facture de vente"
        verbose_name_plural = "Lignes de facture de vente"
        ordering = ['facture_vente', 'article']
    
    def __str__(self):
        return f"{self.facture_vente.numero_ticket} - {self.article.designation}"

class DocumentVente(models.Model):
    """Modèle pour les documents de vente journaliers (fermeture de caisse)"""
    numero_document = models.CharField(max_length=50, unique=True, verbose_name="Numéro de document")
    date = models.DateField(verbose_name="Date")
    heure_fermeture = models.DateTimeField(verbose_name="Heure de fermeture")
    session_caisse = models.ForeignKey('SessionCaisse', on_delete=models.CASCADE, verbose_name="Session de caisse")
    vendeuse_nom = models.CharField(max_length=200, verbose_name="Nom de la vendeuse")
    nombre_factures = models.IntegerField(default=0, verbose_name="Nombre de factures")
    total_articles = models.IntegerField(default=0, verbose_name="Total des articles")
    chiffre_affaires = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Chiffre d'affaires")
    factures_data = models.JSONField(default=dict, verbose_name="Données des factures")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    class Meta:
        verbose_name = "Document de vente"
        verbose_name_plural = "Documents de vente"
        ordering = ['-date', '-heure_fermeture']
    
    def __str__(self):
        return f"Document {self.numero_document} - {self.date}"

class FactureTemporaire(models.Model):
    """Modèle pour les factures temporaires en attente"""
    session_key = models.CharField(max_length=100, verbose_name="Clé de session")
    session_caisse = models.ForeignKey('SessionCaisse', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Session de caisse")
    contenu = models.JSONField(verbose_name="Contenu de la facture")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Facture temporaire"
        verbose_name_plural = "Factures temporaires"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Facture temporaire {self.id} - {self.date_creation}"

# ===== MODULE DE GESTION DE STOCK ET COMPTABILITÉ =====

class FactureAchat(models.Model):
    """Modèle pour les factures d'achat"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('validee', 'Validée'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée'),
    ]
    
    numero_fournisseur = models.CharField(max_length=50, verbose_name="Numéro fournisseur")
    date_achat = models.DateField(verbose_name="Date d'achat")
    heure = models.TimeField(verbose_name="Heure")
    reference_achat = models.CharField(max_length=100, unique=True, verbose_name="Référence achat")
    prix_total_global = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix total global")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon', verbose_name="Statut")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    # Relations
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, verbose_name="Fournisseur")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    employe = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Employé")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Facture d'achat"
        verbose_name_plural = "Factures d'achat"
        ordering = ['-date_achat']
    
    def __str__(self):
        return f"Facture {self.reference_achat} - {self.fournisseur.intitule}"

class LigneFactureAchat(models.Model):
    """Modèle pour les lignes de facture d'achat"""
    facture_achat = models.ForeignKey(FactureAchat, on_delete=models.CASCADE, related_name='lignes', verbose_name="Facture d'achat")
    reference_article = models.CharField(max_length=50, verbose_name="Référence article")
    designation = models.CharField(max_length=200, verbose_name="Désignation")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantite = models.IntegerField(verbose_name="Quantité")
    prix_total_article = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix total article")
    
    # Relations
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Article")
    
    class Meta:
        verbose_name = "Ligne de facture d'achat"
        verbose_name_plural = "Lignes de facture d'achat"
        ordering = ['facture_achat', 'reference_article']
    
    def __str__(self):
        return f"{self.facture_achat.reference_achat} - {self.designation}"

class FactureTransfert(models.Model):
    """Modèle pour les factures de transfert entre agences"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    ETAT_CHOICES = [
        ('entrer', 'Entrer'),
        ('sortir', 'Sortir'),
    ]
    
    numero_compte = models.CharField(max_length=50, verbose_name="Numéro de compte")
    date_transfert = models.DateField(verbose_name="Date de transfert")
    reference_transfert = models.CharField(max_length=100, unique=True, verbose_name="Référence transfert")
    lieu_depart = models.CharField(max_length=100, verbose_name="Lieu de départ")
    lieu_arrivee = models.CharField(max_length=100, verbose_name="Lieu d'arrivée")
    quantite = models.IntegerField(verbose_name="Quantité")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut")
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES, default='entrer', verbose_name="État")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    # Relations
    agence_source = models.ForeignKey(Agence, on_delete=models.CASCADE, related_name='transferts_sortants', verbose_name="Agence source")
    agence_destination = models.ForeignKey(Agence, on_delete=models.CASCADE, related_name='transferts_entrants', verbose_name="Agence destination")
    employe_expediteur = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='transferts_expedies', verbose_name="Employé expéditeur")
    employe_destinataire = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True, related_name='transferts_recus', verbose_name="Employé destinataire")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Facture de transfert"
        verbose_name_plural = "Factures de transfert"
        ordering = ['-date_transfert']
    
    def __str__(self):
        return f"Transfert {self.reference_transfert} - {self.lieu_depart} → {self.lieu_arrivee}"

class LigneFactureTransfert(models.Model):
    """Modèle pour les lignes de facture de transfert"""
    facture_transfert = models.ForeignKey(FactureTransfert, on_delete=models.CASCADE, related_name='lignes', verbose_name="Facture de transfert")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    quantite = models.IntegerField(verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    valeur_totale = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur totale")
    
    class Meta:
        verbose_name = "Ligne de facture de transfert"
        verbose_name_plural = "Lignes de facture de transfert"
        ordering = ['facture_transfert', 'article']
    
    def __str__(self):
        return f"{self.facture_transfert.reference_transfert} - {self.article.designation}"

class PlanComptable(models.Model):
    """Modèle pour le plan comptable"""
    NATURE_COMPTE_CHOICES = [
        ('actif', 'Actif'),
        ('passif', 'Passif'),
        ('produit', 'Produit'),
        ('charge', 'Charge'),
        ('tresorerie', 'Trésorerie'),
    ]
    
    numero = models.CharField(max_length=10, unique=True, verbose_name="Numéro")
    intitule = models.CharField(max_length=200, verbose_name="Intitulé")
    compte = models.CharField(max_length=10, verbose_name="Compte")
    abrege = models.CharField(max_length=50, verbose_name="Abrégé")
    nature_compte = models.CharField(max_length=20, choices=NATURE_COMPTE_CHOICES, verbose_name="Nature compte")
    compte_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Compte parent")
    niveau = models.IntegerField(default=1, verbose_name="Niveau")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    class Meta:
        verbose_name = "Plan comptable"
        verbose_name_plural = "Plan comptable"
        ordering = ['numero']
    
    def __str__(self):
        return f"{self.numero} - {self.intitule}"

class PlanTiers(models.Model):
    """Modèle pour le plan des tiers"""
    TYPE_TIERS_CHOICES = [
        ('client', 'Client'),
        ('fournisseur', 'Fournisseur'),
        ('banque', 'Banque'),
        ('etat', 'État'),
        ('salarie', 'Salarié'),
        ('autre', 'Autre'),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_TIERS_CHOICES, verbose_name="Type")
    numero_compte = models.CharField(max_length=20, unique=True, verbose_name="Numéro compte")
    intitule_compte = models.CharField(max_length=200, verbose_name="Intitulé de compte")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    compte_comptable = models.ForeignKey(PlanComptable, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Compte comptable")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    # Relations
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    class Meta:
        verbose_name = "Plan des tiers"
        verbose_name_plural = "Plan des tiers"
        ordering = ['numero_compte']
    
    def __str__(self):
        return f"{self.numero_compte} - {self.intitule_compte}"

class CodeJournaux(models.Model):
    """Modèle pour les codes journaux"""
    TYPE_DOCUMENT_CHOICES = [
        ('document_achat', 'Document achat'),
        ('document_banque', 'Document banque'),
        ('caisse', 'Caisse'),
        ('monnaie_electronique', 'Monnaie électronique'),
        ('operation_diverse', 'Opération diverse'),
    ]
    
    type_document = models.CharField(max_length=30, choices=TYPE_DOCUMENT_CHOICES, verbose_name="Type de document")
    intitule = models.CharField(max_length=100, verbose_name="Intitulé")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    compte_contrepartie = models.ForeignKey(PlanComptable, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Compte et contrepartie")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    class Meta:
        verbose_name = "Code journal"
        verbose_name_plural = "Codes journaux"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.intitule}"

class TauxTaxe(models.Model):
    """Modèle pour les taux de taxe"""
    TYPE_TAXE_CHOICES = [
        ('tva', 'TVA'),
        ('tps', 'TPS'),
        ('autre', 'Autre'),
    ]
    
    SENS_CHOICES = [
        ('debit', 'Débit'),
        ('credit', 'Crédit'),
    ]
    
    ASSUJETTISSEMENT_CHOICES = [
        ('oui', 'Oui'),
        ('non', 'Non'),
    ]
    
    # Identification
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    sens = models.CharField(max_length=10, choices=SENS_CHOICES, verbose_name="Sens")
    intitule = models.CharField(max_length=100, verbose_name="Intitulé")
    compte = models.ForeignKey(PlanComptable, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Compte")
    taux = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux (%)")
    
    # Caractéristiques
    type = models.CharField(max_length=20, choices=TYPE_TAXE_CHOICES, verbose_name="Type")
    assujettissement = models.CharField(max_length=10, choices=ASSUJETTISSEMENT_CHOICES, verbose_name="Assujettissement")
    code_regroupement = models.CharField(max_length=20, blank=True, verbose_name="Code de regroupement")
    provenance = models.CharField(max_length=100, blank=True, verbose_name="Provenance")
    
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    
    class Meta:
        verbose_name = "Taux de taxe"
        verbose_name_plural = "Taux de taxe"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.intitule} ({self.taux}%)"

class InventaireStock(models.Model):
    """Modèle pour les inventaires de stock"""
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    numero_inventaire = models.CharField(max_length=50, unique=True, verbose_name="Numéro d'inventaire")
    date_debut = models.DateTimeField(verbose_name="Date de début")
    date_fin = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours', verbose_name="Statut")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    # Relations
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    responsable = models.ForeignKey(Employe, on_delete=models.CASCADE, verbose_name="Responsable")
    
    class Meta:
        verbose_name = "Inventaire de stock"
        verbose_name_plural = "Inventaires de stock"
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"Inventaire {self.numero_inventaire} - {self.date_debut.strftime('%d/%m/%Y')}"

class LigneInventaireStock(models.Model):
    """Modèle pour les lignes d'inventaire de stock"""
    inventaire = models.ForeignKey(InventaireStock, on_delete=models.CASCADE, related_name='lignes', verbose_name="Inventaire")
    reference_article = models.CharField(max_length=50, verbose_name="Référence article")
    designation = models.CharField(max_length=200, verbose_name="Désignation")
    quantite_stock = models.IntegerField(verbose_name="Quantité en stock")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    valeur = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valeur")
    conditionnement = models.CharField(max_length=50, verbose_name="Conditionnement")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    # Relations
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Article")
    
    class Meta:
        verbose_name = "Ligne d'inventaire de stock"
        verbose_name_plural = "Lignes d'inventaire de stock"
        ordering = ['reference_article']
    
    def __str__(self):
        return f"{self.inventaire.numero_inventaire} - {self.designation}"

class StatistiqueVente(models.Model):
    """Modèle pour les statistiques de vente"""
    reference_article = models.CharField(max_length=50, verbose_name="Référence article")
    designation = models.CharField(max_length=200, verbose_name="Désignation")
    quantite = models.IntegerField(verbose_name="Quantité")
    marge_profit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Marge (profit)")
    chiffre_affaires = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Chiffre d'affaires")
    pourcentage_marge = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Pourcentage de marge")
    chiffre_affaires_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Chiffre d'affaires total")
    
    # Relations
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Statistique de vente"
        verbose_name_plural = "Statistiques de vente"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Statistiques {self.reference_article} - {self.designation}"

class MouvementStock(models.Model):
    """Modèle pour les mouvements de stock"""
    TYPE_MOUVEMENT_CHOICES = [
        ('entree', 'Entrée'),
        ('sortie', 'Sortie'),
        ('ajustement', 'Ajustement'),
        ('inventaire', 'Inventaire'),
        ('transfert', 'Transfert'),
        ('perte', 'Perte'),
        ('retour', 'Retour'),
    ]
    
    date_mouvement = models.DateTimeField(verbose_name="Date de mouvement")
    type_mouvement = models.CharField(max_length=20, choices=TYPE_MOUVEMENT_CHOICES, verbose_name="Type de mouvement")
    numero_piece = models.CharField(max_length=100, verbose_name="Numéro de pièce")
    quantite_stock = models.IntegerField(verbose_name="Quantité en stock")
    stock_initial = models.IntegerField(verbose_name="Stock initial")
    solde = models.IntegerField(verbose_name="Solde")
    quantite = models.IntegerField(verbose_name="Quantité")
    cout_moyen_pondere = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Coût moyen pondéré")
    stock_permanent = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Stock permanent")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    # Relations
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    employe = models.ForeignKey(Employe, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Employé")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fournisseur")
    facture_vente = models.ForeignKey(FactureVente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Facture de vente")
    facture_achat = models.ForeignKey(FactureAchat, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Facture d'achat")
    inventaire = models.ForeignKey(InventaireStock, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Inventaire")
    facture_transfert = models.ForeignKey(FactureTransfert, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Facture de transfert")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date_mouvement']
    
    def __str__(self):
        return f"{self.get_type_mouvement_display()} - {self.article.designation} ({self.quantite})"
