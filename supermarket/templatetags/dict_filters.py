from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Filtre pour accéder à un élément d'un dictionnaire par sa clé"""
    if dictionary is None:
        return None
    return dictionary.get(key)


