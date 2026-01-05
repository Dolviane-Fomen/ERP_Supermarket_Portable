# Script de migration SQLite vers PostgreSQL
# Usage: .\migrate_to_postgresql.ps1

Write-Host "=== Migration SQLite vers PostgreSQL ===" -ForegroundColor Cyan
Write-Host ""

# Vérifier que le fichier d'export existe
if (-not (Test-Path "export_data.json")) {
    Write-Host "ERREUR: export_data.json introuvable!" -ForegroundColor Red
    Write-Host "Exécutez d'abord: py manage.py dumpdata supermarket --output export_data.json" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Fichier export_data.json trouvé ($([math]::Round((Get-Item export_data.json).Length/1MB, 2)) MB)" -ForegroundColor Green
Write-Host ""

# Vérifier que psycopg2 est installé
Write-Host "Vérification de psycopg2-binary..." -ForegroundColor Cyan
$psycopg2 = py -c "import psycopg2; print('OK')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "psycopg2-binary n'est pas installé. Installation..." -ForegroundColor Yellow
    py -m pip install psycopg2-binary
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERREUR: Impossible d'installer psycopg2-binary" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ psycopg2-binary est installé" -ForegroundColor Green
Write-Host ""

# Demander les informations PostgreSQL
Write-Host "=== Configuration PostgreSQL ===" -ForegroundColor Cyan
Write-Host ""

$dbName = Read-Host "Nom de la base de données [erp_db]"
if ([string]::IsNullOrWhiteSpace($dbName)) { $dbName = "erp_db" }

$dbUser = Read-Host "Nom d'utilisateur PostgreSQL [erp_user]"
if ([string]::IsNullOrWhiteSpace($dbUser)) { $dbUser = "erp_user" }

$dbPassword = Read-Host "Mot de passe PostgreSQL" -AsSecureString
$dbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($dbPassword))

$dbHost = Read-Host "Host [localhost]"
if ([string]::IsNullOrWhiteSpace($dbHost)) { $dbHost = "localhost" }

$dbPort = Read-Host "Port [5432]"
if ([string]::IsNullOrWhiteSpace($dbPort)) { $dbPort = "5432" }

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Base: $dbName"
Write-Host "  Utilisateur: $dbUser"
Write-Host "  Host: $dbHost"
Write-Host "  Port: $dbPort"
Write-Host ""

# Mettre à jour le fichier de configuration
Write-Host "Mise à jour de settings_local_postgresql.py..." -ForegroundColor Cyan
$settingsContent = @"
"""
Configuration Django pour PostgreSQL en local
Copie de settings.py avec PostgreSQL au lieu de SQLite
"""
from .settings import *
import os

# Base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$dbName',
        'USER': '$dbUser',
        'PASSWORD': '$dbPasswordPlain',
        'HOST': '$dbHost',
        'PORT': '$dbPort',
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Garder les autres paramètres de settings.py
"@

$settingsContent | Out-File -FilePath "erp_project\settings_local_postgresql.py" -Encoding UTF8
Write-Host "✅ Fichier de configuration créé" -ForegroundColor Green
Write-Host ""

# Tester la connexion
Write-Host "Test de connexion à PostgreSQL..." -ForegroundColor Cyan
$testConnection = py manage.py check --settings=erp_project.settings_local_postgresql 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Connexion réussie!" -ForegroundColor Green
} else {
    Write-Host "ERREUR: Impossible de se connecter à PostgreSQL" -ForegroundColor Red
    Write-Host $testConnection
    Write-Host ""
    Write-Host "Vérifiez que:" -ForegroundColor Yellow
    Write-Host "  1. PostgreSQL est installé et démarré"
    Write-Host "  2. La base de données '$dbName' existe"
    Write-Host "  3. L'utilisateur '$dbUser' existe avec les bonnes permissions"
    Write-Host "  4. Le mot de passe est correct"
    exit 1
}
Write-Host ""

# Créer les tables (migrations)
Write-Host "Création des tables dans PostgreSQL..." -ForegroundColor Cyan
py manage.py migrate --settings=erp_project.settings_local_postgresql
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERREUR lors de la création des tables" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Tables créées" -ForegroundColor Green
Write-Host ""

# Importer les données
Write-Host "Importation des données..." -ForegroundColor Cyan
Write-Host "Cela peut prendre quelques minutes..." -ForegroundColor Yellow
py manage.py loaddata export_data.json --settings=erp_project.settings_local_postgresql
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Migration réussie!" -ForegroundColor Green
    Write-Host ""
    
    # Vérifier les données
    Write-Host "Vérification des données importées..." -ForegroundColor Cyan
    py manage.py shell --settings=erp_project.settings_local_postgresql -c "from supermarket.models import Compte, Client, Article; print(f'Comptes: {Compte.objects.count()}'); print(f'Clients: {Client.objects.count()}'); print(f'Articles: {Article.objects.count()}')"
    
    Write-Host ""
    Write-Host "=== Migration terminée avec succès! ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pour tester l'application avec PostgreSQL:" -ForegroundColor Cyan
    Write-Host "  py manage.py runserver --settings=erp_project.settings_local_postgresql" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Le fichier export_data.json est prêt pour OVH!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "ERREUR lors de l'importation des données" -ForegroundColor Red
    Write-Host "Consultez les messages d'erreur ci-dessus" -ForegroundColor Yellow
    exit 1
}






