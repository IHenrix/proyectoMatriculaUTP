"""
Signals del sistema académico.

OBSERVER PATTERN:
Los signals implementan el patrón Observer, permitiendo que diferentes
partes del sistema reaccionen a eventos sin acoplamiento directo.

Cuando ocurre un evento (crear matrícula, eliminar matrícula), los
observadores (receivers) son notificados automáticamente.
"""

from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.db import transaction


@receiver(post_save, sender='academic_system.Matricula')
def actualizar_vacantes_al_matricular(sender, instance, created, **kwargs):
    """
    OBSERVER PATTERN: Observer que reacciona cuando se crea una matrícula.

    Cuando se crea una nueva matrícula activa, automáticamente:
    - Incrementa las vacantes ocupadas de la sección
    - Mantiene la consistencia del sistema

    Args:
        sender: La clase Matricula
        instance: La instancia de matrícula creada/modificada
        created: Boolean indicando si es una nueva instancia
        **kwargs: Argumentos adicionales del signal
    """
    # Solo actuar si es una matrícula nueva y está activa
    if created and instance.is_active:
        # Incrementar vacantes ocupadas
        instance.seccion.vacantes_ocupadas += 1
        instance.seccion.save(update_fields=['vacantes_ocupadas'])


@receiver(pre_delete, sender='academic_system.Matricula')
def liberar_vacante_al_desmatricular(sender, instance, **kwargs):
    """
    OBSERVER PATTERN: Observer que reacciona antes de eliminar una matrícula.

    Cuando se elimina una matrícula activa, automáticamente:
    - Decrementa las vacantes ocupadas de la sección
    - Libera el cupo para otros estudiantes

    Args:
        sender: La clase Matricula
        instance: La instancia de matrícula a eliminar
        **kwargs: Argumentos adicionales del signal
    """
    # Solo liberar vacante si la matrícula estaba activa
    if instance.is_active:
        instance.seccion.vacantes_ocupadas -= 1
        instance.seccion.save(update_fields=['vacantes_ocupadas'])


@receiver(post_save, sender='academic_system.Nota')
def notificar_cambio_nota(sender, instance, created, **kwargs):
    """
    OBSERVER PATTERN: Observer que reacciona a cambios en notas.

    Este observer podría extenderse para:
    - Enviar notificaciones por email al alumno
    - Registrar en un log de auditoría
    - Actualizar estadísticas en tiempo real
    - Disparar otros procesos (ej: verificar si aprobó el curso)

    Por ahora solo documenta el patrón para futuras extensiones.

    Args:
        sender: La clase Nota
        instance: La instancia de nota creada/modificada
        created: Boolean indicando si es una nueva instancia
        **kwargs: Argumentos adicionales del signal
    """
    # TODO: Implementar notificaciones o logging aquí
    # Ejemplo: enviar_email_nota_registrada(instance.matricula.alumno, instance)
    pass


# VENTAJAS DEL OBSERVER PATTERN CON SIGNALS:
#
# 1. DESACOPLAMIENTO: La clase Matricula no necesita saber quién reacciona
#    a sus cambios. Solo emite el signal y los observers se suscriben.
#
# 2. EXTENSIBILIDAD: Podemos agregar más observers sin modificar Matricula:
#    @receiver(post_save, sender='academic_system.Matricula')
#    def enviar_email_bienvenida(sender, instance, created, **kwargs):
#        if created:
#            send_mail('Bienvenido', ...)
#
# 3. MANTENIBILIDAD: La lógica de negocio está separada en funciones
#    específicas, más fáciles de probar y mantener.
#
# 4. REUTILIZACIÓN: Los mismos signals pueden ser observados por múltiples
#    receivers para diferentes propósitos.
