@echo off
echo ========================================
echo RESOLUTION AUTOMATIQUE PING PC1
echo ========================================
echo.

echo PROBLEME : PC1 ne peut pas recevoir les pings de PC2
echo SOLUTION : Configuration automatique du firewall et reseau
echo.

echo 1. VERIFICATION DE LA CONFIGURATION ACTUELLE...
echo.
echo Configuration IP de PC1 :
ipconfig /all
echo.

echo 2. DESACTIVATION TEMPORAIRE DU FIREWALL...
echo.
echo Desactivation du firewall Windows...
netsh advfirewall set allprofiles state off
echo Firewall desactive temporairement
echo.

echo 3. CONFIGURATION DES REGLES FIREWALL...
echo.
echo Ajout de regles pour permettre les pings...
netsh advfirewall firewall add rule name="Allow ICMP Echo Request" dir=in action=allow protocol=icmpv4:8,any
netsh advfirewall firewall add rule name="Allow ICMP Echo Reply" dir=out action=allow protocol=icmpv4:0,any
netsh advfirewall firewall add rule name="Allow ICMP Destination Unreachable" dir=in action=allow protocol=icmpv4:3,any
netsh advfirewall firewall add rule name="Allow ICMP Time Exceeded" dir=in action=allow protocol=icmpv4:11,any
echo Regles ICMP ajoutees
echo.

echo 4. CONFIGURATION DU PROTOCOLE ICMP...
echo.
echo Activation du protocole ICMP...
netsh interface ipv4 set global icmpredirects=enabled
netsh interface ipv6 set global icmpredirects=enabled
echo Protocole ICMP active
echo.

echo 5. CONFIGURATION DE LA CARTE RESEAU...
echo.
echo Redemarrage de la carte reseau...
netsh interface set interface "Connexion au reseau local" disable
timeout /t 3 /nobreak >nul
netsh interface set interface "Connexion au reseau local" enable
echo Carte reseau redemarree
echo.

echo 6. LIBERATION ET RENOUVELLEMENT DE L'IP...
echo.
echo Liberation de l'IP actuelle...
ipconfig /release
echo.
echo Renouvellement de l'IP...
ipconfig /renew
echo.

echo 7. VERIFICATION DE LA NOUVELLE CONFIGURATION...
echo.
echo Nouvelle configuration IP :
ipconfig /all
echo.

echo 8. TEST DE CONNECTIVITE...
echo.
echo Test de ping vers la passerelle...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "Passerelle"') do (
    set GATEWAY=%%a
    set GATEWAY=!GATEWAY: =!
)
if not "%GATEWAY%"=="" (
    echo Passerelle detectee : %GATEWAY%
    ping -n 2 %GATEWAY%
) else (
    echo ERREUR : Aucune passerelle detectee
)
echo.

echo 9. TEST DE PING VERS PC2...
echo.
echo Test de ping vers PC2 (192.168.8.11)...
ping -n 4 192.168.8.11
echo.

echo 10. CONFIGURATION DES ROUTES...
echo.
echo Configuration des routes reseau...
route add 0.0.0.0 mask 0.0.0.0 %GATEWAY% metric 1
echo Route par defaut configuree
echo.

echo 11. VERIFICATION DES ROUTES...
echo.
echo Table de routage :
route print
echo.

echo 12. TEST DE PING BIDIRECTIONNEL...
echo.
echo Test de ping PC1 vers PC2 :
ping -n 4 192.168.8.11
echo.

echo Test de ping PC2 vers PC1 :
echo (A executer sur PC2)
echo ping -n 4 192.168.8.10
echo.

echo ========================================
echo CONFIGURATION TERMINEE
echo ========================================
echo.

echo VERIFICATION FINALE :
echo 1. PC1 doit pouvoir envoyer des pings vers PC2
echo 2. PC2 doit pouvoir envoyer des pings vers PC1
echo 3. Les deux PC doivent pouvoir communiquer
echo.

echo REACTIVATION DU FIREWALL :
echo.
echo Voulez-vous reactiver le firewall ? (O/N)
set /p REACTIVATE=
if /i "%REACTIVATE%"=="O" (
    netsh advfirewall set allprofiles state on
    echo Firewall reactive
) else (
    echo Firewall reste desactive
)

echo.
echo ========================================
echo RESOLUTION TERMINEE
echo ========================================
echo.

echo PROCHAINES ETAPES :
echo 1. Tester le ping depuis PC2 vers PC1
echo 2. Si ca marche, configurer la synchronisation ERP
echo 3. Si ca ne marche pas, verifier la connexion physique
echo.

pause

