@echo off
REM Script pour tester le deploiement automatique

echo ========================================
echo ETAPE 3: Tester le deploiement automatique
echo ========================================
echo.
echo Maintenant, testons si tout fonctionne:
echo.
echo 1. Faites une petite modification dans votre projet
echo    (Par exemple: modifiez un commentaire dans un fichier)
echo.
echo 2. Double-cliquez sur SYNC_OVH.bat
echo.
echo 3. Allez sur GitHub Actions:
echo    https://github.com/Dolviane-Fomen/ERP_Supermarket_Portable/actions
echo.
echo 4. Vous devriez voir un workflow "Deploy to OVH" qui se lance
echo.
echo 5. Attendez qu'il soit vert (SUCCESS)
echo.
echo 6. Verifiez sur le serveur OVH:
echo    ssh ubuntu@51.68.124.152
echo    cd /home/ubuntu/erp_project
echo    git log -1
echo.
echo ========================================
echo Si le workflow est vert, c'est bon!
echo ========================================
echo.
pause




