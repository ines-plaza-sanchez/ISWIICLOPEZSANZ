# Sistema de Reviews - Implementación con TDD

## Resumen

Se ha implementado un sistema completo de reviews (opiniones) para destinos y cruceros usando **Test-Driven Development (TDD)**. El sistema permite que usuarios registrados que hayan realizado compras dejen opiniones con ratings del 1 al 5, y muestra el promedio de valoraciones.

## Características Implementadas

### 1. **Modelos de Base de Datos** (`models.py`)

#### Modelo `Purchase`
- Registra las compras de cruceros por usuarios
- Relación de muchos-a-muchos entre usuarios y cruceros
- Restricción única para evitar duplicados

#### Modelo `DestinationReview`
- Reviews para destinos
- Campos: usuario, destino, rating (1-5), comentario, timestamp
- Métodos helper: `get_average_rating()`, `get_review_count()`
- Un usuario solo puede tener un review por destino

#### Modelo `CruiseReview`
- Reviews para cruceros
- Campos: usuario, crucero, rating (1-5), comentario, timestamp
- Métodos helper: `get_average_rating()`, `get_review_count()`
- Un usuario solo puede tener un review por crucero

#### Extensiones a Modelos Existentes
- `Destination.get_average_rating()` - Calcula el promedio de ratings
- `Destination.get_review_count()` - Cuenta el número de reviews
- `Cruise.get_average_rating()` - Calcula el promedio de ratings
- `Cruise.get_review_count()` - Cuenta el número de reviews
- `User.has_purchased_cruise()` - Verifica si el usuario compró un crucero

### 2. **Vistas** (`views.py`)

#### `DestinationReviewCreateView`
- Clase basada en vistas para crear reviews de destinos
- Requiere autenticación (LoginRequiredMixin)
- Verifica que el usuario haya comprado al menos un crucero
- Permite actualizar reviews existentes
- Redirige a la página del destino después de guardar

#### `CruiseReviewCreateView`
- Clase basada en vistas para crear reviews de cruceros
- Requiere autenticación (LoginRequiredMixin)
- Verifica que el usuario haya comprado el crucero específico
- Permite actualizar reviews existentes
- Redirige a la página del crucero después de guardar

### 3. **Templates**

#### `destination_review_form.html`
- Formulario para crear/editar reviews de destinos
- Interfaz visual con botones para seleccionar rating (1-5 estrellas)
- Campo opcional de comentario
- Mensajes de confirmación/error

#### `cruise_review_form.html`
- Formulario para crear/editar reviews de cruceros
- Interfaz visual con botones para seleccionar rating (1-5 estrellas)
- Campo opcional de comentario
- Mensajes de confirmación/error

#### `destination_detail.html` (Actualizado)
- Muestra el promedio de ratings y número total de reviews
- Lista todos los reviews existentes con autor, fecha y comentario
- Botón para escribir/editar review (solo para usuarios autenticados)
- Muestra ratings de los cruceros disponibles
- Layout mejorado con Bootstrap

#### `cruise_detail.html` (Actualizado)
- Muestra el promedio de ratings y número total de reviews
- Lista todos los reviews existentes con autor, fecha y comentario
- Botón para escribir/editar review (solo para usuarios autenticados)
- Muestra ratings de los destinos disponibles
- Layout mejorado con Bootstrap

### 4. **Tests (TDD)** (`tests.py`)

Se han escrito 10 tests para validar toda la funcionalidad:

#### Pruebas de Creación de Reviews
- ✅ `test_review_creation_with_valid_data` - Crear review con datos válidos
- ✅ `test_cruise_review_creation` - Crear review para crucero

#### Pruebas de Validación
- ✅ `test_review_rating_must_be_between_1_and_5` - Validar rango de ratings

#### Pruebas de Cálculo de Promedios
- ✅ `test_average_rating_destination` - Calcular promedio para destino
- ✅ `test_average_rating_cruise` - Calcular promedio para crucero
- ✅ `test_average_rating_no_reviews` - Promedio cuando no hay reviews

#### Pruebas de Conteo
- ✅ `test_review_count_for_destination` - Contar reviews por destino
- ✅ `test_review_count_for_cruise` - Contar reviews por crucero

#### Pruebas de Permisos
- ✅ `test_user_with_purchase_can_create_review` - Usuario con compra puede escribir
- ✅ `test_user_without_purchase_cannot_create_review` - Usuario sin compra no puede escribir

**Resultado:** Todos los tests pasan exitosamente ✅

### 5. **URLs** (`urls.py`)

Se han añadido dos nuevas rutas:
- `destination/<int:pk>/review/` → `DestinationReviewCreateView` (nombre: `destination_review`)
- `cruise/<int:pk>/review/` → `CruiseReviewCreateView` (nombre: `cruise_review`)

### 6. **Admin** (`admin.py`)

Se han registrado los nuevos modelos en el panel de administración:
- `Purchase`
- `DestinationReview`
- `CruiseReview`

### 7. **Migraciones** (`migrations/0003_cruisereview_destinationreview_purchase.py`)

Se ha creado la migración que añade las tres nuevas tablas a la base de datos.

## Restricciones de Seguridad

1. **Autenticación Requerida**: Solo usuarios registrados pueden escribir reviews
2. **Validación de Compra**: Solo usuarios que hayan comprado un crucero pueden escribir reviews
3. **Un Review por Usuario**: Cada usuario puede tener solo un review por destino/crucero
4. **Validación de Rating**: El rating debe estar entre 1 y 5
5. **Actualización**: Si un usuario ya escribió un review, puede actualizarlo

## Flujo de Usuario

1. Usuario se registra e inicia sesión
2. Usuario compra un crucero (se registra en modelo `Purchase`)
3. Usuario visita página de destino o crucero
4. Sistema muestra promedio de ratings (si existen)
5. Si usuario está autenticado y compró, ve botón "Write a Review"
6. Usuario completa formulario con rating (1-5) y comentario opcional
7. Review se guarda y se actualiza automáticamente el promedio
8. Review se muestra en la página con información del usuario y fecha

## Tecnologías Utilizadas

- **Django 5.2.9**
- **Bootstrap 5** (para UI)
- **Python 3.13**
- **SQLite** (base de datos de pruebas)

## Validación TDD

El desarrollo ha seguido estrictamente el enfoque TDD:
1. ✅ Se escribieron los tests primero
2. ✅ Se implementó el código para pasar los tests
3. ✅ Se refactorizó el código manteniendo los tests en verde
4. ✅ Todos los 10 tests pasan exitosamente

## Próximas Mejoras Posibles

1. Agregación de imágenes a reviews
2. Sistema de "helpful" para marcar reviews útiles
3. Filtrado de reviews por rating
4. Ordenamiento de reviews por fecha o utilidad
5. Notificaciones por email cuando alguien responde a un review
6. Moderación de reviews (admin)
7. Análisis de sentimiento
