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
PROJECT_DIR="/home/ubuntu/erp_project"
VENV_DIR="$PROJECT_DIR/venv"
SETTINGS_MODULE="erp_project.settings_production"

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

# Redémarrer Gunicorn
echo -e "\n${GREEN}🔄 Redémarrage de Gunicorn...${NC}"
sudo systemctl restart gunicorn

# Vérifier le statut
echo -e "\n${GREEN}✅ Vérification du statut...${NC}"
sleep 2
if sudo systemctl is-active --quiet gunicorn; then
    echo -e "${GREEN}✅ Gunicorn est actif!${NC}"
else
    echo -e "${RED}❌ Erreur: Gunicorn n'est pas actif!${NC}"
    echo -e "${YELLOW}Vérifiez les logs avec: sudo journalctl -u gunicorn -n 50${NC}"
    exit 1
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Déploiement terminé avec succès!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}💡 Pour voir les logs: sudo journalctl -u gunicorn -f${NC}"




