#!/bin/bash

# Script de déploiement automatique pour ERP Supermarket
# Usage: ./deploy.sh

set -e  # Arrêter en cas d'erreur

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}🚀 Déploiement ERP Supermarket${NC}"
echo -e "${YELLOW}========================================${NC}"

# Variables
# Détecter automatiquement le répertoire du projet
PROJECT_DIR="${PROJECT_DIR:-$(cd "$(dirname "$0")" && pwd)}"
VENV_DIR="$PROJECT_DIR/venv"
SETTINGS_MODULE="erp_project.settings_production"
SERVICE_NAME="${SERVICE_NAME:-erp}"  # Nom du service systemd

# Vérifier que nous sommes dans le bon répertoire ou le créer
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Erreur: Le dossier $PROJECT_DIR n'existe pas!${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

echo -e "\n${GREEN}📂 Répertoire: $PROJECT_DIR${NC}"

# Activer l'environnement virtuel
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${RED}❌ Erreur: L'environnement virtuel n'existe pas!${NC}"
    exit 1
fi

echo -e "${GREEN}🔧 Activation de l'environnement virtuel...${NC}"
source "$VENV_DIR/bin/activate"

# Récupérer les dernières modifications depuis GitHub
echo -e "\n${GREEN}📥 Récupération des modifications depuis GitHub...${NC}"
git pull origin main || {
    echo -e "${RED}❌ Erreur lors du git pull!${NC}"
    exit 1
}

# Installer/mettre à jour les dépendances
echo -e "\n${GREEN}📦 Installation des dépendances...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Exécuter les migrations
echo -e "\n${GREEN}🗄️  Exécution des migrations...${NC}"
DJANGO_SETTINGS_MODULE=$SETTINGS_MODULE python manage.py migrate --noinput

# Collecter les fichiers statiques
echo -e "\n${GREEN}📁 Collecte des fichiers statiques...${NC}"
DJANGO_SETTINGS_MODULE=$SETTINGS_MODULE python manage.py collectstatic --noinput

# Redémarrer le service Gunicorn/ERP
echo -e "\n${GREEN}🔄 Redémarrage du service ERP...${NC}"

# Vérifier si le service existe
if systemctl list-unit-files | grep -q "$SERVICE_NAME.service"; then
    sudo systemctl restart $SERVICE_NAME
    
    # Vérifier le statut
    echo -e "\n${GREEN}✅ Vérification du statut...${NC}"
    sleep 2
    if sudo systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}✅ Service $SERVICE_NAME est actif!${NC}"
    else
        echo -e "${RED}❌ Erreur: Service $SERVICE_NAME n'est pas actif!${NC}"
        echo -e "${YELLOW}Vérifiez les logs avec: sudo journalctl -u $SERVICE_NAME -n 50${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  Service $SERVICE_NAME non trouvé. Redémarrage manuel requis.${NC}"
    echo -e "${YELLOW}💡 Vérifiez que le service systemd est configuré correctement.${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Déploiement terminé avec succès!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}💡 Pour voir les logs: sudo journalctl -u gunicorn -f${NC}"




