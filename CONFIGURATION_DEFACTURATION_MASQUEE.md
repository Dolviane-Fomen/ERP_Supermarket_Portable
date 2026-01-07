# Configuration de la Défacturation Sans Retour de Stock

## 🔒 Fonctionnalité Masquée

La fonctionnalité de **défacturation sans retour de stock** est masquée par défaut dans le code source pour GitHub. Cette fonctionnalité permet de défacturer une vente sans remettre les produits en stock.

## 📋 Comment Activer Localement

Pour activer cette fonctionnalité sur votre machine locale (sans l'exposer sur GitHub) :

### Étape 1 : Créer le fichier `.env`

Créez un fichier `.env` à la racine du projet avec le contenu suivant :

```env
ENABLE_DEFACTURATION_SANS_RETOUR=True
```

**Important** : Le fichier `.env` est déjà dans `.gitignore`, donc il ne sera **PAS** versionné sur GitHub.

### Étape 2 : Vérifier que python-decouple est installé

La bibliothèque `python-decouple` est déjà dans `requirements.txt`. Si elle n'est pas installée :

```bash
pip install python-decouple
```

### Étape 3 : Redémarrer le serveur Django

Après avoir créé le fichier `.env`, redémarrez votre serveur Django :

```bash
py manage.py runserver
```

## ✅ Vérification

Une fois activée, la fonctionnalité sera disponible uniquement pour :
- L'utilisateur `admin1`
- Dans l'agence `MARCHE HUITIEME`

Le bouton "Défacturer (sans retour stock)" apparaîtra dans l'interface uniquement si ces conditions sont remplies.

## 🔐 Sécurité

- La fonctionnalité est **désactivée par défaut** dans le code source
- Elle nécessite une variable d'environnement pour être activée
- Le fichier `.env` n'est **jamais** versionné sur GitHub
- Même si quelqu'un télécharge le projet, la fonctionnalité restera masquée

## 📝 Fichiers Modifiés

Les fichiers suivants ont été modifiés pour supporter cette fonctionnalité masquée :

1. `erp_project/settings.py` - Ajout du setting `ENABLE_DEFACTURATION_SANS_RETOUR`
2. `supermarket/defacturation_views.py` - Vérification du setting avant d'exécuter
3. `supermarket/views.py` - Vérification du setting pour afficher le bouton
4. `supermarket/urls.py` - Route conditionnelle basée sur le setting

## ⚠️ Note Importante

Cette fonctionnalité est destinée à un usage spécifique et contrôlé. Assurez-vous de comprendre les implications avant de l'activer.

