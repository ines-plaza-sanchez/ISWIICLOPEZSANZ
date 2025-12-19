# � GUÍA COMPLETA: CI/CD con Azure DevOps - Proyecto Relecloud

## 🎓 Contexto Académico

Esta guía aplica conceptos de **Ingeniería del Software II** para implementar:
- **Git Flow**: Metodología de branching
- **CI/CD**: Integración y Entrega Continua
- **DoD (Definition of Done)**: Criterios de completitud
- **QAS (Quality Attribute Scenarios)**: Criterios de aceptación
- **TDD (Test-Driven Development)**: Desarrollo guiado por pruebas
- **Code Review**: Revisión de código mediante Pull Requests

---

## 📋 Checklist de Configuración Inicial

### PASO 1: Subir el archivo del pipeline al repositorio

```powershell
# Desde la carpeta raíz del proyecto (ISWIICLOPEZSANZ)
git add azure-pipelines.yml
git commit -m "Añadir pipeline CI/CD para cumplir DoD"
git push origin main
```

---

### PASO 2: Configurar Service Connection en Azure DevOps

1. **Ir a Azure DevOps** → Tu proyecto → **Project Settings** (abajo a la izquierda)

2. **Pipelines** → **Service Connections**

3. **New Service Connection** → **Azure Resource Manager**

4. **Seleccionar:**
   - Authentication method: **Service Principal (automatic)**
   - Scope level: **Subscription**
   - Selecciona tu suscripción de Azure
   - Resource group: (el de tu App Service)
   - Service connection name: `Azure-Service-Connection`
   - ✅ Grant access permission to all pipelines

5. **Save**

---

### PASO 3: Crear el Pipeline en Azure DevOps

1. **Ir a Pipelines** → **New Pipeline**

2. **Where is your code?** → **Azure Repos Git**

3. **Select a repository** → (Tu repositorio)

4. **Configure your pipeline** → **Existing Azure Pipelines YAML file**

5. **Select an existing YAML file:**
   - Branch: `main`
   - Path: `/azure-pipelines.yml`

6. **Continue** → **Save** (no Run todavía)

---

### PASO 4: Configurar Variables (si es necesario)

1. En el pipeline recién creado → **Edit**

2. **Variables** (arriba a la derecha) → **New variable**

3. Añadir estas si las necesitas:
   ```
   DJANGO_SECRET_KEY = tu-secret-key-aqui (🔒 Keep this value secret)
   DATABASE_URL = tu-connection-string (🔒 Keep this value secret)
   ```

---

### PASO 5: Editar el archivo YAML con tus datos

Abre `azure-pipelines.yml` y cambia estas líneas:

```yaml
# Línea 97: Nombre de tu Service Connection
azureSubscription: 'Azure-Service-Connection'  # 👈 Debe coincidir con el nombre del PASO 2

# Línea 99: Nombre de tu Azure App Service
appName: 'rober-djangowebapp-babgd9bkfybugqfd'  # 👈 Tu App Service en Azure

# Línea 115: URL de verificación
curl -f https://rober-djangowebapp-babgd9bkfybugqfd.azurewebsites.net  # 👈 Tu URL
```

---

### PASO 6: Probar el Pipeline

#### Opción A: Con una rama de prueba (RECOMENDADO)

```powershell
# Crear rama de prueba
git checkout -b feature/test-pipeline

# Hacer un cambio mínimo (ej: agregar comentario)
# Editar un archivo cualquiera

git add .
git commit -m "Test: Probar pipeline CI/CD #123"
git push origin feature/test-pipeline
```

1. El pipeline se ejecutará automáticamente
2. Ve a **Pipelines** en Azure DevOps para ver el progreso
3. Verifica que pase todas las etapas:
   - ✅ Build y Tests
   - ⏸️ Deploy (no se ejecuta en ramas feature)

#### Opción B: Directamente en main (no recomendado al principio)

```powershell
git push origin main
```

---

## 🎯 Flujo de Trabajo Completo con el Pipeline

### Para cada nueva funcionalidad:

