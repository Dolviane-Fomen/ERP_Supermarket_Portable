@echo off
echo ========================================
echo DIAGNOSTIC PING - RESEAU LOCAL
echo ========================================
echo.

echo 1. IP du PC actuel :
ipconfig | findstr "IPv4"
echo.

echo 2. Test de ping vers l'autre PC...
echo Entrez l'IP de l'autre PC (ex: 192.168.1.101) :
set /p TARGET_IP=

echo.
echo 3. Test de ping vers %TARGET_IP% :
ping -n 4 %TARGET_IP%
echo.

echo 4. Test de ping vers la passerelle :
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "Passerelle"') do (
    set GATEWAY=%%a
    set GATEWAY=!GATEWAY: =!
)
echo Passerelle detectee : %GATEWAY%
ping -n 2 %GATEWAY%
echo.

echo 5. Test de ping vers 8.8.8.8 (Internet) :
ping -n 2 8.8.8.8
echo.

echo 6. Informations reseau detaillees :
ipconfig /all
echo.

echo 7. Test de resolution DNS :
nslookup %TARGET_IP%
echo.

echo 8. Test de telnet (si disponible) :
telnet %TARGET_IP% 80
echo.

echo ========================================
echo DIAGNOSTIC TERMINE
echo ========================================
pause

