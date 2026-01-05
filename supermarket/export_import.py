"""
Module d'export et d'import des données pour migration vers nouvelle version
"""
import json
from datetime import datetime
def parse_iso_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


def parse_iso_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def parse_iso_time(value):
    if not value:
        return None
    formats = ("%H:%M:%S.%f", "%H:%M:%S")
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).time()
        except ValueError:
            continue
    return None
from decimal import Decimal
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Agence, Famille, Compte, Employe, Client, Fournisseur,
    Article, Caisse, SessionCaisse, FactureVente, LigneFactureVente,
    FactureAchat, LigneFactureAchat, FactureTransfert, LigneFactureTransfert,
    MouvementStock, InventaireStock, StatistiqueVente, TypeVente,
    PlanComptable, PlanTiers, CodeJournaux, TauxTaxe, DocumentVente
)


class DecimalEncoder(json.JSONEncoder):
    """Encoder personnalisé pour gérer les Decimal en JSON"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def export_data(agence_id=None, include_users=True):
    """
    Exporte toutes les données de l'ERP au format JSON
    
    Args:
        agence_id: ID de l'agence à exporter (None pour toutes les agences)
        include_users: Si True, inclut les comptes utilisateurs (sans mots de passe)
    
    Returns:
        dict: Dictionnaire contenant toutes les données exportées
    """
    data = {
        'version': '1.0',
        'date_export': datetime.now().isoformat(),
        'agence_id': agence_id,
        'agences': [],
        'familles': [],
        'comptes': [],
        'employes': [],
        'clients': [],
        'fournisseurs': [],
        'articles': [],
        'types_vente': [],
        'caisses': [],
        'sessions_caisse': [],
        'factures_vente': [],
        'documents_vente': [],
        'lignes_factures_vente': [],
        'factures_achat': [],
        'lignes_factures_achat': [],
        'factures_transfert': [],
        'lignes_factures_transfert': [],
        'mouvements_stock': [],
        'inventaires_stock': [],
        'statistiques_vente': [],
        'plan_comptable': [],
        'plan_tiers': [],
        'code_journaux': [],
        'taux_taxes': [],
    }
    
    # Export des Agences
    if agence_id:
        agences = Agence.objects.filter(id_agence=agence_id)
    else:
        agences = Agence.objects.all()
    
    for agence in agences:
        data['agences'].append({
            'id_agence': agence.id_agence,
            'nom_agence': agence.nom_agence,
            'adresse': agence.adresse,
        })
    
    # Export des Familles (toutes, pas liées à une agence)
    for famille in Famille.objects.all():
        data['familles'].append({
            'code': famille.code,
            'intitule': famille.intitule,
            'unite_vente': famille.unite_vente,
            'suivi_stock': famille.suivi_stock,
        })
    
    # Export des Comptes (optionnel)
    if include_users:
        if agence_id:
            comptes = Compte.objects.filter(agence_id=agence_id, actif=True)
        else:
            comptes = Compte.objects.filter(actif=True)
        
        for compte in comptes:
            data['comptes'].append({
                'numero_compte': compte.numero_compte,
                'type_compte': compte.type_compte,
                'nom': compte.nom,
                'prenom': compte.prenom,
                'telephone': compte.telephone,
                'email': compte.email,
                'actif': compte.actif,
                'date_creation': compte.date_creation.isoformat() if compte.date_creation else None,
                'date_derniere_connexion': compte.date_derniere_connexion.isoformat() if compte.date_derniere_connexion else None,
                'agence_id': compte.agence.id_agence if compte.agence else None,
                'username': compte.user.username if compte.user else None,
                # Note: Le mot de passe n'est PAS exporté pour des raisons de sécurité
            })
    
    # Export des Employés
    if agence_id:
        employes = Employe.objects.filter(compte__agence_id=agence_id)
    else:
        employes = Employe.objects.all()
    
    for employe in employes:
        data['employes'].append({
            'numero_employe': employe.numero_employe,
            'poste': employe.poste,
            'departement': employe.departement,
            'date_embauche': employe.date_embauche.isoformat() if employe.date_embauche else None,
            # 'salaire': str(employe.salaire) if hasattr(employe, 'salaire') and employe.salaire else None,  # Champ commenté dans le modèle
            'numero_compte': employe.compte.numero_compte if employe.compte else None,
        })
    
    # Export des Clients
    if agence_id:
        clients = Client.objects.filter(agence_id=agence_id)
    else:
        clients = Client.objects.all()
    
    for client in clients:
        data['clients'].append({
            'id': client.id,  # Utiliser l'ID comme identifiant unique
            'intitule': client.intitule,
            'adresse': client.adresse,
            'telephone': client.telephone,
            'email': client.email,
            'agence_id': client.agence.id_agence if client.agence else None,
        })
    
    # Export des Fournisseurs
    if agence_id:
        fournisseurs = Fournisseur.objects.filter(agence_id=agence_id)
    else:
        fournisseurs = Fournisseur.objects.all()
    
    for fournisseur in fournisseurs:
        data['fournisseurs'].append({
            'id': fournisseur.id,  # Utiliser l'ID comme identifiant unique
            'intitule': fournisseur.intitule,
            'adresse': fournisseur.adresse,
            'telephone': fournisseur.telephone,
            'email': fournisseur.email,
            'agence_id': fournisseur.agence.id_agence if fournisseur.agence else None,
        })
    
    # Export des Articles
    if agence_id:
        articles = Article.objects.filter(agence_id=agence_id)
    else:
        articles = Article.objects.all()
    
    for article in articles:
        data['articles'].append({
            'reference_article': article.reference_article,
            'designation': article.designation,
            'categorie_code': article.categorie.code if article.categorie else None,
            'suivi_stock': article.suivi_stock,
            'conditionnement': article.conditionnement if hasattr(article, 'conditionnement') else '',
            'prix_achat': str(article.prix_achat),
            'dernier_prix_achat': str(article.dernier_prix_achat),
            'unite_vente': article.unite_vente,
            'prix_vente': str(article.prix_vente),
            'stock_actuel': str(article.stock_actuel),
            'stock_minimum': str(article.stock_minimum),
            'date_creation': article.date_creation.isoformat() if article.date_creation else None,
            'agence_id': article.agence.id_agence if article.agence else None,
        })
    
    # Export des Types de Vente
    if agence_id:
        types_vente = TypeVente.objects.filter(article__agence_id=agence_id)
    else:
        types_vente = TypeVente.objects.all()
    
    for type_vente in types_vente:
        data['types_vente'].append({
            'id': type_vente.id,
            'intitule': type_vente.intitule,
            'prix': str(type_vente.prix),
            'reference_article': type_vente.article.reference_article if type_vente.article else None,
            'agence_id': type_vente.article.agence.id_agence if type_vente.article and type_vente.article.agence else None,
        })
    
    # Export des Caisses
    if agence_id:
        caisses = Caisse.objects.filter(agence_id=agence_id)
    else:
        caisses = Caisse.objects.all()
    
    for caisse in caisses:
        data['caisses'].append({
            'numero_caisse': caisse.numero_caisse,
            'nom_caisse': caisse.nom_caisse,
            'solde_initial': str(caisse.solde_initial),
            'solde_actuel': str(caisse.solde_actuel),
            'statut': caisse.statut,
            'date_ouverture': caisse.date_ouverture.isoformat() if caisse.date_ouverture else None,
            'date_fermeture': caisse.date_fermeture.isoformat() if caisse.date_fermeture else None,
            'agence_id': caisse.agence.id_agence if caisse.agence else None,
        })
    
    # Export des Sessions de Caisse
    if agence_id:
        sessions = SessionCaisse.objects.filter(caisse__agence_id=agence_id)
    else:
        sessions = SessionCaisse.objects.all()
    
    for session in sessions:
        data['sessions_caisse'].append({
            'id': session.id,
            'numero_caisse': session.caisse.numero_caisse if session.caisse else None,
            'date_ouverture': session.date_ouverture.isoformat() if session.date_ouverture else None,
            'date_fermeture': session.date_fermeture.isoformat() if session.date_fermeture else None,
            'solde_ouverture': str(session.solde_ouverture),
            'solde_fermeture': str(session.solde_fermeture) if session.solde_fermeture else None,
            'statut': session.statut,
            'agence_id': session.agence.id_agence if session.agence else None,
            'numero_compte': session.employe.compte.numero_compte if session.employe and session.employe.compte else None,
        })
    
    # Export des Documents de Vente (documents de fermeture)
    if agence_id:
        documents = DocumentVente.objects.filter(agence_id=agence_id)
    else:
        documents = DocumentVente.objects.all()
    
    for document in documents:
        data['documents_vente'].append({
            'numero_document': document.numero_document,
            'date': document.date.isoformat() if document.date else None,
            'heure_fermeture': document.heure_fermeture.isoformat() if document.heure_fermeture else None,
            'session_caisse_id': document.session_caisse.id if document.session_caisse else None,
            'vendeuse_nom': document.vendeuse_nom,
            'nombre_factures': document.nombre_factures,
            'total_articles': document.total_articles,
            'chiffre_affaires': str(document.chiffre_affaires),
            'factures_data': document.factures_data,
            'agence_id': document.agence.id_agence if document.agence else None,
        })
    
    # Export des Factures de Vente
    if agence_id:
        factures_vente = FactureVente.objects.filter(agence_id=agence_id)
    else:
        factures_vente = FactureVente.objects.all()
    
    for facture in factures_vente:
        data['factures_vente'].append({
            'id': facture.id,
            'numero_ticket': facture.numero_ticket,
            'date': facture.date.isoformat() if facture.date else None,
            'heure': facture.heure.isoformat() if facture.heure else None,
            'remise': str(facture.remise) if facture.remise else None,
            'nette_a_payer': str(facture.nette_a_payer),
            'montant_regler': str(facture.montant_regler) if facture.montant_regler else None,
            'rendu': str(facture.rendu) if facture.rendu else None,
            'en_attente': facture.en_attente,
            'nom_vendeuse': facture.nom_vendeuse,
            'numero_caisse': facture.caisse.numero_caisse if facture.caisse else None,
            'client_id': facture.client.id if facture.client else None,
            'agence_id': facture.agence.id_agence if facture.agence else None,
            'session_caisse_id': facture.session_caisse.id if facture.session_caisse else None,
        })
    
    # Export des Lignes de Factures de Vente
    if agence_id:
        lignes_vente = LigneFactureVente.objects.filter(facture_vente__agence_id=agence_id)
    else:
        lignes_vente = LigneFactureVente.objects.all()
    
    for ligne in lignes_vente:
        data['lignes_factures_vente'].append({
            'id': ligne.id,
            'facture_vente_id': ligne.facture_vente.id if ligne.facture_vente else None,
            'reference_article': ligne.article.reference_article if ligne.article else None,
            'designation': ligne.designation,
            'quantite': str(ligne.quantite),
            'prix_unitaire': str(ligne.prix_unitaire),
            'prix_total': str(ligne.prix_total),
        })
    
    # Export des Factures d'Achat
    if agence_id:
        factures_achat = FactureAchat.objects.filter(agence_id=agence_id)
    else:
        factures_achat = FactureAchat.objects.all()
    
    for facture in factures_achat:
        data['factures_achat'].append({
            'id': facture.id,
            'numero_fournisseur': facture.numero_fournisseur,
            'reference_achat': facture.reference_achat,
            'date_achat': facture.date_achat.isoformat() if facture.date_achat else None,
            'heure': facture.heure.isoformat() if facture.heure else None,
            'prix_total_global': str(facture.prix_total_global),
            'statut': facture.statut,
            'commentaire': facture.commentaire,
            'fournisseur_id': facture.fournisseur.id if facture.fournisseur else None,
            'agence_id': facture.agence.id_agence if facture.agence else None,
            'numero_employe': facture.employe.numero_employe if facture.employe else None,
        })
    
    # Export des Lignes de Factures d'Achat
    if agence_id:
        lignes_achat = LigneFactureAchat.objects.filter(facture_achat__agence_id=agence_id)
    else:
        lignes_achat = LigneFactureAchat.objects.all()
    
    for ligne in lignes_achat:
        data['lignes_factures_achat'].append({
            'id': ligne.id,
            'facture_achat_id': ligne.facture_achat.id if ligne.facture_achat else None,
            'reference_article': ligne.reference_article if ligne.reference_article else (ligne.article.reference_article if ligne.article else None),
            'designation': ligne.designation,
            'quantite': str(ligne.quantite),
            'prix_unitaire': str(ligne.prix_unitaire),
            'prix_total_article': str(ligne.prix_total_article),
        })
    
    # Export des Factures de Transfert
    if agence_id:
        # Les factures de transfert peuvent être liées à l'agence source ou destination
        factures_transfert = FactureTransfert.objects.filter(
            Q(agence_source_id=agence_id) | Q(agence_destination_id=agence_id)
        )
    else:
        factures_transfert = FactureTransfert.objects.all()
    
    for facture in factures_transfert:
        data['factures_transfert'].append({
            'id': facture.id,
            'numero_compte': facture.numero_compte,
            'reference_transfert': facture.reference_transfert,
            'date_transfert': facture.date_transfert.isoformat() if facture.date_transfert else None,
            'lieu_depart': facture.lieu_depart,
            'lieu_arrivee': facture.lieu_arrivee,
            'quantite': facture.quantite,
            'statut': facture.statut,
            'etat': facture.etat,
            'commentaire': facture.commentaire,
            'agence_source_id': facture.agence_source.id_agence if facture.agence_source else None,
            'agence_destination_id': facture.agence_destination.id_agence if facture.agence_destination else None,
            'numero_employe_expediteur': facture.employe_expediteur.numero_employe if facture.employe_expediteur else None,
            'numero_employe_destinataire': facture.employe_destinataire.numero_employe if facture.employe_destinataire else None,
        })
    
    # Export des Lignes de Factures de Transfert
    if agence_id:
        # Les lignes de facture de transfert sont liées via facture_transfert qui a agence_source ou agence_destination
        lignes_transfert = LigneFactureTransfert.objects.filter(
            Q(facture_transfert__agence_source_id=agence_id) | Q(facture_transfert__agence_destination_id=agence_id)
        )
    else:
        lignes_transfert = LigneFactureTransfert.objects.all()
    
    for ligne in lignes_transfert:
        data['lignes_factures_transfert'].append({
            'id': ligne.id,
            'facture_transfert_id': ligne.facture_transfert.id if ligne.facture_transfert else None,
            'reference_article': ligne.article.reference_article if ligne.article else None,
            'designation': ligne.article.designation if ligne.article else None,
            'quantite': ligne.quantite,
            'prix_unitaire': str(ligne.prix_unitaire),
            'valeur_totale': str(ligne.valeur_totale),
        })
    
    # Export des Mouvements de Stock
    if agence_id:
        mouvements = MouvementStock.objects.filter(agence_id=agence_id)
    else:
        mouvements = MouvementStock.objects.all()
    
    for mouvement in mouvements:
        data['mouvements_stock'].append({
            'id': mouvement.id,
            'date_mouvement': mouvement.date_mouvement.isoformat() if mouvement.date_mouvement else None,
            'type_mouvement': mouvement.type_mouvement,
            'numero_piece': mouvement.numero_piece,
            'quantite_stock': str(mouvement.quantite_stock),
            'stock_initial': str(mouvement.stock_initial),
            'solde': str(mouvement.solde),
            'quantite': str(mouvement.quantite),
            'cout_moyen_pondere': str(mouvement.cout_moyen_pondere),
            'stock_permanent': str(mouvement.stock_permanent),
            'commentaire': mouvement.commentaire,
            'reference_article': mouvement.article.reference_article if mouvement.article else None,
            'agence_id': mouvement.agence.id_agence if mouvement.agence else None,
            'numero_employe': mouvement.employe.numero_employe if mouvement.employe else None,
            'fournisseur_id': mouvement.fournisseur.id if mouvement.fournisseur else None,
            'facture_vente_id': mouvement.facture_vente.id if mouvement.facture_vente else None,
            'facture_achat_id': mouvement.facture_achat.id if mouvement.facture_achat else None,
        })
    
    # Export des autres données si nécessaire
    # (InventaireStock, StatistiqueVente, TypeVente, PlanComptable, etc.)
    
    return data


def import_data(data, agence_id=None, clear_existing=False):
    """
    Importe les données depuis un fichier JSON
    
    Args:
        data: Dictionnaire contenant les données à importer
        agence_id: ID de l'agence cible (None pour utiliser les IDs du fichier)
        clear_existing: Si True, supprime les données existantes avant l'import
    
    Returns:
        dict: Résultat de l'import avec statistiques
    """
    # Détecter si on importe vers la même agence que celle exportée
    agence_source_id = data.get('agence_id')
    is_same_agence = (agence_id is not None and agence_source_id is not None and agence_id == agence_source_id)
    
    stats = {
        'agences': 0,
        'familles': 0,
        'comptes': 0,
        'employes': 0,
        'clients': 0,
        'fournisseurs': 0,
        'articles': 0,
        'caisses': 0,
        'sessions_caisse': 0,
        'factures_vente': 0,
        'lignes_factures_vente': 0,
        'factures_achat': 0,
        'lignes_factures_achat': 0,
        'documents_vente': 0,
        'factures_transfert': 0,
        'lignes_factures_transfert': 0,
        'mouvements_stock': 0,
        'types_vente': 0,
        'errors': [],
    }
    
    # Mapping des IDs pour gérer les références
    agence_map = {}  # ancien_id -> nouveau_id
    famille_map = {}  # ancien_code -> nouveau_code
    compte_map = {}  # ancien_numero -> nouveau_numero
    client_map = {}  # ancien_code -> nouveau_code
    fournisseur_map = {}  # ancien_code -> nouveau_code
    article_map = {}  # ancien_reference -> nouveau_reference
    caisse_map = {}  # ancien_numero -> nouveau_numero
    session_caisse_map = {}  # ancien_id -> nouveau_id
    facture_vente_map = {}  # ancien_id -> nouveau_id
    facture_achat_map = {}  # ancien_id -> nouveau_id
    facture_transfert_map = {}  # ancien_id -> nouveau_id
    
    # Utiliser savepoint pour permettre de continuer même en cas d'erreur partielle
    try:
        # 1. Import des Agences
        with transaction.atomic():
            for agence_data in data.get('agences', []):
                try:
                    agence, created = Agence.objects.get_or_create(
                        id_agence=agence_data['id_agence'],
                        defaults={
                            'nom_agence': agence_data['nom_agence'],
                            'adresse': agence_data.get('adresse', ''),
                        }
                    )
                    if not created:
                        agence.nom_agence = agence_data['nom_agence']
                        agence.adresse = agence_data.get('adresse', '')
                        agence.save()
                    agence_map[agence_data['id_agence']] = agence.id_agence
                    stats['agences'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import agence {agence_data.get('nom_agence', 'N/A')}: {str(e)}")
            
        # 2. Import des Familles
        with transaction.atomic():
            for famille_data in data.get('familles', []):
                try:
                    famille, created = Famille.objects.get_or_create(
                        code=famille_data['code'],
                        defaults={
                            'intitule': famille_data['intitule'],
                            'unite_vente': famille_data.get('unite_vente', ''),
                            'suivi_stock': famille_data.get('suivi_stock', True),
                        }
                    )
                    if not created:
                        famille.intitule = famille_data['intitule']
                        famille.unite_vente = famille_data.get('unite_vente', '')
                        famille.suivi_stock = famille_data.get('suivi_stock', True)
                        famille.save()
                    famille_map[famille_data['code']] = famille.code
                    stats['familles'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import famille {famille_data.get('code', 'N/A')}: {str(e)}")
            
            # 3. Import des Comptes (sans créer les utilisateurs Django - doit être fait manuellement)
            # Note: Les comptes nécessitent des utilisateurs Django, donc on les importe mais sans créer les users
            
        # 4. Import des Clients
        with transaction.atomic():
            for client_data in data.get('clients', []):
                try:
                    # Si une agence cible est spécifiée, l'utiliser directement
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(client_data.get('agence_id'))
                    
                    if not agence_id_import:
                        stats['errors'].append(f"Agence introuvable pour client {client_data.get('intitule', 'N/A')}")
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    # Utiliser intitule + agence comme clé unique au lieu de l'ID
                    # pour éviter les conflits d'ID entre agences
                    client, created = Client.objects.update_or_create(
                        intitule=client_data.get('intitule', ''),
                        agence=agence,
                        defaults={
                            'adresse': client_data.get('adresse', ''),
                            'telephone': client_data.get('telephone', ''),
                            'email': client_data.get('email', ''),
                        }
                    )
                    # Mapper l'ancien ID vers le nouvel ID pour les références
                    if client_data.get('id'):
                        client_map[client_data.get('id')] = client.id
                    stats['clients'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import client {client_data.get('intitule', 'N/A')}: {str(e)}")
            
        # 5. Import des Fournisseurs
        with transaction.atomic():
            for fournisseur_data in data.get('fournisseurs', []):
                try:
                    # Si une agence cible est spécifiée, l'utiliser directement
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(fournisseur_data.get('agence_id'))
                    
                    if not agence_id_import:
                        stats['errors'].append(f"Agence introuvable pour fournisseur {fournisseur_data.get('intitule', 'N/A')}")
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    # Utiliser intitule + agence comme clé unique au lieu de l'ID
                    # pour éviter les conflits d'ID entre agences
                    fournisseur, created = Fournisseur.objects.update_or_create(
                        intitule=fournisseur_data.get('intitule', ''),
                        agence=agence,
                        defaults={
                            'adresse': fournisseur_data.get('adresse', ''),
                            'telephone': fournisseur_data.get('telephone', ''),
                            'email': fournisseur_data.get('email', ''),
                        }
                    )
                    # Mapper l'ancien ID vers le nouvel ID pour les références
                    if fournisseur_data.get('id'):
                        fournisseur_map[fournisseur_data.get('id')] = fournisseur.id
                    stats['fournisseurs'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import fournisseur {fournisseur_data.get('intitule', 'N/A')}: {str(e)}")
            
        # 6. Import des Articles
        with transaction.atomic():
            for article_data in data.get('articles', []):
                try:
                    # Si une agence cible est spécifiée, l'utiliser directement
                    # Sinon, utiliser l'agence du JSON
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(article_data.get('agence_id'))
                    
                    if not agence_id_import:
                        stats['errors'].append(f"Agence introuvable pour article {article_data.get('reference_article', 'N/A')} (agence_id JSON: {article_data.get('agence_id')}, agence_id cible: {agence_id})")
                        continue
                    
                    famille_code = famille_map.get(article_data.get('categorie_code'))
                    if not famille_code:
                        famille_code = article_data.get('categorie_code')
                    
                    try:
                        famille = Famille.objects.get(code=famille_code)
                    except Famille.DoesNotExist:
                        stats['errors'].append(f"Famille introuvable {famille_code} pour article {article_data.get('reference_article', 'N/A')}")
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    
                    # Récupérer conditionnement avec valeur par défaut
                    conditionnement = article_data.get('conditionnement', '')
                    if not conditionnement:
                        conditionnement = 'Unité'  # Valeur par défaut
                    
                    reference_article = article_data['reference_article']
                    
                    # Si on importe vers la même agence que celle exportée, on met à jour les articles existants
                    # Sinon, on crée des copies avec des références modifiées
                    if is_same_agence:
                        # Même agence : mettre à jour ou créer dans cette agence
                        try:
                            existing_article = Article.objects.get(reference_article=reference_article, agence=agence)
                            # L'article existe dans cette agence, on met à jour
                            article = existing_article
                            article.designation = article_data.get('designation', '')
                            article.categorie = famille
                            article.suivi_stock = article_data.get('suivi_stock', True)
                            article.conditionnement = conditionnement
                            article.prix_achat = Decimal(str(article_data.get('prix_achat', '0')))
                            article.dernier_prix_achat = Decimal(str(article_data.get('dernier_prix_achat', '0')))
                            article.unite_vente = article_data.get('unite_vente', 'Unité')
                            article.prix_vente = Decimal(str(article_data.get('prix_vente', '0')))
                            # IMPORTANT: Mettre à jour le stock avec la valeur du fichier
                            article.stock_actuel = Decimal(str(article_data.get('stock_actuel', '0')))
                            article.stock_minimum = Decimal(str(article_data.get('stock_minimum', '0')))
                            # Le suivi de stock est toujours activé automatiquement lors de toute modification du stock
                            article.suivi_stock = True
                            article.save()
                            created = False
                            article_map[reference_article] = reference_article
                        except Article.DoesNotExist:
                            # L'article n'existe pas dans cette agence, on le crée
                            article = Article.objects.create(
                                reference_article=reference_article,
                                agence=agence,
                                designation=article_data.get('designation', ''),
                                categorie=famille,
                                suivi_stock=True,  # Toujours activé automatiquement
                                conditionnement=conditionnement,
                                prix_achat=Decimal(str(article_data.get('prix_achat', '0'))),
                                dernier_prix_achat=Decimal(str(article_data.get('dernier_prix_achat', '0'))),
                                unite_vente=article_data.get('unite_vente', 'Unité'),
                                prix_vente=Decimal(str(article_data.get('prix_vente', '0'))),
                                stock_actuel=Decimal(str(article_data.get('stock_actuel', '0'))),
                                stock_minimum=Decimal(str(article_data.get('stock_minimum', '0'))),
                            )
                            created = True
                            article_map[reference_article] = reference_article
                    else:
                        # Autre agence : vérifier si la référence existe globalement
                        try:
                            existing_article = Article.objects.get(reference_article=reference_article)
                            # Si l'article existe déjà dans la même agence cible, on met à jour
                            if existing_article.agence.id_agence == agence_id_import:
                                article = existing_article
                                article.designation = article_data.get('designation', '')
                                article.categorie = famille
                                # Le suivi de stock est toujours activé automatiquement
                                article.suivi_stock = True
                                article.conditionnement = conditionnement
                                article.prix_achat = Decimal(str(article_data.get('prix_achat', '0')))
                                article.dernier_prix_achat = Decimal(str(article_data.get('dernier_prix_achat', '0')))
                                article.unite_vente = article_data.get('unite_vente', 'Unité')
                                article.prix_vente = Decimal(str(article_data.get('prix_vente', '0')))
                                # IMPORTANT: Mettre à jour le stock avec la valeur du fichier
                                article.stock_actuel = Decimal(str(article_data.get('stock_actuel', '0')))
                                article.stock_minimum = Decimal(str(article_data.get('stock_minimum', '0')))
                                article.save()
                                created = False
                                article_map[reference_article] = reference_article
                            else:
                                # L'article existe dans une autre agence, on crée une copie avec une référence modifiée
                                agence_suffix = agence.nom_agence[:3].upper().replace(' ', '')
                                new_reference = f"{reference_article}_{agence_suffix}"
                                counter = 1
                                while Article.objects.filter(reference_article=new_reference).exists():
                                    new_reference = f"{reference_article}_{agence_suffix}{counter}"
                                    counter += 1
                                    if counter > 999:
                                        stats['errors'].append(f"Impossible de générer une référence unique pour {reference_article}")
                                        continue
                                
                                article = Article.objects.create(
                                    reference_article=new_reference,
                                    agence=agence,
                                    designation=article_data.get('designation', ''),
                                    categorie=famille,
                                    suivi_stock=article_data.get('suivi_stock', True),
                                    conditionnement=conditionnement,
                                    prix_achat=Decimal(str(article_data.get('prix_achat', '0'))),
                                    dernier_prix_achat=Decimal(str(article_data.get('dernier_prix_achat', '0'))),
                                    unite_vente=article_data.get('unite_vente', 'Unité'),
                                    prix_vente=Decimal(str(article_data.get('prix_vente', '0'))),
                                    stock_actuel=Decimal(str(article_data.get('stock_actuel', '0'))),
                                    stock_minimum=Decimal(str(article_data.get('stock_minimum', '0'))),
                                )
                                created = True
                                article_map[reference_article] = new_reference
                        except Article.DoesNotExist:
                            # L'article n'existe pas, on le crée avec la référence originale
                            article = Article.objects.create(
                                reference_article=reference_article,
                                agence=agence,
                                designation=article_data.get('designation', ''),
                                categorie=famille,
                                suivi_stock=True,  # Toujours activé automatiquement
                                conditionnement=conditionnement,
                                prix_achat=Decimal(str(article_data.get('prix_achat', '0'))),
                                dernier_prix_achat=Decimal(str(article_data.get('dernier_prix_achat', '0'))),
                                unite_vente=article_data.get('unite_vente', 'Unité'),
                                prix_vente=Decimal(str(article_data.get('prix_vente', '0'))),
                                stock_actuel=Decimal(str(article_data.get('stock_actuel', '0'))),
                                stock_minimum=Decimal(str(article_data.get('stock_minimum', '0'))),
                            )
                            created = True
                            article_map[reference_article] = reference_article
                    
                    # S'assurer que le mapping est correct pour les références
                    if reference_article not in article_map:
                        article_map[reference_article] = article.reference_article
                    stats['articles'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import article {article_data.get('reference_article', 'N/A')}: {str(e)}")
            
        # 7. Import des Types de Vente (doit venir après les articles)
        with transaction.atomic():
            for type_data in data.get('types_vente', []):
                try:
                    reference_article = type_data.get('reference_article')
                    if not reference_article:
                        continue
                    
                    mapped_reference = article_map.get(reference_article, reference_article)
                    try:
                        article = Article.objects.get(reference_article=mapped_reference)
                    except Article.DoesNotExist:
                        # Essayer la référence originale si aucune correspondance trouvée
                        try:
                            article = Article.objects.get(reference_article=reference_article)
                        except Article.DoesNotExist:
                            stats['errors'].append(f"Article introuvable pour type de vente {type_data.get('intitule', 'N/A')} ({reference_article})")
                            continue
                    
                    TypeVente.objects.update_or_create(
                        article=article,
                        intitule=type_data.get('intitule', ''),
                        defaults={
                            'prix': Decimal(str(type_data.get('prix', '0'))),
                        }
                    )
                    stats['types_vente'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import type de vente {type_data.get('intitule', 'N/A')}: {str(e)}")
        
        # 8. Import des Caisses
        with transaction.atomic():
            for caisse_data in data.get('caisses', []):
                try:
                    # Si une agence cible est spécifiée, l'utiliser directement
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(caisse_data.get('agence_id'))
                    
                    if not agence_id_import:
                        stats['errors'].append(f"Agence introuvable pour caisse {caisse_data.get('numero_caisse', 'N/A')}")
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    # Utiliser update_or_create pour mettre à jour si la caisse existe déjà
                    caisse_defaults = {
                        'nom_caisse': caisse_data.get('nom_caisse', ''),
                        'solde_initial': Decimal(str(caisse_data.get('solde_initial', '0'))),
                        'solde_actuel': Decimal(str(caisse_data.get('solde_actuel', '0'))),
                        'statut': caisse_data.get('statut', 'fermee'),
                        'agence': agence,
                        'date_ouverture': parse_iso_datetime(caisse_data.get('date_ouverture')),
                        'date_fermeture': parse_iso_datetime(caisse_data.get('date_fermeture')),
                    }
                    
                    caisse, created = Caisse.objects.update_or_create(
                        numero_caisse=caisse_data['numero_caisse'],
                        defaults=caisse_defaults
                    )
                    caisse_map[caisse_data['numero_caisse']] = caisse.numero_caisse
                    stats['caisses'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import caisse {caisse_data.get('numero_caisse', 'N/A')}: {str(e)}")

        # 9. Import des Sessions de Caisse
        with transaction.atomic():
            for session_data in data.get('sessions_caisse', []):
                try:
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(session_data.get('agence_id'))
                    
                    if not agence_id_import:
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    caisse = None
                    if session_data.get('numero_caisse'):
                        mapped_caisse = caisse_map.get(session_data['numero_caisse'], session_data['numero_caisse'])
                        caisse = Caisse.objects.filter(numero_caisse=mapped_caisse).first()
                        if caisse and caisse.agence != agence:
                            caisse.agence = agence
                            caisse.save()
                    if not caisse:
                        caisse = Caisse.objects.filter(agence=agence).first()
                    if not caisse:
                        stats['errors'].append(f"Aucune caisse disponible pour la session {session_data.get('id')}")
                        continue
                    
                    session = SessionCaisse.objects.create(
                        caisse=caisse,
                        agence=agence,
                        solde_ouverture=Decimal(str(session_data.get('solde_ouverture', '0'))),
                        solde_fermeture=Decimal(str(session_data.get('solde_fermeture', '0'))) if session_data.get('solde_fermeture') else None,
                        statut=session_data.get('statut', 'fermee'),
                        date_ouverture=parse_iso_datetime(session_data.get('date_ouverture')),
                        date_fermeture=parse_iso_datetime(session_data.get('date_fermeture')),
                    )
                    session_caisse_map[session_data['id']] = session.id
                    stats['sessions_caisse'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import session caisse {session_data.get('id', 'N/A')}: {str(e)}")
        
        # 10. Import des Documents de Vente
        with transaction.atomic():
            for document_data in data.get('documents_vente', []):
                try:
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(document_data.get('agence_id'))
                    
                    if not agence_id_import:
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    session = None
                    if document_data.get('session_caisse_id'):
                        mapped_session_id = session_caisse_map.get(document_data['session_caisse_id'])
                        if mapped_session_id:
                            session = SessionCaisse.objects.filter(id=mapped_session_id).first()
                    
                    document_defaults = {
                        'date': parse_iso_date(document_data.get('date')) or datetime.now().date(),
                        'heure_fermeture': parse_iso_datetime(document_data.get('heure_fermeture')) or datetime.now(),
                        'session_caisse': session,
                        'vendeuse_nom': document_data.get('vendeuse_nom', ''),
                        'nombre_factures': document_data.get('nombre_factures', 0) or 0,
                        'total_articles': document_data.get('total_articles', 0) or 0,
                        'chiffre_affaires': Decimal(str(document_data.get('chiffre_affaires', '0'))),
                        'factures_data': document_data.get('factures_data', {}),
                        'agence': agence,
                    }
                    
                    DocumentVente.objects.update_or_create(
                        numero_document=document_data.get('numero_document', ''),
                        defaults=document_defaults
                    )
                    stats['documents_vente'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import document vente {document_data.get('numero_document', 'N/A')}: {str(e)}")
        
        # 11. Import des Factures de Vente
        with transaction.atomic():
            for facture_data in data.get('factures_vente', []):
                try:
                    # Si une agence cible est spécifiée, l'utiliser directement
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(facture_data.get('agence_id'))
                    
                    if not agence_id_import:
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    caisse = None
                    numero_caisse = facture_data.get('numero_caisse')
                    if numero_caisse:
                        mapped_caisse = caisse_map.get(numero_caisse, numero_caisse)
                        caisse = Caisse.objects.filter(numero_caisse=mapped_caisse).first()
                        if caisse and caisse.agence != agence:
                            caisse.agence = agence
                            caisse.save()
                    if not caisse:
                        caisse = Caisse.objects.filter(agence=agence).first()
                    
                    client = None
                    if facture_data.get('client_id'):
                        mapped_client_id = client_map.get(facture_data['client_id'])
                        if mapped_client_id:
                            client = Client.objects.filter(id=mapped_client_id).first()
                        if not client:
                            client = Client.objects.filter(intitule__iexact=facture_data.get('client_nom', ''), agence=agence).first()
                    if not client:
                        client = Client.objects.filter(agence=agence).first()
                    if not client:
                        client = Client.objects.create(
                            intitule=f"Client importé {facture_data.get('numero_ticket', '')}",
                            adresse='',
                            telephone='',
                            email='',
                            agence=agence
                        )
                    
                    session_caisse = None
                    if facture_data.get('session_caisse_id'):
                        mapped_session_id = session_caisse_map.get(facture_data['session_caisse_id'])
                        if mapped_session_id:
                            session_caisse = SessionCaisse.objects.filter(id=mapped_session_id).first()
                    
                    facture_defaults = {
                        'date': parse_iso_date(facture_data.get('date')),
                        'heure': parse_iso_time(facture_data.get('heure')),
                        'remise': Decimal(facture_data.get('remise', '0')) if facture_data.get('remise') else Decimal('0'),
                        'nette_a_payer': Decimal(facture_data.get('nette_a_payer', '0')),
                        'montant_regler': Decimal(facture_data.get('montant_regler', '0')) if facture_data.get('montant_regler') else Decimal('0'),
                        'rendu': Decimal(facture_data.get('rendu', '0')) if facture_data.get('rendu') else Decimal('0'),
                        'en_attente': facture_data.get('en_attente', False),
                        'nom_vendeuse': facture_data.get('nom_vendeuse', ''),
                        'caisse': caisse,
                        'client': client,
                        'agence': agence,
                        'session_caisse': session_caisse,
                    }
                    facture, _ = FactureVente.objects.update_or_create(
                        numero_ticket=facture_data.get('numero_ticket', ''),
                        defaults=facture_defaults
                    )
                    facture_vente_map[facture_data['id']] = facture.id
                    stats['factures_vente'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import facture vente {facture_data.get('numero_ticket', 'N/A')}: {str(e)}")
            
        # 12. Import des Lignes de Factures de Vente
        with transaction.atomic():
            for ligne_data in data.get('lignes_factures_vente', []):
                try:
                    facture_id = facture_vente_map.get(ligne_data.get('facture_vente_id'))
                    if not facture_id:
                        continue
                    
                    facture = FactureVente.objects.get(id=facture_id)
                    article = None
                    if ligne_data.get('reference_article'):
                        # Utiliser le mapping pour trouver la nouvelle référence si elle a été modifiée
                        reference_article = article_map.get(ligne_data['reference_article'], ligne_data['reference_article'])
                        try:
                            article = Article.objects.get(reference_article=reference_article, agence=facture.agence)
                        except Article.DoesNotExist:
                            # Essayer avec la référence originale si le mapping n'existe pas
                            try:
                                article = Article.objects.get(reference_article=ligne_data['reference_article'], agence=facture.agence)
                            except Article.DoesNotExist:
                                pass
                    
                    LigneFactureVente.objects.create(
                        facture_vente=facture,
                        article=article,
                        designation=ligne_data.get('designation', ''),
                        quantite=Decimal(str(ligne_data.get('quantite', '0'))),
                        prix_unitaire=Decimal(str(ligne_data.get('prix_unitaire', '0'))),
                        prix_total=Decimal(str(ligne_data.get('prix_total', '0'))),
                    )
                    stats['lignes_factures_vente'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import ligne facture vente: {str(e)}")
            
        # 13. Import des Mouvements de Stock
        with transaction.atomic():
            for mouvement_data in data.get('mouvements_stock', []):
                try:
                    # Si une agence cible est spécifiée, l'utiliser directement
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(mouvement_data.get('agence_id'))
                    
                    if not agence_id_import:
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    article = None
                    if mouvement_data.get('reference_article'):
                        # Utiliser le mapping pour trouver la nouvelle référence si elle a été modifiée
                        reference_article = article_map.get(mouvement_data['reference_article'], mouvement_data['reference_article'])
                        try:
                            article = Article.objects.get(reference_article=reference_article, agence=agence)
                        except Article.DoesNotExist:
                            # Essayer avec la référence originale si le mapping n'existe pas
                            try:
                                article = Article.objects.get(reference_article=mouvement_data['reference_article'], agence=agence)
                            except Article.DoesNotExist:
                                continue
                    
                    # Ne pas créer de mouvement de stock si l'article n'existe pas
                    if not article:
                        continue
                    
                    MouvementStock.objects.create(
                        article=article,
                        agence=agence,
                        date_mouvement=datetime.fromisoformat(mouvement_data['date_mouvement']) if mouvement_data.get('date_mouvement') else datetime.now(),
                        type_mouvement=mouvement_data.get('type_mouvement', 'entree'),
                        numero_piece=mouvement_data.get('numero_piece', ''),
                        quantite_stock=Decimal(str(mouvement_data.get('quantite_stock', '0'))),
                        stock_initial=Decimal(str(mouvement_data.get('stock_initial', '0'))),
                        solde=Decimal(str(mouvement_data.get('solde', '0'))),
                        quantite=Decimal(str(mouvement_data.get('quantite', '0'))),
                        cout_moyen_pondere=Decimal(str(mouvement_data.get('cout_moyen_pondere', '0'))),
                        stock_permanent=Decimal(str(mouvement_data.get('stock_permanent', '0'))),
                        commentaire=mouvement_data.get('commentaire', ''),
                    )
                    stats['mouvements_stock'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import mouvement stock: {str(e)}")
        
        # 14. Import des Factures d'Achat
        with transaction.atomic():
            for facture_data in data.get('factures_achat', []):
                try:
                    # Si une agence cible est spécifiée, l'utiliser directement
                    if agence_id:
                        agence_id_import = agence_id
                    else:
                        agence_id_import = agence_map.get(facture_data.get('agence_id'))
                    
                    if not agence_id_import:
                        continue
                    
                    agence = Agence.objects.get(id_agence=agence_id_import)
                    fournisseur = None
                    if facture_data.get('fournisseur_id'):
                        fournisseur_id = fournisseur_map.get(facture_data['fournisseur_id'])
                        if fournisseur_id:
                            fournisseur = Fournisseur.objects.filter(id=fournisseur_id).first()
                        if not fournisseur:
                            fournisseur = Fournisseur.objects.filter(intitule__iexact=facture_data.get('fournisseur_nom', ''), agence=agence).first()
                    if not fournisseur:
                        fournisseur = Fournisseur.objects.filter(agence=agence).first()
                    if not fournisseur:
                        fournisseur = Fournisseur.objects.create(
                            intitule=f"Fournisseur importé {facture_data.get('reference_achat', '')}",
                            adresse='',
                            telephone='',
                            email='',
                            agence=agence
                        )
                    
                    facture_defaults = {
                        'numero_fournisseur': facture_data.get('numero_fournisseur', ''),
                        'date_achat': parse_iso_date(facture_data.get('date_achat')),
                        'heure': parse_iso_time(facture_data.get('heure')),
                        'prix_total_global': Decimal(str(facture_data.get('prix_total_global', '0'))),
                        'statut': facture_data.get('statut', 'en_attente'),
                        'commentaire': facture_data.get('commentaire', ''),
                        'fournisseur': fournisseur,
                        'agence': agence,
                    }
                    facture, _ = FactureAchat.objects.update_or_create(
                        reference_achat=facture_data.get('reference_achat', ''),
                        defaults=facture_defaults
                    )
                    facture_achat_map[facture_data['id']] = facture.id
                    stats['factures_achat'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import facture achat {facture_data.get('reference_achat', 'N/A')}: {str(e)}")
            
            # 15. Import des Lignes de Factures d'Achat
            for ligne_data in data.get('lignes_factures_achat', []):
                try:
                    facture_id = facture_achat_map.get(ligne_data.get('facture_achat_id'))
                    if not facture_id:
                        continue
                    
                    facture = FactureAchat.objects.get(id=facture_id)
                    article = None
                    if ligne_data.get('reference_article'):
                        # Utiliser le mapping pour trouver la nouvelle référence si elle a été modifiée
                        reference_article = article_map.get(ligne_data['reference_article'], ligne_data['reference_article'])
                        try:
                            article = Article.objects.get(reference_article=reference_article, agence=facture.agence)
                        except Article.DoesNotExist:
                            # Essayer avec la référence originale si le mapping n'existe pas
                            try:
                                article = Article.objects.get(reference_article=ligne_data['reference_article'], agence=facture.agence)
                            except Article.DoesNotExist:
                                pass
                    
                    LigneFactureAchat.objects.create(
                        facture_achat=facture,
                        article=article,
                        reference_article=ligne_data.get('reference_article', ''),
                        designation=ligne_data.get('designation', ''),
                        quantite=Decimal(str(ligne_data.get('quantite', '0'))),
                        prix_unitaire=Decimal(str(ligne_data.get('prix_unitaire', '0'))),
                        prix_total_article=Decimal(str(ligne_data.get('prix_total_article', '0'))),
                    )
                    stats['lignes_factures_achat'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import ligne facture achat: {str(e)}")

        # 16. Import des Factures de Transfert
        with transaction.atomic():
            for transfert_data in data.get('factures_transfert', []):
                try:
                    if agence_id:
                        agence_source_id = agence_id
                        agence_destination_id = agence_id
                    else:
                        agence_source_id = agence_map.get(transfert_data.get('agence_source_id'))
                        agence_destination_id = agence_map.get(transfert_data.get('agence_destination_id'))
                    
                    # Au moins une des deux agences doit être disponible
                    if not agence_source_id and not agence_destination_id:
                        continue
                    
                    agence_source = Agence.objects.filter(id_agence=agence_source_id).first()
                    agence_destination = Agence.objects.filter(id_agence=agence_destination_id).first()
                    
                    employe_expediteur = None
                    if transfert_data.get('numero_employe_expediteur'):
                        employe_expediteur = Employe.objects.filter(numero_employe=transfert_data['numero_employe_expediteur']).first()
                    
                    employe_destinataire = None
                    if transfert_data.get('numero_employe_destinataire'):
                        employe_destinataire = Employe.objects.filter(numero_employe=transfert_data['numero_employe_destinataire']).first()
                    
                    transfert_defaults = {
                        'numero_compte': transfert_data.get('numero_compte', ''),
                        'date_transfert': parse_iso_date(transfert_data.get('date_transfert')),
                        'lieu_depart': transfert_data.get('lieu_depart', ''),
                        'lieu_arrivee': transfert_data.get('lieu_arrivee', ''),
                        'quantite': transfert_data.get('quantite', 0) or 0,
                        'statut': transfert_data.get('statut', 'en_attente'),
                        'etat': transfert_data.get('etat', 'entrer'),
                        'commentaire': transfert_data.get('commentaire', ''),
                        'agence_source': agence_source or agence_destination,
                        'agence_destination': agence_destination or agence_source,
                        'employe_expediteur': employe_expediteur,
                        'employe_destinataire': employe_destinataire,
                    }
                    
                    transfert, _ = FactureTransfert.objects.update_or_create(
                        reference_transfert=transfert_data.get('reference_transfert', ''),
                        defaults=transfert_defaults
                    )
                    facture_transfert_map[transfert_data['id']] = transfert.id
                    stats['factures_transfert'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import facture transfert {transfert_data.get('reference_transfert', 'N/A')}: {str(e)}")
        
        # 17. Import des Lignes de Factures de Transfert
        with transaction.atomic():
            for ligne_data in data.get('lignes_factures_transfert', []):
                try:
                    transfert_id = facture_transfert_map.get(ligne_data.get('facture_transfert_id'))
                    if not transfert_id:
                        continue
                    
                    transfert = FactureTransfert.objects.get(id=transfert_id)
                    article = None
                    if ligne_data.get('reference_article'):
                        reference_article = article_map.get(ligne_data['reference_article'], ligne_data['reference_article'])
                        article = Article.objects.filter(reference_article=reference_article).first()
                        if not article:
                            article = Article.objects.filter(reference_article=ligne_data['reference_article']).first()
                    if not article:
                        continue
                    
                    LigneFactureTransfert.objects.update_or_create(
                        facture_transfert=transfert,
                        article=article,
                        defaults={
                            'quantite': ligne_data.get('quantite', 0) or 0,
                            'prix_unitaire': Decimal(str(ligne_data.get('prix_unitaire', '0'))),
                            'valeur_totale': Decimal(str(ligne_data.get('valeur_totale', '0'))),
                        }
                    )
                    stats['lignes_factures_transfert'] += 1
                except Exception as e:
                    stats['errors'].append(f"Erreur import ligne facture transfert: {str(e)}")
    
    except Exception as e:
        stats['errors'].append(f"Erreur générale lors de l'import: {str(e)}")
        raise
    
    return stats

