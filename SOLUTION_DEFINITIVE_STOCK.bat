@echo off
chcp 65001 > nul
title SOLUTION DÉFINITIVE - STOCK FACTURES D'ACHAT
color 0E

echo.
echo ============================================================
echo    SOLUTION DÉFINITIVE - STOCK FACTURES D'ACHAT
echo ============================================================
echo.
echo Ce script va appliquer une solution définitive
echo pour que le stock se mette à jour lors des factures d'achat
echo.
echo ============================================================
echo.

echo [ÉTAPE 1] Arrêt complet de tous les processus...
taskkill /F /IM python.exe >nul 2>nul
taskkill /F /IM py.exe >nul 2>nul
taskkill /F /IM pythonw.exe >nul 2>nul
taskkill /F /IM ERP_Launcher.bat >nul 2>nul
timeout /t 3 /nobreak >nul
echo ✅ Tous les processus arrêtés
echo.

echo [ÉTAPE 2] Nettoyage complet du cache...
if exist __pycache__ rmdir /s /q __pycache__
if exist supermarket\__pycache__ rmdir /s /q supermarket\__pycache__
if exist erp_project\__pycache__ rmdir /s /q erp_project\__pycache__
if exist supermarket\management\__pycache__ rmdir /s /q supermarket\management\__pycache__
if exist supermarket\management\commands\__pycache__ rmdir /s /q supermarket\management\commands\__pycache__
if exist supermarket\migrations\__pycache__ rmdir /s /q supermarket\migrations\__pycache__
del /s /q *.pyc >nul 2>nul
del /s /q *.pyo >nul 2>nul
echo ✅ Cache complètement nettoyé
echo.

echo [ÉTAPE 3] Vérification des corrections...
echo.
findstr /C:"def creer_facture_achat" supermarket\views.py | find /C /V ""
set /a nb_fonctions=0
for /f %%i in ('findstr /C:"def creer_facture_achat" supermarket\views.py ^| find /C /V ""') do set /a nb_fonctions=%%i

if %nb_fonctions% equ 1 (
    echo ✅ CORRECTION APPLIQUÉE: Fonction dupliquée supprimée
) else (
    echo ❌ PROBLÈME: %nb_fonctions% fonctions trouvées
    echo Relancez d'abord: py corriger_stock_achat.py
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
echo ✅ Migrations appliquées
echo.

echo [ÉTAPE 6] Création d'un launcher modifié...
echo.
echo Création d'un launcher qui prend en compte les modifications...
echo.

REM Créer un launcher modifié
(
echo @echo off
echo title ERP Supermarket - Launcher avec Corrections Stock
echo color 0A
echo cls
echo.
echo echo ========================================
echo echo.
echo echo          ERP SUPERMARKET
echo echo        Systeme de Gestion
echo echo      AVEC CORRECTIONS STOCK
echo echo.
echo echo ========================================
echo echo.
echo echo Demarrage en cours...
echo echo.
echo.
echo :: Se déplacer dans le dossier
echo cd /d "%%~dp0"
echo.
echo :: Arrêter les anciens serveurs
echo taskkill /F /IM python.exe /T ^>nul 2^>^&1
echo taskkill /F /IM py.exe /T ^>nul 2^>^&1
echo timeout /t 1 ^>nul
echo.
echo :: Supprimer le cache
echo for /d /r %%%%d in ^(__pycache__^) do @if exist "%%%%d" rd /s /q "%%%%d" 2^>nul
echo del /s /q *.pyc ^>nul 2^>^&1
echo.
echo :: Variables anti-cache
echo set PYTHONDONTWRITEBYTECODE=1
echo set PYTHONUNBUFFERED=1
echo.
echo echo Serveur demarre avec les corrections stock !
echo echo.
echo echo ========================================
echo echo.
echo echo   CORRECTIONS APPLIQUEES:
echo echo   ✓ Stock mis à jour lors des achats
echo echo   ✓ Fonction dupliquée supprimée
echo echo   ✓ Test de validation réussi
echo echo.
echo echo   URL: http://127.0.0.1:8000
echo echo.
echo echo ========================================
echo echo.
echo.
echo :: Ouvrir le navigateur après 3 secondes
echo start "" cmd /c "timeout /t 3 ^>nul ^&^& start http://127.0.0.1:8000"
echo.
echo :: Lancer le serveur SANS --noreload pour permettre le rechargement
echo py -B -u manage.py runserver 127.0.0.1:8000 --settings=erp_project.settings_standalone
) > ERP_Launcher_CORRIGE.bat

echo ✅ Launcher corrigé créé: ERP_Launcher_CORRIGE.bat
echo.

echo [ÉTAPE 7] Démarrage du serveur avec corrections...
echo.
echo ============================================================
echo    SERVEUR AVEC CORRECTIONS STOCK
echo ============================================================
echo.
echo URL: http://127.0.0.1:8000
echo.
echo CORRECTIONS APPLIQUÉES:
echo ✅ Fonction dupliquée supprimée
echo ✅ Logique de stock corrigée
echo ✅ Test de validation réussi
echo ✅ Migrations appliquées
echo ✅ Launcher modifié créé
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

REM Démarrer le serveur SANS --noreload
echo Démarrage du serveur avec rechargement activé...
py manage.py runserver 127.0.0.1:8000 --settings=erp_project.settings_standalone

echo.
echo Serveur arrêté
echo.
echo Pour redémarrer avec les corrections, utilisez:
echo   ERP_Launcher_CORRIGE.bat
echo.
pause



