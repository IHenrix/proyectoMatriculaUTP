#!/bin/bash
# Startup script para Azure App Service
# Este script se ejecuta automáticamente al iniciar el contenedor

echo "=== Iniciando Sistema de Matrículas UTP en Azure ==="

# Activar entorno virtual si existe
if [ -d "antenv" ]; then
    source antenv/bin/activate
fi

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements-azure.txt

# Colectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar migraciones de base de datos
echo "Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

# Crear superusuario si no existe (solo desarrollo/staging)
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "Creando superusuario..."
    python manage.py shell <<EOF
from academic_system.models import Usuario
if not Usuario.objects.filter(numero_documento='admin').exists():
    Usuario.objects.create_superuser(
        numero_documento='admin',
        password='${ADMIN_PASSWORD}',
        email='admin@utp.edu.pe',
        nombres='Administrador',
        apellidos='Sistema',
        rol='administrador'
    )
    print("Superusuario creado")
else:
    print("Superusuario ya existe")
EOF
fi

# Iniciar Gunicorn
echo "Iniciando servidor Gunicorn..."
gunicorn sistema_matriculas.wsgi:application \
    --bind=0.0.0.0:8000 \
    --workers=4 \
    --threads=2 \
    --timeout=120 \
    --access-logfile '-' \
    --error-logfile '-' \
    --log-level info
