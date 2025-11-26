"""
Singleton Pattern - Configuración del Sistema.

SINGLETON PATTERN:
Garantiza que una clase tenga una única instancia en todo el sistema
y proporciona un punto de acceso global a ella.

Este patrón es útil para:
- Configuraciones globales del sistema
- Gestores de recursos compartidos (conexiones, cache)
- Coordinadores centrales
- Registros (logs, auditoría)
"""

from decimal import Decimal
from threading import Lock


class ConfiguracionSistema:
    """
    SINGLETON PATTERN: Configuración única del sistema académico.

    Esta clase implementa el patrón Singleton thread-safe, garantizando
    que solo exista una instancia de la configuración en todo el sistema.

    Características:
    - Thread-safe: Usa Lock para evitar problemas de concurrencia
    - Lazy initialization: Se crea solo cuando se necesita
    - Single instance: Garantiza una única instancia

    Ejemplo de uso:
        config = ConfiguracionSistema()
        nota_minima = config.nota_minima_aprobacion

        # En otro lugar del código
        config2 = ConfiguracionSistema()
        # config y config2 son LA MISMA instancia
        assert config is config2  # True
    """

    _instance = None
    _lock = Lock()
    _initialized = False

    def __new__(cls):
        """
        SINGLETON PATTERN: Controla la creación de instancias.

        Usa double-checked locking para garantizar thread-safety:
        1. Primera verificación sin lock (rápida)
        2. Si no existe, adquiere lock
        3. Segunda verificación con lock (segura)
        4. Crea instancia si aún no existe

        Returns:
            ConfiguracionSistema: La única instancia del sistema
        """
        # Primera verificación (sin lock, para performance)
        if cls._instance is None:
            # Adquirir lock para thread-safety
            with cls._lock:
                # Segunda verificación (con lock, para seguridad)
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Inicializa la configuración solo una vez.

        Usa flag _initialized para evitar reinicializar en llamadas
        subsiguientes al constructor.
        """
        # Solo inicializar la primera vez
        if not ConfiguracionSistema._initialized:
            self._cargar_configuracion()
            ConfiguracionSistema._initialized = True

    def _cargar_configuracion(self):
        """
        Carga la configuración del sistema.

        En una implementación completa, podría cargar desde:
        - Base de datos
        - Archivo de configuración
        - Variables de entorno
        - API externa
        """
        # Configuración académica
        self.nota_minima_aprobacion = Decimal('11.6')
        self.nota_maxima = Decimal('20.0')
        self.nota_minima = Decimal('0.0')

        # Configuración de créditos
        self.max_creditos_por_ciclo = 24
        self.min_creditos_por_ciclo = 12
        self.creditos_por_curso_tipico = 3

        # Configuración de secciones
        self.vacantes_minimas_por_seccion = 15
        self.vacantes_maximas_por_seccion = 40
        self.alerta_pocas_vacantes = 5

        # Configuración de ciclos
        self.duracion_ciclo_semanas = 18
        self.duracion_periodo_matricula_dias = 14

        # Configuración de reportes
        self.formato_fecha_reportes = '%d/%m/%Y'
        self.formato_hora_reportes = '%H:%M'

        # Configuración de códigos
        self.longitud_codigo_usuario = 8
        self.prefijo_codigo_usuario = 'U'
        self.longitud_codigo_seccion = 6
        self.prefijo_codigo_seccion = 'SEC'

        # Información de la universidad
        self.nombre_universidad = 'Universidad Tecnológica del Perú'
        self.nombre_corto_universidad = 'UTP'

    def es_nota_aprobatoria(self, nota):
        """
        INFORMATION EXPERT: La configuración sabe qué es una nota aprobatoria.

        Args:
            nota (Decimal): Nota a evaluar

        Returns:
            bool: True si la nota es aprobatoria
        """
        return nota >= self.nota_minima_aprobacion

    def validar_creditos_ciclo(self, creditos):
        """
        Valida que los créditos estén en el rango permitido.

        Args:
            creditos (int): Cantidad de créditos a validar

        Returns:
            bool: True si está en rango válido
        """
        return self.min_creditos_por_ciclo <= creditos <= self.max_creditos_por_ciclo

    def validar_vacantes_seccion(self, vacantes):
        """
        Valida que las vacantes estén en el rango permitido.

        Args:
            vacantes (int): Cantidad de vacantes a validar

        Returns:
            bool: True si está en rango válido
        """
        return self.vacantes_minimas_por_seccion <= vacantes <= self.vacantes_maximas_por_seccion

    def hay_pocas_vacantes(self, vacantes_disponibles):
        """
        Determina si hay pocas vacantes disponibles.

        Args:
            vacantes_disponibles (int): Vacantes disponibles

        Returns:
            bool: True si hay pocas vacantes (alerta)
        """
        return 0 < vacantes_disponibles <= self.alerta_pocas_vacantes

    def actualizar_configuracion(self, **kwargs):
        """
        Actualiza valores de configuración en tiempo de ejecución.

        Args:
            **kwargs: Pares clave-valor de configuración a actualizar

        Ejemplo:
            config = ConfiguracionSistema()
            config.actualizar_configuracion(
                nota_minima_aprobacion=Decimal('12.0'),
                max_creditos_por_ciclo=27
            )
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def reset(self):
        """
        Resetea la configuración a valores por defecto.

        Útil para testing o para recargar configuración.
        """
        self._cargar_configuracion()

    @classmethod
    def destruir_instancia(cls):
        """
        Destruye la instancia del Singleton.

        ADVERTENCIA: Solo usar en testing. En producción el Singleton
        debe mantener su instancia durante toda la vida de la aplicación.
        """
        with cls._lock:
            cls._instance = None
            cls._initialized = False

    def __repr__(self):
        """Representación del objeto para debugging"""
        return f"<ConfiguracionSistema id={id(self)}>"


# EJEMPLO DE USO DEL SINGLETON:
#
# En cualquier parte del código:
# from academic_system.singleton import ConfiguracionSistema
#
# config = ConfiguracionSistema()
# if config.es_nota_aprobatoria(nota):
#     print("Aprobado!")
#
# En otro módulo diferente:
# config2 = ConfiguracionSistema()
# # config2 es LA MISMA instancia que config
# assert config is config2  # True
#
# VENTAJAS:
# 1. Punto único de acceso a configuración
# 2. Garantiza consistencia en todo el sistema
# 3. Lazy initialization (se crea solo cuando se necesita)
# 4. Thread-safe (seguro para aplicaciones concurrentes)
# 5. Fácil de testear y mockear
#
# CUÁNDO USAR:
# - Configuración global del sistema
# - Gestión de recursos únicos (connection pools, caches)
# - Coordinadores centrales
# - Logs y auditoría
