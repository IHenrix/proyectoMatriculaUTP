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

**SOLID:**
- Single Responsibility Principle
- Open/Closed Principle
- Liskov Substitution Principle
- Interface Segregation Principle
- Dependency Inversion Principle

**GOF Patterns:**
- Factory Pattern (Creación de usuarios y reportes)
- Builder Pattern (Construcción de reportes)
- Singleton Pattern (Configuración global)
- Decorator Pattern (Control de acceso por roles)
- Facade Pattern (Servicios)
- Strategy Pattern (Validaciones y cálculos)
- Command Pattern (Operaciones de matrícula)
- Composite Pattern (Relaciones entre modelos)

**GRASP Patterns:**
- Controller (Vistas como controladores)
- Information Expert (Modelos conocen sus datos)
- Creator (Creación de relaciones)
- Low Coupling / High Cohesion

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
