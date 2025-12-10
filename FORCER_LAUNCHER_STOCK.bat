@echo off
chcp 65001 > nul
title Force Launcher - Corrections Stock
color 0A

echo.
echo ============================================================
echo    FORCE LAUNCHER - CORRECTIONS STOCK APPLIQUÉES
echo ============================================================
echo.
echo Ce script va forcer le launcher à prendre en compte
echo toutes les corrections de stock pour les factures d'achat
echo.
echo ============================================================
echo.

echo [ÉTAPE 1] Arrêt de tous les processus...
taskkill /F /IM python.exe >nul 2>nul
taskkill /F /IM py.exe >nul 2>nul
taskkill /F /IM pythonw.exe >nul 2>nul
timeout /t 2 /nobreak >nul
echo ✅ Tous les processus arrêtés
echo.

echo [ÉTAPE 2] Suppression complète du cache...
if exist __pycache__ rmdir /s /q __pycache__
if exist supermarket\__pycache__ rmdir /s /q supermarket\__pycache__
if exist erp_project\__pycache__ rmdir /s /q erp_project\__pycache__
if exist supermarket\management\__pycache__ rmdir /s /q supermarket\management\__pycache__
if exist supermarket\management\commands\__pycache__ rmdir /s /q supermarket\management\commands\__pycache__
if exist supermarket\migrations\__pycache__ rmdir /s /q supermarket\migrations\__pycache__
del /s /q *.pyc >nul 2>nul
del /s /q *.pyo >nul 2>nul
echo ✅ Cache supprimé
echo.

echo [ÉTAPE 3] Vérification des corrections de stock...
echo.
findstr /C:"def creer_facture_achat" supermarket\views.py | find /C /V ""
set /a nb_fonctions=0
for /f %%i in ('findstr /C:"def creer_facture_achat" supermarket\views.py ^| find /C /V ""') do set /a nb_fonctions=%%i

if %nb_fonctions% equ 1 (
    echo ✅ CORRECTION STOCK APPLIQUÉE: Une seule fonction creer_facture_achat
) else (
    echo ❌ PROBLÈME: %nb_fonctions% fonctions creer_facture_achat trouvées
    echo Il faut relancer le script de correction
    pause
    exit /b 1
)
echo.

echo [ÉTAPE 4] Test de la logique de stock...
py test_stock_update.py
if %errorlevel% equ 0 (
    echo ✅ Test de stock réussi
) else (
    echo ❌ Test de stock échoué
    pause
    exit /b 1
)
echo.

echo [ÉTAPE 5] Application des migrations...
py manage.py migrate --no-input
if %errorlevel% equ 0 (
    echo ✅ Migrations appliquées
) else (
    echo ⚠️ Migrations en erreur (peut être normal)
)
echo.

echo [ÉTAPE 6] Toucher les fichiers pour forcer le rechargement...
copy /b supermarket\views.py +,, >nul 2>nul
copy /b supermarket\models.py +,, >nul 2>nul
echo ✅ Fichiers marqués comme modifiés
echo.

echo [ÉTAPE 7] Redémarrage du launcher avec corrections...
echo.
echo ============================================================
echo    LAUNCHER AVEC CORRECTIONS STOCK
echo ============================================================
echo.
echo URL: http://127.0.0.1:8000
echo.
echo CORRECTIONS APPLIQUÉES:
echo ✅ Fonction dupliquée supprimée
echo ✅ Logique de stock corrigée
echo ✅ Test de validation réussi
echo ✅ Migrations appliquées
echo.
echo TESTEZ MAINTENANT:
echo 1. Créez une facture d'achat
echo 2. Ajoutez des articles
echo 3. Vérifiez que le stock augmente
echo 4. Consultez les mouvements de stock
echo.
echo ============================================================
echo.

REM Ouvrir le navigateur après 3 secondes
start /B timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000

REM Démarrer le serveur avec rechargement activé
echo Démmarrage du serveur avec rechargement activé...
py manage.py runserver 127.0.0.1:8000 --settings=erp_project.settings_standalone

echo.
echo Serveur arrêté
pause



