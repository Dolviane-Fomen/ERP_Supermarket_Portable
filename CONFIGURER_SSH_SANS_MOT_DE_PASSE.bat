@echo off
setlocal enabledelayedexpansion
REM Script pour configurer l'authentification SSH sans mot de passe
REM Cela permettra à la synchronisation automatique de fonctionner

echo ========================================
echo Configuration SSH sans mot de passe
echo ========================================
echo.
echo Ce script va:
echo   1. Generer une cle SSH (si elle n'existe pas)
echo   2. Copier la cle publique sur le serveur OVH
echo   3. Tester la connexion
echo.
echo IMPORTANT: Vous devrez entrer le mot de passe
echo   UNE SEULE FOIS lors de la copie de la cle.
echo.
pause

REM Charger la configuration
if not exist ".ovh_config.json" (
    echo ERREUR: Fichier .ovh_config.json introuvable!
    echo Utilisation des valeurs par defaut...
    set OVH_HOST=51.68.124.152
    set OVH_USER=ubuntu
) else (
    REM Extraire l'IP et l'utilisateur depuis le fichier JSON
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
)

echo.
echo Configuration detectee:
echo   Serveur: %OVH_USER%@%OVH_HOST%
echo.

REM Verifier si SSH est disponible
where ssh >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: SSH n'est pas disponible!
    echo Installez Git for Windows ou OpenSSH
    pause
    exit /b 1
)

REM Creer le dossier .ssh s'il n'existe pas
if not exist "%USERPROFILE%\.ssh" (
    mkdir "%USERPROFILE%\.ssh"
    echo [OK] Dossier .ssh cree
)

REM Verifier si une cle SSH existe deja
if exist "%USERPROFILE%\.ssh\id_rsa" (
    echo.
    echo [INFO] Une cle SSH existe deja: %USERPROFILE%\.ssh\id_rsa
    set /p GENERATE_NEW="Voulez-vous generer une nouvelle cle? (O/N): "
    if /i not "%GENERATE_NEW%"=="O" (
        echo Utilisation de la cle existante...
        goto :copy_key
    )
)

REM Generer une nouvelle cle SSH
echo.
echo [1/3] Generation de la cle SSH...
echo.
ssh-keygen -t rsa -b 4096 -f "%USERPROFILE%\.ssh\id_rsa" -N ""
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Echec de la generation de la cle SSH
    pause
    exit /b 1
)
echo [OK] Cle SSH generee

:copy_key
REM Copier la cle publique sur le serveur (methode compatible Windows)
echo.
echo [2/3] Copie de la cle publique sur le serveur...
echo.
echo ATTENTION: Vous devrez entrer le mot de passe du serveur maintenant!
echo.

REM Lire la cle publique
set "PUBLIC_KEY_FILE=%USERPROFILE%\.ssh\id_rsa.pub"
if not exist "!PUBLIC_KEY_FILE!" (
    echo ERREUR: Fichier de cle publique introuvable: !PUBLIC_KEY_FILE!
    pause
    exit /b 1
)

REM Afficher la cle publique pour reference
echo.
echo Votre cle publique:
echo ----------------------------------------
type "!PUBLIC_KEY_FILE!"
echo ----------------------------------------
echo.

REM Copier la cle publique sur le serveur en utilisant SSH avec heredoc
REM Note: Cette methode fonctionne sur Windows avec OpenSSH
echo Copie de la cle sur le serveur...
type "!PUBLIC_KEY_FILE!" | ssh %OVH_USER%@%OVH_HOST% "mkdir -p ~/.ssh 2>nul && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && echo 'Cle SSH ajoutee avec succes!'"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERREUR: Echec de la copie automatique de la cle
    echo.
    echo ========================================
    echo SOLUTION MANUELLE (RECOMMANDEE)
    echo ========================================
    echo.
    echo Etape 1: Copiez votre cle publique ci-dessus
    echo.
    echo Etape 2: Connectez-vous au serveur:
    echo   ssh %OVH_USER%@%OVH_HOST%
    echo.
    echo Etape 3: Sur le serveur, executez ces commandes:
    echo   mkdir -p ~/.ssh
    echo   chmod 700 ~/.ssh
    echo   nano ~/.ssh/authorized_keys
    echo.
    echo Etape 4: Dans nano, collez votre cle publique (une seule ligne)
    echo   Appuyez sur Ctrl+O pour sauvegarder
    echo   Appuyez sur Ctrl+X pour quitter
    echo.
    echo Etape 5: Fixez les permissions:
    echo   chmod 600 ~/.ssh/authorized_keys
    echo.
    echo Etape 6: Testez la connexion:
    echo   exit
    echo   ssh %OVH_USER%@%OVH_HOST%
    echo   ^(Ne devrait plus demander de mot de passe^)
    echo.
    pause
    exit /b 1
)
echo [OK] Cle copiee sur le serveur

REM Tester la connexion
echo.
echo [3/3] Test de la connexion sans mot de passe...
echo.
ssh -o ConnectTimeout=5 -o BatchMode=yes %OVH_USER%@%OVH_HOST% "echo 'Connexion OK - Authentification par cle reussie!'"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo CONFIGURATION REUSSIE!
    echo ========================================
    echo.
    echo La synchronisation automatique peut maintenant fonctionner
    echo sans demander de mot de passe.
    echo.
) else (
    echo.
    echo ATTENTION: La connexion sans mot de passe n'a pas fonctionne
    echo Verifiez la configuration manuellement.
    echo.
)

pause
