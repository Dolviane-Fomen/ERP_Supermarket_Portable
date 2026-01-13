#!/bin/bash
# Script à exécuter sur OVH pour autoriser les connexions distantes PostgreSQL

echo "Configuration PostgreSQL pour connexions distantes..."

# Modifier postgresql.conf
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf

# Ajouter dans pg_hba.conf
echo "host    all             all             0.0.0.0/0               md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf > /dev/null

# Redémarrer PostgreSQL
sudo systemctl restart postgresql

# Ouvrir le port
sudo ufw allow 5432/tcp

echo "OK: PostgreSQL configuré pour accepter les connexions distantes"




