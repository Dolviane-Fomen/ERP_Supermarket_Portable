# Generated manually for adding NUI and code_postal fields to Agence
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0057_add_entreprise_info_to_agence'),
    ]

    operations = [
        migrations.AddField(
            model_name='agence',
            name='nui',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="NUI (Numéro d'Identification Unique)"),
        ),
        migrations.AddField(
            model_name='agence',
            name='code_postal',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Code postal'),
        ),
    ]
