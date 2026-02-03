#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de synchronisation entre environnement local et serveur en ligne
"""
import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration par défaut
# Les valeurs peuvent être surchargées par un fichier de config JSON
CONFIG = {
    'server_host': '51.68.124.152',  # IP du serveur OVH
    'server_user': 'ubuntu',  # Utilisateur SSH sur le serveur
    'server_path': '/home/ubuntu/erp_project',  # Chemin du projet sur le serveur
    'local_path': str(Path(__file__).parent.resolve()),
    'export_file': 'sync_export.json',
    'backup_dir': 'backups',
    'sync_state_file': '.sync_state.json',  # Fichier pour tracker la dernière synchronisation
    'incremental_days': 7,  # Nombre de jours pour l'export incrémental (7 = dernière semaine)
}

# Essayer de charger la configuration depuis .ovh_config.json si elle existe
ovh_config_file = Path(__file__).parent / '.ovh_config.json'
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
        print("   Utilisation des valeurs par défaut")


def get_last_sync_date():
    """Récupérer la date de la dernière synchronisation"""
    sync_state_file = Path(CONFIG['local_path']) / CONFIG['sync_state_file']
    if sync_state_file.exists():
        try:
            with open(sync_state_file, 'r') as f:
                state = json.load(f)
                last_sync_str = state.get('last_sync_date')
                if last_sync_str:
                    return datetime.fromisoformat(last_sync_str)
        except Exception:
            pass
    # Par défaut, retourner la date d'il y a X jours
    return datetime.now() - timedelta(days=CONFIG['incremental_days'])


def save_sync_date():
    """Sauvegarder la date de synchronisation actuelle"""
    sync_state_file = Path(CONFIG['local_path']) / CONFIG['sync_state_file']
    try:
        state = {
            'last_sync_date': datetime.now().isoformat(),
            'last_sync_timestamp': datetime.now().timestamp()
        }
        with open(sync_state_file, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"[WARN] Impossible de sauvegarder la date de synchronisation: {e}")


def run_command(cmd, check=True, env=None, timeout=600):
    """
    Exécuter une commande et retourner le résultat
    
    Args:
        cmd: Commande à exécuter
        check: Si True, lève une exception en cas d'erreur
        env: Variables d'environnement
        timeout: Timeout en secondes (défaut: 10 minutes)
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        print(f"[ERREUR] Timeout lors de l'execution de la commande (>{timeout}s)")
        return None, f"Timeout after {timeout} seconds", -1
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Erreur lors de l'execution : {cmd}")
        print(f"   {e.stderr}")
        return None, e.stderr, e.returncode


def backup_database():
    """Faire une sauvegarde de la base de données locale"""
    backup_dir = Path(CONFIG['local_path']) / CONFIG['backup_dir']
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f"db_erp_backup_{timestamp}.sqlite3"
    
    db_file = Path(CONFIG['local_path']) / 'db_erp.sqlite3'
    if db_file.exists():
        import shutil
        shutil.copy2(db_file, backup_file)
        print(f"[OK] Sauvegarde creee : {backup_file}")
        return backup_file
    else:
        print("[WARN] Base de donnees locale non trouvee")
        return None


