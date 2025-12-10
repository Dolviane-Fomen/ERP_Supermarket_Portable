/**
 * Configuration pour imprimante thermique
 * Support pour imprimantes thermiques courantes (Epson, Star, etc.)
 */

class ThermalPrinter {
    constructor() {
        this.printerConfig = {
            // Configuration par défaut pour imprimante thermique 80mm
            width: 300, // pixels
            fontSize: 12,
            fontFamily: 'Courier New, monospace',
            margins: {
                top: 5,
                right: 5,
                bottom: 5,
                left: 5
            }
        };
    }

    /**
     * Optimiser le contenu pour l'impression thermique
     */
    optimizeForThermal(content) {
        // Appliquer les styles optimisés pour imprimante thermique
        const optimizedContent = `
            <style>
                @page {
                    size: 80mm auto;
                    margin: 0;
                }
                
                @media print {
                    * {
                        -webkit-print-color-adjust: exact !important;
                        color-adjust: exact !important;
                    }
                    
                    body {
                        font-family: 'Courier New', monospace !important;
                        font-size: 12px !important;
                        line-height: 1.2 !important;
                        width: 300px !important;
                        margin: 0 !important;
                        padding: 5px !important;
                        background: white !important;
                    }
                    
                    .no-print {
                        display: none !important;
                    }
                    
                    /* Optimisations pour imprimante thermique */
                    .invoice {
                        width: 100% !important;
                        max-width: none !important;
                        border: none !important;
                        box-shadow: none !important;
                    }
                    
                    /* Assurer que les bordures s'impriment */
                    .separator, .border {
                        border-color: black !important;
                        border-style: dashed !important;
                    }
                    
                    /* Optimiser les espaces */
                    h1, h2, h3 {
                        margin: 5px 0 !important;
                    }
                    
                    p, div {
                        margin: 2px 0 !important;
                    }
                    
                    /* Forcer l'impression des couleurs */
                    .total, .thank-you {
                        font-weight: bold !important;
                        color: black !important;
                    }
                }
            </style>
            ${content}
        `;
        
        return optimizedContent;
    }

    /**
     * Imprimer directement avec l'imprimante par défaut
     */
    async printDirect(content) {
        try {
            // Créer une nouvelle fenêtre pour l'impression
            const printWindow = window.open('', '_blank', 'width=400,height=600');
            
            if (!printWindow) {
                throw new Error('Impossible d\'ouvrir la fenêtre d\'impression. Vérifiez les pop-ups bloqués.');
            }

            // Optimiser le contenu pour l'impression thermique
            const optimizedContent = this.optimizeForThermal(content);
            
            // Écrire le contenu dans la nouvelle fenêtre
            printWindow.document.write(optimizedContent);
            printWindow.document.close();
            
            // Attendre que le contenu soit chargé
            await new Promise((resolve) => {
                printWindow.onload = resolve;
                // Fallback si onload ne se déclenche pas
                setTimeout(resolve, 1000);
            });
            
            // Lancer l'impression
            printWindow.print();
            
            // Fermer la fenêtre après impression
            setTimeout(() => {
                printWindow.close();
            }, 1000);
            
            return { success: true, message: 'Impression lancée avec succès' };
            
        } catch (error) {
            console.error('Erreur lors de l\'impression:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Configurer l'imprimante (pour futures améliorations)
     */
    configurePrinter(config) {
        this.printerConfig = { ...this.printerConfig, ...config };
    }

    /**
     * Détecter le type d'imprimante disponible
     */
    detectPrinter() {
        // Cette fonction pourrait être étendue pour détecter
        // automatiquement le type d'imprimante connectée
        return {
            type: 'thermal',
            width: '80mm',
            supported: true
        };
    }
}

// Instance globale
window.thermalPrinter = new ThermalPrinter();

// Fonctions utilitaires globales
window.imprimerDirect = function(content) {
    return window.thermalPrinter.printDirect(content);
};

window.afficherApercu = function() {
    window.print();
};

window.fermerFacture = function() {
    window.close();
};

// Configuration automatique au chargement
document.addEventListener('DOMContentLoaded', function() {
    console.log('Imprimante thermique configurée:', window.thermalPrinter.detectPrinter());
});






