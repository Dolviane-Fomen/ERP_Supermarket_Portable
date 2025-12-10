#!/usr/bin/env python3
"""
Vérification finale de la longueur de facture après toutes les modifications
"""

def calculer_longueur():
    """Calcule la longueur finale de la facture"""
    
    print("=" * 70)
    print("   VÉRIFICATION LONGUEUR FINALE DE LA FACTURE")
    print("=" * 70)
    print()
    
    # Conversion px vers mm (96 DPI standard)
    px_to_mm = 0.26
    
    # Valeurs ACTUELLES après toutes les modifications
    
    print("ESPACEMENTS (marges)")
    print("-" * 70)
    espacements = {
        'company-name margin': 0.8 * 2,
        'company-info margin-bottom': 0.8,
        'separator margin (×4)': 0.7 * 2 * 4,  # 4 séparateurs
        'info-line margin (×5)': 0.7 * 5,
        'article-item margin (×5)': 0.7 * 2 * 5,
        'totals margin': 0.5,
        'total-line margin (×4)': 0.7 * 4,
        'grand-total margin': 0.8 * 2,
        'footer margin-top': 0.8,
        'footer-line margin (×2)': 0.7 * 2,
    }
    
    # Convertir mm en px pour calcul
    total_margin_mm = sum(espacements.values())
    print(f"Total espacements : {total_margin_mm:.1f} mm")
    print()
    
    print("HAUTEURS DE TEXTE (polices x line-height 1.2)")
    print("-" * 70)
    
    # line-height variable selon les éléments
    textes = {
        'company-name (16px × 1.1)': 16 * 1.1 * px_to_mm,
        'company-info (11px × 1.2 × 4 lignes)': 11 * 1.2 * 4 * px_to_mm,
        'separateur (7px × 4)': 7 * 0.9 * 4 * px_to_mm,
        'info lignes (12px × 5)': 12 * 1.1 * 5 * px_to_mm,
        'article-header (12px)': 12 * 1.1 * px_to_mm,
        'articles (11-12px × 5 articles × 1 ligne)': 12 * 1.1 * 5 * px_to_mm,
        'total lignes (13px × 4)': 13 * 1.1 * 4 * px_to_mm,
        'grand-total (16px)': 16 * 1.1 * px_to_mm,
        'footer (12px × 2)': 12 * 1.1 * 2 * px_to_mm,
    }
    
    total_texte_mm = sum(textes.values())
    print(f"Total hauteur textes : {total_texte_mm:.1f} mm")
    print()
    
    print("PADDINGS")
    print("-" * 70)
    paddings = {
        'body padding vertical': 0,  # Pas de padding vertical
        'sections padding': 0,  # Minimal
    }
    
    total_padding_mm = sum(paddings.values())
    print(f"Total paddings : {total_padding_mm:.1f} mm")
    print()
    
    # TOTAL
    total_mm = total_margin_mm + total_texte_mm + total_padding_mm
    total_cm = total_mm / 10
    
    print("=" * 70)
    print("   LONGUEUR TOTALE")
    print("=" * 70)
    print()
    print(f"Espacements :  {total_margin_mm:6.1f} mm")
    print(f"Textes :       {total_texte_mm:6.1f} mm")
    print(f"Paddings :     {total_padding_mm:6.1f} mm")
    print("-" * 70)
    print(f"TOTAL :        {total_mm:6.1f} mm = {total_cm:.1f} cm")
    print()
    
    # Comparaison avec Sage
    sage_mm = 120
    diff_mm = total_mm - sage_mm
    diff_percent = (diff_mm / sage_mm) * 100
    
    print("=" * 70)
    print("   COMPARAISON AVEC SAGE")
    print("=" * 70)
    print()
    print(f"Sage (5 articles)  : {sage_mm} mm = {sage_mm/10} cm")
    print(f"Notre ticket       : {total_mm:.1f} mm = {total_cm:.1f} cm")
    print()
    
    if abs(diff_mm) <= 5:
        print(f"OK ! Difference : {abs(diff_mm):.1f} mm ({abs(diff_percent):.1f}%)")
        print("   Longueur identique a Sage !")
    elif diff_mm < 0:
        print(f"OK ! Plus court de {abs(diff_mm):.1f} mm ({abs(diff_percent):.1f}%)")
    else:
        print(f"ATTENTION ! Plus long de {diff_mm:.1f} mm ({diff_percent:.1f}%)")
        print()
        print("   RECOMMANDATION :")
        print(f"   -> Reduire les marges de {diff_mm:.1f} mm")
        print("   -> Ou reduire les polices de 1px")
    
    print()
    print("=" * 70)
    
    return total_mm

if __name__ == "__main__":
    print("\n")
    calculer_longueur()
    print("\n")
    input("Appuyez sur Entrée pour fermer...")

