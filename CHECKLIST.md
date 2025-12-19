# ✅ CHECKLIST EJECUTIVO - Configuración y Ejecución

## 🚀 CONFIGURACIÓN INICIAL (Hacer UNA VEZ)

### ☑️ Paso 1: Subir Pipeline al Repositorio (5 minutos)

```powershell
cd "c:\Users\rober\Documents\UFV\3\1 cuatri\IS2\Práctica2\ISWIICLOPEZSANZ"

# Verificar archivos creados
ls azure-pipelines.yml
ls WORKFLOW-GUIDE.md
ls WORKFLOW-DIAGRAMS.md
ls PT-CODE-EXAMPLES.md

# Subir al repositorio
git add .
git commit -m "Configurar pipeline CI/CD y documentación del flujo de trabajo"
git push origin main
```

**✅ Completado cuando:** Archivos visibles en Azure DevOps → Repos

---

### ☑️ Paso 2: Crear Service Connection (10 minutos)

1. **Azure DevOps** → Tu proyecto → **Project Settings** (⚙️ abajo izquierda)
2. **Pipelines** → **Service Connections** → **New Service Connection**
3. Seleccionar **Azure Resource Manager** → **Next**
4. **Authentication method**: Service Principal (automatic)
5. **Scope level**: Subscription
6. **Subscription**: Seleccionar tu suscripción de Azure
7. **Resource group**: Seleccionar el RG de tu App Service
8. **Service connection name**: `Azure-Service-Connection`
9. ✅ **Grant access permission to all pipelines**
10. **Save**

**✅ Completado cuando:** Service Connection aparece en la lista

---

### ☑️ Paso 3: Crear Pipeline en Azure DevOps (10 minutos)

1. **Azure DevOps** → **Pipelines** → **New Pipeline**
2. **Where is your code?** → **Azure Repos Git**
3. **Select repository** → Seleccionar tu repositorio
4. **Configure pipeline** → **Existing Azure Pipelines YAML file**
5. **Branch**: main
6. **Path**: `/azure-pipelines.yml`
7. **Continue**
8. **Review** → Verificar que el YAML es correcto
9. **Save** (no Run todavía)

**✅ Completado cuando:** Pipeline aparece en Pipelines con estado "Not run yet"

---

### ☑️ Paso 4: Editar YAML con tus Datos (5 minutos)

Abrir `azure-pipelines.yml` y cambiar:

```yaml
# Línea ~97
azureSubscription: 'Azure-Service-Connection'  # ✅ Ya está bien

# Línea ~99
appName: 'TU-APP-SERVICE-AQUI'  # 🔧 CAMBIAR por tu App Service

# Ejemplo:
appName: 'rober-djangowebapp-babgd9bkfybugqfd'
```

```powershell
# Guardar y subir cambios
git add azure-pipelines.yml
git commit -m "Configurar nombre de App Service en pipeline"
git push origin main
```

**✅ Completado cuando:** Pipeline tiene el nombre correcto de tu App Service

---

### ☑️ Paso 5: Configurar Branch Policies (IMPORTANTE) (10 minutos)

1. **Azure DevOps** → **Repos** → **Branches**
2. Click en los `...` junto a `main` → **Branch policies**
3. **Configurar políticas:**
   - ✅ **Require a minimum number of reviewers**: 1
   - ✅ **Check for linked work items**: Required (o Warning)
   - ✅ **Build Validation**:
     - Click **+** → Seleccionar tu pipeline
     - Policy requirement: Required
     - Build expiration: Immediately
4. **Save changes**

**✅ Completado cuando:** No se puede hacer merge a main sin aprobación

---

### ☑️ Paso 6: Probar Pipeline (Primera Ejecución) (15 minutos)

```powershell
# Crear rama de prueba
git checkout -b test/pipeline-initial

# Hacer cambio mínimo (ej: añadir comentario en README)
echo "# Pipeline CI/CD configurado" >> README.md

git add README.md
git commit -m "Test: Primera ejecución del pipeline"
git push origin test/pipeline-initial
```

**Ir a Azure DevOps → Pipelines:**
- Debería aparecer ejecución en progreso
- Esperar 3-5 minutos
- Verificar que todos los steps estén ✅ verdes

**Si algo falla:**
- Click en el step con error
- Leer logs
- Arreglar y volver a push

**✅ Completado cuando:** Pipeline ejecuta completamente en verde ✅

---

## 📋 FLUJO DIARIO (Para cada PT)

