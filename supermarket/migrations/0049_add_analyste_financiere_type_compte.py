# Generated manually on 2026-01-14 11:23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supermarket', '0048_depense_agence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compte',
            name='type_compte',
            field=models.CharField(choices=[
                ('admin', 'Administrateur'),
                ('gerant', 'Gérant'),
                ('caissier', 'Caissier'),
                ('vendeur', 'Vendeur'),
                ('magasinier', 'Magasinier'),
                ('comptable', 'Comptable'),
                ('acm', 'ACM'),
                ('livreur', 'Livreur'),
                ('responsable_logistique', 'Responsable Logistique'),
                ('responsable_rh', 'Responsable Ressource Humaine'),
                ('assistant_comptable', 'Assistant Comptable'),
                ('responsable_achat', 'Responsable Achat'),
                ('analyste_financiere', 'Analyste Financière'),
            ], default='vendeur', max_length=30, verbose_name='Type de compte'),
        ),
    ]
