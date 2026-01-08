@echo off
REM Script de synchronisation simple pour Windows
REM Double-cliquez sur ce fichier pour synchroniser avec OVH

echo ========================================
echo Synchronisation ERP avec OVH
echo ========================================
echo.

REM Ajouter Git au PATH si GitHub Desktop est installe
if exist "%LOCALAPPDATA%\GitHubDesktop" (
    for /f "delims=" %%i in ('dir /b /ad "%LOCALAPPDATA%\GitHubDesktop\app-*" 2^>nul') do (
        if exist "%LOCALAPPDATA%\GitHubDesktop\%%i\resources\app\git\cmd" (
            set "PATH=%PATH%;%LOCALAPPDATA%\GitHubDesktop\%%i\resources\app\git\cmd"
        )
    )
)

REM Verifier Git
git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ATTENTION: Git n'est pas dans le PATH
    echo Essayons d'utiliser GitHub Desktop...
    echo.
)

REM Verifier si PowerShell est disponible
powershell.exe -Command "& {Get-Host}" >nul 2>&1
if errorlevel 1 (
    echo Erreur: PowerShell n'est pas disponible
    pause
    exit /b 1
)

REM Executer le script PowerShell
powershell.exe -ExecutionPolicy Bypass -File "%~dp0sync_ovh.ps1" push

echo.
echo ========================================
pause

