from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

# Create your models here.
class Destination(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    image = models.ImageField(
        upload_to='destinations/',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        """Obtener la valoración media de los reviews de este destino"""
        avg = self.destination_reviews.aggregate(Avg('rating'))['rating__avg']
        return avg if avg is not None else 0
    
    def get_review_count(self):
        """Obtener el número de reviews de este destino"""
        return self.destination_reviews.count()

class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises'
    )
    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        """Obtener la valoración media de los reviews de este crucero"""
        avg = self.cruise_reviews.aggregate(Avg('rating'))['rating__avg']
        return avg if avg is not None else 0
    
    def get_review_count(self):
        """Obtener el número de reviews de este crucero"""
        return self.cruise_reviews.count()

class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT
    )

class Purchase(models.Model):
    """Modelo para registrar compras de cruceros por usuarios"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'cruise')
    
    def __str__(self):
        return f"{self.user.username} - {self.cruise.name}"

class DestinationReview(models.Model):
    """Modelo para reviews de destinos"""
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='destination_reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='destination_reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5'
    )
    comment = models.TextField(
        max_length=1000,
        blank=True,
        default=''
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('destination', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.destination.name} ({self.rating}★)"

class CruiseReview(models.Model):
    """Modelo para reviews de cruceros"""
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.CASCADE,
        related_name='cruise_reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cruise_reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5'
    )
    comment = models.TextField(
        max_length=1000,
        blank=True,
        default=''
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cruise', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.cruise.name} ({self.rating}★)"