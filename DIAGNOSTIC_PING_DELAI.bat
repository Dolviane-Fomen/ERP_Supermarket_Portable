@echo off
echo ========================================
echo DIAGNOSTIC PING - DELAI DEPASSE
echo ========================================
echo.

echo PROBLEME : Ping PC1 vers PC2 = DELAI DEPASSE
echo Ping PC2 vers PC1 = SUCCES
echo.

echo CAUSE PROBABLE : Firewall PC2 bloque les reponses
echo.

echo 1. VERIFICATION DE LA CONFIGURATION RESEAU...
echo.
echo Configuration IP actuelle :
ipconfig /all
echo.

echo 2. TEST DE PING VERS PC2...
echo.
echo Test de ping vers PC2 (192.168.8.11) :
ping -n 4 192.168.8.11
echo.

echo 3. TEST DE PING VERS LA PASSERELLE...
echo.
echo Test de ping vers la passerelle :
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

echo 4. VERIFICATION DU FIREWALL...
echo.
echo Statut du firewall :
netsh advfirewall show allprofiles state
echo.

echo 5. CONFIGURATION DES REGLES FIREWALL...
echo.
echo Ajout de regles pour permettre les pings...
netsh advfirewall firewall add rule name="Allow ICMP Echo Request" dir=in action=allow protocol=icmpv4:8,any
netsh advfirewall firewall add rule name="Allow ICMP Echo Reply" dir=out action=allow protocol=icmpv4:0,any
echo Regles ICMP ajoutees
echo.

echo 6. TEST DE PING AVEC TRACERT...
echo.
echo Test de tracert vers PC2 :
tracert 192.168.8.11
echo.

echo 7. TEST DE PING AVEC TELNET...
echo.
echo Test de telnet vers PC2 (port 80) :
telnet 192.168.8.11 80
echo.

echo ========================================
echo DIAGNOSTIC TERMINE
echo ========================================
echo.

echo SOLUTIONS RECOMMANDEES :
echo.
echo 1. Sur PC2, desactiver temporairement le firewall
echo 2. Sur PC2, ajouter des regles ICMP
echo 3. Sur PC2, verifier l'antivirus
echo 4. Sur PC2, verifier la configuration reseau
echo.

pause

