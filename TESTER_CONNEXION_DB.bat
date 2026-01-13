@echo off
REM Script pour tester la connexion a la base de donnees partagee

echo ========================================
echo Test de connexion a la base partagee
echo ========================================
echo.

REM Changer vers le repertoire du projet
cd /d "%~dp0"

REM Activer l'environnement virtuel si il existe
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Tester la connexion
echo Test de connexion a PostgreSQL sur OVH...
echo.

REM Essayer avec py (Windows) d'abord, puis python
py manage.py migrate --settings=erp_project.settings_shared_db --check 2>nul
if errorlevel 1 (
    python manage.py migrate --settings=erp_project.settings_shared_db --check 2>nul
    if errorlevel 1 (
        echo ERREUR: Python non trouve!
        echo Essayez d'utiliser: py manage.py migrate --settings=erp_project.settings_shared_db --check
        echo.
        goto :error
    )
)

if errorlevel 1 (
    :error
    echo.
    echo ERREUR: Impossible de se connecter a la base de donnees!
    echo.
    echo Verifiez:
    echo 1. Le fichier .env contient les bonnes informations
    echo 2. PostgreSQL sur OVH accepte les connexions distantes
    echo 3. Le port 5432 est ouvert dans le firewall
    echo 4. psycopg2-binary est installe: py -m pip install psycopg2-binary
    echo 5. Le fichier .env existe dans le repertoire du projet
    echo.
    goto :end
)

echo.
echo ========================================
echo SUCCESS: Connexion OK!
echo ========================================
echo.
echo Vous pouvez maintenant utiliser la base partagee.
echo Les modifications en local seront visibles en ligne en temps reel!
echo.

:end

pause

