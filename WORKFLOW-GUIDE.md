# 📘 GUÍA METODOLÓGICA: Desarrollo Colaborativo con Azure DevOps

## 🎯 Objetivo del Proyecto

Aplicar prácticas profesionales de desarrollo colaborativo sobre Relecloud (Django):
- **Git Flow** para gestión de ramas
- **CI/CD** con Azure Pipelines
- **Definition of Done (DoD)** para asegurar calidad
- **Quality Attribute Scenarios (QAS)** como criterios de aceptación
- **Test-Driven Development (TDD)** para PT1 y PT3
- **Code Review** mediante Pull Requests

---

## 📊 PARTE 1: ENTENDER LA ESTRUCTURA DEL PROYECTO

### 1.1 Jerarquía en Azure Boards

```
Feature (Agrupación funcional)
  └─ PBI (Product Backlog Item = Historia de Usuario)
      └─ Task (Unidad técnica de implementación)
```

**Ejemplo para PT2 - Imágenes en Destinos:**

```
📦 Feature: PT2 - Imágenes en Destinos
   │
   ├─ 📄 PBI #101: Como usuario quiero ver imágenes de cada destino
   │   │
   │   ├─ ✓ Task #101.1: Modificar modelo Destination (añadir ImageField)
   │   ├─ ✓ Task #101.2: Crear migración de base de datos
   │   ├─ ✓ Task #101.3: Actualizar formulario en admin
   │   ├─ ✓ Task #101.4: Modificar template destination_detail.html
   │   └─ ✓ Task #101.5: Escribir tests (TDD)
   │
   └─ 📄 PBI #102: Como admin quiero subir múltiples imágenes
       └─ ✓ Task #102.1: ... (y así sucesivamente)
```

### 1.2 Definition of Done (DoD)

**Para cerrar cualquier PBI, DEBE cumplir:**

- [x] ✅ **Código compilable sin errores** → Pipeline verde
- [x] ✅ **Pruebas (Unitarias/TDD) pasadas** → `python manage.py test`
- [x] ✅ **Pull Request aprobada** → Al menos 1 compañero (Code Review)
- [x] ✅ **Pipeline de Azure ejecutado correctamente** → CI/CD completo

### 1.3 Quality Attribute Scenarios (QAS)

Los **criterios de aceptación** deben escribirse como QAS. Ejemplo:

```markdown
## QAS para PT2 (Imágenes en Destinos)

**Escenario 1: Carga de imagen**
- **Estímulo**: Admin sube imagen de destino (< 5MB, formato JPG/PNG)
- **Respuesta**: Sistema almacena imagen y la asocia al destino
- **Medida**: Tiempo de carga < 3 segundos, sin errores

**Escenario 2: Visualización**
- **Estímulo**: Usuario accede a detalle de destino con imagen
- **Respuesta**: Sistema muestra imagen optimizada
- **Medida**: Página carga en < 2 segundos, imagen responsive

**Escenario 3: Mantenibilidad**
- **Estímulo**: Desarrollador modifica modelo Destination
- **Respuesta**: Tests detectan cambios incompatibles
- **Medida**: Coverage > 80%, tests ejecutan en < 30 segundos
```

---

## 🌿 PARTE 2: GIT FLOW - METODOLOGÍA DE BRANCHING

### 2.1 Estructura de Ramas

```
main (producción)
  │
  └─ feature/PT1-email-notifications  ← Rama de trabajo
  └─ feature/PT2-destination-images   ← Rama de trabajo
  └─ feature/PT3-reviews-system       ← Rama de trabajo
  └─ feature/PT4-sort-by-popularity   ← Rama de trabajo
  └─ hotfix/fix-critical-bug          ← Correcciones urgentes
```

