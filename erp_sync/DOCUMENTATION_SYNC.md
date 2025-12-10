## Mise en place de la synchronisation locale

1. Exécuter `INIT_SYNC_ENV.bat` sur chaque PC (crée `C:\erp_sync\{entrant,sortant,archive,logs}`).
2. Partager `C:\erp_sync` avec droits lecture/écriture (ex. `\\CAISSE01\erp_sync`).
3. Ajuster `erp_sync/erp_launcher_config.json` : pour chaque PC, définir `agence_id`, `local_sync_dir`, et la liste des `remote_targets` (chemins UNC vers les autres postes).
   - Option : utiliser `CONFIG_SYNC.ps1 -PcName "CAISSE01" -AgenceId 8 -RemoteShare "\\COMPTA01\erp_sync"`.
4. Lancer `ERP_Launcher.bat` sur chaque machine : le script démarre Django + `ERP_LAUNCHER_SYNC.py` (boucle export/import automatique).
5. Vérifier `C:\erp_sync\logs\sync.log` pour confirmer la réussite (exports, imports, erreurs).  
6. En cas de nouveau PC, répéter les étapes 1-3 et ajouter son entrée dans la config JSON.  
7. Les utilisateurs n'ont rien à faire : la synchronisation tourne en arrière-plan.  








