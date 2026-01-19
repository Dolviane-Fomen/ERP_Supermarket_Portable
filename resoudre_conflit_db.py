#!/usr/bin/env python
"""
Script pour résoudre le conflit Git sur db_erp.sqlite3
Ce fichier ne devrait pas être versionné car c'est une base de données locale
"""

import os
import subprocess
import sys

def resoudre_conflit_db():
    """Résoudre le conflit sur db_erp.sqlite3 en le retirant du suivi Git"""
    
    print("=" * 80)
    print("RESOLUTION DU CONFLIT GIT - db_erp.sqlite3")
    print("=" * 80)
    
    fichier_db = "db_erp.sqlite3"
    
    # Vérifier si le fichier existe
    if os.path.exists(fichier_db):
        print(f"\n[INFO] Le fichier {fichier_db} existe localement")
        taille = os.path.getsize(fichier_db) / (1024 * 1024)  # Taille en MB
        print(f"       Taille: {taille:.2f} MB")
    else:
        print(f"\n[INFO] Le fichier {fichier_db} n'existe pas localement")
    
    print("\n" + "=" * 80)
    print("SOLUTION RECOMMANDEE:")
    print("=" * 80)
    print("\nLe fichier db_erp.sqlite3 est une base de donnees locale qui ne devrait")
    print("PAS etre versionnee dans Git. Il est deja dans .gitignore mais etait")
    print("probablement suivi avant d'etre ajoute au .gitignore.")
    print("\nETAPES POUR RESOUDRE LE CONFLIT:")
    print("\n1. Dans GitHub Desktop:")
    print("   - Cliquez sur 'Abort merge' pour annuler le merge en cours")
    print("   - OU choisissez 'Resolve' puis 'Use ours' ou 'Use theirs'")
    print("   - Puis cliquez sur 'Continue merge'")
    print("\n2. Ensuite, retirez le fichier du suivi Git avec cette commande:")
    print(f"   git rm --cached {fichier_db}")
    print("\n3. Commitez cette suppression:")
    print("   git commit -m \"Remove db_erp.sqlite3 from version control\"")
    print("\n4. Poussez les changements:")
    print("   git push")
    print("\n" + "=" * 80)
    print("COMMANDES A EXECUTER (si Git est disponible):")
    print("=" * 80)
    print("\n# Annuler le merge en cours")
    print("git merge --abort")
    print("\n# OU resoudre le conflit en retirant le fichier")
    print(f"git rm --cached {fichier_db}")
    print("git commit -m \"Remove db_erp.sqlite3 from version control\"")
    print("\n" + "=" * 80)
    
    # Essayer d'exécuter les commandes si Git est disponible
    try:
        print("\nTentative d'execution des commandes Git...")
        
        # Vérifier si on est en cours de merge
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("[OK] Git est disponible")
            
            # Vérifier l'état
            status_result = subprocess.run(
                ["git", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "merge" in status_result.stdout.lower() or "conflit" in status_result.stdout.lower():
                print("\n[INFO] Un merge est en cours")
                print("\nVoulez-vous:")
                print("1. Annuler le merge (git merge --abort)")
                print("2. Retirer le fichier du suivi Git (git rm --cached)")
                print("\nPour executer manuellement, utilisez les commandes ci-dessus.")
            else:
                # Essayer de retirer le fichier du suivi
                print(f"\nRetrait de {fichier_db} du suivi Git...")
                rm_result = subprocess.run(
                    ["git", "rm", "--cached", fichier_db],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if rm_result.returncode == 0:
                    print(f"[OK] {fichier_db} retire du suivi Git")
                    print("\nVous devez maintenant commiter ce changement:")
                    print("git commit -m \"Remove db_erp.sqlite3 from version control\"")
                else:
                    print(f"[INFO] {rm_result.stderr}")
        else:
            print("[INFO] Git n'est pas disponible en ligne de commande")
            print("       Utilisez GitHub Desktop pour resoudre le conflit")
            
    except FileNotFoundError:
        print("\n[INFO] Git n'est pas installe ou n'est pas dans le PATH")
        print("       Utilisez GitHub Desktop pour resoudre le conflit manuellement")
    except Exception as e:
        print(f"\n[INFO] Erreur: {e}")
        print("       Utilisez GitHub Desktop pour resoudre le conflit manuellement")

if __name__ == '__main__':
    resoudre_conflit_db()
