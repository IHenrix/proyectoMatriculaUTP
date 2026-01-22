# Guía de Instalación - Sistema de Matrículas SENATI

## 1. Requisitos Previos

Instalar:
- Python 3.9 o superior
- MySQL 8.0 o superior

## 2. Configurar MySQL

Abrir MySQL y ejecutar:
```sql
CREATE DATABASE sistema_matriculas CHARACTER SET utf8mb4;
```

## 3. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto con este contenido:
```
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=sistema_matriculas
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_HOST=localhost
DB_PORT=3306

UNIVERSITY_NAME=Servicio Nacional de Adiestramiento en Trabajo Industrial
UNIVERSITY_SHORT_NAME=SENATI
```

Cambiar `tu_password_mysql` por tu contraseña de MySQL.

## 4. Crear Entorno Virtual

Abrir terminal en la carpeta del proyecto y ejecutar:
```bash
python -m venv venv
```

## 5. Activar Entorno Virtual

PowerShell:
```bash
venv\Scripts\Activate.ps1
```

CMD:
```bash
venv\Scripts\activate
```

Git Bash:
```bash
source venv/Scripts/activate
```

Si PowerShell da error de permisos:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 6. Instalar Dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 7. Aplicar Migraciones

```bash
python manage.py migrate
```

## 8. Crear Datos de Prueba

```bash
python manage.py crear_datos_prueba
```

Anotar las credenciales que aparecen en la terminal.

## 9. Iniciar Servidor

```bash
python manage.py runserver
```

## 10. Acceder al Sistema

Abrir navegador en: http://localhost:8000

## Credenciales de Acceso

Administrador:
- Usuario: 75911772
- Contraseña: Pedro1415@

Profesor y Alumno:
- Usar los códigos y contraseñas que mostró el comando crear_datos_prueba

## Comandos Útiles

Detener servidor:
```
Ctrl + C
```

Acceder a Django Admin:
```
http://localhost:8000/admin/
```
