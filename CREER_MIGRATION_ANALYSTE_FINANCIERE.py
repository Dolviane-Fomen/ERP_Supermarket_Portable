"""
Script pour créer la migration pour ajouter le type de compte 'analyste_financiere'
"""
import os
import sys
from datetime import datetime

# Ajouter le chemin du projet Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings')

import django
django.setup()

from django.db import migrations, models

def create_migration():
    """Créer le fichier de migration"""
    migration_content = f'''# Generated manually on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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
'''
    
    migration_file = 'supermarket/migrations/0049_add_analyste_financiere_type_compte.py'
    
    with open(migration_file, 'w', encoding='utf-8') as f:
        f.write(migration_content)
    
    print(f"Migration créée avec succès : {migration_file}")
    print("\nPour appliquer la migration, exécutez :")
    print("python manage.py migrate")

if __name__ == '__main__':
    create_migration()