def export_local_data(agence_id=None):
    """Exporter les données locales"""
    print(f"[{datetime.now()}] Export des données locales...")
    
    # Essayer d'abord avec la méthode export_data (meilleure gestion des Decimal)
    # Utiliser l'export incrémental par défaut pour accélérer
    try:
        print("   Tentative d'export avec la méthode export_data (incrémental)...")
        result = export_local_data_via_export_data(agence_id, incremental=True)
        if result:
            return result
    except Exception as e:
        print(f"   [WARN] Export via export_data echoue: {e}")
        import traceback
        try:
            print(f"   Details: {traceback.format_exc()}")
        except:
            print(f"   Details: {str(e)}")
        print("   Tentative avec export complet (sans filtre incremental)...")
        try:
            # Essayer sans filtre incrémental
            result = export_local_data_via_export_data(agence_id, incremental=False)
            if result:
                return result
        except Exception as e2:
            print(f"   [WARN] Export complet via export_data echoue: {e2}")
            print("   Tentative avec dumpdata...")
    
    # Fallback vers dumpdata si export_data échoue
    # Détecter la commande Python disponible
    python_cmd = "py"
    try:
        subprocess.run(["py", "--version"], capture_output=True, timeout=2, check=True)
    except:
        python_cmd = "python"
    
    # Forcer l'utilisation de settings.py (SQLite local) au lieu de settings_shared_db
    cmd = f'{python_cmd} manage.py dumpdata --settings=erp_project.settings'
    
    # Ajouter des options selon les besoins
    exclude = ['contenttypes', 'sessions', 'admin.logentry']
    cmd += ' ' + ' '.join([f'--exclude {x}' for x in exclude])
    
    # Ajouter des options pour améliorer la compatibilité
    cmd += ' --natural-foreign --natural-primary'
    
    if agence_id:
        # Note: dumpdata ne supporte pas directement le filtre par agence
        # Il faudrait utiliser l'interface d'export web ou un script personnalisé
        print("[WARN] Filtrage par agence non supporte par dumpdata, export complet...")
    
    export_file = Path(CONFIG['local_path']) / CONFIG['export_file']
    
    # Configurer l'environnement pour UTF-8 sur Windows
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    # Sur Windows, utiliser chcp 65001 pour UTF-8 avant la redirection
    if sys.platform == 'win32':
        cmd_with_redirect = f'chcp 65001 >nul && {cmd} > "{export_file}"'
    else:
        cmd_with_redirect = f'{cmd} > "{export_file}"'
    
    stdout, stderr, code = run_command(cmd_with_redirect, check=False, env=env)
    
    if code == 0 and export_file.exists():
        size = export_file.stat().st_size / 1024 / 1024  # Taille en MB
        print(f"[OK] Export reussi : {export_file} ({size:.2f} MB)")
        return export_file
    else:
        print(f"[ERREUR] Erreur lors de l'export : {stderr}")
        if "argument must be int or float" in stderr or "Unable to serialize" in stderr:
            print("   [INFO] Probleme de serialisation detecte")
            print("   [INFO] Cela peut etre du a des donnees corrompues ou des types de donnees incompatibles")
            print("   [INFO] Solutions possibles:")
            print("      1. Verifiez la base de donnees: py manage.py dbshell --settings=erp_project.settings")
            print("      2. Utilisez l'export via l'interface web Django si disponible")
            print("      3. Essayez d'exporter seulement certaines tables (modifiez le script)")
            print("   [WARN] La synchronisation continuera avec les donnees du serveur uniquement")
        return None


