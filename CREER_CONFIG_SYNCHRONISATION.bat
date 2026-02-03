@echo off
chcp 65001 >nul
echo ============================================================
echo   CREATION DU FICHIER DE CONFIGURATION SYNCHRONISATION
echo ============================================================
echo.

REM Verifier si le fichier existe deja
if exist .ovh_config.json (
    echo [INFO] Le fichier .ovh_config.json existe deja.
    echo [INFO] Voulez-vous le recreer avec les valeurs par defaut?
    echo.
    choice /C ON /M "O=Oui, N=Non"
    if errorlevel 2 goto :fin
    if errorlevel 1 goto :creer
    goto :fin
)

:creer
echo Creation automatique du fichier .ovh_config.json...
echo Configuration serveur OVH (identique pour tous les utilisateurs):
echo   - Serveur: ubuntu@51.68.124.152
echo   - Chemin: /home/ubuntu/erp_project
echo.

(
echo {
echo     "ovh_host": "51.68.124.152",
echo     "ovh_user": "ubuntu",
echo     "ovh_project_path": "/home/ubuntu/erp_project"
echo }
) > .ovh_config.json

echo [OK] Fichier .ovh_config.json cree avec succes!
echo.
echo Configuration enregistree:
echo   - Serveur: ubuntu@51.68.124.152
echo   - Chemin: /home/ubuntu/erp_project
echo.
echo Vous pouvez maintenant utiliser la synchronisation.
echo.

:fin
pause
