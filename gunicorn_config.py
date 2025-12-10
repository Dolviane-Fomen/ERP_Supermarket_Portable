"""
Configuration Gunicorn pour l'ERP Supermarket
Ce fichier doit être placé à la racine du projet
"""
import multiprocessing

# Adresse et port d'écoute
bind = "127.0.0.1:8000"

# Nombre de workers (recommandé: (2 x CPU cores) + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Nombre de threads par worker (optionnel)
threads = 2

# Timeout en secondes
timeout = 120

# Nombre de requêtes avant redémarrage d'un worker (pour éviter les fuites mémoire)
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# Nom du processus
proc_name = "erp_supermarket"

# User et Group (à configurer selon votre serveur)
# user = "erpuser"
# group = "www-data"

# Mode daemon (False si géré par systemd)
daemon = False

# Préchargement de l'application (améliore les performances)
preload_app = True

# Worker class (par défaut: sync, peut utiliser gevent pour async)
worker_class = "sync"