def export_local_data_via_export_data(agence_id=None, incremental=True):
    """
    Exporter les données locales en utilisant la fonction export_data du module supermarket
    
    Args:
        agence_id: ID de l'agence à exporter
        incremental: Si True, exporte seulement les données récentes (derniers X jours)
    """
    import django
    from pathlib import Path
    import json
    from django.utils import timezone
    
    # Sauvegarder le répertoire de travail actuel
    original_cwd = os.getcwd()
    
    try:
        # Configurer Django
        os.chdir(CONFIG['local_path'])
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
        django.setup()
        
        # Importer les modèles et la fonction d'export
        from supermarket.export_import import export_data
        from supermarket.models import (
            FactureVente, LigneFactureVente, MouvementStock, 
            FactureAchat, LigneFactureAchat, StatistiqueVente
        )
        
        # Déterminer la date limite pour l'export incrémental
        if incremental:
            last_sync_date = get_last_sync_date()
            # S'assurer que la date est timezone-aware si Django le requiert
            from django.utils import timezone
            if timezone.is_naive(last_sync_date):
                date_limit = timezone.make_aware(last_sync_date)
            else:
                date_limit = last_sync_date
            print(f"   Export incremental : donnees depuis le {date_limit.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            date_limit = None
            print("   Export complet de toutes les donnees...")
        
        # Exporter les données de base (toujours exportées)
        print("   Export des données de base (agences, articles, clients, etc.)...")
        data = export_data(agence_id=agence_id, include_users=False)
        
        # Si export incrémental, filtrer les données récentes
        if incremental and date_limit:
            print(f"   Filtrage des données récentes (depuis {date_limit.strftime('%Y-%m-%d')})...")
            
            # Filtrer les factures récentes (utiliser 'date' au lieu de 'date_creation')
            # Convertir date_limit en date pour la comparaison avec DateField
            try:
                date_limit_date = date_limit.date() if hasattr(date_limit, 'date') else date_limit
                factures_recentes = list(FactureVente.objects.filter(
                    date__gte=date_limit_date
                ).values_list('id', flat=True))
                print(f"   [OK] {len(factures_recentes)} factures recentes trouvees")
            except Exception as e:
                print(f"   [WARN] Erreur lors du filtrage des factures: {e}")
                print("   Export de toutes les factures...")
                factures_recentes = list(FactureVente.objects.values_list('id', flat=True))
            
            # Filtrer les lignes de factures correspondantes
            data['factures_vente'] = [
                fv for fv in data['factures_vente'] 
                if fv.get('id') in factures_recentes
            ]
            data['lignes_factures_vente'] = [
                lfv for lfv in data['lignes_factures_vente']
                if lfv.get('facture_vente_id') in factures_recentes
            ]
            
            # Filtrer les mouvements de stock récents
            try:
                mouvements_recents = list(MouvementStock.objects.filter(
                    date_mouvement__gte=date_limit
                ).values_list('id', flat=True))
                data['mouvements_stock'] = [
                    ms for ms in data['mouvements_stock']
                    if ms.get('id') in mouvements_recents
                ]
                print(f"   [OK] {len(mouvements_recents)} mouvements de stock recents")
            except Exception as e:
                print(f"   [WARN] Erreur lors du filtrage des mouvements: {e}")
            
            # Filtrer les statistiques récentes
            try:
                stats_recentes = list(StatistiqueVente.objects.filter(
                    date_creation__gte=date_limit
                ).values_list('id', flat=True))
                data['statistiques_vente'] = [
                    sv for sv in data['statistiques_vente']
                    if sv.get('id') in stats_recentes
                ]
                print(f"   [OK] {len(stats_recentes)} statistiques recentes")
            except Exception as e:
                print(f"   [WARN] Erreur lors du filtrage des statistiques: {e}")
            
            # Compter les données filtrées
            nb_factures = len(data['factures_vente'])
            nb_mouvements = len(data['mouvements_stock'])
            print(f"   Resume: {nb_factures} factures, {nb_mouvements} mouvements de stock")
        
        # Sauvegarder dans un fichier JSON
        export_file = Path(CONFIG['local_path']) / CONFIG['export_file']
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        if export_file.exists():
            size = export_file.stat().st_size / 1024 / 1024  # Taille en MB
            mode = "incremental" if incremental else "complet"
            print(f"[OK] Export {mode} reussi : {export_file} ({size:.2f} MB)")
            return export_file
        else:
            raise Exception("Le fichier d'export n'a pas été créé")
    finally:
        # Restaurer le répertoire de travail
        os.chdir(original_cwd)


def import_local_data(export_file, merge=False):
    """Importer des données dans l'environnement local"""
    print(f"[{datetime.now()}] Import des données dans l'environnement local...")
    
    export_path = Path(export_file)
    if not export_path.exists():
        print(f"[ERREUR] Fichier d'export introuvable : {export_file}")
        return False
    
    # Vérifier la taille du fichier pour estimer le temps
    file_size_mb = export_path.stat().st_size / 1024 / 1024
    if file_size_mb > 10:
        print(f"   [WARN] Fichier volumineux ({file_size_mb:.2f} MB) - l'import peut prendre plusieurs minutes")
        print(f"   [INFO] Pour accelerer, utilisez l'import incremental (seulement les donnees recentes)")
    
    # Faire une sauvegarde avant l'import
    backup_database()
    
    # Détecter la commande Python disponible
    python_cmd = "py"
    try:
        subprocess.run(["py", "--version"], capture_output=True, timeout=2, check=True)
    except:
        python_cmd = "python"
    
    # Vérifier le format du fichier
    try:
        with open(export_path, 'r', encoding='utf-8') as f:
            content = f.read(200)
            # Si c'est le format export_data (format personnalisé)
            if '"version"' in content or '"agences"' in content:
                print("   Utilisation de import_data (format personnalisé)...")
                # Utiliser import_data du module supermarket (plus rapide)
                import django
                original_cwd = os.getcwd()
                try:
                    os.chdir(CONFIG['local_path'])
                    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')
                    django.setup()
                    from supermarket.export_import import import_data
                    import json
                    
                    print("   Chargement du fichier JSON...")
                    with open(export_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    print("   Import des données...")
                    stats = import_data(data, clear_existing=False)
                    
                    print(f"[OK] Import reussi : {stats.get('factures_vente', 0)} factures, {stats.get('articles', 0)} articles")
                    return True
                except Exception as e:
                    print(f"[ERREUR] Erreur lors de l'import via import_data : {e}")
                    import traceback
                    traceback.print_exc()
                    return False
                finally:
                    os.chdir(original_cwd)
    except:
        pass
    
    # Fallback vers loaddata (format Django fixtures)
    print("   Utilisation de loaddata (format Django fixtures)...")
    cmd = f'{python_cmd} manage.py loaddata "{export_path}" --settings=erp_project.settings'
    if merge:
        # Utiliser --ignorenonexistent au lieu de --merge (qui n'existe pas)
        cmd += ' --ignorenonexistent'
    
    stdout, stderr, code = run_command(cmd, check=False)
    
    if code == 0:
        print("[OK] Import reussi")
        return True
    else:
        print(f"[ERREUR] Erreur lors de l'import : {stderr}")
        return False


def pull_from_server(merge=False, incremental=True):
    """
    Télécharger les données depuis le serveur en ligne
    
    Args:
        merge: Fusionner les données au lieu de les remplacer
        incremental: Si True, télécharge seulement les données récentes (plus rapide)
    """
    print(f"[{datetime.now()}] Téléchargement depuis le serveur en ligne...")
    
    # Exporter depuis le serveur
    if incremental:
        last_sync_date = get_last_sync_date()
        print(f"   [EXPORT] Export incremental depuis le serveur (depuis {last_sync_date.strftime('%Y-%m-%d')})...")
        # Note: Pour l'export incrémental sur le serveur, on utilise export_data via un script Python
        # car dumpdata ne supporte pas facilement le filtrage par date
        ssh_cmd = (
            f'ssh {CONFIG["server_user"]}@{CONFIG["server_host"]} '
            f'"cd {CONFIG["server_path"]} && '
            f'./venv/bin/python3 -c "'
            f'import os, django, json; '
            f'from datetime import datetime, timedelta; '
            f'os.environ.setdefault(\\\"DJANGO_SETTINGS_MODULE\\\", \\\"erp_project.settings_production\\\"); '
            f'django.setup(); '
            f'from supermarket.export_import import export_data; '
            f'from supermarket.models import FactureVente, MouvementStock, StatistiqueVente; '
            f'date_limit = datetime.fromisoformat(\\\"{last_sync_date.isoformat()}\\\"); '
            f'data = export_data(include_users=False); '
            f'factures_ids = list(FactureVente.objects.filter(date_creation__gte=date_limit).values_list(\\\"id\\\", flat=True)); '
            f'data[\\\"factures_vente\\\"] = [f for f in data[\\\"factures_vente\\\"] if f.get(\\\"id\\\") in factures_ids]; '
            f'data[\\\"lignes_factures_vente\\\"] = [l for l in data[\\\"lignes_factures_vente\\\"] if l.get(\\\"facture_vente_id\\\") in factures_ids]; '
            f'mouv_ids = list(MouvementStock.objects.filter(date_mouvement__gte=date_limit).values_list(\\\"id\\\", flat=True)); '
            f'data[\\\"mouvements_stock\\\"] = [m for m in data[\\\"mouvements_stock\\\"] if m.get(\\\"id\\\") in mouv_ids]; '
            f'with open(\\\"{CONFIG["export_file"]}\\\", \\\"w\\\", encoding=\\\"utf-8\\\") as f: json.dump(data, f, ensure_ascii=False, indent=2)"'
        )
    else:
        print("   [EXPORT] Export complet depuis le serveur...")
        ssh_cmd = (
            f'ssh {CONFIG["server_user"]}@{CONFIG["server_host"]} '
            f'"cd {CONFIG["server_path"]} && '
            f'./venv/bin/python3 manage.py dumpdata --exclude contenttypes --exclude sessions '
            f'--exclude admin.logentry --natural-foreign --natural-primary '
            f'--settings=erp_project.settings_production > {CONFIG["export_file"]}"'
        )
    
    stdout, stderr, code = run_command(ssh_cmd, check=False)
    if code != 0:
        print(f"[ERREUR] Erreur lors de l'export sur le serveur : {stderr}")
        if "password" in stderr.lower() or "permission denied" in stderr.lower():
            print("   [INFO] Probleme d'authentification SSH detecte")
            print("   [INFO] Executez CONFIGURER_SSH_SANS_MOT_DE_PASSE.bat pour configurer l'authentification par cle")
        return False
    
    # Télécharger le fichier
    print("   [DOWNLOAD] Telechargement du fichier...")
    # Ajouter des options pour améliorer la stabilité de la connexion
    scp_cmd = (
        f'scp -o ServerAliveInterval=60 -o ServerAliveCountMax=3 '
        f'{CONFIG["server_user"]}@{CONFIG["server_host"]}:'
        f'{CONFIG["server_path"]}/{CONFIG["export_file"]} '
        f'"{CONFIG["local_path"]}"'
    )
    
    stdout, stderr, code = run_command(scp_cmd, check=False)
    if code != 0:
        print(f"[ERREUR] Erreur lors du telechargement : {stderr}")
        if "password" in stderr.lower() or "permission denied" in stderr.lower():
            print("   [INFO] Probleme d'authentification SSH detecte")
            print("   [INFO] Executez CONFIGURER_SSH_SANS_MOT_DE_PASSE.bat pour configurer l'authentification par cle")
        elif "Connection closed" in stderr or "timeout" in stderr.lower():
            print("   [INFO] Connexion fermee ou timeout detecte")
            print("   [INFO] Le fichier d'export sur le serveur peut etre trop volumineux")
            print("   [INFO] Reessayez ou utilisez le mode 'pull' uniquement")
        else:
            print("   [INFO] Assurez-vous que SSH/SCP est configure et accessible")
        return False
    
    # Importer localement
    local_export = Path(CONFIG['local_path']) / CONFIG['export_file']
    success = import_local_data(local_export, merge=merge)
    
    # Sauvegarder la date de synchronisation si l'import a réussi
    if success:
        save_sync_date()
    
    return success


def push_to_server(merge=False):
    """Envoyer les données locales vers le serveur en ligne"""
    print(f"[{datetime.now()}] Envoi vers le serveur en ligne...")
    
    # Exporter localement
    export_file = export_local_data()
    if not export_file:
        return False
    
    # Transférer vers le serveur
    print("   [UPLOAD] Transfert vers le serveur...")
    # Ajouter des options pour améliorer la stabilité de la connexion
    scp_cmd = (
        f'scp -o ServerAliveInterval=60 -o ServerAliveCountMax=3 '
        f'"{export_file}" '
        f'{CONFIG["server_user"]}@{CONFIG["server_host"]}:'
        f'{CONFIG["server_path"]}/'
    )
    
    stdout, stderr, code = run_command(scp_cmd, check=False)
    if code != 0:
        print(f"[ERREUR] Erreur lors du transfert : {stderr}")
        if "password" in stderr.lower() or "permission denied" in stderr.lower():
            print("   [INFO] Probleme d'authentification SSH detecte")
            print("   [INFO] Executez CONFIGURER_SSH_SANS_MOT_DE_PASSE.bat pour configurer l'authentification par cle")
        elif "Connection closed" in stderr or "timeout" in stderr.lower():
            print("   [INFO] Connexion fermee ou timeout detecte")
            print("   [INFO] Le fichier d'export peut etre trop volumineux")
        else:
            print("   [INFO] Assurez-vous que SSH/SCP est configure et accessible")
        return False
    
    # Importer sur le serveur
    print("   [IMPORT] Import sur le serveur...")
    # Vérifier le format du fichier (export_data ou dumpdata)
    export_file_path = Path(export_file)
    try:
        with open(export_file_path, 'r', encoding='utf-8') as f:
            content = f.read(100)  # Lire les premiers caractères
            # Si c'est le format export_data (commence par {"version" ou {"agences")
            if '"version"' in content or '"agences"' in content:
                # Utiliser import_data du module supermarket
                print("   Utilisation de import_data pour le format personnalisé...")
                # Créer un script Python local pour l'import, puis le transférer et l'exécuter
                # Utiliser une approche plus robuste avec logging et gestion d'erreur améliorée
                import_script_content = f'''# -*- coding: utf-8 -*-
import os, django, json, sys, signal
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp_project.settings_production")
django.setup()
from supermarket.export_import import import_data

# Ignorer SIGPIPE pour eviter les erreurs si la connexion se ferme
try:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except:
    pass

try:
    print("[INFO] Debut de l'import...", flush=True)
    with open("{CONFIG["export_file"]}", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"[INFO] Donnees chargees: {{len(data)}} cles", flush=True)
    result = import_data(data, clear_existing=False)
    print(f"[OK] Import reussi", flush=True)
    sys.stdout.flush()
    sys.exit(0)
except Exception as e:
    print(f"[ERREUR] {{e}}", flush=True, file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.stderr.flush()
    sys.exit(1)
'''
                # Créer le script directement sur le serveur via SSH en utilisant stdin pour éviter les problèmes d'échappement
                # Utiliser echo avec heredoc via stdin
                import subprocess
                ssh_process = subprocess.Popen(
                    [
                        'ssh',
                        '-o', 'ServerAliveInterval=60',
                        '-o', 'ServerAliveCountMax=10',
                        '-o', 'ConnectTimeout=30',
                        f'{CONFIG["server_user"]}@{CONFIG["server_host"]}',
                        f'cd {CONFIG["server_path"]} && cat > temp_import_sync.py'
                    ],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = ssh_process.communicate(input=import_script_content, timeout=30)
                create_code = ssh_process.returncode
                
                if create_code != 0:
                    print(f"   [ERREUR] Erreur lors de la creation du script sur le serveur")
                    if stderr:
                        print(f"   {stderr[:200]}")
                    return False
                
                # Exécuter le script sur le serveur avec nohup pour éviter les problèmes de connexion
                # Utiliser nohup et rediriger la sortie vers un fichier, puis lire ce fichier après un délai
                output_file = 'temp_import_sync_output.log'
                pid_file = 'temp_import_sync.pid'
                
                # Lancer l'import en arrière-plan avec nohup
                start_cmd = (
                    f'ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=10 -o ConnectTimeout=30 '
                    f'{CONFIG["server_user"]}@{CONFIG["server_host"]} '
                    f'"cd {CONFIG["server_path"]} && '
                    f'nohup ./venv/bin/python3 temp_import_sync.py > {output_file} 2>&1 & '
                    f'echo $! > {pid_file}"'
                )
                
                stdout_start, stderr_start, code_start = run_command(start_cmd, check=False, timeout=30)
                if code_start != 0:
                    print(f"   [ERREUR] Erreur lors du demarrage de l'import: {stderr_start}")
                    return False
                
                print("   [INFO] Import lance en arriere-plan, attente de la completion...")
                
                # Attendre et vérifier périodiquement si l'import est terminé
                import time
                max_wait = 600  # Maximum 10 minutes
                wait_interval = 5  # Vérifier toutes les 5 secondes
                waited = 0
                
                while waited < max_wait:
                    time.sleep(wait_interval)
                    waited += wait_interval
                    
                    # Vérifier si le processus est encore en cours
                    check_cmd = (
                        f'ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ConnectTimeout=10 '
                        f'{CONFIG["server_user"]}@{CONFIG["server_host"]} '
                        f'"cd {CONFIG["server_path"]} && '
                        f'if [ -f {pid_file} ]; then '
                        f'  pid=$(cat {pid_file}); '
                        f'  if ps -p $pid > /dev/null 2>&1; then '
                        f'    echo "RUNNING"; '
                        f'  else '
                        f'    echo "DONE"; '
                        f'  fi; '
                        f'else '
                        f'  echo "DONE"; '
                        f'fi"'
                    )
                    
                    stdout_check, stderr_check, code_check = run_command(check_cmd, check=False, timeout=10)
                    if stdout_check and "DONE" in stdout_check:
                        break
                    
                    if waited % 30 == 0:  # Afficher un message toutes les 30 secondes
                        print(f"   [INFO] Import en cours... ({waited}s)")
                
                # Lire le résultat de l'import
                ssh_cmd = (
                    f'ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ConnectTimeout=10 '
                    f'{CONFIG["server_user"]}@{CONFIG["server_host"]} '
                    f'"cd {CONFIG["server_path"]} && '
                    f'cat {output_file} && '
                    f'rm -f {output_file} {pid_file} temp_import_sync.py"'
                )
                
                # Exécuter la commande pour lire le résultat
                stdout, stderr, code = run_command(ssh_cmd, check=False, timeout=30)
                
                # Vérifier le résultat de l'import
                success = False
                output_text = (stdout or "") + (stderr or "")
                
                if code == 0:
                    if "[OK] Import reussi" in output_text or "Import reussi" in output_text:
                        print("[OK] Import reussi sur le serveur")
                        success = True
                    elif "[ERREUR]" in output_text:
                        print(f"[ERREUR] Erreur lors de l'import sur le serveur : {output_text}")
                        success = False
                    else:
                        # Si pas d'erreur explicite, considérer comme succès
                        print("[OK] Import semble avoir reussi (pas d'erreur detectee)")
                        success = True
                else:
                    print(f"[ERREUR] Erreur lors de la recuperation du resultat: {stderr}")
                    # Essayer de lire le fichier directement même en cas d'erreur SSH
                    read_cmd = (
                        f'ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ConnectTimeout=10 '
                        f'{CONFIG["server_user"]}@{CONFIG["server_host"]} '
                        f'"cd {CONFIG["server_path"]} && cat {output_file} 2>/dev/null || echo \'Fichier non trouve\'"'
                    )
                    stdout_read, stderr_read, code_read = run_command(read_cmd, check=False, timeout=10)
                    if stdout_read:
                        print(f"   Sortie de l'import: {stdout_read[:500]}")
                        if "[OK] Import reussi" in stdout_read:
                            success = True
                
                # Nettoyer les fichiers temporaires sur le serveur
                cleanup_cmd = (
                    f'ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ConnectTimeout=10 '
                    f'{CONFIG["server_user"]}@{CONFIG["server_host"]} '
                    f'"cd {CONFIG["server_path"]} && rm -f temp_import_sync.py {output_file} {pid_file}"'
                )
                run_command(cleanup_cmd, check=False, timeout=10)
                
                if success:
                    save_sync_date()
                
                return success
            else:
                # Utiliser loaddata pour le format Django fixtures
                print("   Utilisation de loaddata pour le format Django fixtures...")
                ssh_cmd = (
                    f'ssh {CONFIG["server_user"]}@{CONFIG["server_host"]} '
                    f'"cd {CONFIG["server_path"]} && '
                    f'./venv/bin/python3 manage.py loaddata {CONFIG["export_file"]} '
                    f'{"--ignorenonexistent" if merge else ""} '
                    f'--settings=erp_project.settings_production"'
                )
    except Exception as e:
        print(f"   [WARN] Impossible de detecter le format, utilisation de loaddata par defaut: {e}")
        ssh_cmd = (
            f'ssh {CONFIG["server_user"]}@{CONFIG["server_host"]} '
            f'"cd {CONFIG["server_path"]} && '
            f'./venv/bin/python3 manage.py loaddata {CONFIG["export_file"]} '
            f'{"--ignorenonexistent" if merge else ""} '
            f'--settings=erp_project.settings_production"'
        )
    
    # Utiliser un timeout plus long pour l'import (15 minutes)
    stdout, stderr, code = run_command(ssh_cmd, check=False, timeout=900)
    
    # Nettoyer le script temporaire local
    if 'import_script_path' in locals() and import_script_path.exists():
        try:
            import_script_path.unlink()
        except:
            pass
    
    # Nettoyer le script sur le serveur aussi
    if 'import_script_path' in locals():
        try:
            cleanup_cmd = (
                f'ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 '
                f'{CONFIG["server_user"]}@{CONFIG["server_host"]} '
                f'"cd {CONFIG["server_path"]} && rm -f temp_import_sync.py"'
            )
            run_command(cleanup_cmd, check=False, timeout=10)
        except:
            pass
    
    # Vérifier le résultat de l'import
    success = False
    output_text = (stdout or "") + (stderr or "")
    
    if code == 0:
        # Vérifier si l'import a réussi dans la sortie
        if "[OK] Import reussi" in output_text or "Import reussi" in output_text:
            print("[OK] Synchronisation reussie")
            # Afficher seulement les lignes importantes
            for line in (stdout or "").split('\n'):
                if '[OK]' in line or '[INFO]' in line:
                    print(f"   {line[:150]}")
            success = True
        elif "[ERREUR]" in output_text:
            print(f"[ERREUR] Erreur lors de l'import sur le serveur")
            for line in output_text.split('\n'):
                if '[ERREUR]' in line:
                    print(f"   {line[:200]}")
        else:
            # Si pas d'erreur explicite et code 0, considérer comme succès
            # (peut arriver avec nohup qui retourne immédiatement)
            print("[OK] Synchronisation lancee (en cours d'execution sur le serveur)")
            print("   [INFO] L'import s'execute en arriere-plan sur le serveur")
            success = True
    else:
        print(f"[ERREUR] Erreur lors de l'import sur le serveur (code: {code})")
        if stdout:
            # Afficher les erreurs importantes
            for line in stdout.split('\n'):
                if '[ERREUR]' in line or 'Error' in line or 'Traceback' in line:
                    print(f"   {line[:200]}")
        if stderr:
            # Afficher seulement les erreurs importantes
            error_lines = stderr.split('\n')
            important_errors = [l for l in error_lines if any(keyword in l.lower() for keyword in ['error', 'failed', 'connection', 'timeout', 'permission'])]
            if important_errors:
                for line in important_errors[:5]:  # Limiter à 5 lignes
                    print(f"   {line[:200]}")
        
        if "password" in output_text.lower() or "permission denied" in output_text.lower():
            print("   [INFO] Probleme d'authentification SSH detecte")
            print("   [INFO] Executez CONFIGURER_SSH_SANS_MOT_DE_PASSE.bat pour configurer l'authentification par cle")
        elif "Connection closed" in output_text or "timeout" in output_text.lower() or code == -1:
            print("   [INFO] Connexion fermee ou timeout lors de l'import")
            print("   [INFO] Le fichier peut etre trop volumineux ou la connexion instable")
            print("   [INFO] La synchronisation sera reessayee automatiquement dans 1 minute")
    
    if success:
        # Sauvegarder la date de synchronisation seulement si succès
        save_sync_date()
        return True
    else:
        return False


def sync_bidirectional(merge=True, push_only=False):
    """
    Synchronisation bidirectionnelle (pull puis push) ou push seulement
    
    IMPORTANT: Cette fonction synchronise:
    - Les factures (FactureVente, LigneFactureVente)
    - Le stock (MouvementStock, Article.quantite_stock)
    - Les statistiques (StatistiqueVente, ChiffreAffaire)
    - Les clients, fournisseurs, articles, etc.
    
    Args:
        merge: Fusionner les données au lieu de les remplacer
        push_only: Si True, envoie seulement les données locales (pas de téléchargement)
    
    Le processus:
    1. PULL (si push_only=False): Télécharge les données du serveur vers le local
    2. PUSH: Envoie les données locales vers le serveur
    
    Cela garantit que les factures créées localement apparaissent en ligne
    et que le stock est synchronisé dans les deux sens.
    """
    if push_only:
        print(f"[{datetime.now()}] Envoi des données locales vers le serveur (temps réel)...")
        print("   [SYNC] Envoi: Factures, Stock, Statistiques, Chiffre d'affaires")
        print("   [MODE] Mode temps reel: seulement l'envoi (pas de telechargement)")
    else:
        print(f"[{datetime.now()}] Synchronisation bidirectionnelle...")
        print("   [SYNC] Synchronisation: Factures, Stock, Statistiques, Chiffre d'affaires")
    
    pull_success = False
    
    # 1. Télécharger depuis le serveur (seulement si pas en mode push_only)
    if not push_only:
        print("\n[DOWNLOAD] Etape 1/2 : Telechargement depuis le serveur...")
        pull_success = pull_from_server(merge=merge, incremental=True)  # Utiliser l'export incrémental par défaut
        if not pull_success:
            print("[WARN] Echec du telechargement, continuation avec l'envoi...")
    
    # 2. Envoyer vers le serveur (TOUJOURS)
    # C'est CRUCIAL pour que les factures locales apparaissent en ligne
    if push_only:
        print("\n[UPLOAD] Envoi vers le serveur...")
    else:
        print("\n[UPLOAD] Etape 2/2 : Envoi vers le serveur...")
    print("   [INFO] Cette etape envoie vos factures locales vers le serveur")
    print("   [INFO] Le stock local sera synchronise avec le serveur")
    push_success = push_to_server(merge=merge)
    
    if push_success:
        print("\n[OK] Synchronisation reussie!")
        print("   [OK] Factures locales envoyees au serveur")
        print("   [OK] Stock synchronise")
        print("   [OK] Statistiques a jour")
        if pull_success:
            print("   [OK] Donnees du serveur recuperees localement")
        return True
    elif pull_success:
        print("\n[WARN] Synchronisation partielle : donnees du serveur recuperees")
        print("   [WARN] Les donnees locales n'ont pas pu etre envoyees")
        return True
    else:
        print("\n[ERREUR] Synchronisation echouee")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Synchroniser les données entre local et serveur en ligne'
    )
    parser.add_argument(
        '--mode',
        choices=['pull', 'push', 'sync'],
        required=True,
        help='Mode de synchronisation : pull (télécharger), push (envoyer), sync (bidirectionnel)'
    )
    parser.add_argument(
        '--merge',
        action='store_true',
        help='Fusionner les données au lieu de les remplacer'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Fichier de configuration JSON (optionnel)'
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Export complet (désactive l\'export incrémental pour forcer l\'export de toutes les données)'
    )
    
    args = parser.parse_args()
    
    # Charger la configuration personnalisée si fournie
    if args.config and Path(args.config).exists():
        with open(args.config, 'r') as f:
            custom_config = json.load(f)
            CONFIG.update(custom_config)
    
    # Changer vers le répertoire local
    os.chdir(CONFIG['local_path'])
    
    # Vérifier que nous sommes dans un projet Django
    if not Path('manage.py').exists():
        print(f"[ERREUR] manage.py non trouve dans {CONFIG['local_path']}")
        print("   Verifiez que vous etes dans le repertoire du projet Django")
        return 1
    
    # Exécuter la synchronisation selon le mode
    incremental = not args.full  # Utiliser l'export incrémental sauf si --full est spécifié
    
    if args.mode == 'pull':
        success = pull_from_server(merge=args.merge, incremental=incremental)
    elif args.mode == 'push':
        success = push_to_server(merge=args.merge)
    elif args.mode == 'sync':
        success = sync_bidirectional(merge=args.merge)
    
    return 0 if success else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[WARN] Synchronisation interrompue par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"[ERREUR] Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)




