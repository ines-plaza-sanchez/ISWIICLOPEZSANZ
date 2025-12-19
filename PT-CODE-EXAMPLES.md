# 💼 EJEMPLOS PRÁCTICOS DE CÓDIGO PARA CADA PT

## 🎯 PT1: Email Notifications (TDD Recomendado)

### Paso 1: Escribir Tests PRIMERO (Red)

```python
# relecloud/tests.py

from django.test import TestCase
from django.core import mail
from django.urls import reverse
from .models import InfoRequest

class EmailNotificationTests(TestCase):
    """Tests para PT1 - Email Notifications (TDD)"""
    
    def test_info_request_sends_email_to_user(self):
        """Test: Verificar que se envía email al usuario tras solicitud"""
        # Arrange
        data = {
            'name': 'Juan Pérez',
            'email': 'juan@example.com',
            'message': 'Quiero información sobre París'
        }
        
        # Act
        response = self.client.post(reverse('info_request_create'), data)
        
        # Assert
        self.assertEqual(response.status_code, 302)  # Redirect tras éxito
        self.assertEqual(len(mail.outbox), 1)  # ❌ FALLA (aún no implementado)
        self.assertIn('Relecloud', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ['juan@example.com'])
    
    def test_email_contains_user_info(self):
        """Test: Verificar que el email contiene la info del usuario"""
        data = {
            'name': 'María García',
            'email': 'maria@example.com',
            'message': 'Consulta sobre cruceros'
        }
        
        self.client.post(reverse('info_request_create'), data)
        
        # Assert
        email_body = mail.outbox[0].body
        self.assertIn('María García', email_body)
        self.assertIn('cruceros', email_body)
    
    def test_admin_receives_notification_email(self):
        """Test: Admin recibe notificación de nueva solicitud"""
        data = {
            'name': 'Cliente Test',
            'email': 'cliente@example.com',
            'message': 'Test'
        }
        
        self.client.post(reverse('info_request_create'), data)
        
        # Debe enviar 2 emails: 1 al usuario, 1 al admin
        self.assertEqual(len(mail.outbox), 2)
        admin_email = [e for e in mail.outbox if 'admin@relecloud.com' in e.to][0]
        self.assertIsNotNone(admin_email)
```

### Paso 2: Ejecutar Tests (Deben FALLAR - Red)

```powershell
cd Django_IS
python manage.py test relecloud.tests.EmailNotificationTests

# Salida esperada:
# FAILED (failures=3)
# AssertionError: 0 != 1  (no se envían emails aún)
```

### Paso 3: Implementar Código (Green)

```python
# relecloud/services.py (Nueva clase para servicios)

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class EmailService:
    """Servicio para envío de emails"""
    
    @staticmethod
    def send_info_request_notification(info_request):
        """
        Envía email de confirmación al usuario y notificación al admin
        
        Args:
            info_request: Instancia de InfoRequest
        
        Returns:
            tuple: (emails_enviados_usuario, emails_enviados_admin)
        """
        # Email al usuario
        user_subject = 'Hemos recibido tu solicitud - Relecloud'
        user_message = render_to_string('emails/info_request_user.html', {
            'name': info_request.name,
            'message': info_request.message
        })
        
        user_emails_sent = send_mail(
            subject=user_subject,
            message='',  # Texto plano (opcional)
            html_message=user_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[info_request.email],
            fail_silently=False,
        )
        
        # Email al admin
        admin_subject = f'Nueva solicitud de información de {info_request.name}'
        admin_message = render_to_string('emails/info_request_admin.html', {
            'name': info_request.name,
            'email': info_request.email,
            'message': info_request.message
        })
        
        admin_emails_sent = send_mail(
            subject=admin_subject,
            message='',
            html_message=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        return (user_emails_sent, admin_emails_sent)
```

```python
# relecloud/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InfoRequestForm
from .services import EmailService

def info_request_create(request):
    """Vista para crear solicitud de información"""
    if request.method == 'POST':
        form = InfoRequestForm(request.POST)
        if form.is_valid():
            # Guardar solicitud
            info_request = form.save()
            
            # Enviar emails
            try:
                EmailService.send_info_request_notification(info_request)
                messages.success(
                    request, 
                    'Solicitud enviada. Recibirás un email de confirmación.'
                )
            except Exception as e:
                # Log del error pero no fallar la solicitud
                print(f"Error enviando email: {e}")
                messages.warning(
                    request,
                    'Solicitud guardada, pero hubo un problema enviando el email.'
                )
            
            return redirect('info_request_success')
    else:
        form = InfoRequestForm()
    
    return render(request, 'info_request_create.html', {'form': form})
```

