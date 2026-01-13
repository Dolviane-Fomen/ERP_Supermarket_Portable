@echo off
REM Activer la base de donnees partagee (temps reel)

REM Changer vers le repertoire du projet
cd /d "%~dp0"

echo ========================================
echo Activation Base de Donnees Partagee
echo ========================================
echo.
echo Cette configuration permettra que toutes vos modifications
echo en local (factures, stock, statistiques) soient visibles
echo IMMEDIATEMENT en ligne (temps reel).
echo.

REM Verifier si .env existe
if not exist ".env" (
    echo Creation du fichier .env...
    copy env.example.txt .env >nul
)

echo.
echo Ouvrez le fichier .env et ajoutez ces lignes:
echo.
echo SHARED_DB_NAME=erp_db
echo SHARED_DB_USER=erp_user
echo SHARED_DB_PASSWORD=VOTRE_MOT_DE_PASSE_POSTGRESQL
echo SHARED_DB_HOST=51.68.124.152
echo SHARED_DB_PORT=5432
echo.

REM Verifier si .env existe
if not exist ".env" (
    echo Creation du fichier .env...
    copy env.example.txt .env >nul
)

REM Verifier si les variables sont deja dans .env
findstr /C:"SHARED_DB_NAME" .env >nul 2>&1
if errorlevel 1 (
    echo Ajout des variables dans .env...
    (
        echo.
        echo # Base de donnees partagee sur OVH (temps reel)
        echo SHARED_DB_NAME=erp_db
        echo SHARED_DB_USER=erp_user
        echo SHARED_DB_PASSWORD=MonVps2026Secure
        echo SHARED_DB_HOST=51.68.124.152
        echo SHARED_DB_PORT=5432
    ) >> .env
    echo Variables ajoutees!
) else (
    echo Variables deja presentes dans .env
)

echo.
echo Verification de psycopg2-binary (necessaire pour PostgreSQL)...
REM Activer l'environnement virtuel si il existe
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Essayer py d'abord (Windows), puis python
py -m pip show psycopg2-binary >nul 2>&1
if errorlevel 1 (
    python -m pip show psycopg2-binary >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ATTENTION: psycopg2-binary n'est pas installe!
        echo.
        echo Installation en cours...
        py -m pip install psycopg2-binary
        if errorlevel 1 (
            python -m pip install psycopg2-binary
            if errorlevel 1 (
                echo.
                echo ERREUR: Impossible d'installer psycopg2-binary automatiquement.
                echo Executez INSTALLER_PSYCOPG2.bat manuellement.
                echo.
            ) else (
                echo.
                echo SUCCESS: psycopg2-binary installe!
                echo.
            )
        ) else (
            echo.
            echo SUCCESS: psycopg2-binary installe!
            echo.
        )
    ) else (
        echo psycopg2-binary est deja installe.
    )
) else (
    echo psycopg2-binary est deja installe.
)

echo.
echo ========================================
echo Configuration terminee!
echo ========================================
echo.
echo Pour utiliser la base partagee:
echo   - manage.py utilise deja settings_shared_db
echo   - Les modifications en local seront visibles en ligne en temps reel!
echo.
echo Pour tester la connexion:
echo   - Double-cliquez sur TESTER_CONNEXION_DB.bat
echo.
echo Pour revenir a SQLite local:
echo   - Changez manage.py: settings_standalone au lieu de settings_shared_db
echo.
pause

