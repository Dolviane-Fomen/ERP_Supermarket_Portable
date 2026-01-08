#!/bin/bash

# Script de déploiement automatique pour ERP Supermarket
# Usage: ./deploy.sh

# Ne pas arrêter en cas d'erreur pour git stash (peut ne rien avoir à stasher)
set +e  # Permet de continuer même en cas d'erreur pour certaines commandes

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

# Sauvegarder les modifications locales si elles existent
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Modifications locales détectées, sauvegarde dans stash...${NC}"
    git stash push -m "Auto-stash before pull $(date +%Y%m%d_%H%M%S)" 2>/dev/null || true
fi

# Réactiver la gestion d'erreurs stricte
set -e

# Récupérer depuis GitHub
echo -e "${GREEN}🔄 Récupération des dernières versions depuis GitHub...${NC}"
git fetch origin main

# Forcer la mise à jour pour correspondre exactement à GitHub
echo -e "${GREEN}🔄 Mise à jour du code pour correspondre à GitHub...${NC}"
git reset --hard origin/main

echo -e "${GREEN}✅ Code à jour avec GitHub${NC}"

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

# Redémarrer Gunicorn/ERP
echo -e "\n${GREEN}🔄 Redémarrage de Gunicorn...${NC}"

# Méthode 1: Essayer avec systemd (service erp)
if systemctl list-unit-files | grep -q "erp.service"; then
    echo -e "${GREEN}📦 Redémarrage via systemd (service erp)...${NC}"
    sudo systemctl restart erp
    sleep 2
    if sudo systemctl is-active --quiet erp; then
        echo -e "${GREEN}✅ Service 'erp' redémarré et actif!${NC}"
    else
        echo -e "${YELLOW}⚠️  Service 'erp' ne répond pas, tentative alternative...${NC}"
    fi
fi

# Méthode 2: Essayer avec systemd (service gunicorn)
if systemctl list-unit-files | grep -q "gunicorn.service"; then
    echo -e "${GREEN}📦 Redémarrage via systemd (service gunicorn)...${NC}"
    sudo systemctl restart gunicorn
    sleep 2
    if sudo systemctl is-active --quiet gunicorn; then
        echo -e "${GREEN}✅ Service 'gunicorn' redémarré et actif!${NC}"
    fi
fi

# Méthode 3: Redémarrer via les processus Gunicorn (si systemd n'est pas disponible)
if ! sudo systemctl is-active --quiet erp 2>/dev/null && ! sudo systemctl is-active --quiet gunicorn 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Aucun service systemd trouvé, redémarrage via processus...${NC}"
    
    # Tuer les processus Gunicorn existants
    pkill -f "gunicorn.*erp_project.wsgi:application" 2>/dev/null || true
    sleep 1
    
    # Redémarrer Gunicorn manuellement en arrière-plan
    echo -e "${GREEN}🔄 Démarrage de Gunicorn manuellement...${NC}"
    nohup gunicorn \
        --config gunicorn_config.py \
        --daemon \
        erp_project.wsgi:application > /dev/null 2>&1 || {
        echo -e "${YELLOW}⚠️  Impossible de démarrer Gunicorn automatiquement${NC}"
        echo -e "${YELLOW}💡 Démarrez-le manuellement avec: gunicorn --config gunicorn_config.py erp_project.wsgi:application${NC}"
    }
fi

# Vérification finale
echo -e "\n${GREEN}✅ Vérification finale du redémarrage...${NC}"
sleep 2

# Vérifier si Gunicorn tourne
if pgrep -f "gunicorn.*erp_project.wsgi:application" > /dev/null; then
    echo -e "${GREEN}✅ Gunicorn est en cours d'exécution!${NC}"
else
    echo -e "${RED}❌ Attention: Gunicorn ne semble pas être en cours d'exécution${NC}"
    echo -e "${YELLOW}💡 Vérifiez manuellement avec: ps aux | grep gunicorn${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Déploiement terminé avec succès!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}💡 Pour voir les logs: sudo journalctl -u gunicorn -f${NC}"




