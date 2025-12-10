import os
import subprocess
import sys
from pathlib import Path


def run_migrations():
    """
    Execute `python manage.py migrate --noinput` from the ERP root folder.
    This script is meant to be executed on any target PC to bootstrap the DB.
    """
    project_root = Path(__file__).resolve().parent
    manage_py = project_root / "manage.py"

    if not manage_py.exists():
        print("[ERREUR] Fichier manage.py introuvable.")
        print(f"Chemin attendu : {manage_py}")
        sys.exit(1)

    env = os.environ.copy()
    env.setdefault("DJANGO_SETTINGS_MODULE", "erp_project.settings")

    command = [sys.executable, "manage.py", "migrate", "--noinput"]

    print("===============================================")
    print(" Initialisation de la base de données ERP")
    print("===============================================")
    print(f"Chemin du projet : {project_root}")
    print(f"Commande exécutée : {' '.join(command)}")
    print("-----------------------------------------------")

    try:
        result = subprocess.run(
            command,
            cwd=project_root,
            env=env,
            check=True,
        )
        if result.returncode == 0:
            print("[OK] Migrations exécutées avec succès.")
    except subprocess.CalledProcessError as exc:
        print("[ERREUR] Échec de l'exécution des migrations.")
        print(f"Code de retour : {exc.returncode}")
        sys.exit(exc.returncode)


if __name__ == "__main__":
    run_migrations()







