@echo off
title Surveillance Serveur ERP
color 0E
cls

echo.
echo ========================================
echo.
echo    SURVEILLANCE SERVEUR ERP
echo    Redemarrage automatique
echo.
echo ========================================
echo.

:surveillance_loop
echo [%date% %time%] Verification du serveur...

:: Verifier si le serveur fonctionne
netstat -an | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo    ✅ Serveur actif - Port 8000 ouvert
) else (
    echo    ❌ Serveur arrete - Redemarrage en cours...
    echo.
    echo ========================================
    echo    REDEMARRAGE AUTOMATIQUE
    echo ========================================
    echo.
    
    :: Redemarrer le serveur
    start /B ERP_Reseau_Local.bat
    
    :: Attendre que le serveur demarre
    echo Attente du demarrage...
    timeout /t 10 >nul
    
    :: Verifier que le serveur a redemarre
    netstat -an | findstr :8000 >nul
    if %errorlevel% equ 0 (
        echo    ✅ Serveur redemarre avec succes !
    ) else (
        echo    ❌ Echec du redemarrage - Nouvelle tentative...
    )
)

echo.
echo Prochaine verification dans 30 secondes...
echo Appuyez sur Ctrl+C pour arreter la surveillance
echo.

:: Attendre 30 secondes avant la prochaine verification
timeout /t 30 >nul

goto :surveillance_loop


