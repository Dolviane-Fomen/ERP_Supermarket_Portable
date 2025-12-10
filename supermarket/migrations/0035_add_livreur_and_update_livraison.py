# Generated manually to add Livreur model and update Livraison model

from django.db import migrations, models
import django.db.models.deletion


def set_default_values_for_livraison(apps, schema_editor):
    """Définir des valeurs par défaut pour les nouveaux champs de Livraison"""
    Livraison = apps.get_model('supermarket', 'Livraison')
    
    # Mettre à jour les livraisons existantes
    for livraison in Livraison.objects.all():
        # Convertir l'état existant vers le nouveau système
        if livraison.etat_livraison == 'terminee':
            livraison.etat_livraison = 'livree'
        elif livraison.etat_livraison == 'en_cours':
            livraison.etat_livraison = 'planifiee'
        # Si annulee, garder annulee
        livraison.save()


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0034_add_numero_facture_to_facturecommande'),
    ]

    operations = [
        # Note: Le modèle Livreur existe déjà, on ne le recrée pas
        # Note: Les champs heure_depart, heure_arrivee, zone, notes, ordre_livraison, livreur existent déjà
        # On ajoute seulement heure_livraison qui manque
        
        # Ajouter seulement le champ heure_livraison qui manque
        migrations.AddField(
            model_name='livraison',
            name='heure_livraison',
            field=models.TimeField(blank=True, null=True, verbose_name='Heure de livraison'),
        ),
        
        # Modifier les choix d'état de livraison
        migrations.AlterField(
            model_name='livraison',
            name='etat_livraison',
            field=models.CharField(
                choices=[
                    ('planifiee', 'Planifiée'),
                    ('en_preparation', 'En préparation'),
                    ('en_cours', 'En cours'),
                    ('confirmee', 'Confirmée'),
                    ('livree', 'Livrée'),
                    ('livree_partiellement', 'Livrée partiellement'),
                    ('pas_livree', 'Pas livrée'),
                    ('reportee', 'Reportée'),
                    ('annulee', 'Annulée'),
                ],
                default='planifiee',
                max_length=30,
                verbose_name='État de la livraison'
            ),
        ),
        
        # Mettre à jour les valeurs existantes
        migrations.RunPython(set_default_values_for_livraison, migrations.RunPython.noop),
        
        # Modifier l'ordering
        migrations.AlterModelOptions(
            name='livraison',
            options={'ordering': ['-date_livraison', 'ordre_livraison'], 'verbose_name': 'Livraison', 'verbose_name_plural': 'Livraisons'},
        ),
    ]

