@echo off
echo 🔄 FORÇAGE DU RECHARGEMENT COMPLET DU SERVEUR DJANGO
echo ==================================================

echo.
echo [1/6] Arrêt de tous les processus Python...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [2/6] Nettoyage du cache Python...
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
if exist supermarket\__pycache__ rmdir /s /q supermarket\__pycache__ 2>nul
if exist erp_project\__pycache__ rmdir /s /q erp_project\__pycache__ 2>nul

echo.
echo [3/6] Suppression des fichiers .pyc...
del /s /q *.pyc 2>nul
del /s /q supermarket\*.pyc 2>nul
del /s /q erp_project\*.pyc 2>nul

echo.
echo [4/6] Vérification des modifications dans models.py...
findstr /C:"def mettre_a_jour_stock" supermarket\models.py >nul
if %errorlevel% equ 0 (
    echo ✅ Méthode mettre_a_jour_stock trouvée
) else (
    echo ❌ Méthode mettre_a_jour_stock manquante
)

findstr /C:"def valider_facture" supermarket\models.py >nul
if %errorlevel% equ 0 (
    echo ✅ Méthode valider_facture trouvée
) else (
    echo ❌ Méthode valider_facture manquante
)

echo.
echo [5/6] Vérification des modifications dans views.py...
findstr /C:"article.refresh_from_db" supermarket\views.py >nul
if %errorlevel% equ 0 (
    echo ✅ Validation refresh_from_db trouvée
) else (
    echo ❌ Validation refresh_from_db manquante
)

echo.
echo [6/6] Démarrage du serveur Django avec rechargement...
echo.
echo 🚀 SERVEUR DJANGO EN COURS DE DÉMARRAGE...
echo    Les modifications de stock sont maintenant actives !
echo.
echo 💡 Conseil: Testez maintenant une facture d'achat pour voir
echo    la mise à jour automatique du stock en action.
echo.

py manage.py runserver 0.0.0.0:8000

pause