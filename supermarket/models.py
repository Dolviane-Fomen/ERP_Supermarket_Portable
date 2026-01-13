from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date as date_class

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
        max_length=30,
        choices=[
            ('admin', 'Administrateur'),
            ('gerant', 'Gérant'),
            ('caissier', 'Caissier'),
            ('vendeur', 'Vendeur'),
            ('magasinier', 'Magasinier'),
            ('comptable', 'Comptable'),
            ('acm', 'ACM'),
            ('livreur', 'Livreur'),
            ('responsable_logistique', 'Responsable Logistique'),
            ('responsable_rh', 'Responsable Ressource Humaine'),
            ('assistant_comptable', 'Assistant Comptable'),
            ('responsable_achat', 'Responsable Achat'),
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
    email = models.EmailField(verbose_name="E-mail")
    zone = models.CharField(max_length=100, verbose_name="Zone", default="Non spécifiée")
    ref = models.CharField(max_length=100, blank=True, null=True, verbose_name="Référence")
    detail = models.CharField(max_length=200, blank=True, null=True, verbose_name="Détail")
    potentiel = models.CharField(max_length=100, blank=True, null=True, verbose_name="Potentiel /5")
    
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
    
    def save(self, *args, **kwargs):
        """Override save pour gerer automatiquement la mise a jour du stock"""
        # Vérifier si c'est une nouvelle facture ou une mise à jour
        is_new = self.pk is None
        
        # Si c'est une mise à jour, vérifier si le statut a changé
        statut_avant = None
        if not is_new:
            try:
                ancienne_facture = FactureAchat.objects.get(pk=self.pk)
                statut_avant = ancienne_facture.statut
            except FactureAchat.DoesNotExist:
                pass
        
        # Appeler la méthode save parente
        super().save(*args, **kwargs)
        
        # Mettre a jour le stock automatiquement seulement si la facture est validée
        # et si le statut vient de changer vers 'validee' (ou si c'est une nouvelle facture avec statut 'validee')
        if self.statut == 'validee':
            # Mettre à jour le stock si :
            # 1. C'est une nouvelle facture avec statut 'validee'
            # 2. Le statut vient de changer vers 'validee'
            if is_new or (statut_avant and statut_avant != 'validee'):
                print(f"[INFO] Facture {self.reference_achat} validée - Mise à jour du stock...")
                self.mettre_a_jour_stock()
    
    def mettre_a_jour_stock(self):
        """Methode pour mettre a jour le stock des articles de cette facture"""
        from django.utils import timezone
        
        lignes = self.lignes.all()
        for ligne in lignes:
            if ligne.article:
                try:
                    # IMPORTANT: Vérifier si un mouvement de stock existe déjà pour cette facture et cet article
                    # pour éviter les mises à jour multiples
                    # Cette vérification est cruciale lors des modifications pour éviter de réappliquer la quantité totale
                    # 
                    # On vérifie s'il existe un mouvement récent (moins de 5 secondes) pour cette facture et cet article
                    # Si oui, on ignore car c'est probablement une modification qui a déjà été gérée manuellement
                    mouvements_recents = MouvementStock.objects.filter(
                        facture_achat=self,
                        article=ligne.article,
                        numero_piece=self.reference_achat,
                        date_creation__gte=timezone.now() - timezone.timedelta(seconds=5)
                    ).exists()
                    
                    if mouvements_recents:
                        print(f"[INFO] Mouvement récent détecté pour {ligne.article.designation} - Facture {self.reference_achat}")
                        print(f"[INFO] Ignorant mettre_a_jour_stock() car une modification récente a déjà été gérée manuellement")
                        continue
                    
                    # Vérifier aussi s'il existe un mouvement quelconque pour cette facture et cet article
                    # (pour les modifications plus anciennes)
                    mouvement_existant = MouvementStock.objects.filter(
                        facture_achat=self,
                        article=ligne.article,
                        numero_piece=self.reference_achat
                    ).exists()
                    
                    if mouvement_existant:
                        print(f"[INFO] Stock déjà mis à jour pour {ligne.article.designation} - Facture {self.reference_achat}")
                        print(f"[INFO] Ignorant mettre_a_jour_stock() car un mouvement existe déjà (modification gérée manuellement)")
                        continue
                    
                    # Mettre a jour le stock de l'article
                    ancien_stock = ligne.article.stock_actuel
                    ligne.article.stock_actuel += ligne.quantite
                    ligne.article.dernier_prix_achat = ligne.prix_unitaire
                    # Le suivi de stock est toujours activé automatiquement lors de toute modification du stock
                    ligne.article.suivi_stock = True
                    ligne.article.save()
                    
                    # Créer un mouvement de stock pour la traçabilité
                    MouvementStock.objects.create(
                        article=ligne.article,
                        agence=self.agence,
                        type_mouvement='entree',
                        date_mouvement=timezone.now(),
                        numero_piece=self.reference_achat,
                        quantite_stock=ligne.article.stock_actuel,
                        stock_initial=ancien_stock,
                        solde=ligne.article.stock_actuel,
                        quantite=ligne.quantite,
                        cout_moyen_pondere=float(ligne.prix_unitaire),
                        stock_permanent=float(ligne.article.stock_actuel * ligne.prix_unitaire),
                        facture_achat=self,
                        fournisseur=self.fournisseur,
                        commentaire=f"Achat automatique - {self.reference_achat}"
                    )
                    print(f"[AUTO] Stock mis a jour automatiquement: {ligne.article.designation} - {ancien_stock} -> {ligne.article.stock_actuel}")
                    
                except Exception as e:
                    print(f"[ERREUR] Erreur mise a jour stock automatique pour {ligne.article.designation}: {e}")
                    import traceback
                    traceback.print_exc()
    
    def valider_facture(self):
        """Méthode pour valider une facture et mettre à jour le stock"""
        if self.statut != 'validee':
            self.statut = 'validee'
            self.save()  # Cela déclenchera automatiquement la mise à jour du stock
            return True
        return False
    
    def annuler_facture(self):
        """Méthode pour annuler une facture et remettre le stock à jour"""
        if self.statut in ['validee', 'payee']:
            # Restaurer le stock
            lignes = self.lignes.all()
            for ligne in lignes:
                if ligne.article:
                    ligne.article.stock_actuel -= ligne.quantite
                    if ligne.article.stock_actuel < 0:
                        ligne.article.stock_actuel = 0
                    ligne.article.save()
                    
                    print(f"[ANNULATION] Stock restauré: {ligne.article.designation} - {ligne.article.stock_actuel}")
            
            self.statut = 'annulee'
            self.save()
            return True
        return False

class LigneFactureAchat(models.Model):
    """Modèle pour les lignes de facture d'achat"""
    facture_achat = models.ForeignKey(FactureAchat, on_delete=models.CASCADE, related_name='lignes', verbose_name="Facture d'achat")
    reference_article = models.CharField(max_length=50, verbose_name="Référence article")
    designation = models.CharField(max_length=200, verbose_name="Désignation")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantite = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Quantité")
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
        return f"Transfert {self.reference_transfert} - {self.lieu_depart} -> {self.lieu_arrivee}"

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
    quantite_stock = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Quantité en stock")
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
    quantite = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Quantité")
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
    quantite_stock = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Quantité en stock")
    stock_initial = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Stock initial")
    solde = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Solde")
    quantite = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Quantité")
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


class Commande(models.Model):
    """Modèle pour les commandes"""
    ETAT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_livraison', 'En livraison'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
        ('validee', 'Validée'),
    ]
    
    date = models.DateField(verbose_name="Date")
    heure = models.TimeField(verbose_name="Heure")
    etat_commande = models.CharField(max_length=20, choices=ETAT_CHOICES, default='en_attente', verbose_name="État de la commande")
    quantite = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Quantité")
    quantite_totale = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Quantité totale")
    prix_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix total")
    
    # Relations
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Créé par", related_name='commandes_creees')
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-date', '-heure']
    
    def __str__(self):
        return f"Commande {self.id} - {self.client.intitule}"


