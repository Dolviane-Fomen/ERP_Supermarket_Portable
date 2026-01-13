@echo off
REM Script pour installer psycopg2-binary (necessaire pour PostgreSQL)

echo ========================================
echo Installation de psycopg2-binary
echo ========================================
echo.

REM Changer vers le repertoire du projet
cd /d "%~dp0"

REM Activer l'environnement virtuel si il existe
if exist "venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
    echo.
)

echo Installation de psycopg2-binary...
echo.

REM Essayer avec python -m pip
python -m pip install psycopg2-binary

if errorlevel 1 (
    echo.
    echo ERREUR lors de l'installation avec python -m pip
    echo.
    echo Tentative avec py -m pip...
    py -m pip install psycopg2-binary
)

if errorlevel 1 (
    echo.
    echo ERREUR: Impossible d'installer psycopg2-binary
    echo.
    echo Solutions possibles:
    echo 1. Verifiez que Python est installe: python --version
    echo 2. Installez Python depuis: https://www.python.org/downloads/
    echo 3. Cochez "Add Python to PATH" lors de l'installation
    echo.
) else (
    echo.
    echo ========================================
    echo SUCCESS: psycopg2-binary installe!
    echo ========================================
    echo.
)

pause




