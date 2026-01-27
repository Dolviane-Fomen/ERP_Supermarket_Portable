@echo off
echo ========================================
echo Retrait de db_erp.sqlite3 du suivi Git
echo ========================================
echo.
echo ATTENTION: Ce script va retirer le fichier db_erp.sqlite3 du suivi Git
echo mais ne le supprimera PAS de votre disque dur.
echo.

REM Vérifier si Git est installé
where git >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installé ou n'est pas dans le PATH.
    echo.
    echo SOLUTION: Installez Git ou utilisez GitHub Desktop pour retirer le fichier.
    echo Dans GitHub Desktop: Clic droit sur db_erp.sqlite3 ^> Ignore
    echo.
    pause
    exit /b 1
)

REM Vérifier si on est dans un dépôt Git
if not exist ".git" (
    echo ERREUR: Ce script doit être exécuté dans le répertoire du dépôt Git.
    echo.
    pause
    exit /b 1
)

echo Vérification du fichier...
if not exist "db_erp.sqlite3" (
    echo ATTENTION: Le fichier db_erp.sqlite3 n'existe pas dans ce répertoire.
    echo Le script va quand même essayer de le retirer du suivi Git.
    echo.
)

echo.
echo Appuyez sur une touche pour continuer...
pause
echo.

REM Retirer le fichier de l'index Git (mais le garder sur le disque)
echo Retrait du fichier du suivi Git...
git rm --cached db_erp.sqlite3

if errorlevel 1 (
    echo.
    echo ERREUR lors du retrait du fichier.
    echo Le fichier n'est peut-être pas suivi par Git.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCES!
echo ========================================
echo.
echo Le fichier db_erp.sqlite3 a été retiré du suivi Git.
echo Le fichier existe toujours sur votre disque dur.
echo.
echo Vous pouvez maintenant commiter les autres changements normalement.
echo Dans GitHub Desktop, le fichier ne devrait plus apparaître.
echo.
pause