```html
<!-- relecloud/templates/emails/info_request_user.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
    <h1>¡Hola {{ name }}!</h1>
    <p>Hemos recibido tu solicitud de información:</p>
    <blockquote>
        {{ message }}
    </blockquote>
    <p>Nuestro equipo te contactará pronto.</p>
    <p>Saludos,<br>El equipo de Relecloud</p>
</body>
</html>
```

```python
# project/settings.py (Configuración de email)

# Email configuration (Development - Console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@relecloud.com'
ADMIN_EMAIL = 'admin@relecloud.com'

# Email configuration (Production - SMTP)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
```

### Paso 4: Ejecutar Tests (Deben PASAR - Green)

```powershell
python manage.py test relecloud.tests.EmailNotificationTests

# Salida esperada:
# OK - All tests passed ✅
```

### Paso 5: Refactorizar (si es necesario)

### Commits para PT1:

```bash
git add relecloud/services.py
git commit -m "Crear EmailService para PT1 #87"

git add relecloud/views.py
git commit -m "Integrar envío de emails en info_request_create #87"

git add relecloud/templates/emails/
git commit -m "Añadir templates HTML para emails #87"

git add relecloud/tests.py
git commit -m "Añadir tests TDD para email notifications #87"

git add project/settings.py
git commit -m "Configurar email backend (console para dev) #87"

git push origin feature/PT1-email-notifications
```

---

## 🖼️ PT2: Destination Images (Tests Funcionales)

### Paso 1: Modificar Modelo

```python
# relecloud/models.py

from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # NUEVO: Campo para imagen
    image = models.ImageField(
        upload_to='destinations/',
        null=True,
        blank=True,
        help_text='Imagen del destino (max 5MB)'
    )
    
    # NUEVO: Método para verificar si tiene imagen
    def has_image(self):
        return bool(self.image)
    
    def __str__(self):
        return self.name
```

### Paso 2: Crear Migración

```powershell
python manage.py makemigrations
# Salida: Created migration relecloud/migrations/0002_destination_image.py

python manage.py migrate
# Salida: Applying relecloud.0002_destination_image... OK
```

### Paso 3: Actualizar Admin

```python
# relecloud/admin.py

from django.contrib import admin
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'has_image_icon', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    
    # NUEVO: Campos para edición
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description')
        }),
        ('Media', {
            'fields': ('image',),
            'description': 'Sube una imagen del destino (JPG, PNG, max 5MB)'
        }),
    )
    
    # NUEVO: Icono visual para indicar si tiene imagen
    def has_image_icon(self, obj):
        if obj.has_image():
            return '✅ Sí'
        return '❌ No'
    has_image_icon.short_description = 'Tiene Imagen'
```

### Paso 4: Configurar Media Files

```python
# project/settings.py

import os

# Media files (uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Pillow es necesario para ImageField
# Ya está en requirements.txt: pillow==12.0.0
```

```python
# project/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relecloud.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Paso 5: Actualizar Templates

```html
<!-- relecloud/templates/destination_detail.html -->
{% extends "base.html" %}

{% block content %}
<div class="destination-detail">
    <h1>{{ destination.name }}</h1>
    
    <!-- NUEVO: Mostrar imagen si existe -->
    {% if destination.image %}
        <div class="destination-image">
            <img src="{{ destination.image.url }}" 
                 alt="{{ destination.name }}"
                 class="img-fluid rounded">
        </div>
    {% else %}
        <div class="no-image">
            <p>📷 No hay imagen disponible para este destino</p>
        </div>
    {% endif %}
    
    <div class="destination-description">
        <p>{{ destination.description }}</p>
    </div>
</div>
{% endblock %}
```

```html
<!-- relecloud/templates/destinations.html -->
{% extends "base.html" %}

{% block content %}
<h1>Nuestros Destinos</h1>

