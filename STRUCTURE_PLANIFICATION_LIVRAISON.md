# Structure Complète - Système de Planification des Livraisons

## 1. MODÈLES (models.py)

### 1.1 Modèle Livreur (NOUVEAU)
```python
class Livreur(models.Model):
    nom = CharField(max_length=100)
    prenom = CharField(max_length=100)
    telephone = CharField(max_length=20)
    email = EmailField(blank=True, null=True)
    agence = ForeignKey(Agence)
    actif = BooleanField(default=True)
    date_creation = DateTimeField(auto_now_add=True)
    date_modification = DateTimeField(auto_now=True)
```

### 1.2 Modèle Livraison (MODIFIÉ)
```python
class Livraison(models.Model):
    ETAT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_preparation', 'En préparation'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
        ('reportee', 'Reportée'),
        ('annulee', 'Annulée'),
    ]
    
    commande = OneToOneField(Commande)
    livreur = ForeignKey(Livreur, null=True, blank=True)  # NOUVEAU
    date_livraison = DateField()
    heure_livraison = TimeField()
    zone = CharField(max_length=100, blank=True, null=True)  # NOUVEAU
    etat_livraison = CharField(choices=ETAT_CHOICES, default='planifiee')
    notes = TextField(blank=True, null=True)  # NOUVEAU
    ordre_livraison = PositiveIntegerField(default=0)  # NOUVEAU (pour itinéraire)
    date_creation = DateTimeField(auto_now_add=True)
    date_modification = DateTimeField(auto_now=True)
```

---

## 2. VUES (views.py)

### 2.1 Vue principale : planification_livraison
**URL**: `/commandes/planification-livraison/`
**Fonctionnalités**:
- Afficher les commandes à planifier (état: 'en_attente' ou 'validee')
- Filtrer par date de livraison souhaitée
- Filtrer par zone (récupérée depuis client.zone)
- Vérifier le stock disponible pour chaque article de commande
- Afficher un indicateur visuel si stock insuffisant
- Permettre la sélection multiple de commandes
- Afficher les livreurs disponibles

**Paramètres GET**:
- `date_livraison`: Date de livraison souhaitée
- `zone`: Zone géographique
- `livreur_id`: Filtrer par livreur

**Contexte**:
- `commandes_a_planifier`: Liste des commandes groupées (client, date, heure)
- `livreurs`: Liste des livreurs actifs de l'agence
- `zones_disponibles`: Liste des zones uniques des clients
- `date_livraison`: Date sélectionnée
- `zone_selectionnee`: Zone sélectionnée
- `verifications_stock`: Dict {commande_id: {'suffisant': bool, 'articles_manquants': []}}

### 2.2 Vue : creer_planification_livraison
**URL**: `/commandes/creer-planification-livraison/`
**Méthode**: POST
**Fonctionnalités**:
- Créer des objets Livraison pour les commandes sélectionnées
- Assigner un livreur
- Définir la date et heure de livraison
- Définir la zone
- Définir l'ordre de livraison (pour itinéraire)
- Vérifier le stock AVANT de créer la livraison
- Si stock insuffisant : message d'erreur, ne pas créer
- Mettre à jour l'état de la commande à 'en_livraison'

**Données POST**:
- `commandes_ids[]`: Liste des IDs de commandes (première commande de chaque groupe)
- `livreur_id`: ID du livreur
- `date_livraison`: Date de livraison
- `heure_livraison`: Heure de livraison
- `zone`: Zone de livraison
- `ordre_livraison_{commande_id}`: Ordre pour chaque commande
- `notes_{commande_id}`: Notes optionnelles

**Logique de vérification stock**:
```python
Pour chaque commande:
    Pour chaque ligne de commande (même client, date, heure):
        Vérifier stock disponible de l'article
        Si stock < quantite_requise:
            Ajouter à articles_manquants
    Si articles_manquants:
        Ne pas créer la livraison
        Retourner erreur avec détails
```

