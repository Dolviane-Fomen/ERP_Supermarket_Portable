@echo off
chcp 65001 >nul
title OBTENIR L'ADRESSE IP

echo.
echo ============================================================
echo 🌐 ADRESSE IP DE CE PC
echo ============================================================
echo.

echo 📍 Recherche de l'adresse IP...
echo.

REM Obtenir l'adresse IPv4
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    set IP=!IP: =!
    echo ✅ ADRESSE IP : !IP!
    echo.
)

echo ============================================================
echo 📋 INFORMATIONS RÉSEAU COMPLÈTES
echo ============================================================
echo.

ipconfig | findstr /C:"Carte" /C:"IPv4" /C:"Masque" /C:"Passerelle"

echo.
echo ============================================================
echo 💡 INSTRUCTIONS
echo ============================================================
echo.
echo 1. Notez votre adresse IP (ex: 192.168.1.100)
echo 2. Exécutez ce script sur chaque PC
echo 3. Notez toutes les IPs pour la configuration
echo.
echo ============================================================

echo.
pause