<div class="row">
    {% for destination in destinations %}
    <div class="col-md-4 mb-4">
        <div class="card">
            <!-- NUEVO: Imagen en card -->
            {% if destination.image %}
                <img src="{{ destination.image.url }}" 
                     class="card-img-top" 
                     alt="{{ destination.name }}">
            {% else %}
                <div class="card-img-top bg-secondary text-white text-center py-5">
                    📷 Sin imagen
                </div>
            {% endif %}
            
            <div class="card-body">
                <h5 class="card-title">{{ destination.name }}</h5>
                <a href="{% url 'destination_detail' destination.id %}" 
                   class="btn btn-primary">Ver detalles</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

### Paso 6: Tests Funcionales

```python
# relecloud/tests.py

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Destination

class DestinationImageTests(TestCase):
    """Tests para PT2 - Destination Images"""
    
    def test_destination_can_have_image(self):
        """Test: Destino puede tener imagen asociada"""
        # Crear imagen de prueba
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        
        destination = Destination.objects.create(
            name='París',
            description='Ciudad de la luz',
            image=image
        )
        
        self.assertTrue(destination.has_image())
        self.assertIn('destinations/', destination.image.name)
    
    def test_destination_without_image(self):
        """Test: Destino puede existir sin imagen"""
        destination = Destination.objects.create(
            name='Londres',
            description='Capital del Reino Unido'
        )
        
        self.assertFalse(destination.has_image())
    
    def test_image_displayed_in_template(self):
        """Test: Imagen se muestra en template de detalle"""
        image = SimpleUploadedFile('paris.jpg', b'content', 'image/jpeg')
        destination = Destination.objects.create(
            name='París',
            image=image
        )
        
        response = self.client.get(f'/destination/{destination.id}/')
        
        self.assertContains(response, destination.image.url)
        self.assertContains(response, 'img')
```

### Commits para PT2:

```bash
git add relecloud/models.py
git commit -m "Añadir campo image al modelo Destination #101"

git add relecloud/migrations/
git commit -m "Crear migración para campo image #101"

git add relecloud/admin.py
git commit -m "Actualizar admin para gestionar imágenes #101"

git add project/settings.py project/urls.py
git commit -m "Configurar MEDIA_URL y MEDIA_ROOT #101"

git add relecloud/templates/
git commit -m "Actualizar templates para mostrar imágenes #101"

git add relecloud/tests.py
git commit -m "Añadir tests funcionales para imágenes #101"

git push origin feature/PT2-destination-images
```

---

## ⭐ PT3: Reviews System (TDD OBLIGATORIO)

### Paso 1: Diseño del Modelo (escribir tests PRIMERO)

```python
# relecloud/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Destination, Cruise, Review, Purchase

class ReviewSystemTests(TestCase):
    """Tests TDD para PT3 - Reviews System"""
    
    def setUp(self):
        """Configuración inicial para tests"""
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )
        self.destination = Destination.objects.create(
            name='París',
            description='Ciudad de la luz'
        )
        self.cruise = Cruise.objects.create(
            name='Crucero París',
            destination=self.destination,
            price=1000
        )
    
    def test_user_can_create_review_only_if_purchased(self):
        """Test: Usuario solo puede hacer review si ha comprado"""
        # Sin compra → No puede hacer review
        review = Review(
            user=self.user,
            destination=self.destination,
            rating=5,
            comment='Excelente'
        )
        
        # ❌ Debe fallar (aún no implementado)
        with self.assertRaises(ValueError):
            review.save()
        
        # Con compra → Sí puede hacer review
        Purchase.objects.create(
            user=self.user,
            cruise=self.cruise,
            amount=1000
        )
        
        review = Review.objects.create(
            user=self.user,
            destination=self.destination,
            rating=5,
            comment='Excelente'
        )
        
        self.assertEqual(review.rating, 5)
    
    def test_calculate_average_rating(self):
        """Test: Calcular rating promedio correctamente"""
        # Crear compra para permitir reviews
        Purchase.objects.create(
            user=self.user,
            cruise=self.cruise,
            amount=1000
        )
        
        # Crear 3 reviews: 5, 4, 3
        Review.objects.create(user=self.user, destination=self.destination, rating=5)
        
        user2 = User.objects.create_user('user2', password='pass')
        Purchase.objects.create(user=user2, cruise=self.cruise, amount=1000)
        Review.objects.create(user=user2, destination=self.destination, rating=4)
        
        user3 = User.objects.create_user('user3', password='pass')
        Purchase.objects.create(user=user3, cruise=self.cruise, amount=1000)
        Review.objects.create(user=user3, destination=self.destination, rating=3)
        
        # Promedio: (5+4+3)/3 = 4.0
        avg = self.destination.get_average_rating()
        self.assertEqual(avg, 4.0)
    
    def test_user_cannot_review_twice_same_destination(self):
        """Test: Usuario no puede hacer 2 reviews del mismo destino"""
        Purchase.objects.create(
            user=self.user,
            cruise=self.cruise,
            amount=1000
        )
        
        # Primera review
        Review.objects.create(
            user=self.user,
            destination=self.destination,
            rating=5
        )
        
        # Segunda review → Debe fallar
        with self.assertRaises(Exception):
            Review.objects.create(
                user=self.user,
                destination=self.destination,
                rating=3
            )
```

