#!/usr/bin/env python
"""
Service de synchronisation automatique en arrière-plan
Synchronise les données à intervalles réguliers sans intervention
"""
import os
import sys
import time
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# Configuration
SYNC_INTERVAL = 300  # Secondes entre chaque synchronisation (5 minutes par défaut)
SYNC_SCRIPT = "SYNC_LOCAL_ONLINE.py"
SYNC_MODE = "sync"  # pull, push, ou sync

def log_message(message):
    """Afficher un message avec timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def check_internet():
    """Vérifier si Internet est disponible"""
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def run_sync():
    """Exécuter la synchronisation"""
    log_message("Démarrage de la synchronisation automatique...")
    
    # Vérifier Internet
    if not check_internet():
        log_message("⚠️  Pas de connexion Internet, synchronisation annulée")
        return False
    
    # Vérifier que le script existe
    script_path = Path(__file__).parent / SYNC_SCRIPT
    if not script_path.exists():
        log_message(f"❌ Script introuvable: {SYNC_SCRIPT}")
        return False
    
    # Exécuter la synchronisation
    try:
        # Détecter la commande Python disponible
        python_cmd = "py"
        try:
            subprocess.run(["py", "--version"], capture_output=True, timeout=2, check=True)
        except:
            python_cmd = "python"
        
        cmd = f'{python_cmd} "{script_path}" --mode {SYNC_MODE} --merge'
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600  # Timeout de 10 minutes
        )
        
        if result.returncode == 0:
            log_message("✅ Synchronisation réussie")
            return True
        else:
            log_message(f"⚠️  Synchronisation terminée avec avertissements")
            if result.stderr:
                log_message(f"   Erreur: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        log_message("❌ Synchronisation timeout (trop longue)")
        return False
    except Exception as e:
        log_message(f"❌ Erreur lors de la synchronisation: {e}")
        return False

def sync_loop():
    """Boucle de synchronisation automatique"""
    log_message("Service de synchronisation automatique démarré")
    log_message(f"Intervalle: {SYNC_INTERVAL} secondes ({SYNC_INTERVAL/60:.1f} minutes)")
    log_message(f"Mode: {SYNC_MODE}")
    log_message("Appuyez sur Ctrl+C pour arrêter")
    print()
    
    while True:
        try:
            # Attendre l'intervalle
            time.sleep(SYNC_INTERVAL)
            
            # Exécuter la synchronisation
            run_sync()
            print()
            
        except KeyboardInterrupt:
            log_message("Arrêt du service de synchronisation...")
            break
        except Exception as e:
            log_message(f"❌ Erreur dans la boucle: {e}")
            time.sleep(60)  # Attendre 1 minute avant de réessayer

def main():
    """Fonction principale"""
    print("=" * 60)
    print("SYNCHRONISATION AUTOMATIQUE EN ARRIÈRE-PLAN")
    print("=" * 60)
    print()
    
    # Vérifier Internet
    if not check_internet():
        print("⚠️  Pas de connexion Internet actuellement")
        print("   Le service démarrera quand Internet sera disponible")
        print()
    
    # Démarrer la boucle
    try:
        sync_loop()
    except KeyboardInterrupt:
        print()
        log_message("Service arrêté par l'utilisateur")
    except Exception as e:
        log_message(f"❌ Erreur fatale: {e}")

if __name__ == '__main__':
    main()
