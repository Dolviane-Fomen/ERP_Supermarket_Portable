# Generated manually to fix FactureTemporaire duplicates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0010_fix_sessioncaisse_utilisateur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturetemporaire',
            name='session_key',
            field=models.CharField(max_length=100, unique=True, verbose_name='Clé de session'),
        ),
    ]
