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
SYNC_INTERVAL = 60  # Secondes entre chaque synchronisation (1 minute par défaut pour synchronisation quasi-temps réel)
SYNC_SCRIPT = "SYNC_LOCAL_ONLINE.py"
SYNC_MODE = "push"  # pull, push, ou sync (bidirectionnel)
# Mode "push" = Envoie seulement les données locales vers le serveur (temps réel)
# Mode "sync" = Télécharge puis envoie (bidirectionnel, plus lent)
# Mode "pull" = Télécharge seulement depuis le serveur

# Nombre de tentatives en cas d'échec
MAX_RETRIES = 3
RETRY_DELAY = 30  # Secondes entre les tentatives

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
    """Exécuter la synchronisation avec retry automatique"""
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
    
    # Détecter la commande Python disponible
    python_cmd = "py"
    try:
        subprocess.run(["py", "--version"], capture_output=True, timeout=2, check=True)
    except:
        python_cmd = "python"
    
    cmd = f'{python_cmd} "{script_path}" --mode {SYNC_MODE} --merge'
    
    # Essayer plusieurs fois en cas d'échec
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if attempt > 1:
                log_message(f"Tentative {attempt}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY)
            
            log_message(f"Exécution de la commande: {cmd}")
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600  # Timeout de 10 minutes
            )
            log_message(f"Code de retour: {result.returncode}")
            
            if result.returncode == 0:
                log_message("✅ Synchronisation réussie")
                # Afficher un résumé de la sortie
                if result.stdout:
                    # Chercher les lignes importantes
                    important_lines = [l for l in result.stdout.split('\n') if any(keyword in l for keyword in ['[OK]', '[ERREUR]', 'Export', 'Import', 'Synchronisation'])]
                    if important_lines:
                        for line in important_lines[-5:]:  # Dernières 5 lignes importantes
                            log_message(f"   {line[:150]}")
                return True
            else:
                # Analyser l'erreur
                error_msg = ""
                if result.stderr:
                    error_msg = result.stderr.lower()
                elif result.stdout:
                    error_msg = result.stdout.lower()
                
                # Si c'est une erreur de connexion, réessayer
                if any(keyword in error_msg for keyword in ['connection closed', 'timeout', 'connection refused']):
                    if attempt < MAX_RETRIES:
                        log_message(f"⚠️  Erreur de connexion détectée, nouvelle tentative dans {RETRY_DELAY}s...")
                        continue
                    else:
                        log_message(f"❌ Échec après {MAX_RETRIES} tentatives (erreur de connexion)")
                        # Afficher les erreurs importantes
                        if result.stdout:
                            error_lines = [l for l in result.stdout.split('\n') if '[ERREUR]' in l or 'Error' in l]
                            for line in error_lines[-3:]:
                                log_message(f"   {line[:150]}")
                        return False
                else:
                    # Autre type d'erreur
                    log_message(f"⚠️  Synchronisation terminée avec avertissements")
                    if result.stdout:
                        error_lines = [l for l in result.stdout.split('\n') if '[ERREUR]' in l or 'Error' in l]
                        if error_lines:
                            for line in error_lines[-3:]:
                                log_message(f"   {line[:150]}")
                    if result.stderr:
                        error_text = result.stderr.lower()
                        if "password" in error_text or "permission denied" in error_text:
                            log_message("   💡 Problème d'authentification SSH détecté")
                            log_message("   💡 Exécutez CONFIGURER_SSH_SANS_MOT_DE_PASSE.bat")
                    return False
                    
        except subprocess.TimeoutExpired:
            if attempt < MAX_RETRIES:
                log_message(f"⚠️  Timeout, nouvelle tentative dans {RETRY_DELAY}s...")
                continue
            else:
                log_message("❌ Synchronisation timeout après plusieurs tentatives")
                return False
        except Exception as e:
            log_message(f"❌ Erreur lors de la synchronisation: {e}")
            if attempt < MAX_RETRIES:
                log_message(f"   Nouvelle tentative dans {RETRY_DELAY}s...")
                continue
            else:
                import traceback
                log_message(f"   Traceback complet:")
                for line in traceback.format_exc().split('\n')[-5:]:  # Dernières 5 lignes
                    if line.strip():
                        log_message(f"   {line}")
                return False
    
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
