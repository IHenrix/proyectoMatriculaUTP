"""
URL configuration for sistema_matriculas project.
Sistema de Matrículas y Notas
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Academic System URLs (debe ir primero)
    path('', include('academic_system.urls')),

    # Django Admin (cambiado a django-admin para evitar conflictos)
    path('django-admin/', admin.site.urls),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
