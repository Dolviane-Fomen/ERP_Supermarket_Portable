"""
Script pour créer des factures pour les commandes de l'agence 7 qui n'ont pas encore de facture
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Commande, FactureCommande, Agence
from django.db.models import Q
from datetime import datetime
from django.utils import timezone

# Récupérer l'agence 7
agence_7 = Agence.objects.get(id_agence=7)
print(f"Agence: {agence_7.nom_agence} (ID: {agence_7.id_agence})")

# Récupérer toutes les commandes de l'agence 7
commandes_agence_7 = Commande.objects.filter(agence=agence_7).order_by('date', 'heure', 'client')

# Grouper les commandes par (client, date, heure)
groupes = {}
for commande in commandes_agence_7:
    key = (commande.client.id, commande.date, commande.heure)
    if key not in groupes:
        groupes[key] = []
    groupes[key].append(commande)

print(f"\nNombre de groupes de commandes: {len(groupes)}")

# Pour chaque groupe, vérifier s'il existe déjà une facture
factures_creees = 0
for key, commandes_groupe in groupes.items():
    client_id, date_commande, heure_commande = key
    
    # Vérifier si une facture existe déjà pour ce groupe
    facture_existante = FactureCommande.objects.filter(
        commande__client_id=client_id,
        commande__date=date_commande,
        commande__heure=heure_commande,
        agence=agence_7
    ).first()
    
    if not facture_existante:
        # Créer une facture pour ce groupe
        premiere_commande = commandes_groupe[0]
        
        # Générer un numéro de facture unique
        date_str = date_commande.strftime('%Y%m%d')
        numero_facture = f"FAC{date_str}{len(commandes_groupe):03d}"
        
        # Vérifier l'unicité du numéro
        compteur = 1
        while FactureCommande.objects.filter(numero_facture=numero_facture).exists():
            numero_facture = f"FAC{date_str}{len(commandes_groupe):03d}-{compteur}"
            compteur += 1
        
        # Récupérer l'heure
        if isinstance(heure_commande, str):
            heure_obj = datetime.strptime(heure_commande, '%H:%M').time()
        else:
            heure_obj = heure_commande if hasattr(heure_commande, 'hour') else timezone.now().time()
        
        # Calculer le prix total du groupe
        from decimal import Decimal
        prix_total_groupe = sum(Decimal(str(c.prix_total)) for c in commandes_groupe)
        
        try:
            facture = FactureCommande.objects.create(
                commande=premiere_commande,
                numero_facture=numero_facture,
                date=date_commande,
                heure=heure_obj,
                agence=agence_7,
                prix_total=prix_total_groupe,
                net_a_payer=prix_total_groupe  # Par défaut, net à payer = prix total
            )
            factures_creees += 1
            print(f"✓ Facture créée: {numero_facture} pour {premiere_commande.client.intitule} le {date_commande} (Total: {prix_total_groupe} FCFA)")
        except Exception as e:
            print(f"✗ Erreur lors de la création de la facture: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print(f"- Facture déjà existante: {facture_existante.numero_facture}")

print(f"\nTotal factures créées: {factures_creees}")
print(f"Total factures pour agence 7: {FactureCommande.objects.filter(agence=agence_7).count()}")

