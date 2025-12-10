"""
Système de gestion des permissions basé sur le type de compte
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Compte, Livreur

def get_user_compte(request):
    """Récupérer le compte utilisateur avec gestion des erreurs"""
    if not request.user.is_authenticated:
        return None
    
    try:
        compte = Compte.objects.get(user=request.user, actif=True)
        return compte
    except Compte.DoesNotExist:
        return None
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la récupération du compte: {e}")
        return None

def get_user_livreur(request):
    """Récupérer le livreur associé au compte utilisateur"""
    compte = get_user_compte(request)
    if not compte:
        return None
    try:
        livreur = Livreur.objects.get(compte=compte, actif=True)
        return livreur
    except Livreur.DoesNotExist:
        return None
    except Exception as e:
        print(f"[ERREUR] Erreur lors de la récupération du livreur: {e}")
        return None

# Matrice des permissions par module et fonctionnalité
PERMISSIONS = {
    # Module CAISSE - Caissier et admin
    'caisse': {
        'allowed_types': ['caissier', 'admin'],
        'name': 'Gestion de Caisse',
        'login_url': 'login_caisse'
    },
    
    # Module STOCK - Comptable et admin
    'stock': {
        'allowed_types': ['comptable', 'admin'],
        'name': 'Gestion de Stock',
        'login_url': 'login_stock'
    },
    
    # Module COMMANDES - Permissions granulaires
    'commandes': {
        'dashboard': {
            'allowed_types': ['admin', 'gerant', 'acm', 'responsable_logistique', 'caissier', 'livreur'],
            'name': 'Dashboard Commandes'
        },
        'gestion_commande': {
            'allowed_types': ['admin', 'gerant', 'acm', 'responsable_logistique'],
            'name': 'Gestion Commandes'
        },
        'consulter_livraison': {
            'allowed_types': ['admin', 'gerant', 'acm', 'livreur', 'caissier', 'responsable_logistique'],
            'name': 'Consulter Livraisons'
        },
        'suivi_client': {
            'allowed_types': ['admin', 'gerant', 'acm', 'responsable_logistique'],
            'name': 'Suivi Client'
        },
        'rapport_acm': {
            'allowed_types': ['admin', 'gerant', 'acm', 'responsable_logistique'],
            'name': 'Rapport ACM'
        },
        'gestion_client': {
            'allowed_types': ['admin', 'gerant', 'acm', 'responsable_logistique'],
            'name': 'Gestion Client'
        },
        'definir_etat_livraison': {
            'allowed_types': ['admin', 'gerant', 'livreur', 'responsable_logistique'],
            'name': 'Définir État Livraison'
        },
        'voir_itineraire': {
            'allowed_types': ['admin', 'gerant', 'livreur', 'responsable_logistique'],
            'name': 'Voir Itinéraire'
        },
        'rapport_livreur': {
            'allowed_types': ['admin', 'gerant', 'livreur', 'responsable_logistique'],
            'name': 'Rapport Livreur'
        },
        'facture_commande': {
            'allowed_types': ['admin', 'gerant', 'caissier', 'responsable_logistique'],
            'name': 'Facture Commande'
        },
        'consulter_commande': {
            'allowed_types': ['admin', 'gerant', 'acm', 'caissier', 'responsable_logistique'],
            'name': 'Consulter Commandes'
        },
        'statistique_client': {
            'allowed_types': ['admin', 'gerant', 'responsable_logistique'],
            'name': 'Statistique Client'
        },
        'menu_livraison': {
            'allowed_types': ['admin', 'gerant', 'responsable_logistique'],
            'name': 'Menu Livraison'
        },
        'login_url': 'login_commandes'
    },
    
    # Module COMPTES - Admin uniquement
    'comptes': {
        'allowed_types': ['admin'],
        'name': 'Gestion des Comptes',
        'login_url': 'login_comptes'
    },
}

def require_compte_type(allowed_types, feature_name=None, login_url=None):
    """
    Décorateur pour vérifier que l'utilisateur a le bon type de compte
    
    Args:
        allowed_types: Liste des types de compte autorisés
        feature_name: Nom de la fonctionnalité pour les messages d'erreur
        login_url: URL de login pour rediriger si non autorisé
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if login_url:
                    return redirect(login_url)
                return redirect('index')
            
            compte = get_user_compte(request)
            if not compte:
                messages.error(request, 'Votre compte n\'est pas configuré correctement ou est inactif.')
                if login_url:
                    return redirect(login_url)
                return redirect('index')
            
            if compte.type_compte not in allowed_types:
                feature_display = feature_name or 'cette fonctionnalité'
                type_display = compte.get_type_compte_display()
                allowed_display = ', '.join([
                    dict(Compte._meta.get_field('type_compte').choices).get(t, t.replace('_', ' ').title())
                    for t in allowed_types
                ])
                messages.error(
                    request, 
                    f'Accès refusé à {feature_display}. '
                    f'Votre type de compte ({type_display}) n\'a pas les permissions nécessaires. '
                    f'Types autorisés : {allowed_display}'
                )
                if login_url:
                    return redirect(login_url)
                return redirect('index')
            
            request.compte = compte
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_module_access(module_key):
    """Décorateur pour vérifier l'accès à un module complet"""
    if module_key not in PERMISSIONS:
        raise ValueError(f"Module '{module_key}' non trouvé dans PERMISSIONS")
    
    module_info = PERMISSIONS[module_key]
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                login_url = module_info.get('login_url', 'index')
                return redirect(login_url)
            
            compte = get_user_compte(request)
            if not compte:
                messages.error(request, 'Votre compte n\'est pas configuré correctement ou est inactif.')
                login_url = module_info.get('login_url', 'index')
                return redirect(login_url)
            
            allowed_types = module_info.get('allowed_types', [])
            if compte.type_compte not in allowed_types:
                type_display = compte.get_type_compte_display()
                allowed_display = ', '.join([
                    dict(Compte._meta.get_field('type_compte').choices).get(t, t.replace('_', ' ').title())
                    for t in allowed_types
                ])
                messages.error(
                    request, 
                    f'Accès refusé au module {module_info["name"]}. '
                    f'Votre type de compte ({type_display}) n\'a pas les permissions nécessaires. '
                    f'Types autorisés : {allowed_display}'
                )
                login_url = module_info.get('login_url', 'index')
                return redirect(login_url)
            
            request.compte = compte
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_commandes_feature(feature_key):
    """Décorateur pour vérifier l'accès à une fonctionnalité spécifique du module Commandes"""
    if 'commandes' not in PERMISSIONS:
        raise ValueError("Module 'commandes' non trouvé dans PERMISSIONS")
    
    commandes_perms = PERMISSIONS['commandes']
    if feature_key not in commandes_perms:
        raise ValueError(f"Fonctionnalité '{feature_key}' non trouvée dans PERMISSIONS['commandes']")
    
    feature_info = commandes_perms[feature_key]
    login_url = commandes_perms.get('login_url', 'index')
    
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(login_url)
            
            compte = get_user_compte(request)
            if not compte:
                messages.error(request, 'Votre compte n\'est pas configuré correctement ou est inactif.')
                return redirect(login_url)
            
            allowed_types = feature_info.get('allowed_types', [])
            if compte.type_compte not in allowed_types:
                type_display = compte.get_type_compte_display()
                allowed_display = ', '.join([
                    dict(Compte._meta.get_field('type_compte').choices).get(t, t.replace('_', ' ').title())
                    for t in allowed_types
                ])
                messages.error(
                    request, 
                    f'Accès refusé à {feature_info["name"]}. '
                    f'Votre type de compte ({type_display}) n\'a pas les permissions nécessaires. '
                    f'Types autorisés : {allowed_display}'
                )
                return redirect(login_url)
            
            request.compte = compte
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Décorateurs spécifiques par module
def require_caisse_access(view_func):
    """Décorateur pour l'accès au module Caisse (caissier uniquement)"""
    return require_module_access('caisse')(view_func)

def require_stock_access(view_func):
    """Décorateur pour l'accès au module Stock (comptable uniquement)"""
    return require_module_access('stock')(view_func)

def require_comptes_access(view_func):
    """Décorateur pour l'accès au module Comptes"""
    return require_module_access('comptes')(view_func)

def require_admin_access(view_func):
    """Décorateur pour les actions administratives (admin et gérant uniquement)"""
    return require_compte_type(['admin', 'gerant'], 'cette fonctionnalité administrative')(view_func)
