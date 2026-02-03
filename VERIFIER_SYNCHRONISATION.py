#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour vérifier que les factures locales ont bien été synchronisées sur le serveur
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
CONFIG = {
    'server_user': 'ubuntu',
    'server_host': '51.68.124.152',
    'server_path': '/home/ubuntu/erp_project',
    'local_path': str(Path(__file__).parent),
}

# Charger la configuration depuis .ovh_config.json si elle existe
ovh_config_file = Path(CONFIG['local_path']) / '.ovh_config.json'
if ovh_config_file.exists():
    try:
        with open(ovh_config_file, 'r') as f:
            ovh_config = json.load(f)
            if 'ovh_host' in ovh_config:
                CONFIG['server_host'] = ovh_config['ovh_host']
            if 'ovh_user' in ovh_config:
                CONFIG['server_user'] = ovh_config['ovh_user']
            if 'ovh_project_path' in ovh_config:
                CONFIG['server_path'] = ovh_config['ovh_project_path']
    except Exception as e:
        print(f"[WARN] Impossible de charger .ovh_config.json: {e}")

def run_command(cmd, check=False, timeout=30):
    """Exécuter une commande SSH"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return None, f"Timeout after {timeout} seconds", -1
    except Exception as e:
        return None, str(e), -1

def get_local_factures(days=30, agence_nom=None):
    """Récupérer les factures locales des derniers jours, filtrées par agence si spécifiée"""
    try:
        os.chdir(CONFIG['local_path'])
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
        import django
        django.setup()
        
        from supermarket.models import FactureVente, Agence
        from django.utils import timezone
        
        # Afficher toutes les agences disponibles si aucune facture n'est trouvée
        if agence_nom:
            try:
                agence = Agence.objects.get(nom_agence=agence_nom)
                print(f"   Agence trouvee: {agence_nom} (ID: {agence.id_agence})")
            except Agence.DoesNotExist:
                print(f"   [WARN] Agence '{agence_nom}' non trouvee!")
                print(f"   [INFO] Agences disponibles:")
                all_agences = Agence.objects.all()
                for a in all_agences:
                    print(f"      - {a.nom_agence} (ID: {a.id})")
                return []
        
        date_limit = timezone.now() - timedelta(days=days)
        factures = FactureVente.objects.filter(date__gte=date_limit.date()).order_by('-date', '-heure')
        
        # Filtrer par agence si spécifiée
        if agence_nom:
            try:
                agence = Agence.objects.get(nom_agence=agence_nom)
                factures = factures.filter(agence=agence)
                print(f"   Filtrage par agence: {agence_nom} (ID: {agence.id_agence})")
            except Agence.DoesNotExist:
                print(f"   [WARN] Agence '{agence_nom}' non trouvee, toutes les factures seront affichees")
        
        factures_list = []
        for fv in factures:
            factures_list.append({
                'id': fv.id,
                'numero_ticket': fv.numero_ticket,
                'date': fv.date.isoformat(),
                'heure': str(fv.heure),
                'nette_a_payer': float(fv.nette_a_payer),
                'client': fv.client.intitule if fv.client else '',
                'agence': fv.agence.nom_agence if fv.agence else '',
            })
        
        return factures_list
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la récupération des factures locales: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_server_factures(days=30, agence_nom=None):
    """Récupérer les factures du serveur des derniers jours, filtrées par agence si spécifiée"""
    try:
        # Créer un script Python à exécuter sur le serveur
        agence_nom_repr = repr(agence_nom) if agence_nom else 'None'
        script_content = f'''import os, django, json, sys
from datetime import datetime, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp_project.settings_production")
django.setup()
from supermarket.models import FactureVente, Agence
from django.utils import timezone

date_limit = timezone.now() - timedelta(days={days})
factures = FactureVente.objects.filter(date__gte=date_limit.date()).order_by('-date', '-heure')

# Filtrer par agence si spécifiée
agence_filter_str = {agence_nom_repr}
if agence_filter_str:
    try:
        agence = Agence.objects.get(nom_agence=agence_filter_str)
        factures = factures.filter(agence=agence)
        print(f"Filtrage par agence: {{agence_filter_str}} (ID: {{agence.id_agence}})", file=sys.stderr)
    except Agence.DoesNotExist:
        print(f"Agence '{{agence_filter_str}}' non trouvee", file=sys.stderr)

factures_list = []
for fv in factures:
    factures_list.append({{
        'id': fv.id,
        'numero_ticket': fv.numero_ticket,
        'date': fv.date.isoformat(),
        'heure': str(fv.heure),
        'nette_a_payer': float(fv.nette_a_payer),
        'client': fv.client.intitule if fv.client else '',
        'agence': fv.agence.nom_agence if fv.agence else '',
    }})

print(json.dumps(factures_list, ensure_ascii=False))
'''
        
        # Créer le script temporaire localement
        script_path = Path(CONFIG['local_path']) / 'temp_check_factures.py'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Transférer le script sur le serveur (utiliser des guillemets pour gérer les espaces)
        # Sur Windows avec des espaces dans le chemin, utiliser le chemin absolu avec guillemets
        script_path_abs = str(script_path.absolute())
        scp_cmd = (
            f'scp -o ServerAliveInterval=60 -o ServerAliveCountMax=3 '
            f'"{script_path_abs}" '
            f'{CONFIG["server_user"]}@{CONFIG["server_host"]}:{CONFIG["server_path"]}/temp_check_factures.py'
        )
        scp_stdout, scp_stderr, scp_code = run_command(scp_cmd, timeout=30)
        if scp_code != 0:
            print(f"[ERREUR] Erreur lors du transfert du script: {scp_stderr}")
            return []
        
        # Exécuter le script sur le serveur
        ssh_cmd = (
            f'ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 '
            f'{CONFIG["server_user"]}@{CONFIG["server_host"]} '
            f'"cd {CONFIG["server_path"]} && ./venv/bin/python3 temp_check_factures.py"'
        )
        stdout, stderr, code = run_command(ssh_cmd, timeout=30)
        
        # Nettoyer le script local
        if script_path.exists():
            try:
                script_path.unlink()
            except:
                pass
        
        if code == 0 and stdout:
            try:
                factures_list = json.loads(stdout)
                return factures_list
            except json.JSONDecodeError as e:
                print(f"[ERREUR] Erreur lors du parsing JSON: {e}")
                print(f"   Sortie: {stdout}")
                return []
        else:
            print(f"[ERREUR] Erreur lors de la récupération des factures du serveur: {stderr}")
            return []
    except Exception as e:
        print(f"[ERREUR] Erreur: {e}")
        import traceback
        traceback.print_exc()
        return []

def compare_factures(local_factures, server_factures):
    """Comparer les factures locales et serveur"""
    print("\n" + "="*70)
    print("VERIFICATION DE LA SYNCHRONISATION")
    print("="*70)
    
    # Créer des dictionnaires indexés par numero_ticket
    local_dict = {fv['numero_ticket']: fv for fv in local_factures}
    server_dict = {fv['numero_ticket']: fv for fv in server_factures}
    
    # Factures présentes localement
    local_tickets = set(local_dict.keys())
    server_tickets = set(server_dict.keys())
    
    # Factures synchronisées (présentes sur les deux)
    synchronized = local_tickets & server_tickets
    
    # Factures manquantes sur le serveur
    missing_on_server = local_tickets - server_tickets
    
    # Factures présentes sur le serveur mais pas localement
    extra_on_server = server_tickets - local_tickets
    
    print(f"\n[STATISTIQUES]")
    print(f"   Factures locales (derniers 30 jours): {len(local_factures)}")
    print(f"   Factures sur le serveur (derniers 30 jours): {len(server_factures)}")
    print(f"   Factures synchronisees: {len(synchronized)}")
    print(f"   Factures manquantes sur le serveur: {len(missing_on_server)}")
    print(f"   Factures supplementaires sur le serveur: {len(extra_on_server)}")
    
    if len(local_factures) == 0 and len(server_factures) == 0:
        print(f"\n[INFO] Aucune facture trouvee pour la periode selectionnee.")
        print(f"   Cela peut signifier:")
        print(f"   - Il n'y a pas de factures creees recemment pour cette agence")
        print(f"   - Le nom de l'agence n'est pas exact")
        print(f"   - Les factures sont plus anciennes que 30 jours")
    
    if synchronized:
        print(f"\n[OK] FACTURES SYNCHRONISEES ({len(synchronized)}):")
        for ticket in sorted(synchronized, reverse=True)[:10]:  # Afficher les 10 dernières
            fv_local = local_dict[ticket]
            fv_server = server_dict[ticket]
            agence_info = f" - {fv_local.get('agence', '')}" if fv_local.get('agence') else ''
            print(f"   ✓ {ticket} - {fv_local['date']} - {fv_local['client']}{agence_info} - {fv_local['nette_a_payer']:.0f} FCFA")
        if len(synchronized) > 10:
            print(f"   ... et {len(synchronized) - 10} autres factures synchronisees")
    
    if missing_on_server:
        print(f"\n[ATTENTION] FACTURES MANQUANTES SUR LE SERVEUR ({len(missing_on_server)}):")
        for ticket in sorted(missing_on_server, reverse=True)[:10]:  # Afficher les 10 dernières
            fv = local_dict[ticket]
            agence_info = f" - {fv.get('agence', '')}" if fv.get('agence') else ''
            print(f"   ✗ {ticket} - {fv['date']} - {fv['client']}{agence_info} - {fv['nette_a_payer']:.0f} FCFA")
        if len(missing_on_server) > 10:
            print(f"   ... et {len(missing_on_server) - 10} autres factures manquantes")
        print(f"\n   [ACTION] Ces factures n'ont pas encore ete synchronisees.")
        print(f"   [ACTION] La prochaine synchronisation automatique devrait les envoyer.")
    
    if extra_on_server:
        print(f"\n[INFO] FACTURES SUPPLEMENTAIRES SUR LE SERVEUR ({len(extra_on_server)}):")
        print(f"   Ces factures existent sur le serveur mais pas localement.")
        print(f"   Cela peut etre normal si elles ont ete creees directement sur le serveur.")
    
    print("\n" + "="*70)
    
    # Résumé final
    if len(missing_on_server) == 0:
        print("[SUCCES] Toutes les factures locales sont synchronisees sur le serveur!")
        return True
    else:
        print(f"[ATTENTION] {len(missing_on_server)} facture(s) locale(s) ne sont pas encore sur le serveur.")
        print(f"   La synchronisation automatique devrait les envoyer dans moins d'1 minute.")
        return False

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Verifier la synchronisation des factures')
    parser.add_argument('--agence', type=str, help='Nom de l\'agence a verifier (ex: MARCHE HUITIEME)')
    args = parser.parse_args()
    
    agence_nom = args.agence or "MARCHE HUITIEME"  # Par défaut, vérifier MARCHE HUITIEME
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Verification de la synchronisation...")
    print(f"   Serveur: {CONFIG['server_user']}@{CONFIG['server_host']}")
    print(f"   Chemin: {CONFIG['server_path']}")
    print(f"   Agence: {agence_nom}")
    
    # Récupérer les factures locales
    print("\n[1/3] Recuperation des factures locales...")
    local_factures = get_local_factures(days=30, agence_nom=agence_nom)
    if local_factures is None:
        return 1
    print(f"   {len(local_factures)} factures trouvees localement pour l'agence {agence_nom}")
    
    # Récupérer les factures du serveur
    print("\n[2/3] Recuperation des factures du serveur...")
    server_factures = get_server_factures(days=30, agence_nom=agence_nom)
    print(f"   {len(server_factures)} factures trouvees sur le serveur pour l'agence {agence_nom}")
    
    # Comparer
    print("\n[3/3] Comparaison des factures...")
    success = compare_factures(local_factures, server_factures)
    
    return 0 if success else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[WARN] Verification interrompue par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"[ERREUR] Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
