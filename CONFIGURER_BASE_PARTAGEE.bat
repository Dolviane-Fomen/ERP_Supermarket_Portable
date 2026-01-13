@echo off
REM Script pour configurer la base de donnees partagee sur OVH

echo ========================================
echo Configuration Base de Donnees Partagee
echo ========================================
echo.
echo Cette configuration permettra a tous les PCs d'utiliser
echo la meme base de donnees PostgreSQL sur OVH.
echo.
echo Les modifications en local seront visibles EN TEMPS REEL en ligne!
echo.

REM Verifier si .env existe
if not exist ".env" (
    echo Creation du fichier .env...
    copy env.example.txt .env >nul
    echo Fichier .env cree
    echo.
)

echo.
echo Vous devez maintenant:
echo 1. Configurer PostgreSQL sur OVH pour accepter les connexions distantes
echo 2. Remplir les informations de connexion dans .env
echo.
echo Ouvrez le fichier .env et ajoutez:
echo.
echo SHARED_DB_NAME=erp_db
echo SHARED_DB_USER=erp_user
echo SHARED_DB_PASSWORD=VOTRE_MOT_DE_PASSE_POSTGRESQL
echo SHARED_DB_HOST=51.68.124.152
echo SHARED_DB_PORT=5432
echo.
echo Ensuite, changez manage.py pour utiliser settings_shared_db
echo.
pause




