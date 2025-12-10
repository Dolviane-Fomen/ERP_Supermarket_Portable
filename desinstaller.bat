@echo off
title Desinstallation ERP Supermarket
color 0C

echo.
echo  ========================================
echo     DESINSTALLATION ERP SUPERMARKET
echo  ========================================
echo.
echo  Voulez-vous vraiment desinstaller l'ERP?
echo  Cela supprimera tous les raccourcis et le menu Demarrer
echo.
set /p choice="Continuer? (O/N): "

if /i "%choice%"=="O" (
    echo.
    echo  Suppression des raccourcis...
    
    REM Supprimer le raccourci du bureau
    del "%USERPROFILE%\Desktop\ERP Supermarket.lnk" 2>nul
    
    REM Supprimer le menu Demarrer
    rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\ERP Supermarket" 2>nul
    
    echo  ✓ Desinstallation terminee
    echo  ✓ Les fichiers de l'ERP restent dans le dossier
    echo  ✓ Vous pouvez les supprimer manuellement si desire
) else (
    echo  Desinstallation annulee
)

echo.
pause





