@echo off
chcp 65001 > nul
title Rechargement Correction Stock - Factures d'Achat
color 0A

echo.
echo ============================================================
echo    RECHARGEMENT CORRECTION STOCK - FACTURES D'ACHAT
echo ============================================================
echo.
echo Ce script va recharger les modifications de stock
echo.
echo ============================================================
echo.

echo [ÉTAPE 1] Arrêt des processus Python...
taskkill /F /IM python.exe >nul 2>nul
taskkill /F /IM py.exe >nul 2>nul
taskkill /F /IM pythonw.exe >nul 2>nul
timeout /t 2 /nobreak >nul
echo ✅ Processus Python arrêtés
echo.

echo [ÉTAPE 2] Suppression du cache Python...
if exist __pycache__ rmdir /s /q __pycache__
if exist supermarket\__pycache__ rmdir /s /q supermarket\__pycache__
if exist erp_project\__pycache__ rmdir /s /q erp_project\__pycache__
del /s /q *.pyc >nul 2>nul
echo ✅ Cache supprimé
echo.

echo [ÉTAPE 3] Vérification de la correction du stock...
echo.
findstr /C:"def creer_facture_achat" supermarket\views.py | find /C /V ""
set /a nb_fonctions=0
for /f %%i in ('findstr /C:"def creer_facture_achat" supermarket\views.py ^| find /C /V ""') do set /a nb_fonctions=%%i

if %nb_fonctions% equ 1 (
    echo ✅ CORRECTION APPLIQUÉE: Une seule fonction creer_facture_achat trouvée
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

echo [ÉTAPE 5] Redémarrage du serveur Django...
echo.
echo ============================================================
echo    SERVEUR DJANGO - CORRECTION STOCK APPLIQUÉE
echo ============================================================
echo.
echo URL: http://127.0.0.1:8000
echo.
echo CORRECTIONS APPLIQUÉES:
echo ✅ Fonction dupliquée supprimée
echo ✅ Logique de stock corrigée
echo ✅ Test de validation réussi
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

REM Recherche de Python
py --version >nul 2>nul
if %errorlevel% equ 0 (
    echo Python trouvé (py)
    echo.
    py manage.py runserver
    goto :end
)

python --version >nul 2>nul
if %errorlevel% equ 0 (
    echo Python trouvé (python)
    echo.
    python manage.py runserver
    goto :end
)

echo.
echo ❌ Python non trouvé
echo Installez Python avec: INSTALLER_PYTHON_RAPIDE.bat
echo.
pause

:end



