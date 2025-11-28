"""
Context Processors
Añade variables globales a todos los templates
"""
from django.conf import settings
from datetime import date


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


def matricula_context(request):
    """
    Context processor que añade información sobre el estado de matrícula
    a todos los templates.

    Verifica si hay un ciclo activo con matrícula abierta.
    """
    puede_matricularse = False

    if request.user.is_authenticated and request.user.rol == 'alumno':
        from academic_system.models import Ciclo
        hoy = date.today()

        # Verificar si existe un ciclo con matrícula abierta y dentro del período
        ciclo_activo = Ciclo.objects.filter(
            matricula_abierta=True,
            fecha_inicio_matricula__lte=hoy,
            fecha_fin_matricula__gte=hoy
        ).first()

        puede_matricularse = ciclo_activo is not None

    return {
        'puede_matricularse': puede_matricularse,
    }