class DocumentCommande(models.Model):
    """Modèle pour les documents de commande (comme FactureAchat)"""
    ETAT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_livraison', 'En livraison'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
        ('validee', 'Validée'),
    ]
    
    numero_commande = models.CharField(max_length=50, unique=True, verbose_name="Numéro de commande")
    date = models.DateField(verbose_name="Date")
    heure = models.TimeField(verbose_name="Heure")
    etat_commande = models.CharField(max_length=20, choices=ETAT_CHOICES, default='en_attente', verbose_name="État de la commande")
    quantite_totale = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Quantité totale")
    prix_total_global = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix total global")
    commentaire = models.TextField(blank=True, verbose_name="Commentaire")
    
    # Relations
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Document de commande"
        verbose_name_plural = "Documents de commande"
        ordering = ['-date', '-heure']
    
    def __str__(self):
        return f"Document {self.numero_commande} - {self.client.intitule}"


class LigneCommande(models.Model):
    """Modèle pour les lignes de commande (comme LigneFactureAchat)"""
    document_commande = models.ForeignKey(DocumentCommande, on_delete=models.CASCADE, related_name='lignes', verbose_name="Document de commande")
    quantite = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Prix unitaire")
    prix_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix total")
    
    # Relations
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    
    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"
        ordering = ['document_commande', 'id']
    
    def __str__(self):
        return f"{self.document_commande.numero_commande} - {self.article.designation}"


