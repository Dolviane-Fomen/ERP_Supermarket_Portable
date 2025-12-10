# Generated manually to add agence field to Commande, Livraison, FactureCommande, and StatistiqueClient

from django.db import migrations, models
import django.db.models.deletion


def add_agence_to_commandes(apps, schema_editor):
    """Ajouter l'agence aux commandes existantes"""
    Commande = apps.get_model('supermarket', 'Commande')
    Agence = apps.get_model('supermarket', 'Agence')
    
    # Récupérer la première agence disponible
    agence = Agence.objects.first()
    if agence:
        # Mettre à jour toutes les commandes existantes
        Commande.objects.filter(agence__isnull=True).update(agence=agence)


def add_agence_to_livraisons(apps, schema_editor):
    """Ajouter l'agence aux livraisons existantes"""
    Livraison = apps.get_model('supermarket', 'Livraison')
    Agence = apps.get_model('supermarket', 'Agence')
    
    agence = Agence.objects.first()
    if agence:
        Livraison.objects.filter(agence__isnull=True).update(agence=agence)


def add_agence_to_factures(apps, schema_editor):
    """Ajouter l'agence aux factures existantes"""
    FactureCommande = apps.get_model('supermarket', 'FactureCommande')
    Agence = apps.get_model('supermarket', 'Agence')
    
    agence = Agence.objects.first()
    if agence:
        FactureCommande.objects.filter(agence__isnull=True).update(agence=agence)


def add_agence_to_statistiques(apps, schema_editor):
    """Ajouter l'agence aux statistiques existantes"""
    StatistiqueClient = apps.get_model('supermarket', 'StatistiqueClient')
    Agence = apps.get_model('supermarket', 'Agence')
    
    agence = Agence.objects.first()
    if agence:
        StatistiqueClient.objects.filter(agence__isnull=True).update(agence=agence)


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0031_update_type_compte_choices'),
    ]

    operations = [
        # Ajouter le champ agence à Commande (nullable d'abord)
        migrations.AddField(
            model_name='commande',
            name='agence',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='supermarket.agence',
                verbose_name='Agence'
            ),
        ),
        # Remplir les valeurs existantes
        migrations.RunPython(add_agence_to_commandes, migrations.RunPython.noop),
        # Rendre le champ non-nullable
        migrations.AlterField(
            model_name='commande',
            name='agence',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='supermarket.agence',
                verbose_name='Agence'
            ),
        ),
        
        # Ajouter le champ agence à Livraison (nullable d'abord)
        migrations.AddField(
            model_name='livraison',
            name='agence',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='supermarket.agence',
                verbose_name='Agence'
            ),
        ),
        # Remplir les valeurs existantes
        migrations.RunPython(add_agence_to_livraisons, migrations.RunPython.noop),
        # Rendre le champ non-nullable
        migrations.AlterField(
            model_name='livraison',
            name='agence',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='supermarket.agence',
                verbose_name='Agence'
            ),
        ),
        
        # Ajouter le champ agence à FactureCommande (nullable d'abord)
        migrations.AddField(
            model_name='facturecommande',
            name='agence',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='supermarket.agence',
                verbose_name='Agence'
            ),
        ),
        # Remplir les valeurs existantes
        migrations.RunPython(add_agence_to_factures, migrations.RunPython.noop),
        # Rendre le champ non-nullable
        migrations.AlterField(
            model_name='facturecommande',
            name='agence',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='supermarket.agence',
                verbose_name='Agence'
            ),
        ),
        
        # Ajouter le champ agence à StatistiqueClient (nullable d'abord)
        migrations.AddField(
            model_name='statistiqueclient',
            name='agence',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='supermarket.agence',
                verbose_name='Agence'
            ),
        ),
        # Remplir les valeurs existantes
        migrations.RunPython(add_agence_to_statistiques, migrations.RunPython.noop),
        # Rendre le champ non-nullable
        migrations.AlterField(
            model_name='statistiqueclient',
            name='agence',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='supermarket.agence',
                verbose_name='Agence'
            ),
        ),
    ]

