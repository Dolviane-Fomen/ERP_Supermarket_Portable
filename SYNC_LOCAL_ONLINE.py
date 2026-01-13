#!/usr/bin/env python
"""
Script de synchronisation entre environnement local et serveur en ligne
"""
import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration par défaut (à personnaliser)
CONFIG = {
    'server_host': 'VOTRE_IP_SERVEUR',  # Ex: '123.45.67.89'
    'server_user': 'erpuser',
    'server_path': '/home/erpuser/ERP_Supermarket_Portable',
    'local_path': str(Path(__file__).parent.resolve()),
    'export_file': 'sync_export.json',
    'backup_dir': 'backups',
}


def run_command(cmd, check=True):
    """Exécuter une commande et retourner le résultat"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution : {cmd}")
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
        print(f"✅ Sauvegarde créée : {backup_file}")
        return backup_file
    else:
        print("⚠️  Base de données locale non trouvée")
        return None


def export_local_data(agence_id=None):
    """Exporter les données locales"""
    print(f"[{datetime.now()}] Export des données locales...")
    
    cmd = f'python manage.py dumpdata'
    
    # Ajouter des options selon les besoins
    exclude = ['contenttypes', 'sessions', 'admin.logentry']
    cmd += ' ' + ' '.join([f'--exclude {x}' for x in exclude])
    
    if agence_id:
        # Note: dumpdata ne supporte pas directement le filtre par agence
        # Il faudrait utiliser l'interface d'export web ou un script personnalisé
        print("⚠️  Filtrage par agence non supporté par dumpdata, export complet...")
    
    export_file = Path(CONFIG['local_path']) / CONFIG['export_file']
    cmd += f' > "{export_file}"'
    
    stdout, stderr, code = run_command(cmd, check=False)
    
    if code == 0 and export_file.exists():
        size = export_file.stat().st_size / 1024 / 1024  # Taille en MB
        print(f"✅ Export réussi : {export_file} ({size:.2f} MB)")
        return export_file
    else:
        print(f"❌ Erreur lors de l'export : {stderr}")
        return None


def import_local_data(export_file, merge=False):
    """Importer des données dans l'environnement local"""
    print(f"[{datetime.now()}] Import des données dans l'environnement local...")
    
    export_path = Path(export_file)
    if not export_path.exists():
        print(f"❌ Fichier d'export introuvable : {export_file}")
        return False
    
    # Faire une sauvegarde avant l'import
    backup_database()
    
    cmd = f'python manage.py loaddata "{export_path}"'
    if merge:
        cmd += ' --merge'
    
    stdout, stderr, code = run_command(cmd, check=False)
    
    if code == 0:
        print("✅ Import réussi")
        return True
    else:
        print(f"❌ Erreur lors de l'import : {stderr}")
        return False


def pull_from_server(merge=False):
    """Télécharger les données depuis le serveur en ligne"""
    print(f"[{datetime.now()}] Téléchargement depuis le serveur en ligne...")
    
    # Exporter depuis le serveur
    print("   📤 Export depuis le serveur...")
    ssh_cmd = (
        f'ssh {CONFIG["server_user"]}@{CONFIG["server_host"]} '
        f'"cd {CONFIG["server_path"]} && '
        f'python manage.py dumpdata --exclude contenttypes --exclude sessions '
        f'--exclude admin.logentry --settings=erp_project.settings_production > {CONFIG["export_file"]}"'
    )
    
    stdout, stderr, code = run_command(ssh_cmd, check=False)
    if code != 0:
        print(f"❌ Erreur lors de l'export sur le serveur : {stderr}")
        return False
    
    # Télécharger le fichier
    print("   📥 Téléchargement du fichier...")
    scp_cmd = (
        f'scp {CONFIG["server_user"]}@{CONFIG["server_host"]}:'
        f'{CONFIG["server_path"]}/{CONFIG["export_file"]} '
        f'"{CONFIG["local_path"]}"'
    )
    
    stdout, stderr, code = run_command(scp_cmd, check=False)
    if code != 0:
        print(f"❌ Erreur lors du téléchargement : {stderr}")
        print("   💡 Assurez-vous que SSH/SCP est configuré et accessible")
        return False
    
    # Importer localement
    local_export = Path(CONFIG['local_path']) / CONFIG['export_file']
    return import_local_data(local_export, merge=merge)


def push_to_server(merge=False):
    """Envoyer les données locales vers le serveur en ligne"""
    print(f"[{datetime.now()}] Envoi vers le serveur en ligne...")
    
    # Exporter localement
    export_file = export_local_data()
    if not export_file:
        return False
    
    # Transférer vers le serveur
    print("   📤 Transfert vers le serveur...")
    scp_cmd = (
        f'scp "{export_file}" '
        f'{CONFIG["server_user"]}@{CONFIG["server_host"]}:'
        f'{CONFIG["server_path"]}/'
    )
    
    stdout, stderr, code = run_command(scp_cmd, check=False)
    if code != 0:
        print(f"❌ Erreur lors du transfert : {stderr}")
        print("   💡 Assurez-vous que SSH/SCP est configuré et accessible")
        return False
    
    # Importer sur le serveur
    print("   📥 Import sur le serveur...")
    ssh_cmd = (
        f'ssh {CONFIG["server_user"]}@{CONFIG["server_host"]} '
        f'"cd {CONFIG["server_path"]} && '
        f'python manage.py loaddata {CONFIG["export_file"]} '
        f'{"--merge" if merge else ""} '
        f'--settings=erp_project.settings_production"'
    )
    
    stdout, stderr, code = run_command(ssh_cmd, check=False)
    if code == 0:
        print("✅ Synchronisation réussie")
        return True
    else:
        print(f"❌ Erreur lors de l'import sur le serveur : {stderr}")
        return False


def sync_bidirectional(merge=True):
    """Synchronisation bidirectionnelle (pull puis push)"""
    print(f"[{datetime.now()}] Synchronisation bidirectionnelle...")
    
    # 1. Télécharger depuis le serveur
    print("\n📥 Étape 1/2 : Téléchargement depuis le serveur...")
    if not pull_from_server(merge=merge):
        print("⚠️  Échec du téléchargement, continuation avec l'envoi...")
    
    # 2. Envoyer vers le serveur
    print("\n📤 Étape 2/2 : Envoi vers le serveur...")
    if not push_to_server(merge=merge):
        print("⚠️  Échec de l'envoi")
        return False
    
    print("\n✅ Synchronisation bidirectionnelle terminée")
    return True


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
        print(f"❌ manage.py non trouvé dans {CONFIG['local_path']}")
        print("   Vérifiez que vous êtes dans le répertoire du projet Django")
        return 1
    
    # Exécuter la synchronisation selon le mode
    if args.mode == 'pull':
        success = pull_from_server(merge=args.merge)
    elif args.mode == 'push':
        success = push_to_server(merge=args.merge)
    elif args.mode == 'sync':
        success = sync_bidirectional(merge=args.merge)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())




