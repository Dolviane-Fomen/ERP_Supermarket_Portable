@echo off
REM Configuration automatique de la synchronisation sur tous les PCs
REM Ce script configure tout ce qui est necessaire pour la synchronisation

setlocal enabledelayedexpansion

echo ========================================
echo CONFIGURATION AUTOMATIQUE SYNCHRONISATION
echo ========================================
echo.
echo Ce script va configurer:
echo  1. Fichier .ovh_config.json
echo  2. manage.py pour utiliser SQLite local
echo  3. Verification des dependances
echo  4. Test de connexion SSH
echo.

REM Changer vers le repertoire du projet
cd /d "%~dp0"

REM ========================================
REM ETAPE 1: Configuration .ovh_config.json
REM ========================================
echo [1/4] Configuration du fichier .ovh_config.json...

if exist ".ovh_config.json" (
    echo   Fichier .ovh_config.json existe deja
    echo   Voulez-vous le recreer? (O/N)
    set /p recreate="   Votre choix: "
    if /i not "!recreate!"=="O" (
        echo   Conservation du fichier existant
        goto :check_manage
    )
)

echo   Creation du fichier .ovh_config.json...
(
    echo {
    echo     "git_branch":  "main",
    echo     "deployment_method":  "git",
    echo     "ovh_project_path":  "/home/ubuntu/erp_project",
    echo     "ovh_host":  "51.68.124.152",
    echo     "git_remote":  "origin",
    echo     "ovh_user":  "ubuntu",
    echo     "shared_db_host":  "51.68.124.152",
    echo     "shared_db_port":  "5432",
    echo     "shared_db_name":  "erp_db",
    echo     "shared_db_user":  "erp_user"
    echo }
) > .ovh_config.json

echo   [OK] Fichier .ovh_config.json cree

:check_manage
REM ========================================
REM ETAPE 2: Configuration manage.py pour SQLite local
REM ========================================
echo.
echo [2/4] Configuration de manage.py pour SQLite local...

findstr /C:"settings_shared_db" manage.py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   Modification de manage.py pour utiliser SQLite local...
    powershell -Command "(Get-Content manage.py) -replace 'settings_shared_db', 'settings' | Set-Content manage.py"
    echo   [OK] manage.py configure pour SQLite local
) else (
    findstr /C:"settings" manage.py >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] manage.py utilise deja SQLite local
    ) else (
        echo   [ATTENTION] Impossible de determiner la configuration de manage.py
    )
)

REM ========================================
REM ETAPE 3: Verification des dependances
REM ========================================
echo.
echo [3/4] Verification des dependances...

REM Verifier Python
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Python est installe
    set PYTHON_CMD=py
) else (
    python --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Python est installe
        set PYTHON_CMD=python
    ) else (
        echo   [ERREUR] Python n'est pas installe!
        echo   Installez Python avant de continuer.
        pause
        exit /b 1
    )
)

REM Verifier Django
%PYTHON_CMD% -c "import django; print(django.get_version())" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Django est installe
) else (
    echo   [ATTENTION] Django n'est pas installe
    echo   Installation de Django...
    %PYTHON_CMD% -m pip install django
)

REM Verifier si psycopg2 est installe (optionnel, pour base partagee)
%PYTHON_CMD% -m pip show psycopg2-binary >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] psycopg2-binary est installe (pour base partagee optionnelle)
) else (
    echo   [INFO] psycopg2-binary n'est pas installe (optionnel)
)

REM ========================================
REM ETAPE 4: Configuration SSH
REM ========================================
echo.
echo [4/4] Configuration SSH pour la synchronisation...

REM Verifier si SSH est disponible
where ssh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo   [OK] SSH est disponible
    
    echo.
    echo   Test de connexion au serveur OVH...
    echo   (Vous devrez peut-etre entrer le mot de passe)
    echo.
    
    ssh -o ConnectTimeout=5 -o BatchMode=yes ubuntu@51.68.124.152 "echo 'Connexion OK'" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] Connexion SSH fonctionne (avec cles SSH)
    ) else (
        echo   [INFO] Connexion SSH necessitera un mot de passe
        echo   Pour eviter de taper le mot de passe a chaque fois:
        echo   1. Generez une cle SSH: ssh-keygen -t rsa
        echo   2. Copiez-la sur le serveur: ssh-copy-id ubuntu@51.68.124.152
    )
) else (
    echo   [ATTENTION] SSH n'est pas dans le PATH
    echo   Installez Git for Windows ou OpenSSH
    echo   SSH est necessaire pour la synchronisation
)

REM ========================================
REM ETAPE 5: Creation des dossiers necessaires
REM ========================================
echo.
echo [5/5] Creation des dossiers necessaires...

if not exist "backups" (
    mkdir backups
    echo   [OK] Dossier backups cree
) else (
    echo   [OK] Dossier backups existe deja
)

REM ========================================
REM RESUME
REM ========================================
echo.
echo ========================================
echo CONFIGURATION TERMINEE!
echo ========================================
echo.
echo Fichiers configures:
echo   [OK] .ovh_config.json
echo   [OK] manage.py (SQLite local)
echo.
echo Pour utiliser la synchronisation:
echo   1. SYNC_LOCAL_ONLINE.bat pull  - Telecharger depuis serveur
echo   2. SYNC_LOCAL_ONLINE.bat push  - Envoyer vers serveur
echo   3. SYNC_LOCAL_ONLINE.bat sync  - Synchronisation bidirectionnelle
echo.
echo IMPORTANT:
echo   - Travaillez en local avec SQLite (hors ligne OK)
echo   - Synchronisez quand vous avez Internet
echo   - Faites un PULL avant de commencer a travailler
echo   - Faites un PUSH apres avoir termine
echo.
pause
