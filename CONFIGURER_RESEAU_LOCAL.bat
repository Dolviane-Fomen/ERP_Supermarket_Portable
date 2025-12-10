@echo off
title Configuration ERP en Reseau Local
color 0A
cls

echo.
echo ========================================
echo.
echo    CONFIGURATION ERP EN RESEAU LOCAL
echo    Pour travail synchrone multi-PC
echo.
echo ========================================
echo.

:: Obtenir l'adresse IP locale
echo [1/4] Detection de l'adresse IP locale...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"Adresse IPv4"') do (
    set "IP_ADDRESS=%%a"
    set "IP_ADDRESS=!IP_ADDRESS: =!"
    goto :ip_found
)
:ip_found

echo    Adresse IP detectee: %IP_ADDRESS%
echo.

:: Creer le fichier de configuration reseau
echo [2/4] Creation de la configuration reseau...
echo # Configuration ERP Reseau Local > erp_project/settings_network.py
echo # Pour utilisation multi-PC en reseau local >> erp_project/settings_network.py
echo. >> erp_project/settings_network.py
echo from .settings_standalone import * >> erp_project/settings_network.py
echo. >> erp_project/settings_network.py
echo # Configuration reseau >> erp_project/settings_network.py
echo ALLOWED_HOSTS = ['*']  # Autoriser toutes les adresses IP >> erp_project/settings_network.py
echo DEBUG = True >> erp_project/settings_network.py
echo. >> erp_project/settings_network.py
echo # Configuration pour acces reseau >> erp_project/settings_network.py
echo CSRF_TRUSTED_ORIGINS = [ >> erp_project/settings_network.py
echo     'http://%IP_ADDRESS%:8000', >> erp_project/settings_network.py
echo     'http://localhost:8000', >> erp_project/settings_network.py
echo     'http://127.0.0.1:8000', >> erp_project/settings_network.py
echo ] >> erp_project/settings_network.py
echo. >> erp_project/settings_network.py
echo # Configuration de la base de donnees partagee >> erp_project/settings_network.py
echo # La base SQLite sera partagee entre tous les PC >> erp_project/settings_network.py

echo    Configuration reseau creee: erp_project/settings_network.py
echo.

:: Creer le lanceur reseau
echo [3/4] Creation du lanceur reseau...
echo @echo off > ERP_Reseau_Local.bat
echo title ERP Supermarket - Reseau Local >> ERP_Reseau_Local.bat
echo color 0B >> ERP_Reseau_Local.bat
echo cls >> ERP_Reseau_Local.bat
echo. >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo echo ======================================== >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo echo          ERP SUPERMARKET >> ERP_Reseau_Local.bat
echo echo        Mode Reseau Local >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo echo ======================================== >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo echo Demarrage en cours... >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo. >> ERP_Reseau_Local.bat
echo :: Se deplacer dans le dossier >> ERP_Reseau_Local.bat
echo cd /d "%%~dp0" >> ERP_Reseau_Local.bat
echo. >> ERP_Reseau_Local.bat
echo :: Trouver Python >> ERP_Reseau_Local.bat
echo set "PYTHON_CMD=py" >> ERP_Reseau_Local.bat
echo python --version ^>nul 2^>^&1 >> ERP_Reseau_Local.bat
echo if %%errorlevel%% equ 0 set "PYTHON_CMD=python" >> ERP_Reseau_Local.bat
echo. >> ERP_Reseau_Local.bat
echo :: Arreter les anciens serveurs >> ERP_Reseau_Local.bat
echo taskkill /F /IM python.exe /T ^>nul 2^>^&1 >> ERP_Reseau_Local.bat
echo taskkill /F /IM py.exe /T ^>nul 2^>^&1 >> ERP_Reseau_Local.bat
echo timeout /t 1 ^>nul >> ERP_Reseau_Local.bat
echo. >> ERP_Reseau_Local.bat
echo echo Serveur reseau demarre avec succes ! >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo echo ======================================== >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo echo   Acces reseau local disponible: >> ERP_Reseau_Local.bat
echo echo   URL: http://%IP_ADDRESS%:8000 >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo echo   Autres PC peuvent se connecter avec: >> ERP_Reseau_Local.bat
echo echo   http://%IP_ADDRESS%:8000 >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo echo ======================================== >> ERP_Reseau_Local.bat
echo echo. >> ERP_Reseau_Local.bat
echo. >> ERP_Reseau_Local.bat
echo :: Lancer le serveur reseau >> ERP_Reseau_Local.bat
echo %%PYTHON_CMD%% -B -u manage.py runserver 0.0.0.0:8000 --settings=erp_project.settings_network --noreload >> ERP_Reseau_Local.bat

echo    Lanceur reseau cree: ERP_Reseau_Local.bat
echo.

:: Creer le guide d'utilisation
echo [4/4] Creation du guide d'utilisation...
echo # GUIDE UTILISATION ERP RESEAU LOCAL > GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo ## Configuration Reseau Local ERP Supermarket >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo ### 1. PC SERVEUR (Principal) >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo 1. Executez `ERP_Reseau_Local.bat` sur le PC principal >> GUIDE_RESEAU.md
echo 2. Notez l'adresse IP affichee: **%IP_ADDRESS%** >> GUIDE_RESEAU.md
echo 3. L'ERP sera accessible sur: `http://%IP_ADDRESS%:8000` >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo ### 2. PC CLIENTS (Autres PC) >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo 1. Ouvrez un navigateur web >> GUIDE_RESEAU.md
echo 2. Allez a l'adresse: `http://%IP_ADDRESS%:8000` >> GUIDE_RESEAU.md
echo 3. Connectez-vous avec vos identifiants >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo ### 3. AVANTAGES >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo - **Synchronisation automatique**: Tous les PC voient les memes donnees >> GUIDE_RESEAU.md
echo - **Base de donnees partagee**: Une seule base SQLite pour tous >> GUIDE_RESEAU.md
echo - **Travail collaboratif**: Plusieurs utilisateurs simultanes >> GUIDE_RESEAU.md
echo - **Pas d'installation**: Les PC clients n'ont besoin que d'un navigateur >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo ### 4. SECURITE >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo - L'ERP n'est accessible que sur le reseau local >> GUIDE_RESEAU.md
echo - Utilisez des mots de passe forts >> GUIDE_RESEAU.md
echo - Sauvegardez regulierement la base de donnees >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo ### 5. DEPANNAGE >> GUIDE_RESEAU.md
echo. >> GUIDE_RESEAU.md
echo - Verifiez que tous les PC sont sur le meme reseau >> GUIDE_RESEAU.md
echo - Desactivez temporairement le pare-feu si necessaire >> GUIDE_RESEAU.md
echo - Verifiez l'adresse IP du serveur avec `ipconfig` >> GUIDE_RESEAU.md

echo    Guide cree: GUIDE_RESEAU.md
echo.

echo ========================================
echo.
echo    CONFIGURATION RESEAU TERMINEE !
echo.
echo ========================================
echo.
echo INSTRUCTIONS:
echo.
echo 1. PC SERVEUR (ce PC):
echo    - Executez: ERP_Reseau_Local.bat
echo    - Adresse: http://%IP_ADDRESS%:8000
echo.
echo 2. PC CLIENTS (autres PC):
echo    - Ouvrez navigateur
echo    - Allez a: http://%IP_ADDRESS%:8000
echo.
echo 3. Tous les PC travailleront avec la meme base de donnees !
echo.
echo ========================================
echo.
pause


