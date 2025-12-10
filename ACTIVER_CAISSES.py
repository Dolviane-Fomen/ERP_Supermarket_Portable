#!/usr/bin/env python3
"""
ACTIVER_CAISSES.py
Activer les caisses pour toutes les agences
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def log(msg: str) -> None:
    """Fonction de log avec timestamp"""
    now = datetime.now().strftime('%H:%M:%S')
    line = f"[{now}] {msg}"
    print(line)

def activer_caisses():
    """Activer les caisses pour toutes les agences"""
    
    log("=" * 60)
    log("  ACTIVATION DES CAISSES")
    log("=" * 60)
    
    try:
        # Configuration Django
        os.environ['DJANGO_SETTINGS_MODULE'] = 'erp_project.settings_standalone'
        
        import django
        django.setup()
        
        from supermarket.models import Agence, Caisse
        
        log("✅ Django initialisé")
        
        # 1. Lister toutes les caisses
        log("")
        log("🔍 1. CAISSES ACTUELLES:")
        caisses = Caisse.objects.all().select_related('agence')
        for caisse in caisses:
            log(f"   - {caisse.numero_caisse} ({caisse.agence.nom_agence}) - Statut: {caisse.statut}")
        
        # 2. Activer une caisse par agence
        log("")
        log("🔍 2. ACTIVATION DES CAISSES:")
        agences = Agence.objects.all()
        
        for agence in agences:
            log(f"")
            log(f"🏢 Agence: {agence.nom_agence}")
            
            # Chercher une caisse pour cette agence
            caisse = Caisse.objects.filter(agence=agence).first()
            
            if caisse:
                # Activer cette caisse
                caisse.statut = 'active'
                caisse.save()
                log(f"   ✅ Caisse {caisse.numero_caisse} activée")
            else:
                # Créer une caisse pour cette agence
                caisse = Caisse.objects.create(
                    numero_caisse=f'CAISSE_{agence.id_agence:03d}',
                    nom_caisse=f'Caisse {agence.nom_agence}',
                    agence=agence,
                    solde_initial=0,
                    solde_actuel=0,
                    statut='active'
                )
                log(f"   ✅ Caisse {caisse.numero_caisse} créée et activée")
        
        # 3. Vérification finale
        log("")
        log("🔍 3. VÉRIFICATION FINALE:")
        caisses_actives = Caisse.objects.filter(statut='active')
        for caisse in caisses_actives:
            log(f"   - {caisse.numero_caisse} ({caisse.agence.nom_agence}) - ACTIVE")
        
        log(f"")
        log(f"✅ {caisses_actives.count()} caisses actives au total")
        
        return True
        
    except Exception as e:
        log(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    
    if not Path("manage.py").exists():
        log("❌ Erreur: Ce script doit être exécuté dans le dossier ERP_Supermarket_Portable")
        return 1
    
    if activer_caisses():
        log("")
        log("=" * 60)
        log("✅ CAISSES ACTIVÉES")
        log("=" * 60)
        log("")
        log("💡 MAINTENANT:")
        log("- Toutes les agences ont au moins une caisse active")
        log("- L'enregistrement de facture devrait fonctionner")
        log("- Plus d'erreur 'caisse manquante'")
        log("")
        log("🚀 PROCHAINES ÉTAPES:")
        log("1. Relancez votre application ERP")
        log("2. Testez l'enregistrement de facture")
        log("3. L'erreur devrait être résolue!")
        log("")
        return 0
    else:
        log("❌ Activation échouée")
        return 1

if __name__ == '__main__':
    sys.exit(main())