### 2.3 Vue : verifier_stock_livraison (AJAX)
**URL**: `/commandes/verifier-stock-livraison/`
**Méthode**: POST (AJAX)
**Fonctionnalités**:
- Vérifier le stock en temps réel avant planification
- Retourner JSON avec statut pour chaque article

**Réponse JSON**:
```json
{
    "commande_id": {
        "suffisant": true/false,
        "articles_manquants": [
            {
                "article_id": 1,
                "designation": "Article X",
                "stock_disponible": 10,
                "quantite_requise": 15,
                "manque": 5
            }
        ]
    }
}
```

### 2.4 Vue : reporter_livraison
**URL**: `/commandes/reporter-livraison/<int:livraison_id>/`
**Méthode**: POST
**Fonctionnalités**:
- Reporter une livraison planifiée à une nouvelle date
- Mettre à jour date_livraison et heure_livraison
- Changer l'état à 'planifiee' si nécessaire
- Enregistrer la raison du report dans notes

**Données POST**:
- `nouvelle_date`: Nouvelle date de livraison
- `nouvelle_heure`: Nouvelle heure de livraison
- `raison_report`: Raison du report (optionnel)

### 2.5 Vue : annuler_livraison
**URL**: `/commandes/annuler-livraison/<int:livraison_id>/`
**Méthode**: POST
**Fonctionnalités**:
- Annuler une livraison planifiée
- Changer l'état à 'annulee'
- Remettre l'état de la commande à 'validee' ou 'en_attente'
- Enregistrer la raison dans notes

**Données POST**:
- `raison_annulation`: Raison de l'annulation

### 2.6 Vue : modifier_ordre_livraison (AJAX)
**URL**: `/commandes/modifier-ordre-livraison/`
**Méthode**: POST (AJAX)
**Fonctionnalités**:
- Modifier l'ordre de livraison (itinéraire manuel)
- Permettre de réorganiser les livraisons d'un livreur pour une date

**Données POST**:
- `livraisons_ordre[]`: Liste des IDs de livraisons dans le nouvel ordre

---

## 3. TEMPLATES

### 3.1 planification_livraison.html
**Chemin**: `supermarket/templates/supermarket/commandes/planification_livraison.html`

**Structure**:
- Header avec titre "Planification des Livraisons"
- Section filtres:
  - Date de livraison (date picker)
  - Zone (select avec zones disponibles)
  - Livreur (select avec livreurs actifs)
  - Bouton "Rechercher"
- Section liste des commandes:
  - Tableau avec colonnes:
    - Checkbox (sélection)
    - Client (nom, zone, téléphone)
    - Date commande
    - Articles (liste avec quantités)
    - Stock disponible (indicateur visuel)
    - Actions (voir détails)
  - Indicateur visuel pour stock insuffisant (badge rouge)
  - Indicateur visuel pour stock suffisant (badge vert)
- Section actions en bas:
  - Bouton "Vérifier Stock" (AJAX)
  - Bouton "Planifier les Livraisons Sélectionnées"
  - Formulaire modal pour planification:
    - Sélection livreur
    - Date et heure de livraison
    - Zone (pré-rempli depuis client)
    - Ordre de livraison (drag & drop ou input numérique)
    - Notes (textarea)

**Fonctionnalités JavaScript**:
- Vérification stock en temps réel
- Sélection multiple de commandes
- Modal pour planification
- Drag & drop pour ordre de livraison (optionnel)
- Validation avant soumission

### 3.2 liste_livraisons_planifiees.html (optionnel)
**Chemin**: `supermarket/templates/supermarket/commandes/liste_livraisons_planifiees.html`

**Structure**:
- Liste des livraisons planifiées
- Filtres par date, livreur, zone, état
- Tableau avec:
  - Date livraison
  - Heure livraison
  - Client
  - Zone
  - Livreur
  - Ordre
  - État
  - Actions (Reporter, Annuler, Modifier ordre)

---

## 4. URLs (urls.py)

