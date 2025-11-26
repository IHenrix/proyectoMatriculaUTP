# Sistema de Matrículas y Notas - Django

Sistema académico completo con matrículas en línea, gestión de notas y reportes. Implementado con patrones de diseño SOLID, GOF y GRASP.

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

## Estructura del Proyecto

```
proyectoFinalDiseño/
├── academic_system/          # Aplicación principal
│   ├── models.py            # Modelos de base de datos
│   ├── views.py             # Controladores (vistas)
│   ├── urls.py              # Rutas de la aplicación
│   ├── admin.py             # Configuración del admin
│   ├── decorators.py        # Decoradores de permisos
│   ├── services/            # Capa de servicios (lógica de negocio)
│   │   ├── usuario_service.py
│   │   ├── matricula_service.py
│   │   ├── nota_service.py
│   │   └── reporte_service.py
│   ├── templatetags/        # Filtros personalizados
│   └── management/commands/ # Comandos personalizados
├── templates/               # Plantillas HTML
│   ├── base.html           # Template base
│   ├── auth/               # Login
│   ├── admin/              # Templates de administrador
│   ├── profesor/           # Templates de profesor
│   └── alumno/             # Templates de alumno
├── sistema_matriculas/      # Configuración del proyecto
│   ├── settings.py         # Configuración
│   └── urls.py             # Rutas principales
├── .env                     # Variables de entorno
├── manage.py               # Script de gestión de Django
└── db.sqlite3              # Base de datos SQLite
```

## Funcionalidades por Rol

### Administrador
- Dashboard con estadísticas del sistema
- Crear y gestionar usuarios (alumnos, profesores, administradores)
- Acceso completo al Django Admin para:
  - Gestión de cursos, ciclos y secciones
  - Configuración de componentes de evaluación
  - Asignación de profesores a secciones
  - Control de períodos de matrícula

### Profesor
- Ver secciones asignadas
- Registrar y editar notas de alumnos (escala 0-20)
- Ver estadísticas con gráficos interactivos:
  - Distribución de notas
  - Promedio por componente
  - Top 5 mejores alumnos
  - Alumnos con bajo rendimiento
- Exportar reportes en Excel y PDF

### Alumno
- Dashboard personalizado
- Matricularse en secciones disponibles
- Ver alertas de vacantes (pocas vacantes, última vacante)
- Consultar cursos matriculados
- Ver notas por componente con promedio ponderado
- Ver estado: APROBADO (≥11.6), DESAPROBADO (<11.6), PENDIENTE

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
- **Cobertura**: Creacionales (3/5), Estructurales (2/6), Comportamiento (3/5), GRASP (8/8) ⭐
- **Principios SOLID**: 5/5 ✅
- **Código documentado**: Todos los patrones tienen comentarios explicativos
- **Testing**: Lógica de negocio en servicios facilita pruebas unitarias

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

## Soporte

Para más información sobre Django:
- Documentación oficial: https://docs.djangoproject.com/

## Licencia

Proyecto académico - Universidad Tecnológica del Perú (UTP)
Desarrollado con Patrones de Diseño - 2025
