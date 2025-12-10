@echo off
echo ========================================
echo VERIFICATION CONNEXION ROUTEUR
echo ========================================
echo.

echo DIAGNOSTIC COMPLET DE LA CONNEXION RESEAU
echo.

echo 1. VERIFICATION DE LA CONNEXION PHYSIQUE...
echo.
echo Verifiez que :
echo - Le cable reseau est bien connecte sur PC1
echo - Le cable est connecte au routeur/switch
echo - Les LEDs de connexion sont allumees
echo - Le routeur/switch est allume
echo.

echo 2. VERIFICATION DE LA CARTE RESEAU...
echo.
echo Statut de la carte reseau :
netsh interface show interface
echo.

echo 3. VERIFICATION DE LA CONFIGURATION IP...
echo.
echo Configuration IP actuelle :
ipconfig /all
echo.

echo 4. TEST DE CONNECTIVITE VERS LE ROUTEUR...
echo.
echo Test de ping vers le routeur (192.168.8.1) :
ping -n 4 192.168.8.1
echo.

echo 5. TEST DE CONNECTIVITE VERS PC2...
echo.
echo Test de ping vers PC2 (192.168.8.11) :
ping -n 4 192.168.8.11
echo.

echo 6. VERIFICATION DES ROUTES...
echo.
echo Table de routage :
route print
echo.

echo 7. VERIFICATION DU FIREWALL...
echo.
echo Statut du firewall :
netsh advfirewall show allprofiles state
echo.

echo 8. VERIFICATION DES SERVICES RESEAU...
echo.
echo Services reseau actifs :
net start | findstr /i "dhcp\|dns\|tcpip"
echo.

echo ========================================
echo DIAGNOSTIC TERMINE
echo ========================================
echo.

echo SOLUTIONS RECOMMANDEES :
echo.

echo Si PC1 a toujours une IP 169.254.x.x :
echo 1. Verifiez la connexion physique
echo 2. Redemarrez la carte reseau
echo 3. Liberez et renouvelez l'IP
echo 4. Configurez manuellement l'IP
echo.

echo Si PC1 a maintenant une IP 192.168.8.x :
echo 1. Testez le ping vers PC2
echo 2. Testez le ping depuis PC2 vers PC1
echo 3. Configurez la synchronisation ERP
echo.

pause
