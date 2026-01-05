"""
Script pour vérifier le contenu des fichiers d'export
"""
import json
import sys
import os

def verifier_export(fichier):
    """Vérifier le contenu d'un fichier d'export"""
    if not os.path.exists(fichier):
        print(f"❌ Fichier {fichier} introuvable!")
        return
    
    print(f"\n{'='*60}")
    print(f"Vérification de: {fichier}")
    print(f"{'='*60}\n")
    
    try:
        # Essayer différents encodages
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        data = None
        
        for encoding in encodings:
            try:
                with open(fichier, 'r', encoding=encoding) as f:
                    data = json.load(f)
                print(f"✅ Encodage détecté: {encoding}")
                break
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
        
        if data is None:
            print("❌ Impossible de décoder le fichier avec les encodages testés")
            return
        
        # Compter par modèle
        models = {}
        for item in data:
            model = item.get('model', 'unknown')
            if model not in models:
                models[model] = []
            models[model].append(item)
        
        # Afficher les résultats
        print("📊 MODÈLES EXPORTÉS:\n")
        
        # Trier par nom de modèle
        for model in sorted(models.keys()):
            count = len(models[model])
            if 'supermarket' in model:
                print(f"  ✅ {model}: {count} objets")
            else:
                print(f"  ⚠️  {model}: {count} objets")
        
        print(f"\n{'='*60}")
        print(f"TOTAL: {len(data)} objets exportés")
        print(f"{'='*60}\n")
        
        # Vérifier spécifiquement les agences et factures
        print("🔍 VÉRIFICATION SPÉCIALE:\n")
        
        agences = [item for item in data if 'agence' in item.get('model', '').lower()]
        factures = [item for item in data if 'facture' in item.get('model', '').lower()]
        
        print(f"  Agences: {len(agences)}")
        if agences:
            print(f"    Modèles: {set(item['model'] for item in agences)}")
        
        print(f"  Factures: {len(factures)}")
        if factures:
            print(f"    Modèles: {set(item['model'] for item in factures)}")
        
        print()
        
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    # Vérifier les fichiers d'export
    fichiers = [
        'export_data.json', 
        'export_data_complet.json', 
        'export_agences_factures.json',
        'export_data_utf8.json'
    ]
    
    for fichier in fichiers:
        if os.path.exists(fichier):
            verifier_export(fichier)
            print()

