"""
Utilitaires pour le filtrage des données selon le type de compte et l'utilisateur
"""
from .models import Compte, Livreur, Commande, SuiviClientAction, Livraison
from django.db.models import Q

def filter_commandes_by_user(queryset, compte):
    """
    Filtrer les commandes selon le type de compte
    - ACM : seulement ses commandes (created_by)
    - Autres : toutes les commandes de l'agence
    """
    if compte.type_compte == 'acm':
        # ACM voit seulement ses propres commandes
        return queryset.filter(created_by=compte.user)
    else:
        # Admin, gérant, etc. voient toutes les commandes de l'agence
        return queryset

def filter_suivi_client_by_user(queryset, compte):
    """
    Filtrer les actions de suivi client selon le type de compte
    - ACM : seulement ses actions (created_by)
    - Autres : toutes les actions de l'agence
    """
    if compte.type_compte == 'acm':
        # ACM voit seulement ses propres actions
        return queryset.filter(created_by=compte.user)
    else:
        # Admin, gérant, etc. voient toutes les actions de l'agence
        return queryset

def filter_livraisons_by_user(queryset, compte):
    """
    Filtrer les livraisons selon le type de compte
    - Livreur : seulement ses livraisons (livreur.compte = compte)
    - Autres : toutes les livraisons de l'agence
    """
    if compte.type_compte == 'livreur':
        # Récupérer le livreur associé au compte
        livreur = get_user_livreur(compte)
        if livreur:
            # Livreur voit seulement ses propres livraisons
            return queryset.filter(livreur=livreur)
        else:
            # Si pas de livreur associé, retourner queryset vide
            return queryset.none()
    else:
        # Admin, gérant, etc. voient toutes les livraisons de l'agence
        return queryset

def get_user_livreur(compte):
    """Récupérer le livreur associé à un compte"""
    try:
        return Livreur.objects.get(compte=compte, actif=True)
    except Livreur.DoesNotExist:
        return None

def can_access_feature(compte, feature_key):
    """
    Vérifier si un compte peut accéder à une fonctionnalité
    Retourne (bool, message_erreur)
    """
    from .decorators import PERMISSIONS
    
    if feature_key.startswith('commandes.'):
        # Fonctionnalité du module commandes
        feature = feature_key.split('.', 1)[1]
        commandes_perms = PERMISSIONS.get('commandes', {})
        if feature in commandes_perms:
            feature_info = commandes_perms[feature]
            allowed_types = feature_info.get('allowed_types', [])
            if compte.type_compte in allowed_types:
                return True, None
            else:
                type_display = compte.get_type_compte_display()
                allowed_display = ', '.join([
                    dict(Compte._meta.get_field('type_compte').choices).get(t, t.replace('_', ' ').title())
                    for t in allowed_types
                ])
                return False, f'Votre type de compte ({type_display}) n\'a pas accès à cette fonctionnalité. Types autorisés : {allowed_display}'
    
    # Module complet
    module_info = PERMISSIONS.get(feature_key)
    if module_info:
        allowed_types = module_info.get('allowed_types', [])
        if compte.type_compte in allowed_types:
            return True, None
        else:
            type_display = compte.get_type_compte_display()
            allowed_display = ', '.join([
                dict(Compte._meta.get_field('type_compte').choices).get(t, t.replace('_', ' ').title())
                for t in allowed_types
            ])
            return False, f'Votre type de compte ({type_display}) n\'a pas accès à ce module. Types autorisés : {allowed_display}'
    
    return False, 'Fonctionnalité non trouvée'

