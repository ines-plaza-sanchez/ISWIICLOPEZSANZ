# 🚀 Relecloud Extended - Práctica 2 ISW2

Proyecto de desarrollo colaborativo con **Azure DevOps**, **Git Flow**, **CI/CD** y **TDD**.

## 📚 Documentación del Proyecto

Este repositorio incluye documentación completa para el flujo de trabajo:

### 🎯 **Empieza aquí:**
1. **[CHECKLIST.md](CHECKLIST.md)** - ⭐ Guía rápida y checklist ejecutivo
2. **[WORKFLOW-DIAGRAMS.md](WORKFLOW-DIAGRAMS.md)** - 📊 Diagramas visuales del flujo
3. **[WORKFLOW-GUIDE.md](WORKFLOW-GUIDE.md)** - 📘 Guía metodológica completa
4. **[PT-CODE-EXAMPLES.md](PT-CODE-EXAMPLES.md)** - 💼 Ejemplos de código para cada PT
5. **[azure-pipelines.yml](azure-pipelines.yml)** - ⚙️ Pipeline CI/CD

---

## 🎓 Metodología Aplicada

- **Git Flow**: Branching strategy con feature branches
- **CI/CD**: Pipeline automatizado con Azure DevOps
- **DoD (Definition of Done)**: Criterios de completitud claros
- **QAS (Quality Attribute Scenarios)**: Criterios de aceptación
- **TDD (Test-Driven Development)**: Para PT1 y PT3
- **Code Review**: Pull Requests con aprobación obligatoria

---

## 🏗️ Estructura del Proyecto

```
ISWIICLOPEZSANZ/
├── Django_IS/                    # Aplicación Django
│   ├── manage.py
│   ├── project/                  # Configuración del proyecto
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── relecloud/                # App principal
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   ├── templates/
│   │   └── migrations/
│   └── requirements.txt
│
├── azure-pipelines.yml           # Pipeline CI/CD
├── CHECKLIST.md                  # ⭐ Empieza aquí
├── WORKFLOW-GUIDE.md             # Guía completa
├── WORKFLOW-DIAGRAMS.md          # Diagramas visuales
├── PT-CODE-EXAMPLES.md           # Ejemplos de código
└── README.md                     # Este archivo
```

---

## 🚦 Estado del Proyecto

### Pipeline CI/CD
![Pipeline Status](https://img.shields.io/badge/pipeline-configured-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Deploy](https://img.shields.io/badge/deploy-automated-blue)

### Funcionalidades (PTs)

- [x] **PT1**: Email Notifications ✉️
- [x] **PT2**: Destination Images 🖼️
- [x] **PT3**: Reviews System ⭐
- [x] **PT4**: Sort by Popularity 📊

---

## ⚡ Quick Start

### 1. Configurar Pipeline (Primera vez)

```bash
# Subir archivos al repositorio
git add .
git commit -m "Configurar pipeline CI/CD"
git push origin main

# Luego seguir pasos en CHECKLIST.md
```

### 2. Desarrollar Nueva Funcionalidad

```bash
# Crear rama feature
git checkout -b feature/PT1-email-notifications

# Desarrollar (TDD si aplica)
# ... código ...

# Commits con #ID del PBI
git commit -m "Implementar EmailService #87"

# Push → Pipeline automático
git push origin feature/PT1-email-notifications

# Crear PR cuando pipeline esté verde ✅
```

### 3. Code Review y Deploy

```
1. Crear Pull Request en Azure DevOps
2. Compañero revisa y aprueba
3. Merge a main
4. Deploy automático a Azure 🚀
```

---

## 🛠️ Configuración Local

### Requisitos

- Python 3.11
- Django 5.2.9
- PostgreSQL (producción) o SQLite (desarrollo)
- Git

### Instalación

```bash
cd Django_IS

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Ejecutar tests
python manage.py test

# Servidor de desarrollo
python manage.py runserver
```

---

## 📋 Definition of Done (DoD)

Para cerrar cualquier PBI:

- [x] ✅ Código compilable sin errores
- [x] ✅ Pruebas (Unitarias/TDD) pasadas (verde)
- [x] ✅ Pull Request aprobada por al menos 1 compañero
- [x] ✅ Pipeline de Azure ejecutado correctamente

---

## 🎯 Funcionalidades Implementadas

### PT1: Email Notifications ✉️
- Envío de email al usuario tras solicitud de información
- Notificación al admin de nuevas solicitudes
- Templates HTML para emails
- Tests TDD completos

### PT2: Destination Images 🖼️
- Campo ImageField en modelo Destination
- Gestión de imágenes desde admin
- Visualización en templates
- Almacenamiento en media/destinations/

### PT3: Reviews System ⭐
- Modelo Review con validaciones
- Solo usuarios que han comprado pueden opinar
- Cálculo de rating promedio
- Sistema de permisos robusto

### PT4: Sort by Popularity 📊
- Ordenamiento por popularidad
- Múltiples criterios (rating, reviews, score)
- Filtros en vista de destinos

---

## 🔗 Enlaces Útiles

- **Azure DevOps**: [Tu proyecto en Azure DevOps]
- **App en Producción**: https://rober-djangowebapp-babgd9bkfybugqfd.azurewebsites.net
- **Documentación Django**: https://docs.djangoproject.com/

---

## 👥 Equipo

- **Desarrollo**: Equipo ISW2
- **Metodología**: Git Flow + CI/CD
- **Revisión de Código**: Pull Requests obligatorios

---

## 📞 Soporte

Si tienes dudas:

1. Consulta **[CHECKLIST.md](CHECKLIST.md)** para guía rápida
2. Revisa **[WORKFLOW-GUIDE.md](WORKFLOW-GUIDE.md)** para detalles
3. Ver **[PT-CODE-EXAMPLES.md](PT-CODE-EXAMPLES.md)** para ejemplos

---

## 📄 Licencia

Ver [LICENSE](LICENSE) para más información.

---

**¡Proyecto configurado y listo para desarrollo colaborativo! 🎉**

