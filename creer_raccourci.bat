@echo off
echo Creation du raccourci ERP sur le bureau...

REM Creer le raccourci
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\ERP Supermarket.lnk'); $Shortcut.TargetPath = '%~dp0ERP_Launcher.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'ERP Supermarket - Systeme de Gestion'; $Shortcut.IconLocation = 'shell32.dll,21'; $Shortcut.Save()"

echo Raccourci cree sur le bureau: "ERP Supermarket"
echo L'utilisateur peut maintenant double-cliquer sur le raccourci pour lancer l'ERP
pause
