"""
Decorators para control de acceso por roles

Patrones de Diseño:
- Decorator Pattern: Añade funcionalidad de control de acceso
- Strategy Pattern: Diferentes estrategias de autenticación
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def rol_requerido(*roles_permitidos):
    """
    Decorator Pattern: Restringe acceso a vistas según el rol del usuario.

    Args:
        *roles_permitidos: Roles que pueden acceder a la vista

    Usage:
        @rol_requerido('administrador')
        def vista_admin(request):
            ...

        @rol_requerido('profesor', 'administrador')
        def vista_profesor_admin(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if request.user.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect('dashboard')
        return wrapped_view
    return decorator


def admin_required(view_func):
    """
    Decorator para vistas que requieren rol de administrador.

    Usage:
        @admin_required
        def vista_admin(request):
            ...
    """
    return rol_requerido('administrador')(view_func)


def profesor_required(view_func):
    """
    Decorator para vistas que requieren rol de profesor.

    Usage:
        @profesor_required
        def vista_profesor(request):
            ...
    """
    return rol_requerido('profesor')(view_func)


def alumno_required(view_func):
    """
    Decorator para vistas que requieren rol de alumno.

    Usage:
        @alumno_required
        def vista_alumno(request):
            ...
    """
    return rol_requerido('alumno')(view_func)
