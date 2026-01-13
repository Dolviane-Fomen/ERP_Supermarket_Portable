@echo off
REM Créer le fichier .env pour la base partagée

if exist ".env" (
    echo Fichier .env existe deja
    echo Voulez-vous le remplacer? (o/n)
    set /p replace="> "
    if /i not "%replace%"=="o" exit /b
)

(
echo # Base de donnees partagee sur OVH
echo SHARED_DB_NAME=erp_db
echo SHARED_DB_USER=erp_user
echo SHARED_DB_PASSWORD=
echo SHARED_DB_HOST=51.68.124.152
echo SHARED_DB_PORT=5432
) > .env

echo Fichier .env cree!
echo.
echo IMPORTANT: Remplissez SHARED_DB_PASSWORD avec le mot de passe PostgreSQL
echo.
notepad .env
pause




