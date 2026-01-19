@echo off
REM Script principal pour configurer la synchronisation sur TOUS les PCs
REM A executer sur chaque PC une seule fois

echo ========================================
echo CONFIGURATION SYNCHRONISATION - TOUS LES PCs
echo ========================================
echo.
echo Ce script va configurer automatiquement:
echo   - La synchronisation locale ^<^-> serveur
echo   - SQLite local pour travailler hors ligne
echo   - Connexion SSH au serveur OVH
echo.
echo Appuyez sur une touche pour commencer...
pause >nul

REM Appeler le script de configuration
call "%~dp0CONFIGURER_SYNC_AUTOMATIQUE.bat"

echo.
echo ========================================
echo CONFIGURATION TERMINEE SUR CE PC
echo ========================================
echo.
echo Repetez cette operation sur tous les autres PCs.
echo.
echo Sur chaque PC:
echo   1. Copiez ce dossier ERP complet
echo   2. Executez CONFIGURER_SYNC_AUTOMATIQUE_TOUS_PC.bat
echo   3. C'est tout!
echo.
pause
