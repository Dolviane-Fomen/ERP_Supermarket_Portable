@echo off
echo ========================================
echo CORRECTION CONFIGURATION RESEAU
echo ========================================
echo.

echo PROBLEME IDENTIFIE :
echo PC1 utilise une adresse APIPA (169.254.x.x)
echo au lieu d'une adresse du routeur (192.168.x.x)
echo.

echo SOLUTIONS A APPLIQUER :
echo.

echo 1. VERIFICATION DE LA CONNEXION PHYSIQUE...
echo Verifiez que le cable reseau est bien connecte sur PC1
echo Verifiez que le cable est connecte au routeur/switch
echo Verifiez que les LEDs de connexion sont allumees
echo.

echo 2. REDEMARRAGE DE LA CARTE RESEAU...
echo Redemarrage de la carte reseau...
netsh interface set interface "Connexion au reseau local" disable
timeout /t 3 /nobreak >nul
netsh interface set interface "Connexion au reseau local" enable
echo Carte reseau redemarree
echo.

echo 3. LIBERATION ET RENOUVELLEMENT DE L'IP...
echo Liberation de l'IP actuelle...
ipconfig /release
echo.
echo Renouvellement de l'IP...
ipconfig /renew
echo.

echo 4. VERIFICATION DE LA NOUVELLE CONFIGURATION...
echo Nouvelle configuration reseau :
ipconfig /all
echo.

echo 5. TEST DE CONNECTIVITE...
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
    echo Verifiez la connexion au routeur
)
echo.

echo 6. TEST DE PING VERS PC2...
echo Test de ping vers PC2 (192.168.8.11)...
ping -n 4 192.168.8.11
echo.

echo 7. CONFIGURATION MANUELLE SI NECESSAIRE...
echo.
echo Si l'IP n'est toujours pas correcte, configurez manuellement :
echo.
echo - Ouvrir "Parametres reseau" dans Windows
echo - Cliquer sur "Modifier les options d'adaptateur"
echo - Clic droit sur "Connexion au reseau local"
echo - Proprietes → Protocole Internet version 4 (TCP/IPv4)
echo - Proprietes → Utiliser l'adresse IP suivante :
echo   IP : 192.168.8.100 (ou autre IP libre)
echo   Masque : 255.255.255.0
echo   Passerelle : 192.168.8.1 (IP du routeur)
echo   DNS : 192.168.8.1
echo.

echo ========================================
echo CORRECTION TERMINEE
echo ========================================
echo.

echo VERIFICATION FINALE :
echo 1. PC1 doit avoir une IP 192.168.8.x
echo 2. PC2 doit avoir une IP 192.168.8.x
echo 3. Les deux PC doivent pouvoir se ping mutuellement
echo.

pause
