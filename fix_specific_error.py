#!/usr/bin/env python
"""
Script pour corriger l'erreur spécifique à la ligne 325
"""

def fix_specific_error():
    print("=== CORRECTION ERREUR LIGNE 325 ===")
    
    # Lire le fichier
    with open('supermarket/views.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Corriger la ligne 325 (index 324)
    if len(lines) > 324:
        line = lines[324]
        if 'session_data:' in line:
            lines[324] = line.replace('session_data:', 'session_data)')
            print("✅ Ligne 325 corrigée: session_data: -> session_data)")
        else:
            print("❌ Ligne 325 ne contient pas session_data:")
    
    # Sauvegarder
    with open('supermarket/views.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Fichier sauvegardé")

if __name__ == "__main__":
    fix_specific_error()
