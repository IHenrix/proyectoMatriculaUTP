"""
Proxy Pattern para gestión de vacantes de una sección.

Centraliza y valida las operaciones de ocupación/liberación de vacantes
para evitar inconsistencia de contadores.
"""

from django.core.exceptions import ValidationError


class SeccionVacanteProxy:
    """Proxy de seguridad para actualizar vacantes de una sección."""

    def __init__(self, seccion):
        self.seccion = seccion

    @property
    def vacantes_disponibles(self):
        return self.seccion.vacantes_totales - self.seccion.vacantes_ocupadas

    def ocupar_vacante(self):
        if self.seccion.vacantes_ocupadas >= self.seccion.vacantes_totales:
            raise ValidationError('No hay vacantes disponibles en esta sección')
        self.seccion.vacantes_ocupadas += 1
        self.seccion.save(update_fields=['vacantes_ocupadas'])

    def liberar_vacante(self):
        if self.seccion.vacantes_ocupadas <= 0:
            # No debería ocurrir, pero protegemos el contador
            self.seccion.vacantes_ocupadas = 0
            self.seccion.save(update_fields=['vacantes_ocupadas'])
            return
        self.seccion.vacantes_ocupadas -= 1
        self.seccion.save(update_fields=['vacantes_ocupadas'])

