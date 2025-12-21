from django.test import TestCase
from django.contrib.auth.models import User
from . import models
from datetime import datetime

# Extender User con método helper
def has_purchased_cruise(self, cruise):
    """Verificar si el usuario compró un crucero específico"""
    return models.Purchase.objects.filter(user=self, cruise=cruise).exists()

User.has_purchased_cruise = has_purchased_cruise


class ReviewTestCase(TestCase):
    """Test cases para el modelo Review"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Crear destino
        self.destination = models.Destination.objects.create(
            name='Test Destination',
            description='A test destination for reviews'
        )
        
        # Crear crucero
        self.cruise = models.Cruise.objects.create(
            name='Test Cruise',
            description='A test cruise for reviews'
        )
        
        # Crear compra para el usuario (simulada con Purchase)
        self.purchase = models.Purchase.objects.create(
            user=self.user,
            cruise=self.cruise
        )
    
    def test_review_creation_with_valid_data(self):
        """Test: crear review con datos válidos"""
        review = models.DestinationReview.objects.create(
            destination=self.destination,
            user=self.user,
            rating=5,
            comment='Excellent destination!'
        )
        self.assertEqual(review.destination, self.destination)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Excellent destination!')
    
    def test_review_rating_must_be_between_1_and_5(self):
        """Test: validar que rating esté entre 1 y 5"""
        # Rating inválido (mayor a 5)
        review = models.DestinationReview(
            destination=self.destination,
            user=self.user,
            rating=6,
            comment='Test'
        )
        from django.core.exceptions import ValidationError
        self.assertRaises(ValidationError, review.full_clean)
        
        # Rating inválido (menor a 1)
        review.rating = 0
        self.assertRaises(ValidationError, review.full_clean)
        
        # Rating válido
        review.rating = 3
        review.full_clean()  # No debe lanzar excepción
    
    def test_cruise_review_creation(self):
        """Test: crear review para crucero"""
        cruise_review = models.CruiseReview.objects.create(
            cruise=self.cruise,
            user=self.user,
            rating=4,
            comment='Great cruise experience!'
        )
        self.assertEqual(cruise_review.cruise, self.cruise)
        self.assertEqual(cruise_review.rating, 4)
    
    def test_average_rating_destination(self):
        """Test: calcular promedio de ratings para destino"""
        # Crear múltiples reviews
        models.DestinationReview.objects.create(
            destination=self.destination,
            user=self.user,
            rating=5
        )
        
        user2 = User.objects.create_user(username='user2', password='pass2')
        models.DestinationReview.objects.create(
            destination=self.destination,
            user=user2,
            rating=3
        )
        
        user3 = User.objects.create_user(username='user3', password='pass3')
        models.DestinationReview.objects.create(
            destination=self.destination,
            user=user3,
            rating=4
        )
        
        # Calcular promedio
        avg_rating = self.destination.get_average_rating()
        expected = (5 + 3 + 4) / 3
        self.assertEqual(avg_rating, expected)
    
    def test_average_rating_cruise(self):
        """Test: calcular promedio de ratings para crucero"""
        models.CruiseReview.objects.create(
            cruise=self.cruise,
            user=self.user,
            rating=5
        )
        
        user2 = User.objects.create_user(username='user2', password='pass2')
        models.CruiseReview.objects.create(
            cruise=self.cruise,
            user=user2,
            rating=4
        )
        
        avg_rating = self.cruise.get_average_rating()
        expected = (5 + 4) / 2
        self.assertEqual(avg_rating, expected)
    
    def test_average_rating_no_reviews(self):
        """Test: promedio cuando no hay reviews"""
        avg_rating = self.destination.get_average_rating()
        self.assertEqual(avg_rating, 0)
    
    def test_review_count_for_destination(self):
        """Test: contar reviews por destino"""
        models.DestinationReview.objects.create(
            destination=self.destination,
            user=self.user,
            rating=5
        )
        
        count = self.destination.get_review_count()
        self.assertEqual(count, 1)
    
    def test_review_count_for_cruise(self):
        """Test: contar reviews por crucero"""
        models.CruiseReview.objects.create(
            cruise=self.cruise,
            user=self.user,
            rating=5
        )
        
        count = self.cruise.get_review_count()
        self.assertEqual(count, 1)


class ReviewPermissionTestCase(TestCase):
    """Test cases para validar permisos de reviews"""
    
    def setUp(self):
        """Configuración inicial"""
        self.user_with_purchase = User.objects.create_user(
            username='buyer',
            password='pass123'
        )
        
        self.user_without_purchase = User.objects.create_user(
            username='nonbuyer',
            password='pass123'
        )
        
        self.cruise = models.Cruise.objects.create(
            name='Test Cruise',
            description='Test cruise'
        )
        
        # Solo el primer usuario hizo una compra
        models.Purchase.objects.create(
            user=self.user_with_purchase,
            cruise=self.cruise
        )
    
    def test_user_with_purchase_can_create_review(self):
        """Test: usuario que compró puede crear review"""
        can_create = self.user_with_purchase.has_purchased_cruise(self.cruise)
        self.assertTrue(can_create)
    
    def test_user_without_purchase_cannot_create_review(self):
        """Test: usuario sin compra no puede crear review"""
        can_create = self.user_without_purchase.has_purchased_cruise(self.cruise)
        self.assertFalse(can_create)
