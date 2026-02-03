#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script rapide pour vérifier les factures d'une agence
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

os.chdir(Path(__file__).parent)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
import django
django.setup()

from supermarket.models import FactureVente, Agence
from django.utils import timezone

print("="*70)
print("VERIFICATION DES FACTURES PAR AGENCE")
print("="*70)

# Afficher toutes les agences
print("\n[AGENCES DISPONIBLES]")
agences = Agence.objects.all()
for agence in agences:
    print(f"   - {agence.nom_agence} (ID: {agence.id_agence})")

# Vérifier les factures de MARCHE HUITIEME
agence_nom = "MARCHE HUITIEME"
print(f"\n[FACTURES DE L'AGENCE: {agence_nom}]")

try:
    agence = Agence.objects.get(nom_agence=agence_nom)
    print(f"   Agence trouvee: {agence_nom} (ID: {agence.id_agence})")
    
    # Factures des 30 derniers jours
    date_limit = timezone.now() - timedelta(days=30)
    factures = FactureVente.objects.filter(
        agence=agence,
        date__gte=date_limit.date()
    ).order_by('-date', '-heure')
    
    print(f"\n   Factures des 30 derniers jours: {factures.count()}")
    
    if factures.exists():
        print(f"\n   Dernieres factures:")
        for fv in factures[:10]:
            print(f"      - {fv.numero_ticket} - {fv.date} - {fv.client.intitule if fv.client else 'N/A'} - {fv.nette_a_payer:.0f} FCFA")
    else:
        print(f"\n   [INFO] Aucune facture trouvee pour les 30 derniers jours")
        
        # Vérifier toutes les factures de cette agence
        all_factures = FactureVente.objects.filter(agence=agence).order_by('-date', '-heure')
        print(f"\n   Total factures de cette agence (toutes periodes): {all_factures.count()}")
        if all_factures.exists():
            print(f"   Derniere facture: {all_factures.first().numero_ticket} - {all_factures.first().date}")
    
except Agence.DoesNotExist:
    print(f"   [ERREUR] Agence '{agence_nom}' non trouvee!")

# Vérifier toutes les factures d'aujourd'hui (toutes agences)
print(f"\n[FACTURES D'AUJOURD'HUI (toutes agences)]")
today = timezone.now().date()
factures_today = FactureVente.objects.filter(date=today).order_by('-heure')
print(f"   Total: {factures_today.count()} factures")
for fv in factures_today:
    print(f"      - {fv.numero_ticket} - {fv.agence.nom_agence} - {fv.client.intitule if fv.client else 'N/A'} - {fv.nette_a_payer:.0f} FCFA")

print("\n" + "="*70)
