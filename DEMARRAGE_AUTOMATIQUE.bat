@echo off
title Demarrage Automatique ERP
color 0A
cls

echo.
echo ========================================
echo.
echo    DEMARRAGE AUTOMATIQUE ERP
echo    Au demarrage de Windows
echo.
echo ========================================
echo.

:: Creer un raccourci de demarrage automatique
echo [1/3] Creation du raccourci de demarrage...

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "CURRENT_PATH=%~dp0"

:: Creer un script de demarrage dans le dossier Startup
echo @echo off > "%STARTUP_FOLDER%\ERP_AutoStart.bat"
echo cd /d "%CURRENT_PATH%" >> "%STARTUP_FOLDER%\ERP_AutoStart.bat"
echo start /MIN ERP_Reseau_Local.bat >> "%STARTUP_FOLDER%\ERP_AutoStart.bat"

echo    ✅ Raccourci cree dans: %STARTUP_FOLDER%
echo.

:: Creer un service Windows (optionnel)
echo [2/3] Configuration du service Windows...
echo.
echo Pour installer comme service Windows, executez en tant qu'administrateur:
echo    sc create "ERP_Supermarket" binPath= "%CURRENT_PATH%ERP_Reseau_Local.bat" start= auto
echo.
echo Pour desinstaller le service:
echo    sc delete "ERP_Supermarket"
echo.

:: Creer un script de sauvegarde automatique
echo [3/3] Creation de la sauvegarde automatique...
echo @echo off > SAUVEGARDE_AUTOMATIQUE.bat
echo title Sauvegarde Automatique ERP >> SAUVEGARDE_AUTOMATIQUE.bat
echo color 0B >> SAUVEGARDE_AUTOMATIQUE.bat
echo cls >> SAUVEGARDE_AUTOMATIQUE.bat
echo. >> SAUVEGARDE_AUTOMATIQUE.bat
echo echo Sauvegarde automatique de la base de donnees... >> SAUVEGARDE_AUTOMATIQUE.bat
echo cd /d "%%~dp0" >> SAUVEGARDE_AUTOMATIQUE.bat
echo. >> SAUVEGARDE_AUTOMATIQUE.bat
echo :: Creer un dossier de sauvegarde >> SAUVEGARDE_AUTOMATIQUE.bat
echo if not exist "backups" mkdir backups >> SAUVEGARDE_AUTOMATIQUE.bat
echo. >> SAUVEGARDE_AUTOMATIQUE.bat
echo :: Sauvegarder avec timestamp >> SAUVEGARDE_AUTOMATIQUE.bat
echo set "TIMESTAMP=%%date:~-4,4%%%%date:~-10,2%%%%date:~-7,2%%_%%time:~0,2%%%%time:~3,2%%%%time:~6,2%%" >> SAUVEGARDE_AUTOMATIQUE.bat
echo set "TIMESTAMP=!TIMESTAMP: =0!" >> SAUVEGARDE_AUTOMATIQUE.bat
echo copy "db_erp.sqlite3" "backups\db_erp_backup_!TIMESTAMP!.sqlite3" >> SAUVEGARDE_AUTOMATIQUE.bat
echo. >> SAUVEGARDE_AUTOMATIQUE.bat
echo echo ✅ Sauvegarde creee: backups\db_erp_backup_!TIMESTAMP!.sqlite3 >> SAUVEGARDE_AUTOMATIQUE.bat
echo. >> SAUVEGARDE_AUTOMATIQUE.bat
echo :: Supprimer les anciennes sauvegardes (garder seulement les 7 dernieres) >> SAUVEGARDE_AUTOMATIQUE.bat
echo for /f "skip=7 delims=" %%%%i in ('dir /b /o-d backups\db_erp_backup_*.sqlite3 2^>nul') do del "backups\%%%%i" >> SAUVEGARDE_AUTOMATIQUE.bat
echo. >> SAUVEGARDE_AUTOMATIQUE.bat
echo timeout /t 5 ^>nul >> SAUVEGARDE_AUTOMATIQUE.bat

echo    ✅ Script de sauvegarde cree: SAUVEGARDE_AUTOMATIQUE.bat
echo.

echo ========================================
echo.
echo    CONFIGURATION TERMINEE !
echo.
echo ========================================
echo.
echo INSTRUCTIONS:
echo.
echo 1. DEMARRAGE AUTOMATIQUE:
echo    - L'ERP demarrera automatiquement au demarrage de Windows
echo    - Le raccourci a ete cree dans le dossier Startup
echo.
echo 2. SURVEILLANCE:
echo    - Executez SURVEILLANCE_SERVEUR.bat pour surveiller le serveur
echo    - Redemarrage automatique en cas de probleme
echo.
echo 3. SAUVEGARDE:
echo    - Executez SAUVEGARDE_AUTOMATIQUE.bat pour sauvegarder
echo    - Planifiez une tache Windows pour l'automatiser
echo.
echo 4. SERVICE WINDOWS (optionnel):
echo    - Executez en tant qu'administrateur pour installer comme service
echo.
echo ========================================
echo.
pause


