#!/usr/bin/env python
"""
Script de vérification pour diagnostiquer les problèmes de modification d'articles
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    django.setup()
    from supermarket.models import Article, TypeVente, Agence, Famille
    from django.contrib.auth.models import User
except ImportError as e:
    print(f"ERREUR: Impossible d'importer Django: {e}")
    sys.exit(1)

def verifier_articles():
    """Vérifier les articles et leurs prix"""
    print("=" * 60)
    print("DIAGNOSTIC DES ARTICLES ET PRIX")
    print("=" * 60)
    
    # Vérifier le nombre d'articles
    total_articles = Article.objects.count()
    print(f"📊 Nombre total d'articles: {total_articles}")
    
    if total_articles == 0:
        print("❌ Aucun article trouvé dans la base de données!")
        return
    
    # Vérifier les 5 premiers articles
    print("\n🔍 DÉTAILS DES 5 PREMIERS ARTICLES:")
    print("-" * 50)
    
    articles = Article.objects.all()[:5]
    for i, article in enumerate(articles, 1):
        print(f"\n📦 Article {i}: {article.designation}")
        print(f"   ID: {article.id}")
        print(f"   Prix achat: {article.prix_achat} (type: {type(article.prix_achat)})")
        print(f"   Prix vente: {article.prix_vente} (type: {type(article.prix_vente)})")
        print(f"   Agence: {article.agence.nom_agence if article.agence else 'Aucune'}")
        print(f"   Famille: {article.categorie.intitule if article.categorie else 'Aucune'}")
        
        # Vérifier les types de vente
        types_vente = TypeVente.objects.filter(article=article)
        print(f"   Types de vente ({types_vente.count()}):")
        for tv in types_vente:
            print(f"     - {tv.intitule}: {tv.prix} (type: {type(tv.prix)})")

def verifier_types_vente():
    """Vérifier les types de vente"""
    print("\n" + "=" * 60)
    print("DIAGNOSTIC DES TYPES DE VENTE")
    print("=" * 60)
    
    total_types = TypeVente.objects.count()
    print(f"📊 Nombre total de types de vente: {total_types}")
    
    if total_types == 0:
        print("❌ Aucun type de vente trouvé!")
        return
    
    # Grouper par intitulé
    print("\n📋 RÉPARTITION PAR TYPE:")
    print("-" * 30)
    
    types_count = {}
    for tv in TypeVente.objects.all():
        intitule = tv.intitule
        if intitule not in types_count:
            types_count[intitule] = 0
        types_count[intitule] += 1
    
    for intitule, count in types_count.items():
        print(f"   {intitule}: {count} entrées")

def tester_vue_modification():
    """Tester la logique de la vue de modification"""
    print("\n" + "=" * 60)
    print("TEST DE LA VUE DE MODIFICATION")
    print("=" * 60)
    
    # Prendre le premier article
    try:
        article = Article.objects.first()
        if not article:
            print("❌ Aucun article pour tester")
            return
        
        print(f"🧪 Test avec l'article: {article.designation} (ID: {article.id})")
        
        # Simuler la logique de la vue
        agences = Agence.objects.all()
        familles = Famille.objects.all()
        types_vente = TypeVente.objects.filter(article=article)
        
        print(f"   Agences disponibles: {agences.count()}")
        print(f"   Familles disponibles: {familles.count()}")
        print(f"   Types de vente pour cet article: {types_vente.count()}")
        
        # Créer le dictionnaire comme dans la vue
        types_vente_dict = {}
        for tv in types_vente:
            if tv.intitule == 'Demi-Gros':
                types_vente_dict['Demi_Gros'] = tv.prix
            elif tv.intitule == 'Détail':
                types_vente_dict['Détail'] = tv.prix
            else:
                types_vente_dict[tv.intitule] = tv.prix
        
        print(f"\n📋 Dictionnaire types_vente généré:")
        for key, value in types_vente_dict.items():
            print(f"   {key}: {value} (type: {type(value)})")
        
        # Tester le formatage
        print(f"\n🔧 Test de formatage:")
        print(f"   Prix achat formaté: {article.prix_achat}")
        print(f"   Prix vente formaté: {article.prix_vente}")
        
        for key, value in types_vente_dict.items():
            print(f"   {key} formaté: {value}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def verifier_base_donnees():
    """Vérifier l'état de la base de données"""
    print("\n" + "=" * 60)
    print("VÉRIFICATION DE LA BASE DE DONNÉES")
    print("=" * 60)
    
    # Vérifier les tables
    tables = [
        ('Article', Article),
        ('TypeVente', TypeVente),
        ('Agence', Agence),
        ('Famille', Famille),
    ]
    
    for table_name, model in tables:
        count = model.objects.count()
        print(f"📊 {table_name}: {count} entrées")
    
    # Vérifier les relations
    print(f"\n🔗 VÉRIFICATION DES RELATIONS:")
    articles_avec_agence = Article.objects.filter(agence__isnull=False).count()
    articles_avec_famille = Article.objects.filter(categorie__isnull=False).count()
    articles_avec_types = Article.objects.filter(types_vente__isnull=False).distinct().count()
    
    print(f"   Articles avec agence: {articles_avec_agence}")
    print(f"   Articles avec famille: {articles_avec_famille}")
    print(f"   Articles avec types de vente: {articles_avec_types}")

def main():
    """Fonction principale"""
    print("🔍 SCRIPT DE VÉRIFICATION - MODIFICATION D'ARTICLES")
    print("=" * 60)
    
    try:
        verifier_base_donnees()
        verifier_articles()
        verifier_types_vente()
        tester_vue_modification()
        
        print("\n" + "=" * 60)
        print("✅ DIAGNOSTIC TERMINÉ")
        print("=" * 60)
        print("\n💡 RECOMMANDATIONS:")
        print("1. Vérifiez que les articles ont des prix d'achat et de vente")
        print("2. Vérifiez que les types de vente sont correctement liés")
        print("3. Rechargez la page de modification dans le navigateur")
        print("4. Videz le cache du navigateur (Ctrl+F5)")
        
    except Exception as e:
        print(f"❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

