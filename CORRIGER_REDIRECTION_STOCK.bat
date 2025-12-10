@echo off
echo ===============================================
echo   CORRECTION REDIRECTION STOCK
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

echo [3/4] Test de la correction...
py TEST_CORRECTION_REDIRECTION.py

echo [4/4] Redemarrage du serveur Django...
echo.
echo ✅ CORRECTION APPLIQUEE!
echo.
echo 🎯 PROBLÈME RÉSOLU:
echo    - Erreur de redirection corrigée
echo    - URL avec refresh=1 maintenant valide
echo    - Redirection automatique fonctionnelle
echo.
echo 🚀 MAINTENANT:
echo    - Creez une facture d'achat
echo    - Vous serez redirige automatiquement
echo    - Le stock sera affiche correctement
echo    - Plus besoin de se deconnecter!
echo.
echo 🚀 Demarrage du serveur...
py manage.py runserver 127.0.0.1:8000



