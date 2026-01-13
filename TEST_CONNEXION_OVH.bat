@echo off
REM Script pour tester la connexion SSH a OVH

echo ========================================
echo Test de connexion SSH a OVH
echo ========================================
echo.

REM Charger la configuration
if not exist ".ovh_config.json" (
    echo ERREUR: Fichier .ovh_config.json introuvable!
    pause
    exit /b 1
)

REM Extraire l'IP et l'utilisateur depuis le fichier JSON
REM Note: Cette methode simple suppose que le format est correct
for /f "tokens=2 delims=:," %%a in ('findstr "ovh_host" .ovh_config.json') do (
    set OVH_HOST=%%a
    set OVH_HOST=!OVH_HOST:"=!
    set OVH_HOST=!OVH_HOST: =!
)

for /f "tokens=2 delims=:," %%a in ('findstr "ovh_user" .ovh_config.json') do (
    set OVH_USER=%%a
    set OVH_USER=!OVH_USER:"=!
    set OVH_USER=!OVH_USER: =!
)

echo.
echo Tentative de connexion avec:
echo   IP: %OVH_HOST%
echo   Utilisateur: %OVH_USER%
echo.

echo Test 1: Connexion avec l'utilisateur configure...
ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no %OVH_USER%@%OVH_HOST% "whoami && pwd && echo --- && echo Connexion reussie!"
if errorlevel 1 (
    echo.
    echo ERREUR: Connexion echouee avec '%OVH_USER%'
    echo.
    echo Test 2: Essai avec 'root'...
    ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no root@%OVH_HOST% "whoami && pwd && echo --- && echo Connexion reussie avec root!"
    if errorlevel 1 (
        echo.
        echo ERREUR: Connexion echouee aussi avec 'root'
        echo Verifiez:
        echo   1. L'IP est correcte: %OVH_HOST%
        echo   2. Le serveur OVH est accessible
        echo   3. SSH est active sur le serveur
    ) else (
        echo.
        echo ========================================
        echo IMPORTANT: Vous devez utiliser 'root'!
        echo ========================================
        echo Modifiez .ovh_config.json et changez:
        echo   "ovh_user": "root"
    )
) else (
    echo.
    echo ========================================
    echo SUCCESS: Connexion OK avec '%OVH_USER%'!
    echo ========================================
)

echo.
pause




