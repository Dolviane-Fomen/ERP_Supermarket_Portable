import os
import shutil
import sys
from pathlib import Path


CACHE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
CACHE_FILE_SUFFIXES = (".pyc", ".pyo")
EXTRA_PATHS_TO_CLEAN = [
    "staticfiles",  # collectstatic output
]


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink(missing_ok=True)


def clean_cache(root: Path) -> None:
    removed_dirs = 0
    removed_files = 0

    for current, dirs, files in os.walk(root):
        current_path = Path(current)

        # Supprimer les dossiers cache connus
        for dir_name in list(dirs):
            if dir_name in CACHE_DIR_NAMES:
                cache_dir = current_path / dir_name
                shutil.rmtree(cache_dir, ignore_errors=True)
                dirs.remove(dir_name)  # éviter de descendre dedans
                removed_dirs += 1

        # Supprimer les fichiers .pyc / .pyo
        for file_name in files:
            if file_name.endswith(CACHE_FILE_SUFFIXES):
                file_path = current_path / file_name
                file_path.unlink(missing_ok=True)
                removed_files += 1

    # Dossiers additionnels à nettoyer
    for rel_path in EXTRA_PATHS_TO_CLEAN:
        extra_dir = root / rel_path
        if extra_dir.exists():
            shutil.rmtree(extra_dir, ignore_errors=True)

    print("==============================================")
    print("  NETTOYAGE CACHE PYTHON / DJANGO TERMINÉ")
    print("==============================================")
    print(f"Répertoire racine: {root}")
    print(f"Dossiers supprimés: {removed_dirs}")
    print(f"Fichiers supprimés: {removed_files}")
    print("----------------------------------------------")
    print("Vous pouvez maintenant relancer ERP_Launcher.bat")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent
    clean_cache(project_root)







