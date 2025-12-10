#!/usr/bin/env python3
"""
Script de correction pour le problème des quantités décimales dans la facturation
Problème : 1.71 devient 31635 au lieu de 3163.5
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
django.setup()

from decimal import Decimal, InvalidOperation
import re

def normalize_decimal_string(value):
    """
    Normalise une chaîne de caractères pour la conversion en Decimal
    Gère les virgules françaises et les espaces
    """
    if value is None:
        return "0"
    
    # Convertir en chaîne si ce n'est pas déjà le cas
    value_str = str(value).strip()
    
    # Remplacer les virgules par des points (format français vers format international)
    value_str = value_str.replace(',', '.')
    
    # Supprimer les espaces et caractères non numériques sauf le point et le signe moins
    value_str = re.sub(r'[^\d.-]', '', value_str)
    
    # Gérer les cas où il n'y a que des caractères non numériques
    if not value_str or value_str in ['-', '.']:
        return "0"
    
    # S'assurer qu'il n'y a qu'un seul point décimal
    parts = value_str.split('.')
    if len(parts) > 2:
        # Garder seulement la première partie et la première décimale
        value_str = parts[0] + '.' + ''.join(parts[1:])
    
    return value_str

def safe_decimal_conversion(value, default=Decimal('0')):
    """
    Conversion sécurisée en Decimal avec gestion d'erreurs
    """
    try:
        normalized = normalize_decimal_string(value)
        return Decimal(normalized)
    except (InvalidOperation, ValueError, TypeError) as e:
        print(f"[WARNING] Erreur conversion Decimal: {value} -> {e}")
        return default

def fix_facturation_decimal_issue():
    """
    Fonction principale pour corriger le problème des décimales
    """
    print("🔧 CORRECTION DU PROBLÈME DES QUANTITÉS DÉCIMALES")
    print("=" * 60)
    
    # 1. Créer une fonction utilitaire pour les vues
    utility_code = '''
def normalize_decimal_input(value):
    """
    Normalise les entrées décimales pour éviter les erreurs de conversion
    Utilisé dans les vues de facturation
    """
    from decimal import Decimal, InvalidOperation
    import re
    
    if value is None:
        return Decimal('0')
    
    # Convertir en chaîne
    value_str = str(value).strip()
    
    # Remplacer les virgules par des points
    value_str = value_str.replace(',', '.')
    
    # Supprimer les caractères non numériques sauf point et moins
    value_str = re.sub(r'[^\d.-]', '', value_str)
    
    # Gérer les cas vides
    if not value_str or value_str in ['-', '.']:
        return Decimal('0')
    
    # S'assurer qu'il n'y a qu'un seul point
    parts = value_str.split('.')
    if len(parts) > 2:
        value_str = parts[0] + '.' + ''.join(parts[1:])
    
    try:
        return Decimal(value_str)
    except (InvalidOperation, ValueError):
        return Decimal('0')

def safe_quantity_conversion(quantity_value):
    """
    Conversion sécurisée des quantités avec gestion des décimales
    """
    return normalize_decimal_input(quantity_value)

def safe_price_conversion(price_value):
    """
    Conversion sécurisée des prix avec gestion des décimales
    """
    return normalize_decimal_input(price_value)
'''
    
    # 2. Code JavaScript corrigé pour les templates
    js_fix_code = '''
// FONCTIONS CORRIGÉES POUR LA GESTION DES DÉCIMALES

function normalizeDecimalInput(value) {
    if (value === null || value === undefined || value === '') {
        return 0;
    }
    
    // Convertir en chaîne
    let valueStr = String(value).trim();
    
    // Remplacer les virgules par des points (format français vers international)
    valueStr = valueStr.replace(',', '.');
    
    // Supprimer les espaces et caractères non numériques sauf point et moins
    valueStr = valueStr.replace(/[^\d.-]/g, '');
    
    // Gérer les cas vides
    if (!valueStr || valueStr === '-' || valueStr === '.') {
        return 0;
    }
    
    // S'assurer qu'il n'y a qu'un seul point décimal
    const parts = valueStr.split('.');
    if (parts.length > 2) {
        valueStr = parts[0] + '.' + parts.slice(1).join('');
    }
    
    const result = parseFloat(valueStr);
    return isNaN(result) ? 0 : result;
}

function safeParseFloat(value) {
    return normalizeDecimalInput(value);
}

function safeParseInt(value) {
    return Math.floor(normalizeDecimalInput(value));
}

// CORRECTION DES FONCTIONS EXISTANTES

function updateQuantity(index, newQuantity) {
    // Utiliser la fonction sécurisée
    const normalizedQuantity = normalizeDecimalInput(newQuantity);
    
    if (normalizedQuantity === 0 && newQuantity !== '0' && newQuantity !== '0.0') {
        alert('Veuillez saisir une quantité valide');
        const input = document.querySelector(`input[data-index="${index}"]`);
        if (input) {
            input.value = input.getAttribute('data-old-value') || '1';
        }
        return;
    }
    
    // Mise à jour immédiate de l'affichage
    updateDisplayRealtime(index, normalizedQuantity);
    
    // Envoyer la mise à jour au serveur
    updateQuantityOnServer(index, normalizedQuantity);
}

function updateDisplayRealtime(index, newQuantity) {
    const row = document.querySelector(`input[data-index="${index}"]`).closest('tr');
    if (!row) return;
    
    // Récupérer le prix unitaire
    const prixUnitaireCell = row.cells[3];
    const prixUnitaireText = prixUnitaireCell.textContent.replace(' FCFA', '').replace(/\s/g, '');
    const prixUnitaire = normalizeDecimalInput(prixUnitaireText);
    
    // Calculer le nouveau total
    const nouveauTotal = prixUnitaire * newQuantity;
    
    // Mettre à jour la cellule du prix total
    const prixTotalCell = row.cells[4];
    prixTotalCell.textContent = nouveauTotal.toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }) + ' FCFA';
    
    // Recalculer le total général
    updateTotalGeneral();
}

function updateTotalGeneral() {
    const rows = document.querySelectorAll('#articles-table tbody tr[data-article-id]');
    let totalGeneral = 0;
    
    rows.forEach(row => {
        const prixTotalCell = row.cells[4];
        const prixTotalText = prixTotalCell.textContent.replace(/[^\d.,]/g, '');
        const prixTotal = normalizeDecimalInput(prixTotalText);
        totalGeneral += prixTotal;
    });
    
    // Mettre à jour l'affichage du total général
    const totalElement = document.getElementById('total-general');
    if (totalElement) {
        totalElement.textContent = totalGeneral.toLocaleString('fr-FR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }) + ' FCFA';
    }
}

// CORRECTION DE LA FONCTION DE CALCUL DES PRIX
function updatePrixTotal(input) {
    const row = input.closest('tr');
    if (!row) return;
    
    const quantiteInput = row.querySelector('.quantity-input');
    const prixUnitaireCell = row.cells[3];
    
    // Utiliser les fonctions sécurisées
    const quantite = normalizeDecimalInput(quantiteInput.value);
    const prixUnitaireText = prixUnitaireCell.textContent.replace(' FCFA', '').replace(/\s/g, '');
    const prixUnitaire = normalizeDecimalInput(prixUnitaireText);
    
    // Calculer le total
    const prixTotal = quantite * prixUnitaire;
    
    // Mettre à jour l'affichage
    const prixTotalCell = row.cells[4];
    prixTotalCell.textContent = prixTotal.toLocaleString('fr-FR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }) + ' FCFA';
    
    // Recalculer le total général
    updateTotalGeneral();
}
'''
    
    # 3. Code Python corrigé pour les vues
    python_fix_code = '''
# CORRECTION DANS LA FONCTION enregistrer_facture

def normalize_decimal_input(value):
    """
    Normalise les entrées décimales pour éviter les erreurs de conversion
    """
    from decimal import Decimal, InvalidOperation
    import re
    
    if value is None:
        return Decimal('0')
    
    # Convertir en chaîne
    value_str = str(value).strip()
    
    # Remplacer les virgules par des points
    value_str = value_str.replace(',', '.')
    
    # Supprimer les caractères non numériques sauf point et moins
    value_str = re.sub(r'[^\d.-]', '', value_str)
    
    # Gérer les cas vides
    if not value_str or value_str in ['-', '.']:
        return Decimal('0')
    
    # S'assurer qu'il n'y a qu'un seul point
    parts = value_str.split('.')
    if len(parts) > 2:
        value_str = parts[0] + '.' + ''.join(parts[1:])
    
    try:
        return Decimal(value_str)
    except (InvalidOperation, ValueError):
        return Decimal('0')

# Dans la fonction enregistrer_facture, remplacer :
# quantite=ligne_temp['quantite']
# Par :
# quantite=normalize_decimal_input(ligne_temp['quantite'])

# Et remplacer :
# prix_unitaire=ligne_temp['prix_unitaire']
# Par :
# prix_unitaire=normalize_decimal_input(ligne_temp['prix_unitaire'])

# Et remplacer :
# prix_total=ligne_temp['prix_total']
# Par :
# prix_total=normalize_decimal_input(ligne_temp['prix_total'])
'''
    
    print("✅ Code de correction généré avec succès")
    print("\n📋 CORRECTIONS À APPLIQUER :")
    print("1. Ajouter les fonctions utilitaires dans views.py")
    print("2. Modifier les templates HTML pour utiliser les fonctions JavaScript corrigées")
    print("3. Mettre à jour la fonction enregistrer_facture")
    
    return {
        'utility_code': utility_code,
        'js_fix_code': js_fix_code,
        'python_fix_code': python_fix_code
    }

if __name__ == "__main__":
    fixes = fix_facturation_decimal_issue()
    
    print("\n🔧 APPLICATION DES CORRECTIONS...")
    
    # Sauvegarder les corrections dans des fichiers
    with open('decimal_fix_utility.py', 'w', encoding='utf-8') as f:
        f.write(fixes['utility_code'])
    
    with open('decimal_fix_javascript.js', 'w', encoding='utf-8') as f:
        f.write(fixes['js_fix_code'])
    
    with open('decimal_fix_python.py', 'w', encoding='utf-8') as f:
        f.write(fixes['python_fix_code'])
    
    print("✅ Fichiers de correction créés :")
    print("   - decimal_fix_utility.py")
    print("   - decimal_fix_javascript.js") 
    print("   - decimal_fix_python.py")
    
    print("\n🎯 PROCHAINES ÉTAPES :")
    print("1. Appliquer les corrections dans views.py")
    print("2. Mettre à jour les templates HTML")
    print("3. Tester avec des quantités décimales")