### 🌿 Iniciar Nueva Funcionalidad

```bash
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Crear rama feature
git checkout -b feature/PT1-email-notifications

# 3. Mover Task a "In Progress" en Azure Boards
```

---

### 💻 Desarrollar (TDD si aplica)

```python
# 4. Escribir tests PRIMERO (si es TDD)
# relecloud/tests.py
def test_nueva_funcionalidad(self):
    # Arrange
    # Act
    # Assert
    pass

# 5. Ejecutar tests (deben fallar - Red)
python manage.py test

# 6. Implementar código (Green)
# relecloud/views.py, models.py, etc.

# 7. Ejecutar tests (deben pasar - Green)
python manage.py test

# 8. Refactorizar si es necesario
```

---

### 📤 Commits y Push

```bash
# 9. Commits frecuentes con #ID del PBI
git add .
git commit -m "Implementar funcionalidad X #101"

# 10. Push a rama feature
git push origin feature/PT1-email-notifications
```

**✅ Verificar:** Pipeline se ejecuta automáticamente en Azure DevOps

---

### 🔍 Pull Request

```bash
# 11. Cuando pipeline esté verde, crear PR en Azure DevOps
```

**Plantilla de PR:**

```markdown
## 📋 Resumen
[Descripción breve de qué hace]

## 🔗 PBIs Relacionados
- Closes #101: [Título del PBI]

## ✅ Definition of Done
- [x] Código compilable sin errores ✅
- [x] Pruebas (TDD) pasadas ✅
- [x] Pipeline ejecutado correctamente ✅
- [ ] Pull Request aprobada (pendiente)

## 🎯 QAS Cumplidos
- [x] [Criterio 1]
- [x] [Criterio 2]

## 🔗 Evidencias
- Pipeline: [Link]
```

---

### ✅ Code Review y Merge

```bash
# 12. Compañero revisa y aprueba
# 13. Merge a main (botón en Azure DevOps)
# 14. Pipeline despliega automáticamente 🚀
# 15. Verificar en producción
# 16. Cerrar PBI en Azure Boards
```

---

## 🎯 CHECKLIST POR PT

### PT1: Email Notifications ✉️

- [ ] Configurar EMAIL_BACKEND en settings.py
- [ ] Crear EmailService class
- [ ] Escribir tests TDD (Red → Green → Refactor)
- [ ] Implementar envío en info_request_create view
- [ ] Crear templates de email (HTML)
- [ ] Tests pasan localmente
- [ ] Push → Pipeline verde ✅
- [ ] PR aprobado → Merge
- [ ] Cerrar PBI #87

**Tiempo estimado:** 1-2 días

---

### PT2: Destination Images 🖼️

- [ ] Añadir ImageField al modelo Destination
- [ ] Crear migración (makemigrations + migrate)
- [ ] Configurar MEDIA_URL y MEDIA_ROOT
- [ ] Actualizar admin.py para gestión de imágenes
- [ ] Modificar templates (destination_detail.html, destinations.html)
- [ ] Escribir tests funcionales
- [ ] Tests pasan localmente
- [ ] Push → Pipeline verde ✅
- [ ] PR aprobado → Merge
- [ ] Cerrar PBI #101

**Tiempo estimado:** 1-2 días

---

### PT3: Reviews System ⭐

- [ ] Crear modelos Review y Purchase
- [ ] Escribir tests TDD PRIMERO (Red)
- [ ] Implementar validaciones (solo compradores pueden hacer review)
- [ ] Implementar get_average_rating() en Destination
- [ ] Crear ReviewForm y vista review_create
- [ ] Tests TDD pasan (Green)
- [ ] Refactorizar si es necesario
- [ ] Push → Pipeline verde ✅
- [ ] PR aprobado → Merge
- [ ] Cerrar PBI #120

**Tiempo estimado:** 2 días (TDD obligatorio)

---

### PT4: Sort by Popularity 📊

- [ ] Implementar get_popularity_score() en Destination
- [ ] Modificar destinations_list view con ordenamiento
- [ ] Añadir filtros (sort=popularity, sort=rating, sort=reviews)
- [ ] Actualizar template con botones de ordenamiento
- [ ] Escribir tests de ordenamiento
- [ ] Tests pasan localmente
- [ ] Push → Pipeline verde ✅
- [ ] PR aprobado → Merge
- [ ] Cerrar PBI #140

**Tiempo estimado:** 1 día

---

## 🆘 TROUBLESHOOTING RÁPIDO

