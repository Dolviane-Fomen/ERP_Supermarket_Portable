@echo off
REM Script pour résoudre le conflit Git sur db_erp.sqlite3
REM Ce fichier ne devrait pas être versionné

echo ================================================================================
echo RESOLUTION DU CONFLIT GIT - db_erp.sqlite3
echo ================================================================================
echo.

REM Vérifier si Git est disponible
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Git n'est pas trouve dans le PATH
    echo.
    echo Veuillez utiliser GitHub Desktop pour resoudre le conflit manuellement.
    echo Consultez GUIDE_RESOLUTION_CONFLIT_DB.md pour les instructions.
    echo.
    pause
    exit /b 1
)

echo [OK] Git est disponible
echo.

REM Vérifier l'état Git
echo Verification de l'etat Git...
git status --porcelain >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Ce repertoire n'est pas un depot Git valide
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo OPTIONS DE RESOLUTION:
echo ================================================================================
echo.
echo 1. Annuler le merge en cours (git merge --abort)
echo 2. Retirer db_erp.sqlite3 du suivi Git (git rm --cached)
echo 3. Les deux: annuler le merge puis retirer le fichier
echo 4. Quitter
echo.
set /p choix="Votre choix (1-4): "

if "%choix%"=="1" goto annuler_merge
if "%choix%"=="2" goto retirer_fichier
if "%choix%"=="3" goto les_deux
if "%choix%"=="4" goto fin
goto choix_invalide

:annuler_merge
echo.
echo Annulation du merge en cours...
git merge --abort
if %ERRORLEVEL% EQU 0 (
    echo [OK] Merge annule avec succes
) else (
    echo [INFO] Aucun merge en cours ou erreur lors de l'annulation
)
goto fin

:retirer_fichier
echo.
echo Retrait de db_erp.sqlite3 du suivi Git...
git rm --cached db_erp.sqlite3
if %ERRORLEVEL% EQU 0 (
    echo [OK] Fichier retire du suivi Git
    echo.
    echo IMPORTANT: Vous devez maintenant commiter ce changement:
    echo   git commit -m "Remove db_erp.sqlite3 from version control"
    echo.
    set /p commit="Voulez-vous commiter maintenant? (O/N): "
    if /i "%commit%"=="O" (
        git commit -m "Remove db_erp.sqlite3 from version control"
        if %ERRORLEVEL% EQU 0 (
            echo [OK] Changement commite
            echo.
            set /p push="Voulez-vous pousser les changements? (O/N): "
            if /i "%push%"=="O" (
                git push
            )
        )
    )
) else (
    echo [ERREUR] Impossible de retirer le fichier du suivi Git
    echo Le fichier est peut-etre deja retire ou n'existe pas dans Git
)
goto fin

:les_deux
echo.
echo Annulation du merge en cours...
git merge --abort
echo.
echo Retrait de db_erp.sqlite3 du suivi Git...
git rm --cached db_erp.sqlite3
if %ERRORLEVEL% EQU 0 (
    echo [OK] Fichier retire du suivi Git
    echo.
    set /p commit="Voulez-vous commiter ce changement? (O/N): "
    if /i "%commit%"=="O" (
        git commit -m "Remove db_erp.sqlite3 from version control"
        if %ERRORLEVEL% EQU 0 (
            echo [OK] Changement commite
        )
    )
)
goto fin

:choix_invalide
echo.
echo [ERREUR] Choix invalide
goto fin

:fin
echo.
echo ================================================================================
echo Operation terminee
echo ================================================================================
echo.
echo NOTE: Le fichier db_erp.sqlite3 reste sur votre disque local.
echo       Seul le suivi Git a ete retire.
echo.
pause
