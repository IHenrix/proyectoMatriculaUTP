from django.apps import AppConfig


class AcademicSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'academic_system'

    def ready(self):
        """
        Método ejecutado cuando la aplicación está lista.
        Registra los signals (OBSERVER PATTERN).
        """
        import academic_system.signals  # noqa
