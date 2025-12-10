"""
Script standalone pour exporter les données depuis une ancienne version
et les importer dans une nouvelle version avec fonctionnalité export/import

Usage:
    python EXPORT_DONNEES_STANDALONE.py
    
Le script va:
1. Se connecter à la base de données actuelle
2. Exporter toutes les données au format JSON
3. Créer un fichier export_erp_standalone_YYYYMMDD_HHMMSS.json

Pour importer dans la nouvelle version:
1. Aller sur /supermarket/export-import/
2. Cliquer sur "Importer des Données"
3. Sélectionner le fichier JSON généré
"""

import os
import sys
import django
from datetime import datetime
import json
from decimal import Decimal

# Configuration du chemin Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

# Import des modèles après la configuration Django
from supermarket.models import (
    Agence, Famille, Compte, Employe, Client, Fournisseur,
    Article, Caisse, SessionCaisse, FactureVente, LigneFactureVente,
    FactureAchat, LigneFactureAchat, FactureTransfert, LigneFactureTransfert,
    MouvementStock, InventaireStock, StatistiqueVente, TypeVente,
    PlanComptable, PlanTiers, CodeJournaux, TauxTaxe
)
from django.db.models import Q


class DecimalEncoder(json.JSONEncoder):
    """Encoder personnalisé pour gérer les Decimal en JSON"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def export_all_data(agence_id=None):
    """
    Exporte les données de l'ERP au format JSON
    
    Args:
        agence_id: ID de l'agence à exporter (None pour toutes les agences)
    """
    
    print("=" * 60)
    print("EXPORT DES DONNÉES ERP - VERSION STANDALONE")
    print("=" * 60)
    print()
    
    if agence_id:
        try:
            agence = Agence.objects.get(id_agence=agence_id)
            print(f"📌 Export des données de l'agence: {agence.nom_agence} (ID: {agence.id_agence})")
        except Agence.DoesNotExist:
            print(f"⚠️  Agence ID {agence_id} introuvable. Export de toutes les agences.")
            agence_id = None
    else:
        print("📌 Export de toutes les agences")
    print()
    
    data = {
        'version': '1.0',
        'date_export': datetime.now().isoformat(),
        'source': 'standalone_export_script',
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
        'lignes_factures_vente': [],
        'factures_achat': [],
        'lignes_factures_achat': [],
        'factures_transfert': [],
        'lignes_factures_transfert': [],
        'mouvements_stock': [],
    }
    
    # Export des Agences
    print("📦 Export des Agences...")
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
    print(f"   ✓ {len(data['agences'])} agence(s) exportée(s)")
    
    # Export des Familles (toutes, pas liées à une agence)
    print("📦 Export des Familles...")
    for famille in Famille.objects.all():
        data['familles'].append({
            'code': famille.code,
            'intitule': famille.intitule,
            'unite_vente': famille.unite_vente,
            'suivi_stock': famille.suivi_stock,
        })
    print(f"   ✓ {len(data['familles'])} famille(s) exportée(s)")
    
    # Export des Comptes
    print("📦 Export des Comptes...")
    if agence_id:
        comptes = Compte.objects.filter(actif=True, agence_id=agence_id)
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
        })
    print(f"   ✓ {len(data['comptes'])} compte(s) exporté(s)")
    
    # Export des Employés
    print("📦 Export des Employés...")
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
            'numero_compte': employe.compte.numero_compte if employe.compte else None,
        })
    print(f"   ✓ {len(data['employes'])} employé(s) exporté(s)")
    
    # Export des Clients
    print("📦 Export des Clients...")
    if agence_id:
        clients = Client.objects.filter(agence_id=agence_id)
    else:
        clients = Client.objects.all()
    for client in clients:
        data['clients'].append({
            'id': client.id,
            'intitule': client.intitule,
            'adresse': client.adresse,
            'telephone': client.telephone,
            'email': client.email,
            'agence_id': client.agence.id_agence if client.agence else None,
        })
    print(f"   ✓ {len(data['clients'])} client(s) exporté(s)")
    
    # Export des Fournisseurs
    print("📦 Export des Fournisseurs...")
    if agence_id:
        fournisseurs = Fournisseur.objects.filter(agence_id=agence_id)
    else:
        fournisseurs = Fournisseur.objects.all()
    for fournisseur in fournisseurs:
        data['fournisseurs'].append({
            'id': fournisseur.id,
            'intitule': fournisseur.intitule,
            'adresse': fournisseur.adresse,
            'telephone': fournisseur.telephone,
            'email': fournisseur.email,
            'agence_id': fournisseur.agence.id_agence if fournisseur.agence else None,
        })
    print(f"   ✓ {len(data['fournisseurs'])} fournisseur(s) exporté(s)")
    
    # Export des Articles
    print("📦 Export des Articles...")
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
            'conditionnement': article.conditionnement if hasattr(article, 'conditionnement') else None,
            'prix_achat': str(article.prix_achat),
            'dernier_prix_achat': str(article.dernier_prix_achat),
            'unite_vente': article.unite_vente,
            'prix_vente': str(article.prix_vente),
            'stock_actuel': str(article.stock_actuel),
            'stock_minimum': str(article.stock_minimum),
            'date_creation': article.date_creation.isoformat() if article.date_creation else None,
            'agence_id': article.agence.id_agence if article.agence else None,
        })
    print(f"   ✓ {len(data['articles'])} article(s) exporté(s)")
    
    # Export des Types de Vente
    print("📦 Export des Types de Vente...")
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
    print(f"   ✓ {len(data['types_vente'])} type(s) de vente exporté(s)")
    
    # Export des Caisses
    print("📦 Export des Caisses...")
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
    print(f"   ✓ {len(data['caisses'])} caisse(s) exportée(s)")
    
    # Export des Sessions de Caisse
    print("📦 Export des Sessions de Caisse...")
    if agence_id:
        sessions = SessionCaisse.objects.filter(agence_id=agence_id)
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
    print(f"   ✓ {len(data['sessions_caisse'])} session(s) exportée(s)")
    
    # Export des Factures de Vente
    print("📦 Export des Factures de Vente...")
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
    print(f"   ✓ {len(data['factures_vente'])} facture(s) de vente exportée(s)")
    
    # Export des Lignes de Factures de Vente
    print("📦 Export des Lignes de Factures de Vente...")
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
    print(f"   ✓ {len(data['lignes_factures_vente'])} ligne(s) exportée(s)")
    
    # Export des Factures d'Achat
    print("📦 Export des Factures d'Achat...")
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
    print(f"   ✓ {len(data['factures_achat'])} facture(s) d'achat exportée(s)")
    
    # Export des Lignes de Factures d'Achat
    print("📦 Export des Lignes de Factures d'Achat...")
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
    print(f"   ✓ {len(data['lignes_factures_achat'])} ligne(s) exportée(s)")
    
    # Export des Factures de Transfert
    print("📦 Export des Factures de Transfert...")
    if agence_id:
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
    print(f"   ✓ {len(data['factures_transfert'])} facture(s) de transfert exportée(s)")
    
    # Export des Lignes de Factures de Transfert
    print("📦 Export des Lignes de Factures de Transfert...")
    if agence_id:
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
    print(f"   ✓ {len(data['lignes_factures_transfert'])} ligne(s) exportée(s)")
    
    # Export des Mouvements de Stock
    print("📦 Export des Mouvements de Stock...")
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
            'facture_transfert_id': mouvement.facture_transfert.id if mouvement.facture_transfert else None,
            'inventaire_id': mouvement.inventaire.id if mouvement.inventaire else None,
        })
    print(f"   ✓ {len(data['mouvements_stock'])} mouvement(s) exporté(s)")
    
    # Créer le nom du fichier avec timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if agence_id:
        try:
            agence_nom = Agence.objects.get(id_agence=agence_id).nom_agence.replace(' ', '_')
            filename = f'export_erp_standalone_{agence_nom}_{timestamp}.json'
        except:
            filename = f'export_erp_standalone_agence_{agence_id}_{timestamp}.json'
    else:
        filename = f'export_erp_standalone_toutes_agences_{timestamp}.json'
    
    # Obtenir le chemin complet du fichier
    filepath = os.path.join(BASE_DIR, filename)
    filepath_abs = os.path.abspath(filepath)
    
    # Sauvegarder le fichier JSON
    print()
    print("💾 Sauvegarde du fichier JSON...")
    with open(filepath_abs, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, cls=DecimalEncoder)
    
    file_size = os.path.getsize(filepath_abs) / (1024 * 1024)  # Taille en MB
    print(f"   ✓ Fichier créé: {filename}")
    print(f"   ✓ Taille: {file_size:.2f} MB")
    print(f"   ✓ Emplacement: {filepath_abs}")
    
    # Afficher le résumé
    print()
    print("=" * 60)
    print("EXPORT TERMINÉ AVEC SUCCÈS!")
    print("=" * 60)
    print()
    print("📊 RÉSUMÉ DE L'EXPORT:")
    print(f"   • Agences: {len(data['agences'])}")
    print(f"   • Familles: {len(data['familles'])}")
    print(f"   • Articles: {len(data['articles'])}")
    print(f"   • Clients: {len(data['clients'])}")
    print(f"   • Fournisseurs: {len(data['fournisseurs'])}")
    print(f"   • Types de vente: {len(data['types_vente'])}")
    print(f"   • Factures de vente: {len(data['factures_vente'])}")
    print(f"   • Factures d'achat: {len(data['factures_achat'])}")
    print(f"   • Factures de transfert: {len(data['factures_transfert'])}")
    print(f"   • Mouvements de stock: {len(data['mouvements_stock'])}")
    print()
    print("📝 PROCHAINES ÉTAPES:")
    print("   1. Installer la nouvelle version avec fonctionnalité export/import")
    print("   2. Aller sur /supermarket/export-import/")
    print("   3. Cliquer sur 'Importer des Données'")
    print(f"   4. Sélectionner le fichier: {filename}")
    print(f"      (Chemin complet: {filepath_abs})")
    print("   5. Choisir les options d'import et valider")
    print()
    print("=" * 60)
    
    return filepath_abs


if __name__ == '__main__':
    import argparse
    
    # Parser les arguments de ligne de commande
    parser = argparse.ArgumentParser(description='Exporter les données ERP au format JSON')
    parser.add_argument('--agence-id', type=int, help='ID de l\'agence à exporter (optionnel)')
    args = parser.parse_args()
    
    try:
        export_all_data(agence_id=args.agence_id)
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERREUR LORS DE L'EXPORT")
        print("=" * 60)
        print(f"Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

