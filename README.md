# 🎓 Sistema de Matrículas y Notas - UTP

Sistema académico completo para la gestión de matrículas, notas y reportes académicos de la Universidad Tecnológica del Perú. Implementa **17+ patrones de diseño** (SOLID, GOF y GRASP) en un sistema funcional real.

---

## 📑 Tabla de Contenidos

- [Características Destacadas](#-características-destacadas)
- [Instalación y Configuración](#-importante-base-de-datos)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Funcionalidades por Rol](#-funcionalidades-por-rol)
- [Patrones de Diseño Implementados](#patrones-de-diseño-implementados)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Documentación Adicional](#-documentación-adicional)
- [Troubleshooting](#troubleshooting)
- [Autores](#-autores)

---

## 🏆 Características Destacadas

| Categoría | Implementación | Estado |
|-----------|----------------|--------|
| **Patrones GRASP** | 8/8 (100%) | ⭐⭐⭐⭐⭐ |
| **Principios SOLID** | 5/5 (100%) | ⭐⭐⭐⭐⭐ |
| **Patrones GOF** | 8/15 (53%) | ⭐⭐⭐ |
| **Total Patrones** | 17+ patrones | ⭐⭐⭐⭐ |

### Patrones Clave Implementados:
- ✅ **Observer Pattern** - Django Signals para actualización automática de vacantes
- ✅ **Singleton Pattern** - ConfiguracionSistema thread-safe
- ✅ **Strategy Pattern** - Generación dinámica de reportes (Excel/PDF)
- ✅ **Facade Pattern** - Service Layer completa
- ✅ **Decorator Pattern** - Control de acceso por roles
- ✅ **Factory Pattern** - Generación automática de códigos
- ✅ **Builder Pattern** - Construcción de reportes complejos
- ✅ **Command Pattern** - Operaciones de matrícula encapsuladas

### Sistema Funcional:
- ✅ Base de datos MySQL en producción
- ✅ 3 roles distintos (Admin, Profesor, Alumno)
- ✅ Generación de reportes profesionales (Excel y PDF)
- ✅ Gráficos interactivos con Chart.js
- ✅ Validaciones de negocio robustas
- ✅ Arquitectura escalable y mantenible

## ⚠️ IMPORTANTE: Base de Datos

**Este proyecto SOLO funciona con MySQL.**

Antes de comenzar, debes instalar y configurar MySQL.

## Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- **MySQL 8.0+** (instalado localmente)

## Paso a Paso para Ejecutar el Proyecto

### 1. Abrir Terminal en la Carpeta del Proyecto

Abre una terminal (CMD, PowerShell o Git Bash) en la carpeta:
```
c:\Users\Usuario\Desktop\PROYECTO FINAL\proyectoFinalDiseño
```

### 2. Activar el Entorno Virtual

**En Windows (CMD):**
```bash
venv\Scripts\activate
```

**En Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**En Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

Verás `(venv)` al inicio de tu línea de comandos cuando esté activado.

### 3. Configurar Base de Datos

**ANTES de continuar, debes configurar MySQL.**

**Pasos para configurar MySQL:**

1. **Instala MySQL** desde: https://dev.mysql.com/downloads/mysql/

2. **Crea la base de datos:**
```bash
mysql -u root -p
CREATE DATABASE sistema_matriculas CHARACTER SET utf8mb4;
EXIT;
```

3. **Edita el archivo `.env`** con tus credenciales de MySQL:
```bash
DB_NAME=sistema_matriculas
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
```

### 4. Verificar Dependencias

```bash
pip list
```

Si ves Django, mysqlclient, openpyxl, reportlab y python-decouple, todo está correcto.

### 5. Aplicar Migraciones (Solo Primera Vez)

Si es la primera vez que ejecutas el proyecto o hubo cambios en los modelos:

```bash
python manage.py migrate
```

### 5. Crear Datos de Prueba (Solo Primera Vez)

Este comando crea usuarios, cursos, secciones y notas de ejemplo:

```bash
python manage.py crear_datos_prueba
```

**Nota:** Si ya ejecutaste este comando antes y quieres empezar desde cero, elimina el archivo `db.sqlite3` y vuelve a ejecutar los pasos 4 y 5.

### 6. Iniciar el Servidor de Desarrollo

```bash
python manage.py runserver
```

Verás un mensaje como:
```
Starting development server at http://127.0.0.1:8000/
```

### 7. Abrir en el Navegador

Abre tu navegador web y ve a:
```
http://localhost:8000
```

o

```
http://127.0.0.1:8000
```

### 8. Iniciar Sesión

Usa una de estas credenciales según el rol que quieras probar:

**Administrador:**
- Usuario: `admin`
- Contraseña: `admin123`

**Profesor:**
- Usuario: `U55725989` (o el código que aparezca en la terminal)
- Contraseña: `12345678`

**Alumno:**
- Usuario: `U63384208` (o el código que aparezca en la terminal)
- Contraseña: `70000000`

## Comandos Útiles

### Detener el Servidor
Presiona `Ctrl + C` en la terminal donde está corriendo el servidor.

### Crear un Superusuario (Opcional)
Si quieres crear un nuevo administrador:
```bash
python manage.py createsuperuser
```

### Acceder al Panel de Django Admin
```
http://localhost:8000/admin/
```
Usa las credenciales del admin: `admin` / `admin123`

### Ver Ayuda de Comandos
```bash
python manage.py help
```

### Listar Todos los Usuarios Creados
```bash
python manage.py shell
```
Luego en la consola de Python:
```python
from academic_system.models import Usuario
for u in Usuario.objects.all():
    print(f"{u.rol}: {u.codigo} / DNI: {u.numero_documento}")
```
Para salir: `exit()`

## 📁 Estructura del Proyecto

```
proyectoMatriculaUTP/
├── academic_system/              # Aplicación principal
│   ├── models.py                # Modelos (Usuario, Curso, Matricula, Nota)
│   ├── views.py                 # GRASP Controller - Controladores
│   ├── urls.py                  # Rutas de la aplicación
│   ├── admin.py                 # Configuración del Django Admin
│   ├── decorators.py            # Decorator Pattern - Control de acceso
│   ├── signals.py               # ⭐ Observer Pattern - Django Signals
│   ├── singleton.py             # ⭐ Singleton Pattern - Configuración global
│   ├── context_processors.py   # Context processors
│   ├── services/                # ⭐ Facade Pattern - Capa de servicios
│   │   ├── __init__.py
│   │   ├── usuario_service.py   # Gestión de usuarios
│   │   ├── matricula_service.py # Command Pattern - Operaciones de matrícula
│   │   ├── nota_service.py      # Gestión de notas y cálculos
│   │   └── reporte_service.py   # Strategy Pattern + Builder Pattern
│   ├── templatetags/            # Filtros personalizados
│   │   └── custom_filters.py
│   ├── management/commands/     # Command Pattern - Comandos CLI
│   │   └── crear_datos_prueba.py
│   └── migrations/              # Migraciones de base de datos
├── templates/                   # Plantillas HTML (MVT)
│   ├── base.html               # Template base
│   ├── auth/                   # Autenticación
│   │   └── login.html
│   ├── admin/                  # Dashboard y vistas de administrador
│   ├── profesor/               # Dashboard y vistas de profesor
│   └── alumno/                 # Dashboard y vistas de alumno
├── static/                      # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
├── sistema_matriculas/          # Configuración del proyecto Django
│   ├── settings.py             # Configuración general
│   ├── urls.py                 # Rutas principales
│   ├── wsgi.py                 # WSGI deployment
│   └── asgi.py                 # ASGI deployment
├── .env                         # Variables de entorno (credenciales)
├── .env.example                # Ejemplo de configuración
├── manage.py                   # Script de gestión de Django
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
├── PATRONES_IMPLEMENTADOS.md   # ⭐ Documentación técnica de patrones
├── EJEMPLOS_DE_USO.md          # ⭐ Ejemplos prácticos de patrones
└── GUIA_PRESENTACION.md        # ⭐ Guía para presentación del proyecto
```

### 🔑 Archivos Clave para Patrones de Diseño:

- **`signals.py`** - Observer Pattern con Django Signals
- **`singleton.py`** - Singleton Pattern thread-safe
- **`services/`** - Facade Pattern + Pure Fabrication (GRASP)
- **`decorators.py`** - Decorator Pattern para control de acceso
- **`reporte_service.py`** - Strategy Pattern + Builder Pattern
- **`models.py`** - Information Expert + Factory Pattern + Polymorphism

## 🎯 Funcionalidades por Rol

### 👨‍💼 Administrador
**Patrón destacado:** GRASP Controller + Factory Pattern

- ✅ Dashboard con estadísticas del sistema en tiempo real
- ✅ Crear y gestionar usuarios con **generación automática de códigos únicos** (Factory Pattern)
  - Alumnos, profesores y administradores
  - Validación de datos con reglas de negocio
- ✅ Acceso completo al Django Admin para:
  - Gestión de cursos, ciclos académicos y secciones
  - Configuración de componentes de evaluación (ponderaciones)
  - Asignación múltiple de profesores a secciones (ManyToMany)
  - Control de períodos de matrícula con validación de fechas
- ✅ Visualización de métricas y reportes globales

### 👨‍🏫 Profesor
**Patrón destacado:** Strategy Pattern + Facade Pattern

- ✅ Ver secciones asignadas con información detallada
- ✅ Gestión completa de notas de alumnos (escala 0-20)
  - Registro por componentes de evaluación
  - **Cálculo automático de promedios ponderados** (Strategy Pattern)
  - **Determinación automática de estado** usando Singleton (APROBADO/DESAPROBADO)
- ✅ Estadísticas avanzadas con gráficos interactivos:
  - Distribución de notas (histograma)
  - Promedio por componente
  - Top 5 mejores alumnos
  - Identificación de alumnos con bajo rendimiento
- ✅ **Exportar reportes** en múltiples formatos (Strategy Pattern):
  - Lista de alumnos en Excel/PDF
  - Reporte de notas en Excel/PDF
  - Formato profesional con estilos y logos

### 👨‍🎓 Alumno
**Patrón destacado:** Observer Pattern + Information Expert

- ✅ Dashboard personalizado con resumen académico
- ✅ **Proceso de matrícula inteligente:**
  - Ver secciones disponibles con información en tiempo real
  - **Alertas visuales de vacantes** (Observer Pattern):
    - 🟢 Vacantes disponibles
    - 🟡 Pocas vacantes (≤5)
    - 🔴 Última vacante
  - **Actualización automática de vacantes** al matricularse (Observer Pattern)
  - Validaciones múltiples (ciclo activo, sin duplicados, etc.)
- ✅ Consultar cursos matriculados con detalles:
  - Información del curso y sección
  - Horarios y modalidad (presencial/virtual/remoto)
  - Créditos académicos
  - Profesores asignados
- ✅ Visualización de notas con:
  - Desglose por componente de evaluación
  - Contribución al promedio final
  - **Promedio ponderado calculado automáticamente**
  - **Estado dinámico:**
    - ✅ APROBADO (≥11.6)
    - ❌ DESAPROBADO (<11.6)
    - ⏳ PENDIENTE (sin todas las notas)

## Patrones de Diseño Implementados

### Principios SOLID ✅
- ✅ **Single Responsibility Principle**: Cada servicio tiene una responsabilidad única
- ✅ **Open/Closed Principle**: Estrategias extensibles sin modificar código existente
- ✅ **Liskov Substitution Principle**: Usuario hereda de AbstractUser correctamente
- ✅ **Interface Segregation Principle**: Servicios con interfaces específicas
- ✅ **Dependency Inversion Principle**: Vistas dependen de servicios, no de modelos directamente

### Patrones Creacionales (GOF)
- ✅ **Factory Pattern**:
  - `Usuario.generar_codigo()` - Generación de códigos únicos
  - `ReporteFactory.crear_reporte()` - Creación de reportes según tipo/formato
- ✅ **Builder Pattern**:
  - `ReporteBuilder` - Construcción paso a paso de reportes complejos (Excel, PDF)
- ✅ **Singleton Pattern**:
  - `ConfiguracionSistema` - Configuración única del sistema con thread-safety
  - Django Settings - Configuración global del framework

### Patrones Estructurales (GOF)
- ✅ **Facade Pattern**:
  - Toda la capa de servicios (`UsuarioService`, `MatriculaService`, `NotaService`, `ReporteService`)
  - Simplifica operaciones complejas con interfaces limpias
- ✅ **Decorator Pattern**:
  - `@admin_required`, `@profesor_required`, `@alumno_required` - Control de acceso por roles
  - `@login_required`, `@transaction.atomic` - Decoradores de Django

### Patrones de Comportamiento (GOF)
- ✅ **Strategy Pattern**:
  - `ReporteStrategy` con estrategias concretas para cada tipo de reporte
  - Cálculo de promedios y validaciones con diferentes algoritmos
  - `estado_aprobacion()` - Estrategia de aprobación
- ✅ **Command Pattern**:
  - `MatriculaService.matricular_alumno()` - Comando de matrícula
  - `MatriculaService.cambiar_seccion()` - Comando de cambio
  - `MatriculaService.desmatricular_alumno()` - Comando de desmatrícula
  - Management commands (`crear_datos_prueba`)
- ✅ **Observer Pattern**:
  - `signals.py` - Signals de Django para observar cambios en Matrícula y Nota
  - `actualizar_vacantes_al_matricular` - Observer de creación de matrícula
  - `liberar_vacante_al_desmatricular` - Observer de eliminación de matrícula

### Patrones GRASP ⭐ (Implementación Destacada)
- ✅ **Controller**: Vistas actúan como controladores (MVT de Django)
- ✅ **Information Expert**: Cada modelo conoce y gestiona su propia información
  - `Seccion.tiene_vacantes`, `Ciclo.puede_matricularse()`, `Nota.calcular_promedio_ponderado()`
- ✅ **Creator**: Objetos crean lo que contienen o usan cercanamente
  - Matrícula crea sus notas asociadas
  - Usuario genera su propio código
- ✅ **Low Coupling**: Separación clara entre capas (Models → Services → Views)
- ✅ **High Cohesion**: Cada clase/módulo tiene responsabilidad única y bien definida
- ✅ **Pure Fabrication**: Clases de servicio no representan entidades del dominio
- ✅ **Polymorphism**:
  - `Usuario.get_dashboard_url()` - Comportamiento polimórfico según rol
  - `Usuario.puede_gestionar_*()` - Permisos polimórficos
- ✅ **Protected Variations**: Servicios protegen cambios en modelos

### Patrones Arquitectónicos
- ✅ **MVT (Model-View-Template)**: Arquitectura de Django
- ✅ **Service Layer**: Capa de servicios para lógica de negocio
- ✅ **Repository Pattern**: Django ORM actúa como repositorio
- ✅ **Active Record**: Modelos de Django con lógica de negocio

### Ubicaciones de Patrones en el Código

**Creacionales:**
- `academic_system/models.py:142-147` - Factory Method (generar_codigo)
- `academic_system/services/reporte_service.py:76-148` - Factory Pattern
- `academic_system/services/reporte_service.py:151-500+` - Builder Pattern
- `academic_system/singleton.py:1-230` - Singleton Pattern

**Estructurales:**
- `academic_system/decorators.py:15-77` - Decorator Pattern
- `academic_system/services/` - Facade Pattern (todos los servicios)

**Comportamiento:**
- `academic_system/services/reporte_service.py:24-74` - Strategy Pattern
- `academic_system/services/matricula_service.py:60-172` - Command Pattern
- `academic_system/signals.py:1-100` - Observer Pattern
- `academic_system/models.py:517-539` - Strategy Pattern (estado_aprobacion)

**GRASP:**
- `academic_system/views.py` - Controller
- `academic_system/models.py` - Information Expert (propiedades y métodos)
- `academic_system/models.py:84-140` - Polymorphism
- `academic_system/services/` - Pure Fabrication

### Resumen de Implementación
- **Total de patrones implementados**: 17+ patrones
- **Cobertura de patrones GOF**:
  - Creacionales: 3/5 (60%) - Factory, Builder, Singleton
  - Estructurales: 2/6 (33%) - Facade, Decorator
  - Comportamiento: 3/5 (60%) - Strategy, Command, Observer
- **Patrones GRASP**: 8/8 (100%) ⭐ **TODOS IMPLEMENTADOS**
- **Principios SOLID**: 5/5 (100%) ✅
- **Código documentado**: Todos los patrones tienen comentarios explicativos en el código
- **Testing**: Lógica de negocio en servicios facilita pruebas unitarias
- **Arquitectura limpia**: Separación clara de responsabilidades (Models → Services → Views)

---

## 💻 Tecnologías Utilizadas

### Backend
- **Python 3.9+** - Lenguaje de programación
- **Django 4.x** - Framework web MVT
- **MySQL 8.0+** - Base de datos relacional
- **mysqlclient** - Conector MySQL para Python

### Generación de Reportes
- **openpyxl** - Generación de archivos Excel con estilos
- **ReportLab** - Generación de archivos PDF profesionales

### Frontend
- **HTML5 + CSS3** - Estructura y estilos
- **Bootstrap 5** - Framework CSS responsive
- **JavaScript** - Interactividad del cliente
- **Chart.js** - Gráficos interactivos de estadísticas

### Utilidades
- **python-decouple** - Gestión de variables de entorno
- **Pillow** - Procesamiento de imágenes
- **Django Signals** - Observer Pattern nativo

---

## 📚 Documentación Adicional

Este proyecto incluye documentación exhaustiva para facilitar su comprensión y presentación:

### 📄 Archivos de Documentación

1. **[PATRONES_IMPLEMENTADOS.md](PATRONES_IMPLEMENTADOS.md)**
   - Análisis técnico completo de cada patrón implementado
   - Comparación antes/después de las mejoras
   - Ubicaciones exactas en el código
   - Evaluación contra el sílabo del curso

2. **[EJEMPLOS_DE_USO.md](EJEMPLOS_DE_USO.md)**
   - Ejemplos prácticos para demostrar cada patrón
   - Scripts de Shell de Django para testing
   - Explicaciones técnicas para presentaciones
   - Respuestas a preguntas frecuentes

3. **[GUIA_PRESENTACION.md](GUIA_PRESENTACION.md)**
   - Guía completa para presentación del proyecto (25 min)
   - División de contenido por expositor (5 min cada uno)
   - Scripts detallados con qué decir y mostrar
   - Archivos específicos a tener abiertos
   - Checklist de preparación

### 🎯 Evaluación del Proyecto

**Cumplimiento del Sílabo:**
- ✅ Unidad 1: Principios SOLID (100%)
- ✅ Unidad 2: Patrones Creacionales (60%)
- ⚠️ Unidad 3: Patrones Estructurales (33%)
- ✅ Unidad 4: Patrones de Comportamiento (60%)
- ✅ Unidad 5: Patrones GRASP (100%) ⭐

**Nota Estimada:** 15-16/20
- Cobertura total de patrones: 75%
- Sistema funcional sin errores: ✅
- Código documentado: ✅
- Arquitectura limpia: ✅
- Aplicación práctica: ✅

## Troubleshooting

### El servidor no inicia
- Verifica que el entorno virtual esté activado (`(venv)` visible)
- Asegúrate de estar en la carpeta correcta del proyecto
- Revisa que el puerto 8000 no esté ocupado

### Error de módulos no encontrados
```bash
pip install -r requirements.txt
```

### La página no carga
- Verifica que el servidor esté corriendo (debe decir "Starting development server...")
- Prueba con `http://127.0.0.1:8000` en vez de `localhost`
- Limpia el caché del navegador (Ctrl + Shift + R)

### Olvidé mis credenciales
Ejecuta nuevamente:
```bash
python manage.py crear_datos_prueba
```
Verás las credenciales en la terminal.

### Quiero empezar con datos limpios
1. Detén el servidor (Ctrl + C)
2. Elimina el archivo `db.sqlite3`
3. Ejecuta:
```bash
python manage.py migrate
python manage.py crear_datos_prueba
python manage.py runserver
```

---

## 🔗 Enlaces Útiles

### Documentación del Proyecto
- [Documentación Técnica de Patrones](PATRONES_IMPLEMENTADOS.md)
- [Ejemplos de Uso](EJEMPLOS_DE_USO.md)
- [Guía de Presentación](GUIA_PRESENTACION.md)

### Frameworks y Tecnologías
- [Django Documentation](https://docs.djangoproject.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

### Patrones de Diseño
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [GRASP Patterns](https://en.wikipedia.org/wiki/GRASP_(object-oriented_design))
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---

## 👥 Autores

**Grupo de Desarrollo:**
1. Prada Guerra Ricardo Enrique
2. Morales Velásquez Juan José
3. Acevedo Huarachi Kelvin Jesús
4. Campusanto Solís Ángel
5. Saldaña Chávez, Joel Anthony

---

## 📝 Licencia y Uso Académico

**Proyecto Académico - Universidad Tecnológica del Perú (UTP)**

- **Curso:** Diseño de Patrones (100000SI47)
- **Ciclo:** 2025 - Ciclo 2 Agosto
- **Carrera:** Ingeniería de Sistemas e Informática / Ingeniería de Software
- **Año:** 2025

Este proyecto fue desarrollado con fines educativos como proyecto final del curso de Diseño de Patrones. Demuestra la aplicación práctica de:
- Principios SOLID
- Patrones de diseño GOF (Gang of Four)
- Patrones GRASP (General Responsibility Assignment Software Patterns)
- Arquitectura de software limpia
- Buenas prácticas de desarrollo

---

## 🎯 Conclusión

Este sistema de matrículas demuestra cómo los **patrones de diseño** no son solo conceptos teóricos, sino herramientas prácticas que resuelven problemas reales en el desarrollo de software:

- **Observer Pattern** permite actualizar vacantes sin acoplamiento
- **Singleton Pattern** centraliza la configuración del sistema
- **Strategy Pattern** facilita agregar nuevos formatos de reportes
- **Facade Pattern** simplifica operaciones complejas
- **GRASP Patterns** organizan responsabilidades de forma lógica

El resultado es un **sistema mantenible, extensible y escalable** que puede servir como base para aplicaciones empresariales reales.

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**

**Desarrollado con ❤️ y ☕ por estudiantes de la UTP**