**Reglas de Git Flow:**
- **main**: Solo código estable y desplegable. NUNCA commits directos.
- **feature/***: Ramas de 1-2 días para cada PT. Se eliminan tras merge.
- **hotfix/***: Correcciones urgentes que van directo a main.

### 2.2 Nomenclatura de Ramas

```bash
# ✅ CORRECTO
feature/PT1-email-notifications
feature/PT2-destination-images
feature/PT3-reviews-system
hotfix/fix-login-error

# ❌ INCORRECTO
mi-rama
test
nuevos-cambios
```

### 2.3 Nomenclatura de Commits

**SIEMPRE** referenciar el PBI o Task:

```bash
# ✅ CORRECTO (referencia #ID del PBI/Task en Azure DevOps)
git commit -m "Añadir ImageField al modelo Destination #101"
git commit -m "Implementar envío de emails con SendGrid #87"
git commit -m "Fix: Corregir migración de reviews #103"

# ❌ INCORRECTO
git commit -m "cambios"
git commit -m "update"
git commit -m "fix bug"
```

**Beneficio**: Azure DevOps vincula automáticamente el commit con el PBI/Task.

---

## 🔄 PARTE 3: FLUJO DE TRABAJO COMPLETO (PASO A PASO)

### 📌 Ejemplo Real: Implementar PT2 (Imágenes en Destinos)

#### **FASE 1: PLANIFICACIÓN (Azure Boards)**

1. **Crear Feature en Azure Boards:**
   - Ir a **Boards** → **Backlogs**
   - New Work Item → **Feature**
   - Título: `PT2 - Imágenes en Destinos`
   - Descripción: Incluir QAS (Scenarios)

2. **Crear PBIs bajo la Feature:**
   - New Work Item → **Product Backlog Item**
   - Título: `Como usuario quiero ver imágenes de cada destino`
   - Acceptance Criteria (QAS):
     ```markdown
     - [x] El modelo Destination tiene campo image
     - [x] Se pueden subir imágenes desde admin
     - [x] Las imágenes se muestran en templates
     - [x] Tests coverage > 80%
     ```
   - Vincular a Feature PT2

3. **Crear Tasks bajo el PBI:**
   - Task #1: Modificar modelo Destination
   - Task #2: Crear migración
   - Task #3: Actualizar admin.py
   - Task #4: Modificar templates
   - Task #5: Escribir tests

#### **FASE 2: DESARROLLO LOCAL (Git + TDD)**

4. **Crear rama feature desde main:**

```powershell
# Asegurarse de estar en main actualizado
git checkout main
git pull origin main

# Crear rama feature
git checkout -b feature/PT2-destination-images

# Verificar rama actual
git branch
# Salida: * feature/PT2-destination-images
```

5. **Mover Task a "In Progress" en Azure Boards:**
   - Ir a **Boards** → **Tasks**
   - Arrastrar Task #1 a columna "Active"

6. **Desarrollo con TDD (opcional pero recomendado):**

```python
# 1. PRIMERO: Escribir test (Red)
# relecloud/tests.py
def test_destination_has_image_field(self):
    destination = Destination.objects.create(name="París")
    self.assertTrue(hasattr(destination, 'image'))

# 2. Ejecutar test → FALLA ❌
python manage.py test

# 3. LUEGO: Implementar código (Green)
# relecloud/models.py
class Destination(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)

# 4. Ejecutar test → PASA ✅
python manage.py test

# 5. REFACTOR: Limpiar código si es necesario
```

7. **Hacer commits frecuentes:**

```powershell
# Después de implementar modelo
git add relecloud/models.py
git commit -m "Añadir campo image al modelo Destination #101"

# Después de crear migración
python manage.py makemigrations
git add relecloud/migrations/
git commit -m "Crear migración para campo image #101"

# Después de actualizar admin
git add relecloud/admin.py
git commit -m "Permitir subida de imágenes en admin #101"

# Después de tests
git add relecloud/tests.py
git commit -m "Añadir tests para campo image (TDD) #101"
```

8. **Push a la rama feature:**

```powershell
git push origin feature/PT2-destination-images
```

#### **FASE 3: PIPELINE CI (Automático)**

9. **El pipeline se ejecuta AUTOMÁTICAMENTE** tras el push:

```
Azure DevOps → Pipelines
   ↓
🔄 Running pipeline for feature/PT2-destination-images
   ↓
📦 Stage 1: BuildAndTest
   ├─ ✅ DoD #1: Código compilable sin errores
   ├─ ✅ DoD #2: Pruebas (TDD) pasadas (verde)
   └─ ✅ Colectar archivos estáticos
   ↓
⏸️  Stage 2: Deploy (SKIP - no es main)
   ↓
✅ Pipeline completed successfully
```

10. **Si el pipeline FALLA:**

```powershell
# Ver el error en Azure DevOps → Pipelines → Ver logs
# Arreglar localmente
git add .
git commit -m "Fix: Corregir test de imagen #101"
git push origin feature/PT2-destination-images
# Pipeline se ejecuta de nuevo automáticamente
```

#### **FASE 4: PULL REQUEST Y CODE REVIEW**

11. **Crear Pull Request (cuando todo esté verde ✅):**

```
Azure DevOps → Repos → Pull Requests → New Pull Request

De: feature/PT2-destination-images
A:  main

Título: PT2: Implementar imágenes en destinos

Descripción:
```

```markdown
## 📋 Resumen
Implementación completa de PT2: Imágenes en destinos

## 🔗 PBIs Relacionados
- Closes #101: Ver imágenes de destinos

## ✅ Definition of Done (DoD)
- [x] Código compilable sin errores (pipeline verde ✅)
- [x] Pruebas (Unitarias/TDD) pasadas ✅
- [x] Pipeline ejecutado correctamente ✅
- [ ] Pull Request aprobada (pendiente revisión)

## 🎯 Quality Attribute Scenarios (QAS) Cumplidos
- [x] Admin puede subir imágenes < 5MB
- [x] Usuarios ven imágenes en detalle de destino
- [x] Imágenes son responsive
- [x] Tests coverage > 80%

## 🔗 Evidencias
- Link al pipeline run: [Ver aquí](https://dev.azure.com/.../pipelines/123)
- Screenshots: (adjuntar si es necesario)

## 📝 Notas para Reviewers
- Revisar migración en relecloud/migrations/000X_add_image.py
- Verificar que ImageField tiene upload_to='destinations/'
- Comprobar tests en relecloud/tests.py
```

12. **Asignar Reviewers:**
   - Añadir al menos 1 compañero como reviewer
   - Añadir políticas de branch (opcional):
     - Mínimo 1 aprobación
     - Build exitoso requerido

13. **Code Review (Compañero):**

```
Compañero revisa:
  ├─ ✓ Código sigue estándares
  ├─ ✓ Tests son adecuados
  ├─ ✓ Sin hardcoded values
  ├─ ✓ Migración correcta
  └─ ✓ Pipeline verde ✅

Compañero aprueba:
  └─ Click en "Approve"
```

14. **Merge a main:**

```
Cuando hay aprobación:
  └─ Click en "Complete Pull Request"
      ├─ Delete source branch: ✅ (limpiar rama feature)
      ├─ Complete associated work items: ✅ (cerrar PBI #101)
      └─ Merge type: "Squash commit" o "Merge commit"
```

#### **FASE 5: DEPLOY AUTOMÁTICO (CD)**

15. **Pipeline se ejecuta en main AUTOMÁTICAMENTE:**

```
Azure DevOps → Pipelines
   ↓
🔄 Running pipeline for main (after merge)
   ↓
📦 Stage 1: BuildAndTest
   ├─ ✅ DoD #1: Código compilable
   ├─ ✅ DoD #2: Tests pasan
   └─ ✅ Static files collected
   ↓
🚀 Stage 2: Deploy to Azure App Service
   ├─ ✅ DoD #3: Deploy a producción
   ├─ ✅ Aplicación actualizada
   └─ ✅ Migrations ejecutadas
   ↓
✅ Pipeline completed - App live in production!
```

16. **Verificar en producción:**

```powershell
# Abrir en navegador
https://rober-djangowebapp-babgd9bkfybugqfd.azurewebsites.net

# Verificar que la funcionalidad está disponible
```

17. **Cerrar Feature en Azure Boards:**
   - Ir a **Boards** → **Features**
   - Cambiar estado de PT2 a "Closed"

---

## 🔧 PARTE 4: CONFIGURACIÓN INICIAL DEL PIPELINE

### Paso 1: Subir archivo YAML al repositorio

```powershell
cd "c:\Users\rober\Documents\UFV\3\1 cuatri\IS2\Práctica2\ISWIICLOPEZSANZ"

# Verificar que azure-pipelines.yml existe
ls azure-pipelines.yml

# Subir al repo
git add azure-pipelines.yml
git commit -m "Añadir pipeline CI/CD para cumplir DoD"
git push origin main
```

### Paso 2: Configurar Service Connection

1. **Azure DevOps** → **Project Settings** (abajo izquierda)
2. **Pipelines** → **Service Connections**
3. **New Service Connection** → **Azure Resource Manager**
4. **Configurar:**
   - Authentication method: **Service Principal (automatic)**
   - Scope level: **Subscription**
   - Subscription: (Seleccionar tu suscripción de Azure)
   - Resource group: (El de tu App Service)
   - Service connection name: `Azure-Service-Connection`
   - ✅ Grant access permission to all pipelines
5. **Save**

### Paso 3: Crear Pipeline en Azure DevOps

1. **Pipelines** → **New Pipeline**
2. **Where is your code?** → **Azure Repos Git**
3. **Select repository** → (Tu repositorio)
4. **Configure pipeline** → **Existing Azure Pipelines YAML file**
5. **Select YAML file:**
   - Branch: `main`
   - Path: `/azure-pipelines.yml`
6. **Continue** → **Run** (primera ejecución)

### Paso 4: Configurar Branch Policies (Importante!)

Para forzar el cumplimiento de DoD:

1. **Repos** → **Branches**
2. Click en `main` → **Branch Policies**
3. **Configurar:**
   - ✅ **Require a minimum number of reviewers**: 1
   - ✅ **Check for linked work items**: Warning
   - ✅ **Build Validation**: Añadir pipeline
   - ✅ **Status Checks**: Required

### Paso 5: Editar YAML con tus datos

```yaml
# Línea 97: Tu Service Connection
azureSubscription: 'Azure-Service-Connection'

# Línea 99: Tu App Service
appName: 'rober-djangowebapp-babgd9bkfybugqfd'

# Línea 115: Tu URL
curl -f https://rober-djangowebapp-babgd9bkfybugqfd.azurewebsites.net
```

---

## 📝 PARTE 5: PLANTILLA PARA CADA PT

### PT1: Email Notifications

**Feature**: Envío de correos electrónicos
**Rama**: `feature/PT1-email-notifications`
**Enfoque**: TDD recomendado

```python
# Tests primero (TDD)
def test_info_request_sends_email(self):
    # Crear solicitud
    response = self.client.post('/info-request/', data)
    # Verificar email enviado
    self.assertEqual(len(mail.outbox), 1)
    self.assertIn('Relecloud', mail.outbox[0].subject)
```

**QAS Ejemplo**:
```markdown
- Estímulo: Usuario envía formulario info_request
- Respuesta: Sistema envía email real en < 5 segundos
- Medida: 99% de emails entregados, logs de error < 1%
```

### PT2: Destination Images

**Feature**: Imágenes en destinos
**Rama**: `feature/PT2-destination-images`
**Enfoque**: Tests funcionales

```python
def test_destination_image_upload(self):
    with open('test_image.jpg', 'rb') as img:
        destination = Destination.objects.create(
            name="París",
            image=SimpleUploadedFile("paris.jpg", img.read())
        )
    self.assertTrue(destination.image)
```

### PT3: Reviews System

**Feature**: Sistema de reviews
**Rama**: `feature/PT3-reviews-system`
**Enfoque**: TDD OBLIGATORIO

```python
# TDD: Tests primero
def test_only_buyers_can_review(self):
    # Usuario sin compra NO puede hacer review
    response = self.client.post('/review/', data)
    self.assertEqual(response.status_code, 403)
    
def test_average_rating_calculation(self):
    # Crear 3 reviews: 5, 4, 3
    avg = destination.get_average_rating()
    self.assertEqual(avg, 4.0)
```

### PT4: Sort by Popularity

**Feature**: Ordenar por popularidad
**Rama**: `feature/PT4-sort-by-popularity`
**Enfoque**: Tests funcionales

```python
def test_destinations_sorted_by_reviews(self):
    # Destino A: 10 reviews, Destino B: 5 reviews
    response = self.client.get('/destinations/')
    destinations = response.context['destinations']
    self.assertEqual(destinations[0].name, "Destino A")
```

---

## 🎯 PARTE 6: CHECKLIST DIARIO

### Al empezar el día:

```powershell
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Crear rama para nueva tarea
git checkout -b feature/PT1-email-notifications

# 3. Mover Task a "In Progress" en Azure Boards
```

### Durante el desarrollo:

```bash
# 4. Commits frecuentes con #ID
git add .
git commit -m "Implementar envío de emails #87"
git push origin feature/PT1-email-notifications

# 5. Verificar pipeline en Azure DevOps
# https://dev.azure.com/tu-org/tu-proyecto/_build
```

### Al terminar funcionalidad:

```bash
# 6. Asegurar que tests pasan localmente
python manage.py test

# 7. Push final
git push origin feature/PT1-email-notifications

# 8. Crear Pull Request en Azure DevOps
# 9. Pedir revisión a compañero
# 10. Esperar aprobación + merge
```

---

## 🚨 TROUBLESHOOTING

### Error: "Pipeline failed - Code not compilable"

```powershell
# Verificar localmente ANTES de push
python -m py_compile Django_IS/manage.py
python -m py_compile Django_IS/relecloud/*.py
```

### Error: "Tests failed"

```powershell
# Ejecutar tests localmente
cd Django_IS
python manage.py test --verbosity=2

# Ver detalles del error
python manage.py test relecloud.tests.TestDestination --verbosity=2
```

### Error: "No Service Connection"

- Verificar en **Project Settings** → **Service Connections**
- El nombre DEBE coincidir con `azureSubscription` en el YAML

### Pipeline verde pero no despliega

- Solo despliega en **main**, NO en feature branches
- Verificar condición en el YAML:
  ```yaml
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  ```

---

## 📚 RECURSOS ADICIONALES

### Comandos Git útiles

```powershell
# Ver estado actual
git status

# Ver ramas
git branch -a

# Cambiar de rama
git checkout main

# Eliminar rama local (tras merge)
git branch -d feature/PT2-destination-images

# Ver historial
git log --oneline --graph
```

### Tests en Django

```python
# Ejecutar todos los tests
python manage.py test

# Tests de una app específica
python manage.py test relecloud

# Test específico con verbosity
python manage.py test relecloud.tests.TestDestination.test_image_upload --verbosity=2

# Con coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## ✅ RESUMEN: Flujo Completo en 10 Pasos

```
1️⃣  Planificar en Azure Boards (Feature → PBI → Tasks)
2️⃣  Crear rama feature desde main
3️⃣  Desarrollar con TDD (Red → Green → Refactor)
4️⃣  Commits frecuentes con #ID del PBI
5️⃣  Push → Pipeline automático (Build + Tests)
6️⃣  Si pipeline verde ✅ → Crear Pull Request
7️⃣  Compañero hace Code Review
8️⃣  Compañero aprueba PR
9️⃣  Merge a main → Deploy automático 🚀
🔟 Cerrar PBI y Feature en Azure Boards
```

**¡El pipeline está configurado y listo para usar!** 🎉