```
1️⃣ Crear rama feature
   git checkout -b feature/PT1-email-notifications

2️⃣ Desarrollar (commits frecuentes)
   git add .
   git commit -m "Implementar envío de emails #456"
   git push origin feature/PT1-email-notifications

3️⃣ Pipeline se ejecuta AUTOMÁTICAMENTE ✨
   - ✅ Verifica código compilable
   - ✅ Ejecuta todos los tests
   - ❌ Si algo falla → arreglar y volver al paso 2

4️⃣ Cuando todo esté verde → Crear Pull Request
   Azure DevOps → Repos → Pull Requests → New Pull Request
   
   Descripción del PR:
   ```markdown
   ## Funcionalidad
   PT1: Envío de emails en info_request
   
   ## PBIs relacionados
   - #456: Enviar email al recibir solicitud
   
   ## DoD Cumplida
   - [x] Código compilable sin errores (pipeline verde ✅)
   - [x] Pruebas (TDD) pasadas (pipeline verde ✅)
   - [x] Pipeline ejecutado correctamente (ver link abajo)
   - [ ] Pull Request aprobada por compañero (pendiente)
   
   ## Link al Pipeline
   [Ver ejecución del pipeline](link-del-pipeline-run)
   ```

5️⃣ Compañero revisa el código
   - Lee el código en el PR
   - Verifica que el pipeline esté verde ✅
   - Aprueba el PR

6️⃣ Merge a main
   - Pipeline se ejecuta de nuevo
   - Esta vez SÍ despliega a Azure 🚀
   - Aplicación actualizada en producción

7️⃣ Cerrar PBIs en Azure Boards
```

---

## 🔍 Cómo Verificar que Funciona

### Ver logs del pipeline:

1. **Azure DevOps** → **Pipelines**
2. Click en la última ejecución
3. Ver cada stage:
   - **BuildAndTest**: debe estar verde ✅
   - **Deploy**: solo se ejecuta en main
   - **Verify**: health check final

### Puntos clave a verificar:

```
✅ "DoD: Código compilable sin errores" → Verde
✅ "DoD: Pruebas (Unitarias/TDD) pasadas" → Verde  
✅ "DoD: Pipeline de Azure ejecutado correctamente" → Verde
```

---

## 🐛 Troubleshooting

### Si el pipeline falla en "Código compilable":
```powershell
# Verificar localmente antes de push
python -m py_compile Django_IS/manage.py
```

### Si falla en "Tests":
```powershell
# Ejecutar tests localmente
cd Django_IS
python manage.py test
```

### Si falla en "Deploy":
- Verificar que el Service Connection esté bien configurado
- Verificar que el nombre del App Service sea correcto
- Revisar logs en Azure DevOps → Pipeline → Deploy stage

---

## 📝 Recordatorios

- **SIEMPRE** trabajar en ramas feature (nunca directamente en main)
- **NUNCA** hacer merge sin que el pipeline esté verde ✅
- **SIEMPRE** referenciar PBIs en commits: `git commit -m "Mensaje #123"`
- **VERIFICAR** que el PR tenga aprobación antes de merge

---

## 🎓 Para los PTs del proyecto

### PT1: Email Notifications
```
Rama: feature/PT1-email-notifications
Tests: test_email_sending, test_info_request_triggers_email
DoD: Pipeline debe pasar tests de envío de emails
```

### PT2: Destination Images  
```
Rama: feature/PT2-destination-images
Tests: test_image_upload, test_image_display
DoD: Pipeline debe pasar tests de subida de imágenes
```

### PT3: Reviews System
```
Rama: feature/PT3-reviews-system
Tests: test_review_creation, test_review_permissions, test_average_rating
DoD: Pipeline debe pasar tests de reviews (TDD recomendado)
```

### PT4: Sort by Popularity
```
Rama: feature/PT4-sort-by-popularity
Tests: test_destination_ordering, test_popularity_calculation
DoD: Pipeline debe pasar tests de ordenamiento
```

---

## ✅ Confirmación de que todo está bien configurado

Cuando hagas tu primer push, deberías ver:

1. En **Azure DevOps → Pipelines**: Ejecución en progreso 🔄
2. Después de 3-5 minutos: ✅ Verde en todos los checks
3. En cada PR: Link automático al pipeline run
4. En main: Deploy automático a Azure

**¡El pipeline está listo para usar!** 🎉
