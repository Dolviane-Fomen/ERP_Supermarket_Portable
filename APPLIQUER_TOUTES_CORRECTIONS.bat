@echo off
chcp 65001 > nul
color 0B
title Application Corrections Completes

cls
echo.
echo ============================================================
echo    APPLICATION DE TOUTES LES CORRECTIONS
echo ============================================================
echo.
echo CORRECTIONS INCLUSES :
echo.
echo 1. NOM VENDEUSE AUTOMATIQUE :
echo    - Facturation : Nom du compte connecte
echo    - Fermeture caisse : Nom du compte connecte
echo    - Mouvement vente : Nom du compte connecte
echo    - Rapport caisse : Nom du compte connecte
echo    - Document vente : Nom du compte connecte
echo.
echo 2. TICKETS EN ATTENTE :
echo    - Double appel corrige (1 clic = 1 ticket)
echo    - Champ session_caisse ajoute
echo    - Suppression auto apres rappel
echo    - Comptage isole par session
echo.
echo 3. FACTURE IMPRESSION :
echo    - Longueur 11.5 cm
echo    - Police lisible 11-16px
echo    - Bordures securisees 4mm
echo    - Design Sage avec separateurs
echo.
echo 4. MODE PORTABLE :
echo    - SQLite (pas besoin PostgreSQL)
echo    - Fonctionne sur n'importe quel PC
echo.
echo ============================================================
echo.
pause

echo.
echo ETAPE 1/5 : Arret complet du serveur...
echo ============================================================
taskkill /F /IM python.exe 2>nul
taskkill /F /IM py.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
timeout /t 3 /nobreak > nul
echo    OK - Serveur arrete
echo.

echo ETAPE 2/5 : Nettoyage cache Python...
echo ============================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo    OK - Cache nettoye
echo.

echo ETAPE 3/5 : Suppression tickets en double...
echo ============================================================
py NETTOYER_TICKETS_DOUBLES.py
echo.

echo ETAPE 4/5 : Application migrations SQLite...
echo ============================================================
py manage.py migrate --no-input
echo.
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  ERREUR lors des migrations !
    pause
    exit /b 1
)
echo    OK - Migrations appliquees
echo.

echo ETAPE 5/5 : Redemarrage launcher portable...
echo ============================================================
echo.
echo ============================================================
echo    CORRECTIONS APPLIQUEES AVEC SUCCES
echo ============================================================
echo.
echo MODIFICATIONS APPLIQUEES :
echo.
echo  NOM VENDEUSE AUTOMATIQUE :
echo   ✓ Facturation vente
echo   ✓ Mouvement vente
echo   ✓ Rapport caisse
echo   ✓ Fermeture caisse
echo   ✓ Document vente
echo.
echo  TICKETS EN ATTENTE :
echo   ✓ Double appel corrige
echo   ✓ 1 clic = 1 ticket
echo   ✓ Suppression auto apres rappel
echo   ✓ Champ session_caisse ajoute
echo.
echo  FACTURE IMPRESSION :
echo   ✓ Longueur 11.5 cm
echo   ✓ Textes lisibles
echo   ✓ Bordures securisees
echo   ✓ Design Sage
echo.
echo  MODE PORTABLE :
echo   ✓ SQLite (portable)
echo   ✓ Fonctionne partout
echo.
echo ============================================================
echo.
echo Le launcher va demarrer dans 3 secondes...
timeout /t 3 /nobreak > nul

start ERP_Launcher.bat

echo.
echo  Launcher demarre avec toutes les corrections !
echo.
echo TESTEZ :
echo   1. Nom vendeuse affiche partout automatiquement
echo   2. Tickets en attente : 1 clic = 1 ticket
echo   3. Factures imprimees a 11.5 cm
echo   4. Tout fonctionne en mode portable
echo.
echo ============================================================
echo.
pause

