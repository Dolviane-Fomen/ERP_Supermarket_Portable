@echo off
echo ========================================
echo CONFIGURATION IP MANUELLE
echo ========================================
echo.

echo CONFIGURATION MANUELLE DE L'ADRESSE IP
echo.

echo PROBLEME : PC1 utilise une adresse APIPA (169.254.x.x)
echo SOLUTION : Configuration manuelle d'une IP du routeur
echo.

echo 1. VERIFICATION DE LA CONFIGURATION ACTUELLE...
echo.
echo Configuration IP actuelle :
ipconfig /all
echo.

echo 2. CONFIGURATION MANUELLE DE L'IP...
echo.
echo Configuration de l'IP 192.168.8.100 pour PC1...
echo.

echo Configuration de l'interface reseau...
netsh interface ip set address "Connexion au reseau local" static 192.168.8.100 255.255.255.0 192.168.8.1
echo.

echo Configuration du DNS...
netsh interface ip set dns "Connexion au reseau local" static 192.168.8.1
echo.

echo 3. VERIFICATION DE LA NOUVELLE CONFIGURATION...
echo.
echo Nouvelle configuration IP :
ipconfig /all
echo.

echo 4. TEST DE CONNECTIVITE...
echo.
echo Test de ping vers le routeur (192.168.8.1) :
ping -n 4 192.168.8.1
echo.

echo Test de ping vers PC2 (192.168.8.11) :
ping -n 4 192.168.8.11
echo.

echo 5. CONFIGURATION DES REGLES FIREWALL...
echo.
echo Ajout de regles pour permettre les pings...
netsh advfirewall firewall add rule name="Allow ICMP Echo Request" dir=in action=allow protocol=icmpv4:8,any
netsh advfirewall firewall add rule name="Allow ICMP Echo Reply" dir=out action=allow protocol=icmpv4:0,any
echo Regles ICMP ajoutees
echo.

echo 6. TEST FINAL DE PING BIDIRECTIONNEL...
echo.
echo Test de ping PC1 vers PC2 :
ping -n 4 192.168.8.11
echo.

echo Test de ping PC2 vers PC1 :
echo (A executer sur PC2)
echo ping -n 4 192.168.8.100
echo.

echo ========================================
echo CONFIGURATION TERMINEE
echo ========================================
echo.

echo VERIFICATION FINALE :
echo 1. PC1 doit avoir l'IP 192.168.8.100
echo 2. PC2 doit avoir l'IP 192.168.8.11
echo 3. Les deux PC doivent pouvoir se ping mutuellement
echo 4. La synchronisation ERP doit fonctionner
echo.

echo PROCHAINES ETAPES :
echo 1. Executer VERIFIER_CONNEXION_ROUTEUR.bat
echo 2. Tester la synchronisation ERP
echo 3. Configurer les autres PC
echo.

pause
