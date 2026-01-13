@echo off
REM Revenir a SQLite local (base separee)

echo ========================================
echo Activation SQLite Local
echo ========================================
echo.
echo Vous allez utiliser SQLite local (base separee)
echo Les modifications ne seront PAS visibles en ligne automatiquement
echo.

REM Modifier manage.py
powershell -Command "(Get-Content manage.py) -replace 'settings_shared_db', 'settings_standalone' | Set-Content manage.py"

echo OK: Configuration changee pour utiliser SQLite local
echo.
pause




