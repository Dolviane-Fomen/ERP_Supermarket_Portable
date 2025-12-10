@echo off
echo ========================================
echo TEST PING BIDIRECTIONNEL
echo ========================================
echo.

echo PC1 vers PC2 : SUCCES
echo PC2 vers PC1 : ECHEC
echo.
echo CAUSES POSSIBLES :
echo.

echo 1. FIREWALL WINDOWS :
echo    - Le firewall de PC1 bloque les pings entrants
echo    - Solution : Desactiver temporairement le firewall
echo.

echo 2. ANTIVIRUS :
echo    - L'antivirus de PC1 bloque les connexions
echo    - Solution : Ajouter une exception reseau
echo.

echo 3. CONFIGURATION RESEAU :
echo    - PC1 a une configuration reseau differente
echo    - Solution : Verifier les parametres reseau
echo.

echo 4. CARTE RESEAU :
echo    - Probleme avec la carte reseau de PC1
echo    - Solution : Redemarrer ou reconfigurer
echo.

echo ========================================
echo SOLUTIONS A TESTER :
echo ========================================
echo.

echo SOLUTION 1 - DESACTIVER FIREWALL PC1 :
echo netsh advfirewall set allprofiles state off
echo.

echo SOLUTION 2 - VERIFIER CONFIGURATION RESEAU :
echo ipconfig /all
echo.

echo SOLUTION 3 - TESTER AVEC TELNET :
echo telnet [IP_PC2] 80
echo.

echo SOLUTION 4 - VERIFIER ROUTES :
echo route print
echo.

echo SOLUTION 5 - TESTER AVEC TRACERT :
echo tracert [IP_PC2]
echo.

echo ========================================
echo EXECUTION DES TESTS :
echo ========================================
echo.

echo 1. Desactivation temporaire du firewall PC1...
netsh advfirewall set allprofiles state off
echo Firewall desactive temporairement
echo.

echo 2. Test de ping depuis PC1 vers PC2...
echo Entrez l'IP de PC2 (ex: 192.168.1.101) :
set /p PC2_IP=
ping -n 4 %PC2_IP%
echo.

echo 3. Test de ping depuis PC2 vers PC1...
echo Entrez l'IP de PC1 (ex: 192.168.1.100) :
set /p PC1_IP=
ping -n 4 %PC1_IP%
echo.

echo 4. Test de telnet PC1 vers PC2...
telnet %PC2_IP% 80
echo.

echo 5. Test de telnet PC2 vers PC1...
telnet %PC1_IP% 80
echo.

echo 6. Verification des routes...
route print
echo.

echo 7. Test de tracert PC1 vers PC2...
tracert %PC2_IP%
echo.

echo 8. Test de tracert PC2 vers PC1...
tracert %PC1_IP%
echo.

echo ========================================
echo REACTIVATION DU FIREWALL :
echo ========================================
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
echo TEST TERMINE
echo ========================================
pause

