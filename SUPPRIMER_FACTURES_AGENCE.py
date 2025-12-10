import os
import sys
import django
from django.db import transaction

# Préparer Django
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
django.setup()

from supermarket.models import (  # noqa: E402
    Agence,
    FactureVente,
    LigneFactureVente,
    FactureAchat,
    LigneFactureAchat,
    FactureTransfert,
    LigneFactureTransfert,
    DocumentVente,
)


def afficher_resume_agences():
    print("============================================================")
    print("       SUPPRESSION DES FACTURES PAR AGENCE")
    print("============================================================")
    print("ID | Agence                | Ventes | Achats | Transferts")
    print("------------------------------------------------------------")
    for ag in Agence.objects.all().order_by('nom_agence'):
        nb_ventes = FactureVente.objects.filter(agence=ag).count()
        nb_achats = FactureAchat.objects.filter(agence=ag).count()
        nb_transferts = FactureTransfert.objects.filter(
            agence_source=ag
        ).count() + FactureTransfert.objects.filter(agence_destination=ag).count()
        print(f"{ag.id_agence:>2} | {ag.nom_agence:<20} | {nb_ventes:>6} | {nb_achats:>6} | {nb_transferts:>9}")
    print("------------------------------------------------------------")


def supprimer_factures_agence():
    afficher_resume_agences()
    choix = input("Entrez l'ID de l'agence ciblée (ou 'ANNULER'): ").strip()
    if choix.upper() == "ANNULER":
        print("Opération annulée.")
        return

    try:
        agence_id = int(choix)
        agence = Agence.objects.get(id_agence=agence_id)
    except (ValueError, Agence.DoesNotExist):
        print("❌ ID d'agence invalide.")
        return

    nb_ventes = FactureVente.objects.filter(agence=agence).count()
    nb_achats = FactureAchat.objects.filter(agence=agence).count()
    nb_transferts_source = FactureTransfert.objects.filter(agence_source=agence).count()
    nb_transferts_destination = FactureTransfert.objects.filter(agence_destination=agence).count()
    nb_docs_vente = DocumentVente.objects.filter(agence=agence).count()

    print("\n============================================================")
    print(f"Agence ciblée : {agence.nom_agence}")
    print(f" - Factures de vente      : {nb_ventes}")
    print(f" - Factures d'achat       : {nb_achats}")
    print(f" - Factures transfert (S) : {nb_transferts_source}")
    print(f" - Factures transfert (D) : {nb_transferts_destination}")
    print(f" - Documents de vente     : {nb_docs_vente}")
    print("============================================================")

    confirmation = input("Taper OUI (en majuscules) pour confirmer la suppression: ").strip()
    if confirmation != "OUI":
        print("Opération annulée.")
        return

    with transaction.atomic():
        # Factures de vente
        LigneFactureVente.objects.filter(facture_vente__agence=agence).delete()
        FactureVente.objects.filter(agence=agence).delete()
        DocumentVente.objects.filter(agence=agence).delete()

        # Factures d'achat
        LigneFactureAchat.objects.filter(facture_achat__agence=agence).delete()
        FactureAchat.objects.filter(agence=agence).delete()

        # Factures de transfert (source ou destination)
        LigneFactureTransfert.objects.filter(
            facture_transfert__agence_source=agence
        ).delete()
        LigneFactureTransfert.objects.filter(
            facture_transfert__agence_destination=agence
        ).delete()
        FactureTransfert.objects.filter(agence_source=agence).delete()
        FactureTransfert.objects.filter(agence_destination=agence).delete()

    print("✅ Toutes les factures et documents liés à cette agence ont été supprimés.")


if __name__ == "__main__":
    supprimer_factures_agence()