```python
# Planification des livraisons
path('commandes/planification-livraison/', views.planification_livraison, name='planification_livraison'),
path('commandes/creer-planification-livraison/', views.creer_planification_livraison, name='creer_planification_livraison'),
path('commandes/verifier-stock-livraison/', views.verifier_stock_livraison, name='verifier_stock_livraison'),
path('commandes/reporter-livraison/<int:livraison_id>/', views.reporter_livraison, name='reporter_livraison'),
path('commandes/annuler-livraison/<int:livraison_id>/', views.annuler_livraison, name='annuler_livraison'),
path('commandes/modifier-ordre-livraison/', views.modifier_ordre_livraison, name='modifier_ordre_livraison'),
```

---

## 5. LOGIQUE DE VÉRIFICATION DE STOCK

### 5.1 Récupération du stock disponible
```python
# Pour chaque article dans une commande
stock_disponible = Article.stock_actuel  # ou InventaireStock
quantite_requise = Commande.quantite

# Vérification
if stock_disponible < quantite_requise:
    stock_insuffisant = True
    manque = quantite_requise - stock_disponible
```

### 5.2 Vérification avant création de livraison
```python
def verifier_stock_avant_livraison(commandes_ids):
    """
    Vérifie le stock pour un groupe de commandes
    Retourne: (stock_suffisant: bool, articles_manquants: list)
    """
    articles_manquants = []
    
    for commande_id in commandes_ids:
        # Récupérer toutes les commandes du même groupe
        premiere_commande = Commande.objects.get(id=commande_id)
        commandes_groupe = Commande.objects.filter(
            client=premiere_commande.client,
            date=premiere_commande.date,
            heure=premiere_commande.heure
        )
        
        for cmd in commandes_groupe:
            stock_article = cmd.article.stock_actuel  # À adapter selon votre modèle
            if stock_article < cmd.quantite:
                articles_manquants.append({
                    'article': cmd.article,
                    'stock_disponible': stock_article,
                    'quantite_requise': cmd.quantite,
                    'manque': cmd.quantite - stock_article
                })
    
    return len(articles_manquants) == 0, articles_manquants
```

---

## 6. FLUX DE TRAVAIL COMPLET

### 6.1 Planification d'une livraison
1. Utilisateur accède à "Planification livraison"
2. Filtre par date et/ou zone
3. Voit la liste des commandes à planifier
4. Vérifie le stock (bouton ou automatique)
5. Sélectionne une ou plusieurs commandes
6. Clique sur "Planifier"
7. Modal s'ouvre avec:
   - Sélection livreur
   - Date/heure livraison
   - Zone (pré-rempli)
   - Ordre de livraison (si plusieurs)
   - Notes
8. Système vérifie le stock AVANT création
9. Si stock OK: Crée Livraison, met Commande à 'en_livraison'
10. Si stock insuffisant: Affiche erreur, ne crée pas

### 6.2 Reporter une livraison
1. Utilisateur accède à la liste des livraisons planifiées
2. Clique sur "Reporter" pour une livraison
3. Modal avec nouvelle date/heure et raison
4. Système met à jour Livraison
5. État reste 'planifiee'

### 6.3 Annuler une livraison
1. Utilisateur clique sur "Annuler"
2. Confirmation demandée
3. Raison d'annulation saisie
4. Système:
   - Met Livraison.etat = 'annulee'
   - Remet Commande.etat = 'validee' ou 'en_attente'
   - Enregistre raison dans notes

### 6.4 Modifier l'ordre (itinéraire)
1. Utilisateur voit les livraisons d'un livreur pour une date
2. Peut réorganiser l'ordre (drag & drop ou input)
3. Sauvegarde l'ordre
4. Système met à jour ordre_livraison pour chaque livraison

---

## 7. GESTION DES LIVREURS

### 7.1 Création/Modification livreur (à ajouter plus tard)
- Formulaire pour créer/modifier livreur
- Liste des livreurs
- Activer/désactiver livreur

---

## 8. INDICATEURS VISUELS

