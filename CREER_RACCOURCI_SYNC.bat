@echo off
REM Créer un raccourci sur le bureau pour la synchronisation

echo ========================================
echo Creation d'un raccourci sur le bureau
echo ========================================
echo.

set SCRIPT_PATH=%~dp0SYNC_OVH.bat
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\SYNC_OVH_ERP.lnk

REM Créer le raccourci avec PowerShell
powershell.exe -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%SCRIPT_PATH%'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Synchroniser ERP avec OVH'; $Shortcut.IconLocation = 'powershell.exe,0'; $Shortcut.Save()"

if exist "%SHORTCUT%" (
    echo.
    echo ========================================
    echo SUCCESS: Raccourci cree sur le bureau!
    echo ========================================
    echo Vous pouvez maintenant double-cliquer sur
    echo "SYNC_OVH_ERP" sur votre bureau pour
    echo synchroniser votre projet avec OVH.
    echo.
) else (
    echo.
    echo ========================================
    echo ERREUR: Impossible de creer le raccourci
    echo ========================================
    echo.
)

pause

