@echo off
title Configuration Sync ERP
color 0B

set /p PC_NAME=Nom du PC (ex: CAISSE01) : 
set /p AGENCE_ID=ID de l'agence (ex: 8) : 
set /p REMOTE1=Chemin partage distant 1 (ex: \\COMPTA01\erp_sync) :
set /p REMOTE2=Chemin partage distant 2 (laisser vide si aucun) :

set CMD=powershell -ExecutionPolicy Bypass -File "%~dp0CONFIG_SYNC.ps1" -PcName "%PC_NAME%" -AgenceId %AGENCE_ID%

if not "%REMOTE1%"=="" set CMD=%CMD% -RemoteShares "%REMOTE1%"
if not "%REMOTE2%"=="" set CMD=%CMD%,"%REMOTE2%"

echo %CMD%
%CMD%

echo.
pause








