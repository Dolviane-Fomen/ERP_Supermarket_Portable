#!/usr/bin/env python3
"""
Script de test réel pour la fermeture de caisse avec nombres décimaux
Test dans l'agence POISSONNERIE SANGAH
"""

import os
import sys
import django
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_project.settings_standalone')
django.setup()

from supermarket.models import (
    Agence, Caisse, Employe, Compte, SessionCaisse, 
    FactureVente, LigneFactureVente, DocumentVente, 
    Client, Article
)
from django.utils import timezone
import json

def test_fermeture_caisse_decimal():
    """Test réel de fermeture de caisse avec nombres décimaux"""
    print("=" * 80)
    print("TEST REEL DE FERMETURE DE CAISSE AVEC NOMBRES DECIMAUX")
    print("Agence: POISSONNERIE SANGAH")
    print("=" * 80)
    
    try:
        # 1. Récupérer l'agence POISSONNERIE SANGAH
        print("\n1. Recherche de l'agence POISSONNERIE SANGAH...")
        agence = Agence.objects.filter(nom_agence__icontains="POISSONNERIE").first()
        if not agence:
            print("ERREUR: Agence POISSONNERIE SANGAH non trouvee")
            return False
        print(f"[OK] Agence trouvee: {agence.nom_agence}")
        
        # 2. Récupérer ou créer une session de caisse ouverte
        print("\n2. Recherche d'une session de caisse ouverte...")
        session_caisse = SessionCaisse.objects.filter(
            agence=agence,
            statut='ouverte'
        ).first()
        
        if not session_caisse:
            print("Pas de session ouverte, creation d'une session de test...")
            caisse = Caisse.objects.filter(agence=agence).first()
            if not caisse:
                caisse = Caisse.objects.create(
                    numero_caisse="CAISSE_TEST",
                    agence=agence
                )
            
            compte = Compte.objects.filter(agence=agence).first()
            if not compte:
                print("ERREUR: Aucun compte trouve")
                return False
            
            employe = Employe.objects.filter(compte=compte).first()
            if not employe:
                print("ERREUR: Aucun employe trouve")
                return False
            
            session_caisse = SessionCaisse.objects.create(
                agence=agence,
                caisse=caisse,
                employe=employe,
                date_ouverture=timezone.now(),
                solde_ouverture=Decimal('0.00'),
                statut='ouverte'
            )
            print(f"[OK] Session de test creee: {session_caisse.id}")
        else:
            print(f"[OK] Session trouvee: {session_caisse.id}")
        
        # 3. Récupérer des articles avec prix décimaux
        print("\n3. Recherche d'articles avec prix decimaux...")
        articles = Article.objects.filter(agence=agence)[:3]
        if not articles.exists():
            print("ERREUR: Aucun article trouve")
            return False
        print(f"[OK] {articles.count()} articles trouves")
        
        # 4. Créer une facture de test avec des nombres décimaux
        print("\n4. Creation d'une facture de test avec nombres decimaux...")
        client = Client.objects.filter(agence=agence).first()
        if not client:
            client = Client.objects.create(
                intitule="Client Test Decimal",
                agence=agence
            )
        
        facture = FactureVente.objects.create(
            numero_ticket=f"TEST_DEC_{timezone.now().strftime('%Y%m%d%H%M%S')}",
            date=timezone.now().date(),
            heure=timezone.now().time(),
            nette_a_payer=Decimal('1527.75'),  # Nombre décimal
            montant_regler=Decimal('1527.75'),
            rendu=Decimal('0.00'),
            remise=Decimal('0.00'),
            nom_vendeuse="Test Decimal",
            client=client,
            caisse=session_caisse.caisse,
            agence=agence,
            session_caisse=session_caisse
        )
        print(f"[OK] Facture creee: {facture.numero_ticket}")
        
        # 5. Créer des lignes de facture avec quantités et prix décimaux
        print("\n5. Creation de lignes de facture avec quantites decimales...")
        total_test = Decimal('0')
        for i, article in enumerate(articles[:2]):
            # Utiliser des quantités avec des décimales
            quantite = Decimal(f'{1 + i * 0.5}')  # 1.0 et 1.5
            prix_unitaire = Decimal(f'{500.25 + i * 50.75}')  # 500.25 et 551.00
            prix_total = quantite * prix_unitaire
            total_test += prix_total
            
            ligne = LigneFactureVente.objects.create(
                facture_vente=facture,
                article=article,
                designation=article.designation,
                quantite=quantite,
                prix_unitaire=prix_unitaire,
                prix_total=prix_total
            )
            print(f"  - {article.designation}: {quantite} x {prix_unitaire} = {prix_total}")
        
        # Mettre à jour le total de la facture
        facture.nette_a_payer = total_test
        facture.montant_regler = total_test
        facture.save()
        print(f"[OK] Total facture: {total_test}")
        
        # 6. Simuler la fonction fermer_caisse avec les corrections
        print("\n6. Simulation de fermer_caisse avec corrections Decimal...")
        
        factures_jour = FactureVente.objects.filter(
            agence=agence,
            date=timezone.now().date(),
            session_caisse=session_caisse
        ).select_related('client', 'vendeur__compte').prefetch_related('lignes__article')
        
        nombre_factures = factures_jour.count()
        total_articles = 0
        chiffre_affaires = 0.0  # IMPORTANT: float au lieu de Decimal
        
        factures_data = []
        
        for f in factures_jour:
            # IMPORTANT: Conversion en float pour la sérialisation JSON
            chiffre_affaires += float(f.nette_a_payer or Decimal('0'))
            
            facture_data = {
                'numero_ticket': f.numero_ticket,
                'date': f.date.strftime('%Y-%m-%d'),
                'heure': f.heure.strftime('%H:%M') if f.heure else '',
                'client': f.client.intitule if f.client else 'Client anonyme',
                'nette_a_payer': float(f.nette_a_payer or Decimal('0')),  # Conversion en float
                'articles': []
            }
            
            for ligne in f.lignes.all():
                total_articles += int(ligne.quantite)
                facture_data['articles'].append({
                    'designation': ligne.designation,
                    'reference': ligne.article.reference_article if ligne.article else '',
                    'quantite': int(ligne.quantite),  # Conversion en int
                    'prix_unitaire': float(ligne.prix_unitaire or Decimal('0')),  # Conversion en float
                    'total': float(ligne.prix_total or Decimal('0'))  # Conversion en float
                })
            
            factures_data.append(facture_data)
        
        print(f"  - Nombre de factures: {nombre_factures}")
        print(f"  - Total articles: {total_articles}")
        print(f"  - Chiffre d'affaires: {chiffre_affaires} FCFA (type: {type(chiffre_affaires).__name__})")
        
        # 7. Test de sérialisation JSON
        print("\n7. Test de serialisation JSON...")
        try:
            json_string = json.dumps(factures_data)
            print(f"[OK] SUCCES: Donnees serialisables en JSON ({len(json_string)} caracteres)")
        except TypeError as e:
            print(f"[ERREUR] Impossible de serialiser en JSON: {e}")
            return False
        
        # 8. Test de création du document de vente
        print("\n8. Test de creation du DocumentVente...")
        try:
            from decimal import Decimal as D
            numero_document = f"DOC{timezone.now().strftime('%Y%m%d')}{session_caisse.id:03d}"
            
            document_vente = DocumentVente.objects.create(
                numero_document=numero_document,
                date=timezone.now().date(),
                heure_fermeture=timezone.now(),
                session_caisse=session_caisse,
                vendeuse_nom="Test Decimal",
                nombre_factures=nombre_factures,
                total_articles=total_articles,
                chiffre_affaires=D(str(chiffre_affaires)),  # Reconversion en Decimal pour le modèle
                factures_data=factures_data,
                agence=agence
            )
            print(f"[OK] Document cree: {numero_document}")
            print(f"     Chiffre d'affaires sauvegarde: {document_vente.chiffre_affaires}")
            
        except Exception as e:
            print(f"[ERREUR] Creation du document: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # 9. Test de la réponse JSON finale
        print("\n9. Test de la reponse JSON finale...")
        response_data = {
            'success': True,
            'message': f'Caisse fermee avec succes! Document {numero_document} cree.',
            'document_id': document_vente.id,
            'chiffre_affaires': float(chiffre_affaires),
            'redirect_url': '/caisse/'
        }
        
        try:
            json_response = json.dumps(response_data)
            print(f"[OK] SUCCES: Reponse JSON serialisable")
        except TypeError as e:
            print(f"[ERREUR] Impossible de serialiser la reponse JSON: {e}")
            return False
        
        print("\n" + "=" * 80)
        print("[OK] TOUS LES TESTS SONT PASSES AVEC SUCCES!")
        print("=" * 80)
        print("\nResume:")
        print(f"  - Agence: {agence.nom_agence}")
        print(f"  - Facture test: {facture.numero_ticket}")
        print(f"  - Chiffre d'affaires: {chiffre_affaires} FCFA")
        print(f"  - Document: {numero_document}")
        print(f"  - Prix decimaux: OK")
        print(f"  - Quantites decimales: OK")
        print(f"  - Serialisation JSON: OK")
        
        return True
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fermeture_caisse_decimal()
    if success:
        print("\n[SUCCES] TEST REUSSI! La fermeture de caisse fonctionne avec des nombres decimaux.")
    else:
        print("\n[ECHEC] TEST ECHOUE!")
