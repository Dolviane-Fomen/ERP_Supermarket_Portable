@echo off
REM Script pour afficher les commandes a executer sur le serveur OVH

echo ========================================
echo ETAPE 1: Generer la cle SSH sur OVH
echo ========================================
echo.
echo Suivez ces etapes sur votre serveur OVH:
echo.
echo 1. Connectez-vous au serveur:
echo    ssh ubuntu@51.68.124.152
echo.
echo 2. Executez ces commandes une par une:
echo.
echo    ssh-keygen -t ed25519 -C "github-actions@ovh" -f ~/.ssh/github_actions_key
echo.
echo    (Appuyez 3 fois sur Entree - pas de mot de passe)
echo.
echo    cat ~/.ssh/github_actions_key
echo.
echo 3. COPIEZ TOUT le texte affiche (de -----BEGIN jusqu'a -----END)
echo.
echo 4. Executez ensuite:
echo    cat ~/.ssh/github_actions_key.pub ^>^> ~/.ssh/authorized_keys
echo.
echo 5. Revenez ici et ouvrez ETAPE2_CONFIGURER_SECRETS.md
echo.
echo ========================================
pause

