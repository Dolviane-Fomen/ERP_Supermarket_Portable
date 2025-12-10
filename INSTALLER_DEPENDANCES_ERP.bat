@echo off
chcp 65001 >nul
title INSTALLATION DEPENDANCES ERP

echo.
echo ============================================================
echo 🚀 INSTALLATION DEPENDANCES ERP
echo ============================================================
echo 📦 Installation automatique de openpyxl et reportlab
echo ============================================================
echo.

REM Vérifier si Python est disponible
echo 🔍 Vérification de Python...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non détecté
    echo 💡 Veuillez installer Python ou utiliser py -3
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Exécuter le script Python
echo 🚀 Démarrage de l'installation...
echo.
py INSTALLER_DEPENDANCES_ERP.py

REM Vérifier le résultat
if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo 🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !
    echo ============================================================
    echo ✅ Toutes les dépendances sont installées
    echo 🚀 Votre ERP est prêt à fonctionner
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo ⚠️ INSTALLATION TERMINÉE AVEC DES ERREURS
    echo ============================================================
    echo ❌ Certaines dépendances n'ont pas pu être installées
    echo 💡 Vérifiez votre connexion internet ou utilisez les packages offline
    echo ============================================================
)

echo.
echo Appuyez sur une touche pour fermer...
pause >nul