### 8.1 Badges de stock
- 🟢 Vert: Stock suffisant
- 🟡 Orange: Stock limite (attention)
- 🔴 Rouge: Stock insuffisant

### 8.2 États de livraison
- Planifiée: Badge bleu
- En préparation: Badge jaune
- En cours: Badge orange
- Livrée: Badge vert
- Reportée: Badge gris
- Annulée: Badge rouge

---

## 9. VALIDATIONS

### 9.1 Avant création livraison
- ✅ Stock suffisant pour tous les articles
- ✅ Livreur sélectionné
- ✅ Date/heure valides
- ✅ Zone définie
- ✅ Commande non déjà livrée

### 9.2 Avant report
- ✅ Nouvelle date >= date actuelle
- ✅ Raison fournie (optionnel mais recommandé)

### 9.3 Avant annulation
- ✅ Confirmation utilisateur
- ✅ Raison fournie

---

## 10. MESSAGES ET NOTIFICATIONS

### 10.1 Messages de succès
- "Livraison planifiée avec succès"
- "Livraison reportée avec succès"
- "Livraison annulée avec succès"
- "Ordre de livraison modifié avec succès"

### 10.2 Messages d'erreur
- "Stock insuffisant pour les articles suivants: [liste]"
- "Veuillez sélectionner un livreur"
- "Veuillez sélectionner au moins une commande"
- "Date de livraison invalide"
- "Cette livraison est déjà en cours"

---

## 11. STYLE ET DESIGN

- Style turquoise du module commandes (#06beb6, #48b1bf)
- Tableaux avec hover effects
- Modals pour actions
- Badges colorés pour états
- Indicateurs visuels pour stock
- Responsive design

---

## 12. FICHIERS À CRÉER/MODIFIER

### À créer:
1. `supermarket/templates/supermarket/commandes/planification_livraison.html`
2. `supermarket/templates/supermarket/commandes/liste_livraisons_planifiees.html` (optionnel)

### À modifier:
1. `supermarket/models.py` (✅ Déjà fait: Livreur, Livraison)
2. `supermarket/views.py` (Ajouter les 6 nouvelles vues)
3. `supermarket/urls.py` (Ajouter les 6 nouvelles URLs)
4. `supermarket/templates/supermarket/commandes/dashboard.html` (✅ Déjà fait: lien ajouté)

---

## 13. MIGRATIONS NÉCESSAIRES

1. Créer migration pour modèle Livreur
2. Créer migration pour modifications Livraison:
   - Ajout champ livreur
   - Ajout champ zone
   - Ajout champ notes
   - Ajout champ ordre_livraison
   - Modification ETAT_CHOICES (ajout 'planifiee', 'reportee')
   - Modification default de etat_livraison

---

## 14. QUESTIONS À RÉSOUDRE

1. **Stock**: Comment récupérer le stock actuel d'un article?
   - Via `Article.stock_actuel`?
   - Via `InventaireStock`?
   - Via `MouvementStock`?

2. **Groupement commandes**: Comment gérer les groupes de commandes?
   - Utiliser la même logique que dans `consulter_commandes` (client, date, heure)?

3. **Ordre livraison**: Interface drag & drop ou input numérique?
   - Recommandation: Input numérique pour simplicité

4. **Livreurs**: Créer interface de gestion livreurs maintenant ou plus tard?
   - Recommandation: Plus tard, pour l'instant juste select dans planification

---

## 15. ORDRE D'IMPLÉMENTATION RECOMMANDÉ

1. ✅ Créer/modifier modèles (DÉJÀ FAIT)
2. Créer migrations
3. Créer vue `planification_livraison` (affichage liste)
4. Créer template `planification_livraison.html` (structure de base)
5. Créer vue `verifier_stock_livraison` (AJAX)
6. Créer vue `creer_planification_livraison` (création)
7. Créer vues `reporter_livraison` et `annuler_livraison`
8. Créer vue `modifier_ordre_livraison`
9. Ajouter URLs
10. Tester et ajuster

---

**Cette structure est complète et prête à être implémentée!**

