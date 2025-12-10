import os
import json
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp_project.settings")

import django  # noqa: E402

django.setup()

from supermarket.export_import import export_data, import_data  # noqa: E402


def main():
    print(">>> Export des données en cours...")
    data = export_data()
    export_path = Path("test_export_all.json")
    export_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Fichier exporté: {export_path.resolve()}")

    print(">>> Import des données en cours (sans suppression préalable)...")
    stats = import_data(data, agence_id=None, clear_existing=False)
    print("Résultat de l'import:")
    for key, value in stats.items():
        if key == "errors":
            print(f"  {key}: {len(value)} erreurs")
            if value:
                print("    Exemple:", value[:3])
        else:
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()








