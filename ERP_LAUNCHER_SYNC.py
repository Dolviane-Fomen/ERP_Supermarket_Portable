#!/usr/bin/env python
"""
Service de synchronisation automatique pour ERP_Launcher.

Chaque PC garde sa base locale. À intervalle régulier :
    1. On exporte les données de l'agence locale vers un dossier partagé.
    2. On importe les fichiers reçus depuis les autres PC.

La configuration se trouve dans erp_sync/erp_launcher_config.json.
"""

import json
import os
import socket
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp_project.settings_standalone")
django.setup()

from supermarket.export_import import export_data, import_data  # noqa: E402


class ERPLauncherSync:
    def __init__(self):
        self.config = self._load_config()
        self.enabled = self.config.get("erp_launcher_sync", False)
        self.interval = int(self.config.get("sync_interval", 300))

        self.local_name = self._detect_pc_name()
        self.machine_config = self._get_machine_config(self.local_name)

        self.agence_id = self.machine_config.get("agence_id")
        self.local_sync_dir = Path(self.machine_config.get("local_sync_dir", "C:/erp_sync"))
        self.remote_targets: List[Dict] = self.machine_config.get("remote_targets", [])

        self.outbox_dir = self.local_sync_dir / "sortant"
        self.inbox_dir = self.local_sync_dir / "entrant"
        self.archive_dir = self.local_sync_dir / "archive"
        self.logs_dir = self.local_sync_dir / "logs"
        for folder in [self.outbox_dir, self.inbox_dir, self.archive_dir, self.logs_dir]:
            folder.mkdir(parents=True, exist_ok=True)

        self.log_file = self.logs_dir / "sync.log"
        self.running = False
        self.thread: threading.Thread | None = None

        self._log(f"Configuration chargée pour {self.local_name} (agence {self.agence_id})")

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------
    def _load_config(self) -> Dict:
        config_path = Path("erp_sync/erp_launcher_config.json")
        if not config_path.exists():
            raise FileNotFoundError("Fichier erp_sync/erp_launcher_config.json introuvable.")
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    
    def _detect_pc_name(self) -> str:
        return os.environ.get("COMPUTERNAME") or socket.gethostname()

    def _get_machine_config(self, pc_name: str) -> Dict:
        machines = self.config.get("machines", {})
        lowered = {name.lower(): cfg for name, cfg in machines.items()}
        match = lowered.get(pc_name.lower())
        if match:
            return match

        default_cfg = lowered.get("default")
        if default_cfg:
            self._log(f"[AVERTISSEMENT] Configuration propre à '{pc_name}' introuvable. "
                      "Utilisation de la section 'default'.", level="WARN")
            return default_cfg

        raise KeyError(
            f"Aucune configuration machine pour '{pc_name}'. "
            "Ajoutez son entrée dans erp_sync/erp_launcher_config.json > machines."
        )

    # ------------------------------------------------------------------
    # Gestion du service
    # ------------------------------------------------------------------
    def start(self):
        if not self.enabled:
            self._log("Synchronisation ERP_Launcher désactivée dans la configuration.")
            return

        if self.running:
            return

            self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()
        self._log("Service de synchronisation démarré.")

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
        self._log("Service de synchronisation arrêté.")

    def _loop(self):
        while self.running:
            try:
                self._export_and_share()
                self._import_inbox()
            except Exception as exc:
                self._log(f"Erreur inattendue: {exc}", level="ERROR")
            finally:
                time.sleep(self.interval)

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------
    def _export_and_share(self):
        if not self.agence_id:
            self._log("Agence locale non définie, export annulé.", level="WARN")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_file = self.outbox_dir / f"export_{self.local_name}_{timestamp}.json"

        self._log("Export des données locales...")
        try:
            data = export_data(agence_id=self.agence_id, include_users=False)
            with export_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            self._log(f"  ✓ Export créé: {export_file}")
        except Exception as exc:
            self._log(f"  ❌ Export échoué: {exc}", level="ERROR")
            return

        for target in self.remote_targets:
            self._send_to_remote(export_file, target)

    def _send_to_remote(self, source_file: Path, target: Dict):
        remote_root = Path(target.get("path", ""))
        target_name = target.get("name") or str(remote_root)
        remote_inbox = remote_root / "entrant"

        try:
            remote_inbox.mkdir(parents=True, exist_ok=True)
            destination = remote_inbox / source_file.name
            destination.write_bytes(source_file.read_bytes())
            self._log(f"  → Export envoyé vers {target_name}")
        except Exception as exc:
            self._log(f"  ❌ Envoi vers {target_name} impossible: {exc}", level="ERROR")

    # ------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------
    def _import_inbox(self):
        files = sorted(self.inbox_dir.glob("*.json"))
        if not files:
            self._log("Aucun fichier reçu.")
            return

        self._log(f"{len(files)} fichier(s) à traiter dans l'inbox.")
        for json_file in files:
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                stats = import_data(data, agence_id=self.agence_id, clear_existing=False)
                self._log(f"  ✓ Import {json_file.name}: {stats}")

                archive_name = f"{json_file.stem}_{datetime.now():%Y%m%d_%H%M%S}.json"
                json_file.rename(self.archive_dir / archive_name)
            except Exception as exc:
                self._log(f"  ❌ Import échoué ({json_file.name}): {exc}", level="ERROR")

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    def _log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] [{self.local_name}] [{level}] {message}"
        print(line)
        try:
            with self.log_file.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass


if __name__ == "__main__":
    service = ERPLauncherSync()
    service.start()
    try:
        while service.enabled:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        service.stop()
