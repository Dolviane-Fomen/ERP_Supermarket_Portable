# Configuration des dépendances ERP
# Fichier généré automatiquement

# Dépendances installées
DEPENDENCIES_INSTALLED = True

# Fonctionnalités disponibles
EXCEL_EXPORT = True
PDF_REPORTS = True
IMAGE_PROCESSING = True

# Versions installées
try:
    import openpyxl
    OPENPYXL_VERSION = openpyxl.__version__
except ImportError:
    OPENPYXL_VERSION = None

try:
    import reportlab
    REPORTLAB_VERSION = reportlab.Version
except ImportError:
    REPORTLAB_VERSION = None

try:
    import PIL
    PILLOW_VERSION = PIL.__version__
except ImportError:
    PILLOW_VERSION = None
