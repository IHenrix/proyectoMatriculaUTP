# 🚀 Guía de Deployment a Azure - Sistema de Matrículas UTP

Esta guía te llevará paso a paso para desplegar tu proyecto Django en Azure usando los servicios profesionales de Microsoft.

---

## 📋 Tabla de Contenidos

1. [Arquitectura en Azure](#arquitectura-en-azure)
2. [Prerrequisitos](#prerrequisitos)
3. [Paso 1: Crear Base de Datos MySQL en Azure](#paso-1-crear-base-de-datos-mysql-en-azure)
4. [Paso 2: Configurar Azure App Service](#paso-2-configurar-azure-app-service)
5. [Paso 3: Configurar Variables de Entorno](#paso-3-configurar-variables-de-entorno)
6. [Paso 4: Desplegar el Código](#paso-4-desplegar-el-código)
7. [Paso 5: Ejecutar Migraciones](#paso-5-ejecutar-migraciones)
8. [Paso 6: Crear Datos de Prueba](#paso-6-crear-datos-de-prueba)
9. [Verificación y Troubleshooting](#verificación-y-troubleshooting)
10. [Costos Estimados](#costos-estimados)

---

## 🏗️ Arquitectura en Azure

```
┌─────────────────────────────────────────────────────┐
│                   INTERNET                          │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Azure App Service    │
         │  (Django + Gunicorn)  │
         │  ✓ Python 3.11        │
         │  ✓ Auto-scaling       │
         │  ✓ HTTPS automático   │
         └───────────┬───────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│ Azure Database  │    │  Azure Blob      │
│ for MySQL       │    │  Storage         │
│ (Flexible)      │    │  (Opcional)      │
│ ✓ Backup auto   │    │  ✓ Archivos      │
│ ✓ SSL/TLS       │    │  ✓ CDN           │
└─────────────────┘    └──────────────────┘
```

**Servicios que usaremos:**
- ☁️ **Azure App Service** - Hosting del Django app
- 🗄️ **Azure Database for MySQL - Flexible Server** - Base de datos administrada
- 📦 **Azure Blob Storage** (Opcional) - Archivos estáticos y media
- 📊 **Application Insights** (Opcional) - Monitoreo y logs

---

## ✅ Prerrequisitos

### 1. Cuenta de Azure
- [ ] Tener una cuenta de Azure (puedes usar [Azure for Students](https://azure.microsoft.com/es-es/free/students/) - $100 USD gratis)
- [ ] Instalar [Azure CLI](https://docs.microsoft.com/es-es/cli/azure/install-azure-cli)

### 2. Herramientas Locales
```bash
# Verificar instalaciones
python --version          # Python 3.8+
git --version            # Git
az --version             # Azure CLI
```

### 3. Iniciar Sesión en Azure
```bash
# Login a Azure
az login

# Verificar suscripción activa
az account show

# (Opcional) Listar todas las suscripciones
az account list --output table

# (Opcional) Cambiar suscripción
az account set --subscription "NOMBRE_O_ID_SUSCRIPCION"
```

---

## 🗄️ Paso 1: Crear Base de Datos MySQL en Azure

### Opción A: Usando Azure Portal (Interfaz Gráfica)

1. **Ir al Portal de Azure**
   - Navega a: https://portal.azure.com
   - Click en "Crear un recurso"
   - Busca "Azure Database for MySQL Flexible Server"

2. **Configuración Básica**
   ```
   Suscripción: Tu suscripción
   Grupo de recursos: Crear nuevo → "rg-sistema-matriculas-utp"
   Nombre del servidor: "mysql-matriculas-utp" (debe ser único globalmente)
   Región: "East US" o "Brazil South" (más cercano a Perú)
   Versión de MySQL: 8.0
   Tipo de carga: Development (más económico para empezar)
   ```

3. **Autenticación**
   ```
   Nombre de usuario administrador: adminutp
   Contraseña: [Una contraseña segura - guárdala bien]

   ⚠️ IMPORTANTE: Anota estas credenciales, las necesitarás después
   ```

4. **Redes**
   - Conectividad: "Acceso público (direcciones IP permitidas)"
   - Reglas de firewall:
     - ✅ Marcar: "Permitir acceso desde cualquier servicio de Azure"
     - Agregar IP actual para gestión local

5. **Revisar y Crear**
   - Click en "Revisar y crear"
   - Esperar ~5-10 minutos para la creación

### Opción B: Usando Azure CLI (Más Rápido)

```bash
# 1. Crear grupo de recursos
az group create \
  --name rg-sistema-matriculas-utp \
  --location eastus

# 2. Crear servidor MySQL Flexible
az mysql flexible-server create \
  --resource-group rg-sistema-matriculas-utp \
  --name mysql-matriculas-utp \
  --location eastus \
  --admin-user adminutp \
  --admin-password "TuContraseñaSegura123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 8.0 \
  --storage-size 32 \
  --public-access 0.0.0.0

# 3. Crear base de datos
az mysql flexible-server db create \
  --resource-group rg-sistema-matriculas-utp \
  --server-name mysql-matriculas-utp \
  --database-name sistema_matriculas

# 4. Configurar reglas de firewall (permitir Azure Services)
az mysql flexible-server firewall-rule create \
  --resource-group rg-sistema-matriculas-utp \
  --name mysql-matriculas-utp \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### Obtener String de Conexión

```bash
# Obtener el hostname del servidor
az mysql flexible-server show \
  --resource-group rg-sistema-matriculas-utp \
  --name mysql-matriculas-utp \
  --query "fullyQualifiedDomainName" \
  --output tsv

# Resultado será algo como: mysql-matriculas-utp.mysql.database.azure.com
```

**Anotar para después:**
```
DB_HOST=mysql-matriculas-utp.mysql.database.azure.com
DB_NAME=sistema_matriculas
DB_USER=adminutp
DB_PASSWORD=[Tu contraseña]
DB_PORT=3306
```

---

## 🌐 Paso 2: Configurar Azure App Service

### Opción A: Usando Azure Portal

1. **Crear App Service**
   - Portal Azure → "Crear un recurso" → "Web App"

2. **Configuración Básica**
   ```
   Grupo de recursos: rg-sistema-matriculas-utp (mismo que MySQL)
   Nombre: sistema-matriculas-utp (será: sistema-matriculas-utp.azurewebsites.net)
   Publicar: Código
   Pila del entorno de ejecución: Python 3.11
   Sistema operativo: Linux
   Región: East US (misma que MySQL)
   ```

3. **Plan de App Service**
   ```
   Plan de Linux: Crear nuevo → "plan-matriculas-utp"
   SKU y tamaño: B1 Basic (para producción ligera)
                 O F1 Free (solo para pruebas)
   ```

4. **Revisar y Crear**

### Opción B: Usando Azure CLI

```bash
# 1. Crear App Service Plan
az appservice plan create \
  --name plan-matriculas-utp \
  --resource-group rg-sistema-matriculas-utp \
  --location eastus \
  --is-linux \
  --sku B1

# 2. Crear Web App
az webapp create \
  --resource-group rg-sistema-matriculas-utp \
  --plan plan-matriculas-utp \
  --name sistema-matriculas-utp \
  --runtime "PYTHON:3.11"

# 3. Configurar startup command
az webapp config set \
  --resource-group rg-sistema-matriculas-utp \
  --name sistema-matriculas-utp \
  --startup-file "startup.sh"
```

---

## 🔐 Paso 3: Configurar Variables de Entorno

### Generar SECRET_KEY Segura

```bash
# En tu terminal local, ejecuta:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copia el resultado, será algo como:
# django-insecure-#9k2@mf8_xqw&3$p^v7n!@jz5er4-ht6gy+2wu*8mc9x&-d
```

### Configurar Variables en Azure App Service

#### Opción A: Azure Portal

1. Portal Azure → Tu App Service → "Configuración" → "Configuración de la aplicación"
2. Click en "Nueva configuración de la aplicación"
3. Agregar una por una:

```
SECRET_KEY = [Tu SECRET_KEY generada arriba]
DEBUG = False
ALLOWED_HOSTS = sistema-matriculas-utp.azurewebsites.net

DB_HOST = mysql-matriculas-utp.mysql.database.azure.com
DB_NAME = sistema_matriculas
DB_USER = adminutp
DB_PASSWORD = [Tu contraseña MySQL]
DB_PORT = 3306

DJANGO_SETTINGS_MODULE = sistema_matriculas.settings_production

UNIVERSITY_NAME = Universidad Tecnológica del Perú
UNIVERSITY_SHORT_NAME = UTP
```

4. Click en "Guardar"

#### Opción B: Azure CLI

```bash
# Configurar todas las variables de una vez
az webapp config appsettings set \
  --resource-group rg-sistema-matriculas-utp \
  --name sistema-matriculas-utp \
  --settings \
    SECRET_KEY="django-insecure-#9k2@mf8_xqw&3$p^v7n!@jz5er4-ht6gy+2wu*8mc9x&-d" \
    DEBUG="False" \
    ALLOWED_HOSTS="sistema-matriculas-utp.azurewebsites.net" \
    DB_HOST="mysql-matriculas-utp.mysql.database.azure.com" \
    DB_NAME="sistema_matriculas" \
    DB_USER="adminutp" \
    DB_PASSWORD="TuContraseñaSegura123!" \
    DB_PORT="3306" \
    DJANGO_SETTINGS_MODULE="sistema_matriculas.settings_production" \
    UNIVERSITY_NAME="Universidad Tecnológica del Perú" \
    UNIVERSITY_SHORT_NAME="UTP"
```

---

## 📤 Paso 4: Desplegar el Código

### Preparar el Proyecto Localmente

```bash
# 1. Navegar al directorio del proyecto
cd "d:\Enrique\UTP\Ciclo 5\Diseño de Patrones\PROYECTO FINAL\proyectoMatriculaUTP"

# 2. Asegurarse de que estés en la rama correcta
git status
git branch

# 3. Verificar que los archivos de Azure existan
ls requirements-azure.txt
ls startup.sh
ls .deployment
ls sistema_matriculas/settings_production.py

# 4. Hacer commit de los nuevos archivos (si no lo has hecho)
git add requirements-azure.txt startup.sh .deployment sistema_matriculas/settings_production.py DEPLOYMENT_AZURE.md
git commit -m "feat: Agregar configuración para deployment en Azure"
git push origin development
```

### Desplegar usando Azure CLI (Recomendado)

```bash
# 1. Configurar Git deployment desde repositorio local
az webapp deployment source config-local-git \
  --name sistema-matriculas-utp \
  --resource-group rg-sistema-matriculas-utp

# Esto devolverá una URL como:
# https://sistema-matriculas-utp.scm.azurewebsites.net/sistema-matriculas-utp.git

# 2. Obtener credenciales de deployment
az webapp deployment list-publishing-credentials \
  --name sistema-matriculas-utp \
  --resource-group rg-sistema-matriculas-utp \
  --query "{username:publishingUserName, password:publishingPassword}" \
  --output table

# 3. Agregar remote de Azure
git remote add azure https://sistema-matriculas-utp.scm.azurewebsites.net/sistema-matriculas-utp.git

# 4. Hacer push a Azure (te pedirá las credenciales)
git push azure development:master

# Esperar ~5-10 minutos mientras Azure:
# - Instala dependencias
# - Colecta archivos estáticos
# - Ejecuta migraciones
# - Inicia Gunicorn
```

### Alternativa: Desplegar usando GitHub Actions (Más Profesional)

Si tienes tu código en GitHub:

1. **Generar credenciales de publicación**
```bash
az webapp deployment list-publishing-profiles \
  --resource-group rg-sistema-matriculas-utp \
  --name sistema-matriculas-utp \
  --xml
```

2. **En GitHub:**
   - Ir a tu repositorio → Settings → Secrets → Actions
   - Crear secret: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Pegar el XML del paso anterior

3. **Crear archivo de workflow:**
`.github/workflows/azure-deploy.yml`
```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main, development ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements-azure.txt

    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'sistema-matriculas-utp'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

---

## 🗃️ Paso 5: Ejecutar Migraciones

### Conectarse por SSH al App Service

```bash
# Abrir SSH en el navegador
az webapp ssh --resource-group rg-sistema-matriculas-utp --name sistema-matriculas-utp

# O obtener la URL SSH
az webapp show \
  --resource-group rg-sistema-matriculas-utp \
  --name sistema-matriculas-utp \
  --query "defaultHostName" --output tsv

# Ir a: https://sistema-matriculas-utp.scm.azurewebsites.net/webssh/host
```

### Ejecutar Comandos Django

```bash
# Una vez conectado por SSH:

# 1. Verificar que las migraciones se ejecutaron
cd /home/site/wwwroot
python manage.py showmigrations

# 2. Si faltan migraciones, ejecutar:
python manage.py migrate

# 3. Crear superusuario (IMPORTANTE)
python manage.py shell
```

```python
# Dentro del shell de Django:
from academic_system.models import Usuario

# Crear administrador
admin = Usuario.objects.create_superuser(
    numero_documento='75911772',
    password='Pedro1415@',
    email='admin@utp.edu.pe',
    nombres='Administrador',
    apellidos='Sistema',
    rol='administrador'
)
print("Superusuario creado exitosamente")
exit()
```

---

## 🎓 Paso 6: Crear Datos de Prueba

### Opción A: Usar Management Command (Si existe)

```bash
# Por SSH en Azure
python manage.py crear_datos_prueba
```

### Opción B: Crear Manualmente por Django Shell

```bash
# Por SSH
python manage.py shell
```

```python
from academic_system.models import Usuario, Ciclo, Curso, Seccion, Matricula
from datetime import date, timedelta

# Crear profesores
profesores = [
    {'doc': '41523678', 'nombres': 'Juan', 'apellidos': 'Ñahui'},
    {'doc': '42634789', 'nombres': 'Carlos', 'apellidos': 'Rayme'},
    {'doc': '43745890', 'nombres': 'María', 'apellidos': 'Ecmias'},
    {'doc': '44856901', 'nombres': 'Luis', 'apellidos': 'Farfan'},
]

for p in profesores:
    Usuario.objects.create_user(
        numero_documento=p['doc'],
        password='Pedro1415@',
        email=f"{p['doc']}@utp.edu.pe",
        nombres=p['nombres'],
        apellidos=p['apellidos'],
        rol='profesor'
    )
print(f"Creados {len(profesores)} profesores")

# Crear alumnos
alumnos = [
    {'doc': '72365087', 'nombres': 'Juan', 'apellidos': 'Morales'},
    {'doc': '73309801', 'nombres': 'Kelvin', 'apellidos': 'Acevedo'},
    {'doc': '74317595', 'nombres': 'Angel', 'apellidos': 'Campusanto'},
    {'doc': '75650077', 'nombres': 'Joel', 'apellidos': 'Saldaña'},
]

for a in alumnos:
    Usuario.objects.create_user(
        numero_documento=a['doc'],
        password='Pedro1415@',
        email=f"{a['doc']}@utp.edu.pe",
        nombres=a['nombres'],
        apellidos=a['apellidos'],
        rol='alumno'
    )
print(f"Creados {len(alumnos)} alumnos")

# Crear ciclo académico
ciclo = Ciclo.objects.create(
    codigo='2024-2',
    nombre='Ciclo Académico 2024-2',
    fecha_inicio=date.today() - timedelta(days=30),
    fecha_fin=date.today() + timedelta(days=90),
    is_active=True
)
print(f"Ciclo creado: {ciclo.codigo}")

# Crear algunos cursos de ejemplo
cursos = [
    {'codigo': 'DESPA', 'nombre': 'Diseño de Patrones', 'creditos': 4},
    {'codigo': 'PROGR', 'nombre': 'Programación Avanzada', 'creditos': 4},
    {'codigo': 'BASES', 'nombre': 'Base de Datos II', 'creditos': 4},
]

for c in cursos:
    Curso.objects.get_or_create(
        codigo=c['codigo'],
        defaults={'nombre': c['nombre'], 'creditos': c['creditos']}
    )
print(f"Creados {len(cursos)} cursos")

exit()
```

---

## ✅ Verificación y Troubleshooting

### Verificar que la App esté corriendo

```bash
# Ver estado del App Service
az webapp show \
  --resource-group rg-sistema-matriculas-utp \
  --name sistema-matriculas-utp \
  --query "state" --output tsv

# Debería retornar: Running
```

### Acceder a la aplicación

1. **Abrir en navegador:**
   ```
   https://sistema-matriculas-utp.azurewebsites.net
   ```

2. **Verificar endpoints:**
   - Login: `https://sistema-matriculas-utp.azurewebsites.net/`
   - Admin: `https://sistema-matriculas-utp.azurewebsites.net/admin/`

### Ver Logs en Tiempo Real

```bash
# Stream de logs en vivo
az webapp log tail \
  --resource-group rg-sistema-matriculas-utp \
  --name sistema-matriculas-utp

# Descargar logs
az webapp log download \
  --resource-group rg-sistema-matriculas-utp \
  --name sistema-matriculas-utp \
  --log-file logs.zip
```

### Problemas Comunes

#### 1. Error 500 - Internal Server Error

**Solución:**
```bash
# Ver logs detallados
az webapp log tail --resource-group rg-sistema-matriculas-utp --name sistema-matriculas-utp

# Verificar variables de entorno
az webapp config appsettings list \
  --resource-group rg-sistema-matriculas-utp \
  --name sistema-matriculas-utp \
  --output table

# Verificar que DEBUG=False y DJANGO_SETTINGS_MODULE estén configurados
```

#### 2. No se cargan los archivos estáticos (CSS/JS)

**Solución:**
```bash
# Por SSH, ejecutar:
python manage.py collectstatic --noinput

# Verificar que STATICFILES_STORAGE esté configurado en settings_production.py
```

#### 3. Error de conexión a MySQL

**Solución:**
```bash
# Verificar firewall de MySQL
az mysql flexible-server firewall-rule list \
  --resource-group rg-sistema-matriculas-utp \
  --name mysql-matriculas-utp \
  --output table

# Asegurar que existe la regla AllowAzureServices

# Probar conexión por SSH:
python manage.py dbshell
```

#### 4. Migraciones no se aplican

**Solución:**
```bash
# Por SSH:
cd /home/site/wwwroot
python manage.py showmigrations
python manage.py migrate --fake-initial
```

---

## 💰 Costos Estimados

### Opción 1: Tier Gratuito (Para pruebas)
```
Azure App Service (F1 Free):        $0.00/mes
Azure Database for MySQL (B1ms):    ~$12.00/mes
TOTAL:                              ~$12/mes
```

**Limitaciones del F1:**
- 60 minutos/día de CPU
- 1 GB de RAM
- 1 GB de almacenamiento
- Solo para pruebas/desarrollo

### Opción 2: Producción Básica
```
Azure App Service (B1):              ~$13.00/mes
Azure Database for MySQL (B1ms):     ~$12.00/mes
Azure Blob Storage (opcional):       ~$2.00/mes
TOTAL:                               ~$27/mes
```

### Opción 3: Producción Profesional
```
Azure App Service (P1v2):            ~$80.00/mes
Azure Database for MySQL (GP 2 cores): ~$120.00/mes
Azure Blob Storage + CDN:            ~$10.00/mes
Application Insights:                ~$5.00/mes
TOTAL:                               ~$215/mes
```

**💡 Tips para reducir costos:**
- Usar Azure for Students ($100 créditos gratis)
- Apagar recursos en horarios no productivos
- Usar tier B1ms para MySQL (Burstable) en lugar de General Purpose
- Compartir App Service Plan entre múltiples apps

---

## 🎯 Próximos Pasos (Mejoras Opcionales)

Una vez que la app esté corriendo:

### 1. Configurar Dominio Personalizado
```bash
# Agregar dominio personalizado
az webapp config hostname add \
  --webapp-name sistema-matriculas-utp \
  --resource-group rg-sistema-matriculas-utp \
  --hostname www.tu-dominio.com

# Habilitar HTTPS con certificado gratuito
az webapp config ssl bind \
  --name sistema-matriculas-utp \
  --resource-group rg-sistema-matriculas-utp \
  --certificate-thumbprint <thumbprint> \
  --ssl-type SNI
```

### 2. Configurar CI/CD con GitHub Actions
- Ver sección en Paso 4 (Alternativa GitHub Actions)

### 3. Agregar Azure Blob Storage para archivos
```bash
# Crear Storage Account
az storage account create \
  --name stmatriculas \
  --resource-group rg-sistema-matriculas-utp \
  --location eastus \
  --sku Standard_LRS

# Crear container para archivos estáticos
az storage container create \
  --name static \
  --account-name stmatriculas \
  --public-access blob
```

### 4. Configurar Backup Automático de MySQL
```bash
az mysql flexible-server backup create \
  --resource-group rg-sistema-matriculas-utp \
  --name mysql-matriculas-utp \
  --backup-name backup-inicial
```

### 5. Monitoreo con Application Insights
- Portal Azure → Crear recurso → Application Insights
- Copiar Instrumentation Key
- Agregar a variables de entorno del App Service

---

## 📞 Soporte y Recursos

### Documentación Oficial
- [Azure App Service Docs](https://docs.microsoft.com/azure/app-service/)
- [Azure Database for MySQL](https://docs.microsoft.com/azure/mysql/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)

### Comandos Útiles de Referencia

```bash
# Ver todos los recursos en el grupo
az resource list \
  --resource-group rg-sistema-matriculas-utp \
  --output table

# Reiniciar App Service
az webapp restart \
  --name sistema-matriculas-utp \
  --resource-group rg-sistema-matriculas-utp

# Ver uso de recursos
az monitor metrics list \
  --resource-group rg-sistema-matriculas-utp \
  --resource sistema-matriculas-utp \
  --resource-type "Microsoft.Web/sites" \
  --metric "CpuTime" \
  --output table

# Eliminar TODO (cuidado!)
# az group delete --name rg-sistema-matriculas-utp --yes
```

---

## ✅ Checklist Final

Antes de declarar el deployment exitoso, verifica:

- [ ] App Service está en estado "Running"
- [ ] Base de datos MySQL está accesible
- [ ] Variables de entorno están configuradas
- [ ] Migraciones aplicadas exitosamente
- [ ] Superusuario creado
- [ ] Archivos estáticos se cargan correctamente
- [ ] Puedes hacer login con las credenciales de CREDENCIALES.md
- [ ] HTTPS está funcionando (Azure lo provee automáticamente)
- [ ] Logs no muestran errores críticos

**URL de tu aplicación:**
```
https://sistema-matriculas-utp.azurewebsites.net
```

---

**🎓 Proyecto:** Sistema de Matrículas UTP - Diseño de Patrones
**📅 Última actualización:** 2025-11-26
**👨‍💻 Autor:** Ricardo Prada et al.

---

## 🆘 ¿Problemas durante el deployment?

Si encuentras algún error durante el proceso:

1. **Revisa los logs:** `az webapp log tail`
2. **Verifica variables de entorno:** `az webapp config appsettings list`
3. **Conéctate por SSH:** `az webapp ssh`
4. **Revisa el firewall de MySQL**
5. **Consulta esta guía:** Todas las soluciones comunes están documentadas arriba

**¡Éxito con tu deployment! 🚀**
