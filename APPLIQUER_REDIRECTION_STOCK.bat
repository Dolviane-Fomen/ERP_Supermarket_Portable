@echo off
echo ===============================================
echo   APPLICATION REDIRECTION STOCK
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

echo [3/4] Test de la redirection...
py TEST_REDIRECTION_STOCK.py

echo [4/4] Redemarrage du serveur Django...
echo.
echo ✅ MODIFICATION APPLIQUEE!
echo.
echo 🎯 MAINTENANT:
echo    1. Creez une facture d'achat
echo    2. Vous serez redirige vers la liste des articles
echo    3. Vous verrez le stock mis a jour automatiquement
echo.
echo 🚀 Demarrage du serveur...
py manage.py runserver 127.0.0.1:8000



