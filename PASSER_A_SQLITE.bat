@echo off
chcp 65001 > nul
color 0B
title Migration vers SQLite

cls
echo.
echo ============================================================
echo    MIGRATION VERS SQLITE
echo ============================================================
echo.
echo Ce script va :
echo   1. Arreter Django
echo   2. Configurer SQLite (deja fait)
echo   3. Creer une nouvelle base SQLite
echo   4. Appliquer toutes les migrations
echo   5. Redemarrer le serveur
echo.
echo ⚠️  ATTENTION : Cela va creer une NOUVELLE base de donnees vide !
echo    (Les anciennes donnees PostgreSQL ne seront pas transferees)
echo.
echo ============================================================
echo.
pause

echo.
echo 1/5 : Arret de Django...
echo ============================================================
taskkill /F /IM python.exe 2>nul
taskkill /F /IM py.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
timeout /t 3 /nobreak > nul
echo    OK - Django arrete
echo.

echo 2/5 : Nettoyage du cache...
echo ============================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo    OK - Cache nettoye
echo.

echo 3/5 : Suppression ancienne base SQLite (si existe)...
echo ============================================================
if exist db.sqlite3 (
    del db.sqlite3
    echo    OK - Ancienne base supprimee
) else (
    echo    OK - Pas d'ancienne base
)
echo.

echo 4/5 : Creation nouvelle base SQLite + migrations...
echo ============================================================
py manage.py migrate
echo.
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️  ERREUR lors des migrations !
    echo.
    pause
    exit /b 1
)
echo    OK - Base SQLite creee avec succes
echo.

echo 5/5 : Creation superutilisateur (optionnel)...
echo ============================================================
echo Voulez-vous creer un superutilisateur maintenant ? (O/N)
set /p create_user="Reponse : "
if /i "%create_user%"=="O" (
    py manage.py createsuperuser
) else (
    echo    Superutilisateur non cree
)
echo.

echo ============================================================
echo    MIGRATION VERS SQLITE TERMINEE
echo ============================================================
echo.
echo Configuration :
echo   - Base de donnees : SQLite (db.sqlite3)
echo   - Toutes les migrations appliquees
echo   - Champ session_caisse ajoute
echo.
echo IMPORTANT : La base est VIDE !
echo Vous devez :
echo   1. Creer les agences
echo   2. Creer les comptes utilisateurs
echo   3. Creer les articles, etc.
echo.
echo ============================================================
echo.
echo Le serveur va demarrer dans 3 secondes...
timeout /t 3 /nobreak > nul

start cmd /k "title ERP Supermarket Server - SQLite && color 0A && py manage.py runserver 127.0.0.1:8000"

echo.
echo  Serveur demarre avec SQLite !
echo.
echo TESTEZ :
echo   1. Ouvrez l'ERP : http://127.0.0.1:8000
echo   2. Creez les donnees de base
echo   3. Testez la mise en attente
echo.
echo ============================================================
echo.
pause

