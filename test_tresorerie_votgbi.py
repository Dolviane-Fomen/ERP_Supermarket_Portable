#!/usr/bin/env python
"""
Script de test pour insérer un dépôt de 50000 FCFA dans le solde bancaire
de l'agence VOTGBI pour tester le système de trésorerie.
"""

import os
import sys
import django
from datetime import date
from decimal import Decimal

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
django.setup()

from supermarket.models import Agence, Tresorerie

def test_depot_banque_votgbi():
    """Test d'insertion d'un dépôt de 50000 FCFA dans le solde bancaire de VOTGBI"""
    
    print("=" * 80)
    print("SCRIPT DE TEST - DÉPÔT BANCAIRE VOTGBI")
    print("=" * 80)
    
    # 1. Rechercher l'agence VOTGBI
    try:
        agence = Agence.objects.filter(nom_agence__icontains='VOTGBI').first()
        if not agence:
            # Essayer avec d'autres variantes
            agence = Agence.objects.filter(nom_agence__icontains='VOT').first()
        
        if not agence:
            print("ERREUR: Agence VOTGBI non trouvee!")
            print("\nAgences disponibles:")
            for a in Agence.objects.all():
                print(f"  - {a.nom_agence} (ID: {a.id_agence})")
            return False
        
        print(f"OK - Agence trouvee: {agence.nom_agence} (ID: {agence.id_agence})")
        
    except Exception as e:
        print(f"ERREUR lors de la recherche de l'agence: {e}")
        return False
    
    # 2. Date d'aujourd'hui
    date_aujourdhui = date.today()
    print(f"Date du jour: {date_aujourdhui}")
    
    # 3. Vérifier si une trésorerie existe déjà pour aujourd'hui
    try:
        treso_existante = Tresorerie.objects.filter(agence=agence, date=date_aujourdhui).first()
        
        if treso_existante:
            print(f"\nTresorerie existante trouvee pour {date_aujourdhui}:")
            print(f"   - Solde initial banque: {treso_existante.banque_initial}")
            print(f"   - Depot actuel: {treso_existante.banque_depot}")
            print(f"   - Retrait actuel: {treso_existante.banque_retrait}")
            print(f"   - Solde final calcule: {treso_existante.solde_banque_final}")
            
            # Ajouter 50000 au dépôt existant
            nouveau_depot = treso_existante.banque_depot + Decimal('50000')
            treso_existante.banque_depot = nouveau_depot
            treso_existante.save()
            
            print(f"\nOK - Depot mis a jour!")
            print(f"   - Nouveau depot: {nouveau_depot}")
            print(f"   - Nouveau solde final: {treso_existante.solde_banque_final}")
            
        else:
            # Chercher le dernier jour enregistré pour récupérer le solde initial
            dernier_jour = Tresorerie.objects.filter(
                agence=agence, 
                date__lt=date_aujourdhui
            ).order_by('-date').first()
            
            if dernier_jour:
                solde_initial = dernier_jour.solde_banque_final
                print(f"\nDernier jour trouve: {dernier_jour.date}")
                print(f"   - Solde final du jour precedent: {solde_initial}")
            else:
                solde_initial = Decimal('0')
                print(f"\nAucun jour precedent trouve, solde initial = 0")
            
            # Créer une nouvelle trésorerie avec dépôt de 50000
            nouvelle_treso = Tresorerie.objects.create(
                agence=agence,
                date=date_aujourdhui,
                banque_initial=solde_initial,
                banque_depot=Decimal('50000'),
                banque_retrait=Decimal('0'),
                caisse_initial=Decimal('0'),
                caisse_entree=Decimal('0'),
                caisse_sortie=Decimal('0'),
                om_initial=Decimal('0'),
                om_depot=Decimal('0'),
                om_retrait=Decimal('0'),
                momo_initial=Decimal('0'),
                momo_depot=Decimal('0'),
                momo_retrait=Decimal('0'),
                sav_initial=Decimal('0'),
                sav_entree=Decimal('0'),
                sav_sortie=Decimal('0'),
            )
            
            print(f"\nOK - Nouvelle tresorerie creee!")
            print(f"   - Solde initial banque: {nouvelle_treso.banque_initial}")
            print(f"   - Depot: {nouvelle_treso.banque_depot}")
            print(f"   - Solde final calcule: {nouvelle_treso.solde_banque_final}")
        
        print("\n" + "=" * 80)
        print("OK - TEST REUSSI - Verifiez maintenant dans l'interface web")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\nERREUR lors de la creation/mise a jour: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_depot_banque_votgbi()
    sys.exit(0 if success else 1)
