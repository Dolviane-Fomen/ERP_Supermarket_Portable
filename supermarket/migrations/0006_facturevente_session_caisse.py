# Generated manually for adding session_caisse field to FactureVente

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0005_alter_sessioncaisse_utilisateur'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturevente',
            name='session_caisse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='supermarket.sessioncaisse', verbose_name='Session de caisse'),
        ),
    ]








