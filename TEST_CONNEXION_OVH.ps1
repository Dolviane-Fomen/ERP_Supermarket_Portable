# Script PowerShell pour tester la connexion SSH a OVH

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Test de connexion SSH a OVH" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

# Charger la configuration
if (-not (Test-Path ".ovh_config.json")) {
    Write-Host "ERREUR: Fichier .ovh_config.json introuvable!" -ForegroundColor Red
    exit 1
}

try {
    $config = Get-Content ".ovh_config.json" -Encoding UTF8 | ConvertFrom-Json
    $ovhHost = $config.ovh_host
    $ovhUser = $config.ovh_user
} catch {
    Write-Host "ERREUR: Impossible de lire .ovh_config.json" -ForegroundColor Red
    exit 1
}

Write-Host "Configuration actuelle:" -ForegroundColor Cyan
Write-Host "  IP: $ovhHost" -ForegroundColor Cyan
Write-Host "  Utilisateur: $ovhUser" -ForegroundColor Cyan
Write-Host ""

# Test 1: Avec l'utilisateur configure
Write-Host "Test 1: Connexion avec l'utilisateur '$ovhUser'..." -ForegroundColor Yellow
try {
    $result = ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "${ovhUser}@${ovhHost}" "whoami && pwd && echo '---' && echo 'Connexion reussie!'" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "SUCCESS: Connexion OK avec '$ovhUser'!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Resultat:" -ForegroundColor Cyan
        Write-Host $result
        Write-Host ""
        Write-Host "Votre configuration est correcte!" -ForegroundColor Green
        exit 0
    }
} catch {
    Write-Host "Echec de la connexion avec '$ovhUser'" -ForegroundColor Red
}

# Test 2: Avec ubuntu (par defaut sur Ubuntu/OVH)
Write-Host ""
Write-Host "Test 2: Essai avec 'ubuntu'..." -ForegroundColor Yellow
try {
    $result = ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "ubuntu@${ovhHost}" "whoami && pwd && echo '---' && echo 'Connexion reussie avec ubuntu!'" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Yellow
        Write-Host "IMPORTANT: Vous devez utiliser 'ubuntu'!" -ForegroundColor Yellow
        Write-Host "========================================" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Resultat:" -ForegroundColor Cyan
        Write-Host $result
        Write-Host ""
        Write-Host "Modifiez .ovh_config.json et changez:" -ForegroundColor Yellow
        Write-Host '  "ovh_user": "ubuntu"' -ForegroundColor Yellow
        Write-Host '  "ovh_project_path": "/home/ubuntu/erp_project"' -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "Echec aussi avec 'ubuntu'" -ForegroundColor Red
}

# Test 3: Avec root (au cas où)
Write-Host ""
Write-Host "Test 3: Essai avec 'root'..." -ForegroundColor Yellow
try {
    $result = ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no "root@${ovhHost}" "whoami && pwd && echo '---' && echo 'Connexion reussie avec root!'" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Yellow
        Write-Host "IMPORTANT: Vous devez utiliser 'root'!" -ForegroundColor Yellow
        Write-Host "========================================" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Resultat:" -ForegroundColor Cyan
        Write-Host $result
        Write-Host ""
        Write-Host "Modifiez .ovh_config.json et changez:" -ForegroundColor Yellow
        Write-Host '  "ovh_user": "root"' -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "Echec aussi avec 'root'" -ForegroundColor Red
}

# Si on arrive ici, les deux ont echoue
Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "ERREUR: Aucune connexion reussie" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "Verifiez:" -ForegroundColor Yellow
Write-Host "  1. L'IP est correcte: $ovhHost" -ForegroundColor Yellow
Write-Host "  2. Le serveur OVH est accessible" -ForegroundColor Yellow
Write-Host "  3. SSH est active sur le serveur (port 22)" -ForegroundColor Yellow
Write-Host "  4. Vos cles SSH ou mot de passe sont corrects" -ForegroundColor Yellow
Write-Host ""