### Paso 2: Ejecutar Tests (RED - deben fallar)

```powershell
python manage.py test relecloud.tests.ReviewSystemTests

# Expected: FAILED (model Review doesn't exist yet)
```

### Paso 3: Implementar Modelos (GREEN)

```python
# relecloud/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Purchase(models.Model):
    """Modelo para registrar compras de cruceros"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cruise = models.ForeignKey('Cruise', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
    
    def __str__(self):
        return f'{self.user.username} - {self.cruise.name}'


class Review(models.Model):
    """Modelo para reviews de destinos"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Puntuación de 1 a 5 estrellas'
    )
    comment = models.TextField(blank=True, help_text='Comentario opcional')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ['user', 'destination']  # Un usuario solo puede hacer 1 review por destino
        ordering = ['-created_at']
    
    def clean(self):
        """Validar que el usuario haya comprado un crucero a este destino"""
        if not self.user_has_purchased_destination():
            raise ValidationError(
                'Solo puedes hacer reviews de destinos que hayas visitado (comprado)'
            )
    
    def user_has_purchased_destination(self):
        """Verificar si el usuario ha comprado algún crucero a este destino"""
        return Purchase.objects.filter(
            user=self.user,
            cruise__destination=self.destination
        ).exists()
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecutar validaciones
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.user.username} - {self.destination.name} ({self.rating}★)'


# Añadir método al modelo Destination
class Destination(models.Model):
    # ... campos existentes ...
    
    def get_average_rating(self):
        """Calcular rating promedio de este destino"""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        
        total = sum(review.rating for review in reviews)
        return round(total / len(reviews), 1)
    
    def get_review_count(self):
        """Número total de reviews"""
        return self.reviews.count()
    
    def get_popularity_score(self):
        """
        Score de popularidad basado en:
        - 70% rating promedio
        - 30% número de reviews (normalizado)
        """
        avg_rating = self.get_average_rating()
        review_count = self.get_review_count()
        
        # Normalizar review_count (max 100 reviews = score 5)
        normalized_count = min(review_count / 20, 5)
        
        return round((avg_rating * 0.7) + (normalized_count * 0.3), 2)
```

### Paso 4: Crear Migración

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Paso 5: Ejecutar Tests (GREEN - deben pasar)

```powershell
python manage.py test relecloud.tests.ReviewSystemTests
# Expected: OK ✅
```

### Paso 6: Crear Vistas y Forms

```python
# relecloud/forms.py

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} ★') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Cuéntanos tu experiencia (opcional)'
            })
        }
```

```python
# relecloud/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Destination, Review, Purchase
from .forms import ReviewForm

@login_required
def review_create(request, destination_id):
    """Vista para crear review (solo usuarios con compra)"""
    destination = get_object_or_404(Destination, id=destination_id)
    
    # Verificar que el usuario haya comprado
    has_purchased = Purchase.objects.filter(
        user=request.user,
        cruise__destination=destination
    ).exists()
    
    if not has_purchased:
        messages.error(
            request,
            'Solo puedes hacer reviews de destinos que hayas visitado.'
        )
        return redirect('destination_detail', destination_id=destination_id)
    
    # Verificar que no haya hecho review previamente
    existing_review = Review.objects.filter(
        user=request.user,
        destination=destination
    ).first()
    
    if existing_review:
        messages.warning(request, 'Ya has hecho una review de este destino.')
        return redirect('destination_detail', destination_id=destination_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.save()
            
            messages.success(request, '¡Gracias por tu review!')
            return redirect('destination_detail', destination_id=destination_id)
    else:
        form = ReviewForm()
    
    return render(request, 'review_create.html', {
        'form': form,
        'destination': destination
    })
```

