"""
CuotaService - Servicio de gestión de cuotas mensuales de pago

Patrones de Diseño Aplicados:
- Strategy Pattern: estrategias de cálculo de precio (normal, beca, convenio)
- Service Layer Pattern: lógica de negocio centralizada
- Information Expert: CuotaService conoce las reglas de generación de cuotas
"""

from decimal import Decimal
from datetime import date, datetime, time as dtime, timedelta
import calendar


# ==============================================================================
# STRATEGY PATTERN — Estrategias de cálculo de precio
# ==============================================================================

class EstrategiaPrecio:
    """Estrategia base — precio completo sin descuento."""
    NOMBRE = 'Sin descuento'

    def calcular(self, monto_base: Decimal) -> Decimal:
        return monto_base


class EstrategiaBeca(EstrategiaPrecio):
    """Beca académica — 50% de descuento."""
    NOMBRE = 'Beca (50%)'

    def calcular(self, monto_base: Decimal) -> Decimal:
        return (monto_base * Decimal('0.50')).quantize(Decimal('0.01'))


class EstrategiaConvenio(EstrategiaPrecio):
    """Convenio institucional — 20% de descuento."""
    NOMBRE = 'Convenio (20%)'

    def calcular(self, monto_base: Decimal) -> Decimal:
        return (monto_base * Decimal('0.80')).quantize(Decimal('0.01'))


ESTRATEGIAS = {
    'NORMAL':   EstrategiaPrecio(),
    'BECA':     EstrategiaBeca(),
    'CONVENIO': EstrategiaConvenio(),
}


# ==============================================================================
# CUOTA SERVICE
# ==============================================================================

class CuotaService:
    """
    Servicio de cuotas mensuales de matrícula.

    Genera N cuotas (una por mes del ciclo) calculando el monto
    en base a los créditos totales matriculados por el alumno.
    """

    PRECIO_POR_CREDITO = Decimal('50.00')

    # ── helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _meses_del_ciclo(ciclo) -> list:
        """
        Retorna lista de fechas de vencimiento (día 28) para cada mes
        completo del ciclo.  Un mes se considera completo si el ciclo
        termina el día 15 o más tarde dentro de ese mes.
        """
        inicio = ciclo.fecha_inicio_ciclo
        fin    = ciclo.fecha_fin_ciclo

        meses = []
        año, mes = inicio.year, inicio.month

        while True:
            if (año, mes) > (fin.year, fin.month):
                break
            if (año, mes) == (fin.year, fin.month) and fin.day < 15:
                break   # mes parcial muy corto → no cuenta

            ultimo = calendar.monthrange(año, mes)[1]
            meses.append(date(año, mes, min(28, ultimo)))

            if mes == 12:
                mes, año = 1, año + 1
            else:
                mes += 1

        return meses

    @staticmethod
    def _creditos_alumno_ciclo(alumno, ciclo) -> int:
        from academic_system.models import Matricula
        return sum(
            m.seccion.curso.creditos
            for m in Matricula.objects.filter(
                alumno=alumno, seccion__ciclo=ciclo, is_active=True
            ).select_related('seccion__curso')
        )

    @staticmethod
    def _codigo_pago(ciclo, alumno, numero: int) -> str:
        nombre = ciclo.nombre.replace(' ', '-')
        return f"CUO-{nombre}-{alumno.numero_documento}-{numero}"

    # ── API pública ───────────────────────────────────────────────────────────

    @classmethod
    def generar_cuotas(cls, alumno, ciclo, estrategia_key: str = 'NORMAL') -> list:
        """
        Crea (o recupera) las cuotas mensuales del alumno para el ciclo.
        Monto = (créditos × S/50 × factor_descuento) ÷ meses
        """
        from academic_system.models import Cuota

        meses = cls._meses_del_ciclo(ciclo)
        if not meses:
            return []

        creditos   = cls._creditos_alumno_ciclo(alumno, ciclo)
        monto_base = cls.PRECIO_POR_CREDITO * creditos
        estrategia = ESTRATEGIAS.get(estrategia_key, ESTRATEGIAS['NORMAL'])
        total      = estrategia.calcular(monto_base)
        mensual    = (total / len(meses)).quantize(Decimal('0.01'))

        cuotas = []
        for i, vencimiento in enumerate(meses, 1):
            cuota, _ = Cuota.objects.get_or_create(
                alumno=alumno,
                ciclo=ciclo,
                numero_cuota=i,
                defaults={
                    'fecha_vencimiento': vencimiento,
                    'monto':             mensual,
                    'estado':            'PENDIENTE',
                    'codigo_pago':       cls._codigo_pago(ciclo, alumno, i),
                }
            )
            cuotas.append(cuota)

        return cuotas

    @classmethod
    def marcar_pagadas(cls, alumno, ciclo):
        """
        Marca todas las cuotas del alumno en el ciclo como PAGADO.
        Usa fechas de pago realistas (3 días antes del vencimiento).
        Solo para datos históricos en el seed.
        """
        from academic_system.models import Cuota
        from django.utils import timezone

        for cuota in Cuota.objects.filter(alumno=alumno, ciclo=ciclo, estado='PENDIENTE'):
            fecha = datetime.combine(
                cuota.fecha_vencimiento - timedelta(days=3),
                dtime(10, 0)
            )
            cuota.estado    = 'PAGADO'
            cuota.fecha_pago = timezone.make_aware(fecha)
            cuota.save()

    @classmethod
    def obtener_cuotas_alumno(cls, alumno):
        """Todas las cuotas del alumno, ordenadas ciclo desc → cuota asc."""
        from academic_system.models import Cuota
        return Cuota.objects.filter(alumno=alumno).select_related('ciclo').order_by(
            '-ciclo__fecha_inicio_ciclo', 'numero_cuota'
        )

    @classmethod
    def recalcular_cuotas(cls, alumno, ciclo) -> list:
        """
        Recalcula las cuotas del alumno para el ciclo.
        Elimina las cuotas PENDIENTES y las regenera con el monto actualizado
        según los créditos actuales matriculados.
        Útil después de una matrícula o desmatrícula.
        """
        from academic_system.models import Cuota
        Cuota.objects.filter(alumno=alumno, ciclo=ciclo, estado='PENDIENTE').delete()
        creditos = cls._creditos_alumno_ciclo(alumno, ciclo)
        if creditos > 0:
            return cls.generar_cuotas(alumno, ciclo)
        return []

    @classmethod
    def resumen(cls, alumno) -> dict:
        cuotas     = cls.obtener_cuotas_alumno(alumno)
        pendientes = [c for c in cuotas if not c.esta_pagado]
        pagadas    = [c for c in cuotas if c.esta_pagado]
        return {
            'total_pendiente':    sum(c.monto for c in pendientes),
            'total_pagado':       sum(c.monto for c in pagadas),
            'cantidad_pendiente': len(pendientes),
            'cantidad_pagado':    len(pagadas),
        }
