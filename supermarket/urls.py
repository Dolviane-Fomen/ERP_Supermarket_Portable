from django.urls import path
from . import views
from . import stock_views
from . import defacturation_views

urlpatterns = [
    path('', views.index, name='index'),
    
    # ===== AUTHENTIFICATION =====
    path('caisse/login/', views.login_caisse, name='login_caisse'),
    path('caisse/logout/', views.logout_caisse, name='logout_caisse'),
    path('commandes/login/', views.login_commandes, name='login_commandes'),
    path('commandes/logout/', views.logout_commandes, name='logout_commandes'),
    path('commandes/enregistrer/', views.enregistrer_commande, name='enregistrer_commande'),
    path('commandes/ajouter-article/', views.ajouter_article_commande, name='ajouter_article_commande'),
    path('commandes/mettre-a-jour-quantites/', views.mettre_a_jour_quantites_commande, name='mettre_a_jour_quantites_commande'),
    path('commandes/supprimer-article/', views.supprimer_article_commande, name='supprimer_article_commande'),
    path('commandes/rechercher-articles/', views.rechercher_articles_commande, name='rechercher_articles_commande'),
       path('commandes/search-window/', views.search_window_commande, name='search_window_commande'),
       path('commandes/consulter/', views.consulter_commandes, name='consulter_commandes'),
       path('commandes/consulter-factures/', views.consulter_factures_commande, name='consulter_factures_commande'),
       path('commandes/facture/<int:facture_id>/', views.detail_facture_commande, name='detail_facture_commande'),
       path('commandes/modifier-facture/<int:facture_id>/', views.modifier_facture_commande, name='modifier_facture_commande'),
       path('commandes/commande/<int:commande_id>/', views.detail_commande, name='detail_commande'),
       path('commandes/commande/<int:commande_id>/generer-facture/', views.generer_facture_commande_existante, name='generer_facture_commande_existante'),
       path('commandes/modifier-commande/<int:commande_id>/', views.modifier_commande, name='modifier_commande'),
       path('commandes/supprimer-commande/<int:commande_id>/', views.supprimer_commande, name='supprimer_commande'),
       path('commandes/imprimer-facture/<int:facture_id>/', views.imprimer_facture_commande, name='imprimer_facture_commande'),
       path('commandes/imprimer-facture/', views.imprimer_facture_commande, name='imprimer_facture_commande_session'),
       path('commandes/imprimer-facture-xprinter/<int:facture_id>/', views.imprimer_facture_commande_xprinter, name='imprimer_facture_commande_xprinter'),
    path('commandes/sauvegarder/', views.sauvegarder_commande, name='sauvegarder_commande'),
    path('commandes/generer-facture/', views.generer_facture_commande, name='generer_facture_commande'),
    path('commandes/enregistrer-client/', views.enregistrer_client, name='enregistrer_client_commandes'),
    path('commandes/consulter-clients/', views.consulter_clients_commandes, name='consulter_clients_commandes'),
    path('commandes/client/<int:client_id>/', views.detail_client_commandes, name='detail_client_commandes'),
    path('commandes/modifier-client/<int:client_id>/', views.modifier_client_commandes, name='modifier_client_commandes'),
    path('commandes/supprimer-client/<int:client_id>/', views.supprimer_client_commandes, name='supprimer_client_commandes'),
    path('commandes/planification-livraison/', views.planification_livraison, name='planification_livraison'),
    path('commandes/creer-planification-livraison/', views.creer_planification_livraison, name='creer_planification_livraison'),
    path('commandes/verifier-stock-livraison/', views.verifier_stock_livraison, name='verifier_stock_livraison'),
    path('commandes/reporter-livraison/<int:livraison_id>/', views.reporter_livraison, name='reporter_livraison'),
    path('commandes/annuler-livraison/<int:livraison_id>/', views.annuler_livraison, name='annuler_livraison'),
    path('commandes/modifier-ordre-livraison/', views.modifier_ordre_livraison, name='modifier_ordre_livraison'),
    path('commandes/voir-itineraire/', views.voir_itineraire, name='voir_itineraire'),
    path('commandes/confirmer-livraison/<int:livraison_id>/', views.confirmer_livraison, name='confirmer_livraison'),
    path('commandes/definir-etat-livraison/', views.definir_etat_livraison, name='definir_etat_livraison'),
    path('commandes/definir-etat-final-livraison/<int:livraison_id>/', views.definir_etat_final_livraison, name='definir_etat_final_livraison'),
    path('commandes/consulter-livraisons/', views.consulter_livraisons, name='consulter_livraisons'),
    path('commandes/suivi-client/', views.suivi_client, name='suivi_client'),
    path('commandes/sauvegarder-action-client/', views.sauvegarder_action_client, name='sauvegarder_action_client'),
    path('commandes/modifier-action-client/', views.modifier_action_client, name='modifier_action_client'),
    path('commandes/rapport-acm/', views.rapport_acm, name='rapport_acm'),
    path('commandes/generer-rapport-acm/', views.generer_rapport_acm, name='generer_rapport_acm'),
    path('commandes/export-rapport-acm-excel/', views.export_rapport_acm_excel, name='export_rapport_acm_excel'),
    path('commandes/statistiques-clients/', views.statistiques_clients, name='statistiques_clients'),
    path('commandes/generer-statistiques-clients/', views.generer_statistiques_clients, name='generer_statistiques_clients'),
    path('commandes/export-statistiques-clients-excel/', views.export_statistiques_clients_excel, name='export_statistiques_clients_excel'),
    path('commandes/rapport-livreur/', views.rapport_livreur, name='rapport_livreur'),
    path('commandes/rapport-livraison/', views.rapport_livreur, name='rapport_livraison'),  # Redirection vers rapport_livreur
    path('commandes/generer-rapport-livreur/', views.generer_rapport_livreur, name='generer_rapport_livreur'),
    path('commandes/generer-rapport-livraison/', views.generer_rapport_livreur, name='generer_rapport_livraison'),  # Redirection vers generer_rapport_livreur
    path('commandes/export-rapport-livreur-excel/', views.export_rapport_livreur_excel, name='export_rapport_livreur_excel'),
    path('commandes/export-rapport-livraison-excel/', views.export_rapport_livreur_excel, name='export_rapport_livraison_excel'),  # Redirection vers export_rapport_livreur_excel
    path('commandes/consulter-livreurs/', views.consulter_livreurs, name='consulter_livreurs'),
    path('commandes/enregistrer-livreur/', views.enregistrer_livreur, name='enregistrer_livreur'),
    path('commandes/livreur/<int:livreur_id>/', views.detail_livreur, name='detail_livreur'),
    path('commandes/modifier-livreur/<int:livreur_id>/', views.modifier_livreur, name='modifier_livreur'),
    path('commandes/supprimer-livreur/<int:livreur_id>/', views.supprimer_livreur, name='supprimer_livreur'),
    path('commandes/get-notifications/', views.get_notifications, name='get_notifications'),
    path('commandes/marquer-notification-lue/<int:notification_id>/', views.marquer_notification_lue, name='marquer_notification_lue'),
    path('commandes/marquer-toutes-notifications-lues/', views.marquer_toutes_notifications_lues, name='marquer_toutes_notifications_lues'),
    
    # ===== MODULE GESTION DE CAISSE =====
    path('caisse/', views.dashboard_caisse, name='dashboard_caisse'),
    path('caisse/kpis-api/', views.dashboard_kpis_api, name='dashboard_kpis_api'),
    path('caisse/facturation/', views.facturation_vente, name='facturation_vente'),
    path('caisse/facturation/<int:facture_id>/', views.facturation_vente, name='facturation_vente_with_id'),
    path('caisse/mouvement/', views.mouvement_vente, name='mouvement_vente'),
    path('caisse/rapport/', views.rapport_caisse, name='rapport_caisse'),
    path('caisse/detail-factures/', views.detail_factures, name='detail_factures'),
    path('caisse/facture-details/<int:facture_id>/', views.facture_details, name='facture_details'),
    path('caisse/documents-vente/', views.documents_vente, name='documents_vente'),
    path('caisse/document-details/<int:document_id>/', views.document_vente_details, name='document_vente_details'),
    path('caisse/articles/', views.liste_articles, name='liste_articles'),
    path('caisse/clients/', views.liste_clients, name='liste_clients'),
    
    # ===== GESTION CAISSE =====
    path('caisse/ouvrir/', views.ouvrir_caisse, name='ouvrir_caisse'),
    path('caisse/fermer/', views.fermer_caisse, name='fermer_caisse'),
    path('caisse/enregistrer-facture/', views.enregistrer_facture, name='enregistrer_facture'),
    path('caisse/ajouter-article/', views.ajouter_article_facture, name='ajouter_article_facture'),
    path('caisse/finaliser-facture/<int:facture_id>/', views.finaliser_facture, name='finaliser_facture'),
    path('caisse/mettre-en-attente/', views.mettre_en_attente, name='mettre_en_attente'),
    path('caisse/rappeler-ticket/', views.rappeler_ticket, name='rappeler_ticket'),
    path('caisse/supprimer-ligne/', views.supprimer_ligne_facture, name='supprimer_ligne_facture'),
    path('caisse/modifier-quantite/', views.modifier_quantite_ligne, name='modifier_quantite_ligne'),
    path('caisse/supprimer-vente/', views.supprimer_vente, name='supprimer_vente'),
    path('caisse/imprimer-facture/<int:facture_id>/', views.imprimer_facture, name='imprimer_facture'),
    path('caisse/imprimer-facture/', views.imprimer_facture, name='imprimer_facture_session'),
    path('caisse/search-window/', views.search_window, name='search_window'),
    path('caisse/search-articles/', views.search_articles_api, name='search_articles_api'),
    path('caisse/get-prix-by-type/', views.get_prix_by_type, name='get_prix_by_type'),
    path('caisse/get-article-types/', views.get_article_types, name='get_article_types'),
    path('caisse/init-test-data/', views.init_test_data, name='init_test_data'),
    
    # ===== GESTION FACTURE TEMPORAIRE =====
    path('caisse/update-quantity-temp/', views.update_quantity_temp, name='update_quantity_temp'),
    path('caisse/remove-article-temp/', views.remove_article_temp, name='remove_article_temp'),
    path('caisse/update-montant-regler/', views.update_montant_regler, name='update_montant_regler'),
    path('caisse/update-type-vente-temp/', views.update_type_vente_temp, name='update_type_vente_temp'),
    path('caisse/update-all-types-vente-temp/', views.update_all_types_vente_temp, name='update_all_types_vente_temp'),
    path('caisse/generate-ticket-number/', views.generate_ticket_number_api, name='generate_ticket_number'),
    path('caisse/clear-facture-temp/', views.clear_facture_temp, name='clear_facture_temp'),
    
    # ===== NOUVELLES URLS POUR RAPPEL TICKET =====
    path('caisse/article-types-vente/<int:article_id>/', views.get_article_types_vente, name='get_article_types_vente'),
    path('caisse/update-type-vente/', views.update_type_vente, name='update_type_vente'),
    path('caisse/get-article-id-by-designation/', views.get_article_id_by_designation, name='get_article_id_by_designation'),
    
    # ===== TESTS =====
    path('test_flux_complet.html', views.test_flux_complet, name='test_flux_complet'),
    
    # ===== IMPRESSION =====
    path('caisse/impression-facture/', views.imprimer_facture, name='impression_facture'),
    
    # ===== GESTION DES FACTURES EN ATTENTE =====
    path('caisse/lister-factures-attente/', views.lister_factures_attente, name='lister_factures_attente'),
    path('caisse/rappeler-facture-specifique/', views.rappeler_facture_specifique, name='rappeler_facture_specifique'),
    path('caisse/supprimer-facture-attente/', views.supprimer_facture_attente, name='supprimer_facture_attente'),
    
    # ===== TESTS =====
    path('caisse/test-urls/', views.test_urls_page, name='test_urls_page'),
    
    # ===== MODULE GESTION DE STOCK =====
    path('stock/', views.dashboard_stock, name='dashboard_stock'),
    path('stock/creer-article/', views.creer_article, name='creer_article'),
    path('stock/generate-reference/', views.generate_reference, name='generate_reference'),
    path('stock/consulter-articles/', views.consulter_articles, name='consulter_articles'),
    path('stock/creer-fournisseur/', views.creer_fournisseur, name='creer_fournisseur'),
    path('stock/consulter-fournisseurs/', views.consulter_fournisseurs, name='consulter_fournisseurs'),
    path('stock/fournisseur/<int:fournisseur_id>/', views.detail_fournisseur, name='detail_fournisseur'),
    path('stock/modifier-fournisseur/<int:fournisseur_id>/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('stock/supprimer-fournisseur/<int:fournisseur_id>/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
    path('stock/creer-client/', views.creer_client, name='creer_client'),
    path('stock/consulter-clients/', views.consulter_clients, name='consulter_clients'),
    path('stock/modifier-article/<int:article_id>/', views.modifier_article, name='modifier_article'),
    path('stock/supprimer-article/<int:article_id>/', views.supprimer_article, name='supprimer_article'),
    path('stock/article/<int:article_id>/', views.detail_article, name='detail_article'),
    path('stock/modifier-client/<int:client_id>/', views.modifier_client, name='modifier_client'),
    path('stock/supprimer-client/<int:client_id>/', views.supprimer_client, name='supprimer_client'),
    path('stock/client/<int:client_id>/', views.detail_client, name='detail_client'),
    
    # Plan Comptable
    path('stock/consulter-plan-comptable/', views.consulter_plan_comptable, name='consulter_plan_comptable'),
    path('stock/creer-plan-comptable/', views.creer_plan_comptable, name='creer_plan_comptable'),
    path('stock/modifier-plan-comptable/<int:compte_id>/', views.modifier_plan_comptable, name='modifier_plan_comptable'),
    path('stock/supprimer-plan-comptable/<int:compte_id>/', views.supprimer_plan_comptable, name='supprimer_plan_comptable'),
    
    # Plan Tiers
    path('stock/consulter-plan-tiers/', views.consulter_plan_tiers, name='consulter_plan_tiers'),
    path('stock/creer-plan-tiers/', views.creer_plan_tiers, name='creer_plan_tiers'),
    path('stock/modifier-plan-tiers/<int:tiers_id>/', views.modifier_plan_tiers, name='modifier_plan_tiers'),
    path('stock/supprimer-plan-tiers/<int:tiers_id>/', views.supprimer_plan_tiers, name='supprimer_plan_tiers'),
    
    # Code Journaux
    path('stock/consulter-code-journaux/', views.consulter_code_journaux, name='consulter_code_journaux'),
    path('stock/creer-code-journaux/', views.creer_code_journaux, name='creer_code_journaux'),
    path('stock/modifier-code-journaux/<int:journal_id>/', views.modifier_code_journaux, name='modifier_code_journaux'),
    path('stock/supprimer-code-journaux/<int:journal_id>/', views.supprimer_code_journaux, name='supprimer_code_journaux'),
    
    # Taux Taxe
    path('stock/consulter-taux-taxe/', views.consulter_taux_taxe, name='consulter_taux_taxe'),
    path('stock/creer-taux-taxe/', views.creer_taux_taxe, name='creer_taux_taxe'),
    path('stock/modifier-taux-taxe/<int:taux_id>/', views.modifier_taux_taxe, name='modifier_taux_taxe'),
    path('stock/supprimer-taux-taxe/<int:taux_id>/', views.supprimer_taux_taxe, name='supprimer_taux_taxe'),
    
    # Factures d'Achat
    path('stock/consulter-factures-achat/', views.consulter_factures_achat, name='consulter_factures_achat'),
    path('stock/creer-facture-achat/', views.creer_facture_achat, name='creer_facture_achat'),
    path('stock/facture-achat/<int:facture_id>/', views.detail_facture_achat, name='detail_facture_achat'),
    path('stock/modifier-facture-achat/<int:facture_id>/', views.modifier_facture_achat, name='modifier_facture_achat'),
    path('stock/supprimer-facture-achat/<int:facture_id>/', views.supprimer_facture_achat, name='supprimer_facture_achat'),
    
    # Factures de Transfert
    path('stock/consulter-factures-transfert/', views.consulter_factures_transfert, name='consulter_factures_transfert'),
    path('stock/creer-facture-transfert/', views.creer_facture_transfert, name='creer_facture_transfert'),
    path('stock/facture-transfert/<int:facture_id>/', views.detail_facture_transfert, name='detail_facture_transfert'),
    path('stock/modifier-facture-transfert/<int:facture_id>/', views.modifier_facture_transfert, name='modifier_facture_transfert'),
    path('stock/supprimer-facture-transfert/<int:facture_id>/', views.supprimer_facture_transfert, name='supprimer_facture_transfert'),
    
    # Inventaire de Stock
    path('stock/inventaire/', views.inventaire_stock, name='inventaire_stock'),
    path('stock/generer-inventaire/', views.generer_inventaire, name='generer_inventaire'),
    path('stock/export-inventaire-excel/', views.export_inventaire_excel, name='export_inventaire_excel'),
    path('stock/export-inventaire-pdf/', views.export_inventaire_pdf, name='export_inventaire_pdf'),
    path('stock/export-inventaire-csv/', views.export_inventaire_csv, name='export_inventaire_csv'),
    
    # Statistiques de Vente
    path('stock/statistiques-vente/', views.statistiques_vente, name='statistiques_vente'),
    path('stock/generer-statistiques-vente/', views.generer_statistiques_vente, name='generer_statistiques_vente'),
    path('stock/export-statistiques-excel/', views.export_statistiques_excel, name='export_statistiques_excel'),
    path('stock/export-statistiques-pdf/', views.export_statistiques_pdf, name='export_statistiques_pdf'),
    path('stock/export-statistiques-csv/', views.export_statistiques_csv, name='export_statistiques_csv'),
    path('stock/test-statistiques/', views.test_statistiques, name='test_statistiques'),
    
    # Mouvements de Stock
    path('stock/mouvements/', views.mouvements_stock, name='mouvements_stock'),
    path('stock/consulter-mouvements/', views.consulter_mouvements_stock, name='consulter_mouvements_stock'),
    path('stock/export-mouvements-excel/', views.export_mouvements_excel, name='export_mouvements_excel'),
    path('stock/export-mouvements-pdf/', views.export_mouvements_pdf, name='export_mouvements_pdf'),
    path('stock/export-mouvements-csv/', views.export_mouvements_csv, name='export_mouvements_csv'),
    path('stock/creer-mouvements-retroactifs/', views.creer_mouvements_retroactifs, name='creer_mouvements_retroactifs'),
    path('stock/diagnostic-mouvements/', views.diagnostic_mouvements, name='diagnostic_mouvements'),
    path('stock/forcer-mouvements/', views.forcer_mouvements, name='forcer_mouvements'),
    path('stock/test-mouvement-simple/', views.test_mouvement_simple, name='test_mouvement_simple'),
    path('stock/creer-mouvements-manuels/', views.creer_mouvements_manuels, name='creer_mouvements_manuels'),
    path('stock/test-consultation-mouvements/', views.test_consultation_mouvements, name='test_consultation_mouvements'),
    path('stock/get-mouvements-session/', views.get_mouvements_session, name='get_mouvements_session'),
    
    # Recherche d'articles pour stock
    path('stock/search-articles/', views.search_articles_stock, name='search_articles_stock'),
    path('stock/create-test-articles/', views.create_test_articles, name='create_test_articles'),
    
    # Alertes et Ruptures de Stock
    path('stock/alertes/', stock_views.stock_alerte, name='stock_alerte'),
    path('stock/ruptures/', stock_views.rupture_stock, name='rupture_stock'),
    
    # Défacturation
    path('stock/defacturer/<int:facture_id>/', defacturation_views.defacturer_vente_confirmation, name='defacturer_confirmation'),
    path('stock/defacturer/<int:facture_id>/confirmer/', defacturation_views.defacturer_vente, name='defacturer_vente'),
    path('stock/defacturer/<int:facture_id>/ligne/<int:ligne_id>/', defacturation_views.defacturer_ligne_vente, name='defacturer_ligne_vente'),
    
    # Export/Import des Données
    path('export-import/', views.export_import_page, name='export_import_page'),
    path('export-data/', views.export_data_view, name='export_data'),
    path('import-data/', views.import_data_view, name='import_data'),
    
    path('stock/login/', views.login_stock, name='login_stock'),
    path('stock/logout/', views.logout_stock, name='logout_stock'),

    # ===== MODULE GESTION COMMANDES =====
    path('commandes/', views.dashboard_commandes, name='dashboard_commandes'),
    path('commandes/travail-acm/', views.travail_acm, name='travail_acm'),
    path('commandes/travail-livreur/', views.travail_livreur, name='travail_livreur'),
    
    # ===== GESTION DES COMPTES UTILISATEURS =====
    path('comptes/login/', views.login_comptes, name='login_comptes'),
    path('comptes/logout/', views.logout_comptes, name='logout_comptes'),
    path('comptes/', views.gestion_comptes, name='gestion_comptes'),
    path('comptes/creer/', views.creer_compte, name='creer_compte'),
    path('comptes/<int:compte_id>/', views.detail_compte, name='detail_compte'),
    path('comptes/<int:compte_id>/modifier/', views.modifier_compte, name='modifier_compte'),
    path('comptes/<int:compte_id>/supprimer/', views.supprimer_compte, name='supprimer_compte'),
    path('comptes/<int:compte_id>/activer-desactiver/', views.activer_desactiver_compte, name='activer_desactiver_compte'),
    path('comptes/<int:compte_id>/reinitialiser-mot-de-passe/', views.reinitialiser_mot_de_passe, name='reinitialiser_mot_de_passe'),

    # ======================== Module Comptabiliter=======================
    path('comptabiliter/login_comptabiliter/', views.login_comptabiliter, name='login_comptabiliter'),
    path('comptabiliter/dashboard/', views.dashboard_comptabiliter, name='dashboard_comptabiliter'),
    path('comptabiliter/dashboard/', views.logout_stock, name='logout_Comptabiliter'),
    path('comptabiliter/creer-depense/', views.creer_depense, name='creer_depense'),
    path('comptabiliter/consulter-depenses/', views.consulter_depenses, name='consulter_depenses'),
]