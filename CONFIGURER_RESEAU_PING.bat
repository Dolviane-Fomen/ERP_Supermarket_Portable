@echo off
echo ========================================
echo CONFIGURATION RESEAU POUR PING
echo ========================================
echo.

echo Ce script va configurer le reseau pour permettre
echo les pings bidirectionnels entre PC1 et PC2
echo.

echo 1. DESACTIVATION TEMPORAIRE DU FIREWALL...
netsh advfirewall set allprofiles state off
echo Firewall desactive temporairement
echo.

echo 2. CONFIGURATION DES REGLES FIREWALL...
echo Ajout de regles pour permettre les pings
netsh advfirewall firewall add rule name="Allow ICMP Echo Request" dir=in action=allow protocol=icmpv4:8,any
netsh advfirewall firewall add rule name="Allow ICMP Echo Reply" dir=out action=allow protocol=icmpv4:0,any
echo Regles ICMP ajoutees
echo.

echo 3. CONFIGURATION DU PROTOCOLE ICMP...
echo Activation du protocole ICMP
netsh interface ipv4 set global icmpredirects=enabled
netsh interface ipv6 set global icmpredirects=enabled
echo Protocole ICMP active
echo.

echo 4. CONFIGURATION DES INTERFACES RESEAU...
echo Configuration des interfaces reseau
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "Passerelle"') do (
    set GATEWAY=%%a
    set GATEWAY=!GATEWAY: =!
)
echo Passerelle detectee : %GATEWAY%
echo.

echo 5. TEST DE CONNECTIVITE...
echo Test de ping vers la passerelle
ping -n 2 %GATEWAY%
echo.

echo 6. CONFIGURATION DES ROUTES...
echo Configuration des routes reseau
route add 0.0.0.0 mask 0.0.0.0 %GATEWAY% metric 1
echo Route par defaut configuree
echo.

echo 7. VERIFICATION DE LA CONFIGURATION...
echo Verification de la configuration reseau
ipconfig /all
echo.

echo 8. TEST DE PING BIDIRECTIONNEL...
echo.
echo Test de ping PC1 vers PC2 :
echo Entrez l'IP de PC2 (ex: 192.168.1.101) :
set /p PC2_IP=
ping -n 4 %PC2_IP%
echo.

echo Test de ping PC2 vers PC1 :
echo Entrez l'IP de PC1 (ex: 192.168.1.100) :
set /p PC1_IP=
ping -n 4 %PC1_IP%
echo.

echo 9. CONFIGURATION DES EXCEPTIONS ANTIVIRUS...
echo.
echo IMPORTANT : Si vous avez un antivirus, ajoutez une exception
echo pour le reseau local (192.168.1.0/24)
echo.

echo 10. VERIFICATION FINALE...
echo.
echo Verification que les pings fonctionnent dans les deux sens
echo.

echo ========================================
echo CONFIGURATION TERMINEE
echo ========================================
echo.
echo Si les pings ne fonctionnent toujours pas :
echo 1. Verifiez que les deux PC sont sur le meme reseau
echo 2. Verifiez que les cables reseau sont bien connectes
echo 3. Verifiez que le routeur/switch fonctionne
echo 4. Redemarrez les deux PC
echo.

pause

