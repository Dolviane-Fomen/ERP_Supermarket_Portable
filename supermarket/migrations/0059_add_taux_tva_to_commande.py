# Generated manually on 2026-01-23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0058_add_nui_code_postal_to_agence'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandefournisseur',
            name='taux_tva',
            field=models.DecimalField(decimal_places=2, default=18.0, max_digits=5, verbose_name='Taux TVA (%)'),
        ),
    ]
