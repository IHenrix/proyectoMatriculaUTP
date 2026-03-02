"""
PagoService - Servicio de gestión de pagos de matrícula

Patrones de Diseño Aplicados:
- Strategy Pattern: estrategias intercambiables de cálculo de precio
- Service Layer Pattern: lógica de negocio centralizada
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from django.utils import timezone
from django.db import transaction


# ==============================================================================
# STRATEGY PATTERN — Estrategias de cálculo de precio
# ==============================================================================

class EstrategiaPrecio(ABC):
    """Interfaz base para estrategias de precio. Strategy Pattern."""

    @abstractmethod
    def calcular(self, monto_base: Decimal) -> Decimal:
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass


class EstrategiaNormal(EstrategiaPrecio):
    """Sin descuento — precio completo."""

    def calcular(self, monto_base: Decimal) -> Decimal:
        return monto_base

    def descripcion(self) -> str:
        return 'Sin descuento'


class EstrategiaBeca(EstrategiaPrecio):
    """Beca académica — 50% de descuento."""

    def calcular(self, monto_base: Decimal) -> Decimal:
        return (monto_base * Decimal('0.50')).quantize(Decimal('0.01'))

    def descripcion(self) -> str:
        return 'Beca (50% descuento)'


class EstrategiaConvenio(EstrategiaPrecio):
    """Convenio institucional — 20% de descuento."""

    def calcular(self, monto_base: Decimal) -> Decimal:
        return (monto_base * Decimal('0.80')).quantize(Decimal('0.01'))

    def descripcion(self) -> str:
        return 'Convenio (20% descuento)'


# ==============================================================================
# PAGO SERVICE
# ==============================================================================

class PagoService:
    """
    Servicio de pagos de matrícula.

    Strategy Pattern: delega el cálculo del monto a la estrategia correspondiente.
    """

    PRECIO_POR_CREDITO = Decimal('50.00')  # S/ 50 por crédito

    ESTRATEGIAS = {
        'NINGUNO':  EstrategiaNormal(),
        'BECA':     EstrategiaBeca(),
        'CONVENIO': EstrategiaConvenio(),
    }

    @classmethod
    def _generar_numero_recibo(cls) -> str:
        """Genera un número de recibo único basado en timestamp."""
        import time
        return f"REC{int(time.time() * 1000) % 10_000_000_000:010d}"

    @classmethod
    @transaction.atomic
    def obtener_o_crear_pago(cls, matricula, tipo_descuento: str = 'NINGUNO'):
        """
        Obtiene el pago existente de la matrícula o lo crea si no existe.
        Strategy Pattern: usa la estrategia de precio según tipo_descuento.
        """
        from academic_system.models import Pago

        if hasattr(matricula, 'pago'):
            return matricula.pago

        monto_base = cls.PRECIO_POR_CREDITO * matricula.seccion.curso.creditos
        estrategia = cls.ESTRATEGIAS.get(tipo_descuento, cls.ESTRATEGIAS['NINGUNO'])
        monto_final = estrategia.calcular(monto_base)

        return Pago.objects.create(
            matricula=matricula,
            numero_recibo=cls._generar_numero_recibo(),
            monto_base=monto_base,
            monto_final=monto_final,
            tipo_descuento=tipo_descuento,
            estado='PENDIENTE',
        )

    @classmethod
    @transaction.atomic
    def realizar_pago(cls, pago_id: int, alumno):
        """
        Procesa el pago: cambia estado a PAGADO y registra la fecha.
        Valida que el pago pertenece al alumno.
        """
        from academic_system.models import Pago

        pago = Pago.objects.select_for_update().get(
            id=pago_id,
            matricula__alumno=alumno
        )

        if pago.esta_pagado:
            return pago, False  # ya pagado

        pago.estado = 'PAGADO'
        pago.fecha_pago = timezone.now()
        pago.save()
        return pago, True

    @classmethod
    def obtener_pagos_alumno(cls, alumno):
        """Retorna todos los pagos activos del alumno, ordenados por ciclo."""
        from academic_system.models import Pago

        return Pago.objects.filter(
            matricula__alumno=alumno,
            matricula__is_active=True,
        ).select_related(
            'matricula__seccion__curso',
            'matricula__seccion__ciclo',
        ).order_by('-matricula__seccion__ciclo__nombre', 'matricula__seccion__curso__nombre')

    @classmethod
    def sincronizar_pagos_alumno(cls, alumno):
        """
        Crea pagos PENDIENTE para matrículas activas que aún no tienen pago.
        Útil para alumnos con matrículas previas al módulo de pagos.
        """
        from academic_system.models import Matricula

        matriculas_sin_pago = Matricula.objects.filter(
            alumno=alumno,
            is_active=True,
        ).exclude(pago__isnull=False).select_related('seccion__curso')

        for matricula in matriculas_sin_pago:
            cls.obtener_o_crear_pago(matricula)

    @classmethod
    def resumen_pagos(cls, alumno) -> dict:
        """Retorna un resumen de pagos del alumno."""
        pagos = cls.obtener_pagos_alumno(alumno)

        total_pagado    = sum(p.monto_final for p in pagos if p.esta_pagado)
        total_pendiente = sum(p.monto_final for p in pagos if not p.esta_pagado)

        return {
            'total_pagado':    total_pagado,
            'total_pendiente': total_pendiente,
            'cantidad_pagado':    pagos.filter(estado='PAGADO').count(),
            'cantidad_pendiente': pagos.filter(estado='PENDIENTE').count(),
        }
