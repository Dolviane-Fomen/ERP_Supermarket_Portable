# Generated manually to add numero_facture field to FactureCommande

from django.db import migrations, models


def generate_numero_facture(apps, schema_editor):
    """Générer des numéros de facture pour les factures existantes"""
    FactureCommande = apps.get_model('supermarket', 'FactureCommande')
    
    for facture in FactureCommande.objects.filter(numero_facture__isnull=True):
        # Générer un numéro de facture basé sur l'ID et la date
        if facture.date_facture:
            date_str = facture.date_facture.strftime('%Y%m%d')
        elif facture.date_creation:
            date_str = facture.date_creation.strftime('%Y%m%d')
        else:
            from datetime import date
            date_str = date.today().strftime('%Y%m%d')
        
        numero_facture = f"FACT-{date_str}-{facture.id:04d}"
        facture.numero_facture = numero_facture
        facture.save()


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0033_add_date_facture_default'),
    ]

    operations = [
        # Étape 1: Ajouter le champ comme nullable temporairement
        migrations.AddField(
            model_name='facturecommande',
            name='numero_facture',
            field=models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Numéro de facture'),
        ),
        # Étape 2: Remplir les valeurs existantes
        migrations.RunPython(generate_numero_facture, migrations.RunPython.noop),
        # Étape 3: Rendre le champ non-nullable
        migrations.AlterField(
            model_name='facturecommande',
            name='numero_facture',
            field=models.CharField(max_length=100, unique=True, verbose_name='Numéro de facture'),
        ),
    ]


