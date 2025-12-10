@echo off
echo ===============================================
echo   APPLICATION GESTION CACHE STOCK
echo ===============================================
echo.

echo [1/4] Arret des processus Python...
taskkill /f /im python.exe 2>nul
taskkill /f /im py.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/4] Nettoyage du cache Python...
if exist "*.pyc" del /q "*.pyc" 2>nul
if exist "__pycache__" rmdir /s /q "__pycache__" 2>nul
if exist "supermarket\__pycache__" rmdir /s /q "supermarket\__pycache__" 2>nul
if exist "erp_project\__pycache__" rmdir /s /q "erp_project\__pycache__" 2>nul

echo [3/4] Test de la gestion du cache...
py TEST_CACHE_STOCK.py

echo [4/4] Redemarrage du serveur Django...
echo.
echo ✅ MODIFICATIONS APPLIQUEES!
echo.
echo 🎯 SOLUTIONS IMPLEMENTEES:
echo    1. Redirection automatique avec refresh=1
echo    2. Vider le cache de session automatiquement
echo    3. Bouton "Actualiser le Stock" ajoute
echo    4. select_related pour optimiser les requetes
echo.
echo 🚀 MAINTENANT:
echo    - Apres creation d'une facture d'achat
echo    - Vous serez redirige automatiquement
echo    - Le cache sera vide automatiquement
echo    - Le stock sera affiche correctement
echo.
echo 🚀 Demarrage du serveur...
py manage.py runserver 127.0.0.1:8000



