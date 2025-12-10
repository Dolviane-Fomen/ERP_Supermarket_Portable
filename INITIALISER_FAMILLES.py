#!/usr/bin/env python3
"""
Script d'initialisation des familles d'articles
S'exécute automatiquement au démarrage de l'ERP
"""

import sqlite3
import os
from pathlib import Path

def initialiser_familles():
    """Initialise les familles d'articles si elles n'existent pas"""
    
    try:
        # Chemin vers la base de données
        script_dir = Path(__file__).parent
        db_path = script_dir / "db_erp.sqlite3"
        
        if not db_path.exists():
            print("❌ Base de données non trouvée")
            return False
        
        # Connexion à la base
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='supermarket_famille';")
        if not cursor.fetchone():
            print("❌ Table famille non trouvée")
            conn.close()
            return False
        
        # Compter les familles existantes
        cursor.execute("SELECT COUNT(*) FROM supermarket_famille;")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"✅ {count} familles déjà présentes")
            conn.close()
            return True
        
        # Ajouter les familles si aucune n'existe
        print("➕ Ajout des familles d'articles...")
        
        familles = [
            ('ALIM', 'Alimentation', 'Unité', 1),
            ('BOIS', 'Boissons', 'Bouteille', 1),
            ('HYG', 'Hygiène', 'Unité', 1),
            ('ENTR', 'Entretien', 'Unité', 1),
            ('CONF', 'Confiserie', 'Unité', 1),
            ('LAIT', 'Produits Laitiers', 'Unité', 1),
            ('VIAN', 'Viandes', 'Kg', 1),
            ('LEG', 'Légumes', 'Kg', 1),
            ('FRUIT', 'Fruits', 'Kg', 1),
            ('AUTRE', 'Autres', 'Unité', 1)
        ]
        
        for code, intitule, unite, suivi in familles:
            try:
                cursor.execute("""
                    INSERT INTO supermarket_famille (code, intitule, unite_vente, suivi_stock)
                    VALUES (?, ?, ?, ?)
                """, (code, intitule, unite, suivi))
                print(f"   ✅ {intitule} ({code})")
            except Exception as e:
                print(f"   ❌ Erreur {intitule}: {e}")
        
        # Valider les changements
        conn.commit()
        
        # Vérifier le résultat
        cursor.execute("SELECT COUNT(*) FROM supermarket_famille;")
        count = cursor.fetchone()[0]
        print(f"✅ {count} familles ajoutées avec succès")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False

if __name__ == "__main__":
    initialiser_familles()





