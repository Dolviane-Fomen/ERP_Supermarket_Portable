from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.contrib import messages
from .models import Article, Agence
from . import views

@login_required
def stock_alerte(request):
    """Vue pour consulter les articles en stock d'alerte"""
    agence = views.get_user_agence(request)
    if not agence:
        messages.error(request, 'Votre compte n\'est pas configuré correctement.')
        return redirect('logout_stock')
    
    # Récupérer les paramètres de recherche
    search_query = request.GET.get('search', '')
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    
    # Construire la requête de base pour les articles en alerte
    articles_alerte = Article.objects.filter(
        agence=agence,
        suivi_stock=True
    ).filter(
        Q(stock_actuel__lte=F('stock_minimum')) | Q(stock_actuel__lte=0)
    )
    
    # Appliquer les filtres
    if search_query:
        articles_alerte = articles_alerte.filter(
            Q(designation__icontains=search_query) |
            Q(reference_article__icontains=search_query)
        )
    
    # Filtrer par période si spécifiée
    if date_debut and date_fin:
        try:
            from datetime import datetime
            date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d').date()
            date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d').date()
            
            # Filtrer les articles qui ont eu des mouvements dans cette période
            articles_alerte = articles_alerte.filter(
                mouvementstock__date_mouvement__date__range=[date_debut_obj, date_fin_obj]
            ).distinct()
        except ValueError:
            pass
    
    # Trier par niveau d'alerte (stock le plus bas en premier)
    articles_alerte = articles_alerte.order_by('stock_actuel')
    
    # Calculer les statistiques
    total_alertes = articles_alerte.count()
    alertes_critiques = articles_alerte.filter(stock_actuel__lte=0).count()
    alertes_warning = articles_alerte.filter(
        stock_actuel__gt=0,
        stock_actuel__lte=F('stock_minimum')
    ).count()
    
    context = {
        'articles_alerte': articles_alerte,
        'agence': agence,
        'total_alertes': total_alertes,
        'alertes_critiques': alertes_critiques,
        'alertes_warning': alertes_warning,
        'date_debut': date_debut,
        'date_fin': date_fin,
    }
    return render(request, 'supermarket/stock/stock_alerte.html', context)

@login_required
def rupture_stock(request):
    """Vue pour consulter les articles en rupture de stock"""
    agence = views.get_user_agence(request)
    if not agence:
        messages.error(request, 'Votre compte n\'est pas configuré correctement.')
        return redirect('logout_stock')
    
    # Récupérer les paramètres de recherche
    search_query = request.GET.get('search', '')
    date_debut = request.GET.get('date_debut', '')
    date_fin = request.GET.get('date_fin', '')
    
    # Construire la requête de base pour les articles en rupture
    articles_rupture = Article.objects.filter(
        agence=agence,
        suivi_stock=True
    ).filter(
        Q(stock_actuel__lte=F('stock_minimum')) | Q(stock_actuel__lte=0)
    )
    
    # Appliquer les filtres
    if search_query:
        articles_rupture = articles_rupture.filter(
            Q(designation__icontains=search_query) |
            Q(reference_article__icontains=search_query)
        )
    
    # Filtrer par période si spécifiée
    if date_debut and date_fin:
        try:
            from datetime import datetime
            date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d').date()
            date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d').date()
            
            # Filtrer les articles qui ont eu des mouvements dans cette période
            articles_rupture = articles_rupture.filter(
                mouvementstock__date_mouvement__date__range=[date_debut_obj, date_fin_obj]
            ).distinct()
        except ValueError:
            pass
    
    # Trier par niveau de rupture (stock le plus bas en premier)
    articles_rupture = articles_rupture.order_by('stock_actuel')
    
    # Calculer les statistiques
    total_ruptures = articles_rupture.count()
    ruptures_critiques = articles_rupture.filter(stock_actuel__lte=0).count()
    ruptures_partielles = articles_rupture.filter(
        stock_actuel__gt=0,
        stock_actuel__lte=F('stock_minimum')
    ).count()
    
    context = {
        'articles_rupture': articles_rupture,
        'agence': agence,
        'total_ruptures': total_ruptures,
        'ruptures_critiques': ruptures_critiques,
        'ruptures_partielles': ruptures_partielles,
        'date_debut': date_debut,
        'date_fin': date_fin,
    }
    return render(request, 'supermarket/stock/rupture_stock.html', context)