### Commits para PT3:

```bash
git add relecloud/tests.py
git commit -m "Añadir tests TDD para sistema de reviews #120"

git add relecloud/models.py
git commit -m "Crear modelos Review y Purchase con validaciones #120"

git add relecloud/migrations/
git commit -m "Crear migraciones para Review y Purchase #120"

git add relecloud/forms.py relecloud/views.py
git commit -m "Implementar formulario y vista para crear reviews #120"

git add relecloud/templates/
git commit -m "Añadir templates para reviews #120"

git push origin feature/PT3-reviews-system
```

---

## 📊 PT4: Sort by Popularity

### Tests y Vista:

```python
# relecloud/tests.py

class PopularityTests(TestCase):
    """Tests para PT4 - Sort by Popularity"""
    
    def test_destinations_sorted_by_popularity(self):
        """Test: Destinos ordenados por score de popularidad"""
        # Destino A: 10 reviews, avg 4.5
        dest_a = Destination.objects.create(name='París')
        user = User.objects.create_user('user1')
        cruise_a = Cruise.objects.create(name='C1', destination=dest_a, price=1000)
        Purchase.objects.create(user=user, cruise=cruise_a, amount=1000)
        
        for i in range(10):
            Review.objects.create(user=user, destination=dest_a, rating=5 if i < 5 else 4)
        
        # Destino B: 2 reviews, avg 3.0
        dest_b = Destination.objects.create(name='Londres')
        cruise_b = Cruise.objects.create(name='C2', destination=dest_b, price=800)
        Purchase.objects.create(user=user, cruise=cruise_b, amount=800)
        Review.objects.create(user=user, destination=dest_b, rating=3)
        
        # Vista debe ordenar por popularidad
        response = self.client.get('/destinations/?sort=popularity')
        destinations = response.context['destinations']
        
        self.assertEqual(destinations[0].name, 'París')
        self.assertEqual(destinations[1].name, 'Londres')
```

```python
# relecloud/views.py

def destinations_list(request):
    """Vista de lista de destinos con ordenamiento por popularidad"""
    destinations = Destination.objects.all()
    
    # Ordenar por popularidad
    sort_by = request.GET.get('sort', 'name')
    
    if sort_by == 'popularity':
        # Ordenar por score de popularidad (descendente)
        destinations = sorted(
            destinations,
            key=lambda d: d.get_popularity_score(),
            reverse=True
        )
    elif sort_by == 'rating':
        destinations = sorted(
            destinations,
            key=lambda d: d.get_average_rating(),
            reverse=True
        )
    elif sort_by == 'reviews':
        destinations = sorted(
            destinations,
            key=lambda d: d.get_review_count(),
            reverse=True
        )
    else:
        destinations = destinations.order_by('name')
    
    return render(request, 'destinations.html', {
        'destinations': destinations,
        'sort_by': sort_by
    })
```

---

## 🎯 RESUMEN: Orden de Implementación

```
1. PT1 (TDD) → feature/PT1-email-notifications
   ├─ Tests primero (Red)
   ├─ Implementar EmailService (Green)
   ├─ Refactorizar (Refactor)
   └─ PR + Merge

2. PT2 (Funcional) → feature/PT2-destination-images
   ├─ Modificar modelo
   ├─ Migración
   ├─ Admin + Templates
   ├─ Tests funcionales
   └─ PR + Merge

3. PT3 (TDD) → feature/PT3-reviews-system
   ├─ Tests TDD primero (Red)
   ├─ Modelos Review + Purchase (Green)
   ├─ Vistas + Forms
   ├─ Templates
   └─ PR + Merge

4. PT4 (Funcional) → feature/PT4-sort-by-popularity
   ├─ Métodos en modelo Destination
   ├─ Vista con ordenamiento
   ├─ Tests de ordenamiento
   └─ PR + Merge
```

**¡Con estos ejemplos tienes todo el código necesario para cada PT!** 💼
