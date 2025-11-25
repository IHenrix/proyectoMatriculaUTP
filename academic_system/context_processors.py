"""
Context Processors
Añade variables globales a todos los templates
"""
from django.conf import settings


def university_context(request):
    """
    Context processor que añade información de la universidad
    a todos los templates.

    Implementa el patrón Singleton para acceso a configuración global.
    """
    return {
        'UNIVERSITY_NAME': settings.UNIVERSITY_NAME,
        'UNIVERSITY_SHORT_NAME': settings.UNIVERSITY_SHORT_NAME,
    }
