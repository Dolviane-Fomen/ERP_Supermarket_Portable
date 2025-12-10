from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Agence,
    Compte,
    Famille,
    Article,
    MouvementStock,
)


class ConsulterMouvementsStockTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username='tester',
            password='password123',
            email='tester@example.com',
        )

        self.agence = Agence.objects.create(
            nom_agence='Agence Test',
            adresse='Adresse Test'
        )

        self.compte = Compte.objects.create(
            user=self.user,
            numero_compte='CPT001',
            type_compte='comptable',
            nom='Test',
            prenom='Utilisateur',
            telephone='0102030405',
            email='tester@example.com',
            actif=True,
            agence=self.agence,
        )

        self.famille = Famille.objects.create(
            code='ALIM',
            intitule='Alimentaire',
            unite_vente='Sac',
            suivi_stock=True,
        )

        self.article = Article.objects.create(
            reference_article='ART001',
            designation='Riz 25kg',
            categorie=self.famille,
            suivi_stock=True,
            conditionnement='Sac',
            prix_achat=Decimal('12000.00'),
            dernier_prix_achat=Decimal('12000.00'),
            unite_vente='Sac',
            prix_vente=Decimal('15000.00'),
            stock_actuel=Decimal('10.00'),
            stock_minimum=Decimal('2.00'),
            agence=self.agence,
        )

        now = timezone.now()
        MouvementStock.objects.create(
            date_mouvement=now,
            type_mouvement='entree',
            numero_piece='ENT001',
            quantite_stock=Decimal('15.000'),
            stock_initial=Decimal('5.000'),
            solde=Decimal('20.000'),
            quantite=Decimal('10.000'),
            cout_moyen_pondere=Decimal('12000.50'),
            stock_permanent=Decimal('240000.00'),
            commentaire='Entrée test',
            article=self.article,
            agence=self.agence,
        )

        MouvementStock.objects.create(
            date_mouvement=now + timezone.timedelta(hours=1),
            type_mouvement='sortie',
            numero_piece='SRT001',
            quantite_stock=Decimal('12.000'),
            stock_initial=Decimal('20.000'),
            solde=Decimal('12.000'),
            quantite=Decimal('8.000'),
            cout_moyen_pondere=Decimal('12000.50'),
            stock_permanent=Decimal('144000.00'),
            commentaire='Sortie test',
            article=self.article,
            agence=self.agence,
        )

    def test_consulter_mouvements_serialization(self):
        self.client.force_login(self.user)

        url = reverse('consulter_mouvements_stock')
        today = timezone.now().date()

        response = self.client.post(url, data={
            'date_debut': today.strftime('%Y-%m-%d'),
            'date_fin': today.strftime('%Y-%m-%d'),
            'articles': [str(self.article.id)],
            'type_mouvement': '',
        })

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload['success'])
        self.assertEqual(payload['total_mouvements'], 2)

        session = self.client.session
        mouvements_stock = session.get('mouvements_stock')
        self.assertIsNotNone(mouvements_stock)

        def assert_no_decimal(obj):
            if isinstance(obj, dict):
                for value in obj.values():
                    assert_no_decimal(value)
            elif isinstance(obj, list):
                for item in obj:
                    assert_no_decimal(item)
            else:
                self.assertNotIsInstance(obj, Decimal)

        assert_no_decimal(mouvements_stock)
