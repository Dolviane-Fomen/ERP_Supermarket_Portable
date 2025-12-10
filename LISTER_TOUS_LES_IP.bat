@echo off
chcp 65001 >nul
title LISTER TOUTES LES IPs DU RÉSEAU

echo.
echo ============================================================
echo 🌐 SCANNER RÉSEAU - TOUS LES PC CONNECTÉS
echo ============================================================
echo.

echo 📍 Obtention de votre IP...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set MYIP=%%a
    set MYIP=!MYIP: =!
    echo ✅ Votre IP : !MYIP!
)

echo.
echo 📡 Scan des PC connectés au routeur...
echo ⏰ Cela peut prendre 1-2 minutes...
echo.

REM Extraire le réseau (ex: 192.168.1)
for /f "tokens=1,2,3 delims=." %%a in ("!MYIP!") do (
    set NETWORK=%%a.%%b.%%c
)

echo 🔍 Réseau détecté : !NETWORK!.0/24
echo.
echo ============================================================
echo 📋 PC TROUVÉS SUR LE RÉSEAU :
echo ============================================================
echo.

REM Scanner le réseau
for /L %%i in (1,1,254) do (
    ping -n 1 -w 100 !NETWORK!.%%i >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ PC trouvé : !NETWORK!.%%i
    )
)

echo.
echo ============================================================
echo 💡 PROCHAINES ÉTAPES
echo ============================================================
echo.
echo 1. Notez toutes les IPs trouvées ci-dessus
echo 2. Identifiez quel PC correspond à quelle IP
echo 3. Utilisez ces IPs pour la configuration ERP
echo.
echo Exemple :
echo   PC1 (Principal) : 192.168.1.100
echo   PC2 (Caisse)    : 192.168.1.101
echo   PC3 (Stock)     : 192.168.1.102
echo   PC4 (Compta)    : 192.168.1.103
echo.
echo ============================================================

echo.
pause


