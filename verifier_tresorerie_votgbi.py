#!/usr/bin/env python
"""
Script pour vérifier l'état de la trésorerie VOTGBI
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

def verifier_tresorerie_votgbi():
    """Vérifier l'état actuel de la trésorerie VOTGBI"""
    
    print("=" * 80)
    print("VERIFICATION TRESORERIE VOTGBI")
    print("=" * 80)
    
    # 1. Rechercher l'agence VOTGBI
    try:
        agence = Agence.objects.filter(nom_agence__icontains='VOTGBI').first()
        if not agence:
            agence = Agence.objects.filter(nom_agence__icontains='VOT').first()
        
        if not agence:
            print("ERREUR: Agence VOTGBI non trouvee!")
            return False
        
        print(f"Agence: {agence.nom_agence} (ID: {agence.id_agence})")
        
    except Exception as e:
        print(f"ERREUR: {e}")
        return False
    
    # 2. Date d'aujourd'hui
    date_aujourdhui = date.today()
    print(f"\nDate du jour: {date_aujourdhui}")
    
    # 3. Vérifier la trésorerie d'aujourd'hui
    try:
        treso = Tresorerie.objects.get(agence=agence, date=date_aujourdhui)
        
        print(f"\n=== TRESORERIE DU JOUR ===")
        print(f"Banque:")
        print(f"  - Solde initial: {treso.banque_initial}")
        print(f"  - Depot: {treso.banque_depot}")
        print(f"  - Retrait: {treso.banque_retrait}")
        print(f"  - Frais banque: {treso.frais_banque}")
        print(f"  - Solde final calcule: {treso.solde_banque_final}")
        
        print(f"\nCaisse:")
        print(f"  - Solde initial: {treso.caisse_initial}")
        print(f"  - Entree: {treso.caisse_entree}")
        print(f"  - Sortie: {treso.caisse_sortie}")
        print(f"  - Solde final calcule: {treso.solde_caisse_final}")
        
        print(f"\nOrange Money:")
        print(f"  - Solde initial: {treso.om_initial}")
        print(f"  - Depot: {treso.om_depot}")
        print(f"  - Retrait: {treso.om_retrait}")
        print(f"  - Frais OM: {treso.frais_om}")
        print(f"  - Solde final calcule: {treso.solde_om_final}")
        
        print(f"\nMTN Money:")
        print(f"  - Solde initial: {treso.momo_initial}")
        print(f"  - Depot: {treso.momo_depot}")
        print(f"  - Retrait: {treso.momo_retrait}")
        print(f"  - Frais Momo: {treso.frais_momo}")
        print(f"  - Solde final calcule: {treso.solde_momo_final}")
        
        print(f"\nSAV:")
        print(f"  - Solde initial: {treso.sav_initial}")
        print(f"  - Entree: {treso.sav_entree}")
        print(f"  - Sortie: {treso.sav_sortie}")
        print(f"  - Solde final calcule: {treso.solde_sav_final}")
        
        print(f"\nTOTAL DISPONIBLE: {treso.total_disponible}")
        
        # Vérifier les 5 derniers jours
        print(f"\n=== HISTORIQUE (5 derniers jours) ===")
        historique = Tresorerie.objects.filter(
            agence=agence
        ).order_by('-date')[:5]
        
        for h in historique:
            print(f"\n{h.date}:")
            print(f"  Banque final: {h.solde_banque_final}")
            print(f"  Caisse final: {h.solde_caisse_final}")
            print(f"  OM final: {h.solde_om_final}")
            print(f"  Momo final: {h.solde_momo_final}")
            print(f"  SAV final: {h.solde_sav_final}")
            print(f"  Total: {h.total_disponible}")
        
        return True
        
    except Tresorerie.DoesNotExist:
        print(f"\nAUCUNE TRESORERIE trouvee pour {date_aujourdhui}")
        return False
    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    verifier_tresorerie_votgbi()
