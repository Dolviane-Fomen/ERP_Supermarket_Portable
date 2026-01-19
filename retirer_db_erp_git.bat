@echo off
REM Script pour retirer db_erp.sqlite3 du suivi Git

echo ========================================
echo Retrait de db_erp.sqlite3 du suivi Git
echo ========================================
echo.

REM Vérifier si Git est installé
where git >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installe ou n'est pas dans le PATH
    echo.
    echo SOLUTION: Utilisez GitHub Desktop pour faire cette operation
    echo.
    pause
    exit /b 1
)

REM Vérifier si on est dans un dépôt Git
if not exist ".git" (
    echo ERREUR: Ce n'est pas un depot Git!
    pause
    exit /b 1
)

echo Retrait de db_erp.sqlite3 du suivi Git...
echo.

REM Retirer le fichier du suivi Git (mais le garder localement)
git rm --cached db_erp.sqlite3

if errorlevel 1 (
    echo.
    echo ATTENTION: Le fichier n'etait peut-etre pas suivi par Git
    echo Continuons quand meme...
) else (
    echo.
    echo SUCCESS: db_erp.sqlite3 retire du suivi Git
)

echo.
echo Verification que le fichier est bien ignore...
git check-ignore db_erp.sqlite3
if errorlevel 1 (
    echo ATTENTION: Le fichier n'est pas dans .gitignore
    echo Ajout dans .gitignore...
    echo db_erp.sqlite3 >> .gitignore
    echo SUCCESS: Fichier ajoute dans .gitignore
) else (
    echo OK: Le fichier est bien dans .gitignore
)

echo.
echo ========================================
echo OPERATION TERMINEE
echo ========================================
echo.
echo Vous pouvez maintenant:
echo 1. Faire un commit de ce changement
echo 2. Faire un fetch/pull normalement
echo.
pause