class Livreur(models.Model):
    """Modèle pour les livreurs"""
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    compte = models.ForeignKey(Compte, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Compte utilisateur", related_name='livreur')
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Livreur"
        verbose_name_plural = "Livreurs"
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"

class SuiviClientAction(models.Model):
    """Modèle pour suivre les actions des ACM sur les clients - Plusieurs appels possibles par client"""
    PLAGE_HORAIRE_CHOICES = [
        ('06h30-08h30', '06h30-08h30'),
        ('08h30-10h00', '08h30-10h00'),
        ('10h00-11h30', '10h00-11h30'),
        ('11h30-12h00', '11h30-12h00'),
        ('14h30-16h00', '14h30-16h00'),
        ('16h00-17h30', '16h00-17h30'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client", related_name='actions_suivi')
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Créé par", related_name='actions_suivi_creees')
    plage_horaire = models.CharField(max_length=20, choices=PLAGE_HORAIRE_CHOICES, blank=True, null=True, verbose_name="Plage horaire")
    heure_appel = models.TimeField(blank=True, null=True, verbose_name="Heure d'appel")
    action = models.TextField(verbose_name="Action/Commande", blank=True, null=True)
    date_action = models.DateTimeField(auto_now_add=True, verbose_name="Date de l'action")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Action de suivi client"
        verbose_name_plural = "Actions de suivi client"
        ordering = ['-date_action', '-heure_appel']
        # Supprimé unique_together pour permettre plusieurs actions par client
    
    def __str__(self):
        heure_str = self.heure_appel.strftime('%H:%M') if self.heure_appel else 'N/A'
        plage = self.plage_horaire if self.plage_horaire else 'N/A'
        return f"Appel {heure_str} ({plage}) - {self.client.intitule} - {self.date_action.strftime('%d/%m/%Y')}"


class Livraison(models.Model):
    """Modèle pour les livraisons"""
    ETAT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_preparation', 'En préparation'),
        ('en_cours', 'En cours'),
        ('confirmee', 'Confirmée'),
        ('livree', 'Livrée'),
        ('livree_partiellement', 'Livrée partiellement'),
        ('pas_livree', 'Pas livrée'),
        ('reportee', 'Reportée'),
        ('annulee', 'Annulée'),
    ]
    
    etat_livraison = models.CharField(max_length=30, choices=ETAT_CHOICES, default='planifiee', verbose_name="État de la livraison")
    date_livraison = models.DateField(verbose_name="Date de livraison")
    heure_depart = models.TimeField(blank=True, null=True, verbose_name="Heure de départ")
    heure_arrivee = models.TimeField(blank=True, null=True, verbose_name="Heure d'arrivée")
    heure_livraison = models.TimeField(blank=True, null=True, verbose_name="Heure de livraison")
    zone = models.CharField(max_length=100, blank=True, null=True, verbose_name="Zone de livraison")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    ordre_livraison = models.PositiveIntegerField(default=0, verbose_name="Ordre de livraison")
    
    # Relations
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Commande")
    livreur = models.ForeignKey('Livreur', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Livreur")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Livraison"
        verbose_name_plural = "Livraisons"
        ordering = ['-date_livraison', 'ordre_livraison']
    
    def __str__(self):
        return f"Livraison {self.id} - {self.get_etat_livraison_display()}"


class FactureCommande(models.Model):
    """Modèle pour les factures de commande"""
    numero_facture = models.CharField(max_length=100, unique=True, verbose_name="Numéro de facture")
    date = models.DateField(verbose_name="Date de facture", null=True, blank=True, default=date_class.today)  # Champ pour compatibilité
    date_facture = models.DateField(verbose_name="Date de facture", default=date_class.today)  # Champ principal dans la DB (NOT NULL)
    heure = models.TimeField(verbose_name="Heure de facture", null=True, blank=True)  # Champ existant dans la DB
    prix_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prix total")  # Champ existant dans la DB
    net_a_payer = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Net à payer")  # Champ existant dans la DB
    
    # Relations
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Commande")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Facture de commande"
        verbose_name_plural = "Factures de commande"
        ordering = ['-date_facture', '-heure']
    
    def __str__(self):
        return f"Facture {self.numero_facture}"
    
    def save(self, *args, **kwargs):
        # Synchroniser date et date_facture
        if self.date_facture and not self.date:
            self.date = self.date_facture
        elif self.date and not self.date_facture:
            self.date_facture = self.date
        super().save(*args, **kwargs)


class StatistiqueClient(models.Model):
    """Modèle pour les statistiques clients"""
    date_debut = models.DateField(verbose_name="Date de début", default=date_class.today)
    date_fin = models.DateField(verbose_name="Date de fin", default=date_class.today)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Montant total")
    nombre_achats = models.IntegerField(default=0, verbose_name="Nombre d'achats")
    
    # Relations
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Statistique client"
        verbose_name_plural = "Statistiques clients"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Statistique {self.client.intitule} - {self.date_debut}"


class Notification(models.Model):
    """Modèle pour les notifications"""
    TYPE_CHOICES = [
        ('commande_enregistree', 'Commande enregistrée'),
        ('livraison_planifiee', 'Livraison planifiée'),
        ('livraison_confirmee', 'Livraison confirmée'),
        ('livraison_terminee', 'Livraison terminée'),
        ('stock_insuffisant', 'Stock insuffisant'),
        ('autre', 'Autre'),
    ]
    
    type_notification = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Type de notification")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    lu = models.BooleanField(default=False, verbose_name="Lu")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    # Relations
    agence = models.ForeignKey(Agence, on_delete=models.CASCADE, verbose_name="Agence")
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications', verbose_name="Commande")
    livraison = models.ForeignKey(Livraison, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications', verbose_name="Livraison")
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['agence', 'lu', '-date_creation']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.get_type_notification_display()}"

# ----------------gestion comptable-------------------------

class Depense(models.Model):  
    """Modèle pour les dépenses"""
    date = models.DateTimeField(null=True, blank=True, verbose_name="Date de dépense")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
 
    libelle = models.CharField(max_length=200, verbose_name="Libellé")

    class Meta:
        verbose_name = "Dépense"      
        verbose_name_plural = "Dépenses"
        ordering = ['-date']         

    def __str__(self):
        return self.libelle

# Suppression des signaux - on utilisera une approche plus directe dans la vue
#  Client
# libele