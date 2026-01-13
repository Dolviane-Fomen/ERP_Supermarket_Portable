@echo off
REM Synchronisation bidirectionnelle des donnees (fusion sans remplacement)

echo ========================================
echo Synchronisation Bidirectionnelle Donnees
echo ========================================
echo.
echo Cette operation va:
echo  1. Exporter vos donnees locales
echo  2. Exporter les donnees depuis OVH
echo  3. Fusionner les deux (sans rien remplacer)
echo  4. Synchroniser dans les deux sens
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0sync_donnees_bidirectionnel.ps1" sync

echo.
pause




