# 🎨 DIAGRAMA VISUAL DEL FLUJO DE TRABAJO

## 📊 Diagrama 1: Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                     AZURE DEVOPS (Gestión)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐   │
│  │   BOARDS    │    │     REPOS    │    │    PIPELINES    │   │
│  │             │    │              │    │                 │   │
│  │ Features    │───>│ Git Flow     │───>│ CI/CD           │   │
│  │ PBIs        │    │ main         │    │ Build→Test→     │   │
│  │ Tasks       │    │ feature/*    │    │ Deploy          │   │
│  └─────────────┘    └──────────────┘    └─────────────────┘   │
│                                                 │               │
└─────────────────────────────────────────────────┼───────────────┘
                                                  │
                                                  ↓
                                    ┌─────────────────────────┐
                                    │   AZURE APP SERVICE     │
                                    │   (Producción)          │
                                    │   Django + PostgreSQL   │
                                    └─────────────────────────┘
```

---

## 🔄 Diagrama 2: Git Flow Simplificado

```
main (producción, siempre estable)
│
├─────────────────────────────────────────────────────────────>
│     merge PR      merge PR      merge PR      merge PR
│         ↑             ↑             ↑             ↑
│         │             │             │             │
├─── feature/PT1 ───┤   │             │             │
│    (1-2 días)         │             │             │
│                       │             │             │
├──────────────────── feature/PT2 ───┤             │
│                      (1-2 días)                   │
│                                                   │
├───────────────────────────────────── feature/PT3 ┤
│                                      (1-2 días)
│
├──────────────────────────────────────────────── feature/PT4
                                                   (1-2 días)

Leyenda:
  → Desarrollo en rama feature (commits frecuentes)
  ↑ Pull Request (Code Review + Aprobación)
  → Merge a main (Deploy automático)
```

---

## 🚦 Diagrama 3: Ciclo de Vida de un PBI

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: PLANIFICACIÓN (Azure Boards)                           │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─ Crear Feature en Backlog
    ├─ Crear PBIs con QAS (criterios de aceptación)
    └─ Crear Tasks técnicas
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: DESARROLLO (Local + Git)                               │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─ git checkout -b feature/PT1-xxx
    ├─ Mover Task a "In Progress" en Boards
    │
    ├─ 🔴 TDD: Escribir test (RED)
    ├─ 🟢 TDD: Implementar código (GREEN)
    ├─ 🔵 TDD: Refactorizar (REFACTOR)
    │
    ├─ git commit -m "Mensaje #PBI_ID"
    └─ git push origin feature/PT1-xxx
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: INTEGRACIÓN CONTINUA (Pipeline Automático)             │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─ ✅ Compilación sin errores (DoD #1)
    ├─ ✅ Tests pasan (DoD #2)
    └─ ✅ Pipeline verde
    │
    ↓
    ┌────────────────────────┐
    │ Pipeline ❌ FALLÓ?     │──> Arreglar código → Volver a FASE 2
    └────────────────────────┘
    │
    │ Pipeline ✅ PASÓ
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: CODE REVIEW (Pull Request)                             │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─ Crear PR en Azure DevOps
    ├─ Describir cambios + Link a PBI
    ├─ Evidencias de DoD cumplida
    │
    ├─ Compañero revisa código
    ├─ Compañero aprueba (DoD #3)
    │
    └─ Merge a main
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ FASE 5: ENTREGA CONTINUA (Deploy Automático)                   │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─ Pipeline se ejecuta en main
    ├─ ✅ Build + Tests (de nuevo)
    ├─ 🚀 Deploy a Azure App Service (DoD #4)
    │
    └─ Aplicación en producción actualizada
    │
    ↓
┌─────────────────────────────────────────────────────────────────┐
│ FASE 6: CIERRE (Azure Boards)                                  │
└─────────────────────────────────────────────────────────────────┘
    │
    ├─ Marcar Tasks como "Closed"
    ├─ Marcar PBI como "Closed"
    └─ Marcar Feature como "Closed" (cuando todos los PBIs estén cerrados)
```

---

## ⚙️ Diagrama 4: Pipeline CI/CD (Detallado)

```
┌──────────────────────────────────────────────────────────────────┐
│  TRIGGER: git push origin feature/PT1-xxx                        │
└──────────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────────┐
│  STAGE 1: BuildAndTest (SIEMPRE se ejecuta)                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Configurar Python 3.11                                 │
│  Step 2: Instalar dependencias (requirements.txt)               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Step 3: ✅ DoD #1: Código compilable sin errores      │     │
│  │  python -m py_compile manage.py                       │     │
│  │  python -m py_compile project/*.py                    │     │
│  │  python -m py_compile relecloud/*.py                  │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 4: Ejecutar migraciones (para tests)                      │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ Step 5: ✅ DoD #2: Pruebas (TDD) pasadas              │     │
│  │  python manage.py test --verbosity=2                  │     │
│  │                                                        │     │
│  │  ├─ relecloud.tests.test_models ✅                    │     │
│  │  ├─ relecloud.tests.test_views ✅                     │     │
│  │  ├─ relecloud.tests.test_emails ✅ (TDD)              │     │
│  │  └─ relecloud.tests.test_reviews ✅ (TDD)             │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  Step 6: Colectar archivos estáticos                            │
│  Step 7: Análisis de seguridad (opcional)                       │
│                                                                  │
│  Resultado: ✅ SUCCESS o ❌ FAILURE                              │
└──────────────────────────────────────────────────────────────────┘
                            ↓
                 ┌──────────────────┐
                 │ ¿Rama = main?    │
                 └──────────────────┘
                      │          │
                 ❌ No          ✅ Sí
                      │          │
                      │          ↓
                      │  ┌──────────────────────────────────────────┐
                      │  │ STAGE 2: Deploy (Solo main)              │
                      │  ├──────────────────────────────────────────┤
                      │  │                                          │
                      │  │ Step 1: Preparar archivos                │
                      │  │ Step 2: Colectar static files            │
                      │  │                                          │
                      │  │ ┌────────────────────────────────────┐  │
                      │  │ │ Step 3: ✅ DoD #4: Deploy a Azure │  │
                      │  │ │  AzureWebApp@1                     │  │
                      │  │ │  → Azure App Service               │  │
                      │  │ │  → Ejecutar migraciones            │  │
                      │  │ │  → Reiniciar app                   │  │
                      │  │ └────────────────────────────────────┘  │
                      │  │                                          │
                      │  │ Resultado: 🚀 DEPLOYED                   │
                      │  └──────────────────────────────────────────┘
                      │                    │
                      ↓                    ↓
              ⏸️ Pipeline             ┌────────────────────────────┐
              terminado               │ STAGE 3: Verify (Opcional) │
              (sin deploy)            │ Health Check de la app     │
                                      └────────────────────────────┘
```

---

## 📋 Diagrama 5: Definition of Done (DoD) en el Pipeline

```
┌───────────────────────────────────────────────────────────────┐
│                    DEFINITION OF DONE                         │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ ✅ DoD #1: Código compilable sin errores           │     │
│  │ ───────────────────────────────────────────────────│     │
│  │ Verificado por: Pipeline Step 3                    │     │
│  │ Comando: python -m py_compile *.py                 │     │
│  │ Falla si: Errores de sintaxis Python               │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ ✅ DoD #2: Pruebas (Unitarias/TDD) pasadas         │     │
│  │ ───────────────────────────────────────────────────│     │
│  │ Verificado por: Pipeline Step 5                    │     │
│  │ Comando: python manage.py test                     │     │
│  │ Falla si: Algún test falla (rojo)                  │     │
│  │ Requiere: Coverage > 80% (recomendado)             │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ ✅ DoD #3: Pull Request aprobada                   │     │
│  │ ───────────────────────────────────────────────────│     │
│  │ Verificado por: Azure DevOps Branch Policies       │     │
│  │ Requiere: Al menos 1 aprobación                    │     │
│  │ Falla si: No hay aprobaciones o hay rechazos       │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ ✅ DoD #4: Pipeline ejecutado correctamente        │     │
│  │ ───────────────────────────────────────────────────│     │
│  │ Verificado por: Pipeline completo verde            │     │
│  │ Incluye: Build + Test + Deploy (si es main)        │     │
│  │ Falla si: Cualquier stage falla                    │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## 🧪 Diagrama 6: Test-Driven Development (TDD)

```
                    CICLO TDD (Red-Green-Refactor)
                    
┌────────────────────────────────────────────────────────────────┐
│ 1️⃣  RED: Escribir test que FALLA                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  # relecloud/tests.py                                         │
│  def test_send_email_on_info_request(self):                   │
│      response = self.client.post('/info/', data)              │
│      self.assertEqual(len(mail.outbox), 1)  # ❌ FALLA        │
│                                                                │
│  Ejecutar: python manage.py test                              │
│  Resultado: ❌ FAILED (1 test)                                 │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 2️⃣  GREEN: Escribir código MÍNIMO para que pase               │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  # relecloud/views.py                                         │
│  from django.core.mail import send_mail                       │
│                                                                │
│  def info_request_create(request):                            │
│      # ... guardar formulario ...                             │
│      send_mail('Subject', 'Message', 'from@', ['to@'])        │
│      return redirect('success')                               │
│                                                                │
│  Ejecutar: python manage.py test                              │
│  Resultado: ✅ PASSED (1 test)                                 │
└────────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────────────────────────────────────────────────┐
│ 3️⃣  REFACTOR: Limpiar y mejorar código                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  # relecloud/services.py (mejor organizado)                   │
│  class EmailService:                                          │
│      @staticmethod                                            │
│      def send_info_request_notification(request_data):        │
│          # Lógica de envío aquí                               │
│          pass                                                 │
│                                                                │
│  # relecloud/views.py                                         │
│  def info_request_create(request):                            │
│      # ... guardar formulario ...                             │
│      EmailService.send_info_request_notification(data)        │
│      return redirect('success')                               │
│                                                                │
│  Ejecutar: python manage.py test                              │
│  Resultado: ✅ PASSED (1 test) - Código más limpio             │
└────────────────────────────────────────────────────────────────┘
                            ↓
                ┌──────────────────────┐
                │ ¿Más funcionalidad?  │
                └──────────────────────┘
                     │           │
                 ✅ Sí         ❌ No
                     │           │
                     ↓           ↓
            Volver a RED     Commit
```

---

## 🎯 Diagrama 7: Estructura de Azure Boards

```
BACKLOG (Vista Jerárquica)
│
├─ 📦 Feature: PT1 - Email Notifications
│   │
│   ├─ 📄 PBI #87: Como usuario quiero recibir email de confirmación
│   │   │
│   │   ├─ ✓ Task #87.1: Configurar SendGrid/SMTP
│   │   ├─ ✓ Task #87.2: Crear EmailService class
│   │   ├─ ✓ Task #87.3: Modificar info_request_create view
│   │   ├─ ✓ Task #87.4: Diseñar template de email
│   │   └─ ✓ Task #87.5: Escribir tests (TDD)
│   │
│   └─ 📄 PBI #88: Como admin quiero recibir notificación de nuevas solicitudes
│       └─ ✓ Task #88.1: ...
│
├─ 📦 Feature: PT2 - Destination Images
│   │
│   ├─ 📄 PBI #101: Como usuario quiero ver imágenes de destinos
│   │   │
│   │   ├─ ✓ Task #101.1: Añadir ImageField a modelo
│   │   ├─ ✓ Task #101.2: Crear migración
│   │   ├─ ✓ Task #101.3: Actualizar admin.py
│   │   ├─ ✓ Task #101.4: Modificar templates
│   │   └─ ✓ Task #101.5: Tests funcionales
│   │
│   └─ 📄 PBI #102: Como admin quiero optimizar imágenes automáticamente
│       └─ ✓ Task #102.1: ...
│
├─ 📦 Feature: PT3 - Reviews System
│   │
│   ├─ 📄 PBI #120: Como usuario registrado quiero dejar reviews
│   │   │  (Solo si he comprado)
│   │   │
│   │   ├─ ✓ Task #120.1: Crear modelo Review (TDD)
│   │   ├─ ✓ Task #120.2: Verificar permisos (TDD)
│   │   ├─ ✓ Task #120.3: Crear formulario de review
│   │   ├─ ✓ Task #120.4: Calcular rating promedio (TDD)
│   │   └─ ✓ Task #120.5: Mostrar reviews en templates
│   │
│   └─ 📄 PBI #121: Como usuario quiero ver valoración media
│       └─ ✓ Task #121.1: ...
│
└─ 📦 Feature: PT4 - Sort by Popularity
    │
    ├─ 📄 PBI #140: Como usuario quiero ver destinos ordenados por popularidad
    │   │
    │   ├─ ✓ Task #140.1: Añadir método get_popularity()
    │   ├─ ✓ Task #140.2: Modificar vista destinations_list
    │   ├─ ✓ Task #140.3: Tests de ordenamiento
    │   └─ ✓ Task #140.4: Añadir filtros (mejor/peor valorados)
    │
    └─ 📄 PBI #141: Como usuario quiero filtrar por número de reviews
        └─ ✓ Task #141.1: ...
```

---

## 🔄 Diagrama 8: Estados de una Task/PBI

```
       New (Creada)
           │
           ↓
       Active (En desarrollo)
           │
           ├─ Coding
           ├─ Testing
           └─ Code Review (PR)
           │
           ↓
       Resolved (PR aprobado, merge hecho)
           │
           ↓
       Closed (Feature completa, en producción)
```

---

## 💡 Diagrama 9: Escenario Completo - De Backlog a Producción

```
DÍA 1 - LUNES
─────────────────────────────────────────────────────────────────
Azure Boards:
  ├─ Crear Feature "PT2 - Destination Images"
  ├─ Crear PBI #101 con QAS
  └─ Crear Tasks bajo PBI #101

Git:
  ├─ git checkout main
  ├─ git pull origin main
  └─ git checkout -b feature/PT2-destination-images

IDE:
  ├─ Modificar models.py (añadir ImageField)
  ├─ python manage.py makemigrations
  ├─ git commit -m "Añadir ImageField al modelo Destination #101"
  └─ git push origin feature/PT2-destination-images

Azure DevOps Pipeline:
  ├─ 🔄 Build & Test ejecutándose...
  └─ ✅ SUCCESS (verde)


DÍA 2 - MARTES
─────────────────────────────────────────────────────────────────
IDE:
  ├─ Actualizar admin.py
  ├─ Modificar templates
  ├─ Escribir tests
  └─ Verificar localmente: python manage.py test

Git:
  ├─ git commit -m "Actualizar admin y templates para imágenes #101"
  ├─ git commit -m "Añadir tests para ImageField #101"
  └─ git push origin feature/PT2-destination-images

Azure DevOps Pipeline:
  ├─ 🔄 Build & Test ejecutándose...
  └─ ✅ SUCCESS (todos los tests pasan)

Azure DevOps PR:
  ├─ Crear Pull Request
  ├─ Descripción con evidencias de DoD
  ├─ Link a PBI #101
  └─ Asignar reviewer (compañero)


DÍA 3 - MIÉRCOLES
─────────────────────────────────────────────────────────────────
Azure DevOps PR:
  ├─ Compañero revisa código
  ├─ Compañero aprueba PR ✅
  └─ Merge a main

Azure DevOps Pipeline (en main):
  ├─ 🔄 Build & Test ejecutándose...
  ├─ ✅ Tests pasan
  ├─ 🚀 Deploy a Azure App Service
  └─ ✅ Deploy exitoso

Producción:
  └─ https://tu-app.azurewebsites.net
      └─ ✅ Funcionalidad disponible para usuarios

Azure Boards:
  ├─ Cerrar Tasks #101.1 - #101.5
  ├─ Cerrar PBI #101
  └─ (Si todos los PBIs están cerrados) Cerrar Feature PT2
```

---

## ✅ RESUMEN VISUAL: Todo en Una Página

```
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO COMPLETO RESUMIDO                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📋 AZURE BOARDS                 🌿 GIT FLOW                    │
│  ┌──────────────┐                ┌──────────────┐              │
│  │ Feature      │                │ main         │              │
│  │  └─ PBI      │────────────────│  └─ feature/ │              │
│  │     └─ Task  │                └──────────────┘              │
│  └──────────────┘                        │                     │
│                                           │                     │
│                                           ↓                     │
│  💻 DESARROLLO LOCAL             🔄 CI/CD PIPELINE              │
│  ┌──────────────┐                ┌──────────────┐              │
│  │ TDD:         │                │ ✅ Compile   │              │
│  │  Red→Green   │────push───────→│ ✅ Test      │              │
│  │  →Refactor   │                │ ✅ Deploy    │              │
│  └──────────────┘                └──────────────┘              │
│         │                                 │                     │
│         │                                 ↓                     │
│         │                         🚀 AZURE APP SERVICE         │
│         │                         ┌──────────────┐              │
│         └────────────────────────→│ Producción   │              │
│                                   └──────────────┘              │
│                                                                 │
│  ✅ DEFINITION OF DONE                                          │
│  ├─ [x] Código compilable                                      │
│  ├─ [x] Tests pasan (TDD)                                      │
│  ├─ [x] PR aprobada                                            │
│  └─ [x] Pipeline verde                                         │
└─────────────────────────────────────────────────────────────────┘
```

**¡Con estos diagramas tienes una visión completa del flujo de trabajo!** 📊