### ❌ Pipeline falla en "Código compilable"

```powershell
# Verificar localmente ANTES de push
python -m py_compile Django_IS/manage.py
python -m py_compile Django_IS/relecloud/*.py
```

---

### ❌ Pipeline falla en "Tests"

```powershell
# Ejecutar tests localmente
cd Django_IS
python manage.py test --verbosity=2

# Test específico
python manage.py test relecloud.tests.EmailNotificationTests
```

---

### ❌ No se puede hacer merge (Branch policy)

**Causas:**
- Falta aprobación de reviewer → Pedir a compañero
- Pipeline no ha ejecutado → Esperar a que termine
- Pipeline está en rojo → Arreglar errores

---

### ❌ Pipeline verde pero no despliega

**Razón:** Solo despliega en `main`, NO en ramas feature.

**Solución:** Es correcto. El deploy ocurre DESPUÉS del merge a main.

---

### ❌ Error en deploy: "Service Connection not found"

**Solución:**
1. Verificar en Project Settings → Service Connections
2. El nombre DEBE ser exactamente: `Azure-Service-Connection`
3. Si es diferente, cambiar en el YAML (línea 97)

---

## 📊 MÉTRICAS DE ÉXITO

### ✅ Pipeline Configurado Correctamente:

- [ ] Pipeline se ejecuta en cada push
- [ ] Pipeline verde ✅ en todas las ramas feature
- [ ] Deploy automático solo en main
- [ ] Branch policies activas en main

---

### ✅ DoD Cumplida en Cada PR:

- [ ] Código compila sin errores
- [ ] Todos los tests pasan
- [ ] Al menos 1 aprobación de compañero
- [ ] Pipeline ejecutado correctamente

---

### ✅ Git Flow Implementado:

- [ ] Nunca commits directos en main
- [ ] Todas las funcionalidades en ramas feature/
- [ ] Nombres de rama consistentes (feature/PTX-descripcion)
- [ ] Commits con #ID del PBI

---

### ✅ Azure Boards Actualizado:

- [ ] Todas las Features creadas
- [ ] PBIs con QAS definidos
- [ ] Tasks movidas a "Closed" tras completar
- [ ] PBIs cerrados tras merge

---

## 🎉 VALIDACIÓN FINAL

### Antes de entregar el proyecto:

- [ ] Los 4 PTs (PT1-PT4) están implementados
- [ ] Todos los PBIs están cerrados
- [ ] Pipeline siempre verde en main ✅
- [ ] Aplicación funciona en producción
- [ ] Cobertura de tests > 80% (recomendado)
- [ ] README.md actualizado con instrucciones
- [ ] Documentación completa en el repositorio

---

## 📚 DOCUMENTOS DISPONIBLES

1. **azure-pipelines.yml** → Pipeline CI/CD
2. **WORKFLOW-GUIDE.md** → Guía metodológica completa
3. **WORKFLOW-DIAGRAMS.md** → Diagramas visuales del flujo
4. **PT-CODE-EXAMPLES.md** → Ejemplos de código para cada PT
5. **Este archivo (CHECKLIST.md)** → Resumen ejecutivo

---

## 🎯 ORDEN RECOMENDADO DE LECTURA

```
1º → Este archivo (CHECKLIST.md) - Visión general
2º → WORKFLOW-DIAGRAMS.md - Entender visualmente el flujo
3º → WORKFLOW-GUIDE.md - Detalles metodológicos
4º → PT-CODE-EXAMPLES.md - Cuando vayas a programar
```

---

## ✨ RESUMEN EN 3 PASOS

```
1️⃣  SETUP (Una vez)
    └─ Configurar pipeline + Service Connection + Branch policies

2️⃣  DESARROLLO (Para cada PT)
    └─ Feature branch → TDD → Commits → Push → Pipeline verde → PR → Merge

3️⃣  VALIDACIÓN (Al terminar)
    └─ Todo verde, todo desplegado, todo documentado
```

**¡Todo listo para empezar! 🚀**

---

## 📞 CONTACTO Y AYUDA

Si tienes dudas durante el desarrollo:

1. **Revisar logs del pipeline** en Azure DevOps
2. **Consultar PT-CODE-EXAMPLES.md** para ejemplos de código
3. **Verificar WORKFLOW-GUIDE.md** para el flujo de trabajo
4. **Preguntar al equipo** en el PR o en Azure Boards

**¡Éxito con el proyecto! 🎓**
