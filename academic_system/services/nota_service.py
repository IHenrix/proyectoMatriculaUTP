"""
NotaService - Servicio para gestión de notas

Patrones de Diseño:
- Service Layer Pattern
- Strategy Pattern: Cálculo de promedios
- Observer Pattern: Notificación de cambios
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import Decimal
from academic_system.models import Nota, Matricula, ComponenteEvaluacion
from academic_system.services.memento import NotaCaretaker


class NotaService:
    """
    Servicio para gestión de notas.

    Implementa Strategy Pattern para cálculos de notas.
    """

    @staticmethod
    @transaction.atomic
    def registrar_nota(matricula_id, componente_id, valor):
        """
        Registra o actualiza una nota.

        Args:
            matricula_id: ID de la matrícula
            componente_id: ID del componente de evaluación
            valor: Valor de la nota (0-20)

        Returns:
            Nota: Nota registrada

        Raises:
            ValidationError: Si los datos son inválidos
        """
        if valor is not None:
            valor = Decimal(str(valor))
            if valor < Decimal('0') or valor > Decimal('20'):
                raise ValidationError('La nota debe estar entre 0 y 20')

        matricula = Matricula.objects.get(pk=matricula_id)
        componente = ComponenteEvaluacion.objects.get(pk=componente_id)

        # Validar que el componente pertenezca al curso
        if componente.curso != matricula.seccion.curso:
            raise ValidationError('El componente no pertenece al curso de la matrícula')

        # Obtener o crear la nota
        nota, created = Nota.objects.get_or_create(
            matricula=matricula,
            componente=componente,
            defaults={'valor': valor}
        )

        if not created:
            NotaCaretaker.guardar_snapshot(nota.id, {"valor": nota.valor})
            nota.valor = valor
            nota.save()

        return nota

    @staticmethod
    def obtener_notas_matricula(matricula_id):
        """
        Obtiene todas las notas de una matrícula.

        Args:
            matricula_id: ID de la matrícula

        Returns:
            QuerySet: Notas de la matrícula
        """
        return Nota.objects.filter(
            matricula_id=matricula_id
        ).select_related('componente').order_by('componente__orden')

    @staticmethod
    def calcular_promedio_matricula(matricula_id):
        """
        Strategy Pattern: Calcula el promedio ponderado de una matrícula.

        Args:
            matricula_id: ID de la matrícula

        Returns:
            dict: {
                'promedio': Decimal o None,
                'estado': str ('APROBADO', 'DESAPROBADO', 'PENDIENTE'),
                'notas_completas': bool
            }
        """
        matricula = Matricula.objects.get(pk=matricula_id)
        promedio = Nota.calcular_promedio_ponderado(matricula)
        estado = Nota.estado_aprobacion(promedio)

        # Verificar si todas las notas están completas
        total_componentes = ComponenteEvaluacion.objects.filter(
            curso=matricula.seccion.curso
        ).count()

        notas_registradas = Nota.objects.filter(
            matricula=matricula,
            valor__isnull=False
        ).count()

        notas_completas = (total_componentes == notas_registradas)

        return {
            'promedio': promedio,
            'estado': estado,
            'notas_completas': notas_completas
        }

    @staticmethod
    def obtener_estadisticas_seccion(seccion_id):
        """
        Calcula estadísticas de notas de una sección.

        Args:
            seccion_id: ID de la sección

        Returns:
            dict: Estadísticas de la sección
        """
        from academic_system.models import Matricula

        matriculas = Matricula.objects.filter(seccion_id=seccion_id, is_active=True)

        estadisticas = {
            'total_alumnos': matriculas.count(),
            'aprobados': 0,
            'desaprobados': 0,
            'pendientes': 0,
            'promedio_general': None,
            'distribucion_notas': {
                '18-20': 0,
                '16-17': 0,
                '14-15': 0,
                '11-13': 0,
                '00-10': 0,
                'sin_nota': 0
            }
        }

        promedios = []

        for matricula in matriculas:
            resultado = NotaService.calcular_promedio_matricula(matricula.id)
            promedio = resultado['promedio']
            estado = resultado['estado']

            if estado == 'APROBADO':
                estadisticas['aprobados'] += 1
            elif estado == 'DESAPROBADO':
                estadisticas['desaprobados'] += 1
            else:
                estadisticas['pendientes'] += 1

            # Distribución de notas
            if promedio is None:
                estadisticas['distribucion_notas']['sin_nota'] += 1
            else:
                promedios.append(float(promedio))
                if promedio >= Decimal('18'):
                    estadisticas['distribucion_notas']['18-20'] += 1
                elif promedio >= Decimal('16'):
                    estadisticas['distribucion_notas']['16-17'] += 1
                elif promedio >= Decimal('14'):
                    estadisticas['distribucion_notas']['14-15'] += 1
                elif promedio >= Decimal('11'):
                    estadisticas['distribucion_notas']['11-13'] += 1
                else:
                    estadisticas['distribucion_notas']['00-10'] += 1

        # Calcular promedio general
        if promedios:
            estadisticas['promedio_general'] = round(sum(promedios) / len(promedios), 2)

        return estadisticas

    @staticmethod
    def obtener_top_alumnos(seccion_id, limite=5, orden='desc'):
        """
        Obtiene los mejores o peores alumnos de una sección.

        Args:
            seccion_id: ID de la sección
            limite: Número de alumnos a retornar
            orden: 'desc' para mejores, 'asc' para peores

        Returns:
            list: Lista de tuplas (alumno, promedio)
        """
        from academic_system.models import Matricula

        matriculas = Matricula.objects.filter(
            seccion_id=seccion_id,
            is_active=True
        ).select_related('alumno')

        alumnos_con_promedio = []

        for matricula in matriculas:
            promedio = Nota.calcular_promedio_ponderado(matricula)
            if promedio is not None:
                alumnos_con_promedio.append((matricula.alumno, float(promedio)))

        # Ordenar
        reverse = (orden == 'desc')
        alumnos_ordenados = sorted(alumnos_con_promedio, key=lambda x: x[1], reverse=reverse)

        return alumnos_ordenados[:limite]

    @staticmethod
    def obtener_progreso_evaluaciones(seccion_id):
        """
        Obtiene el promedio de cada componente de evaluación en una sección.

        Args:
            seccion_id: ID de la sección

        Returns:
            list: Lista de tuplas (componente_nombre, promedio)
        """
        from academic_system.models import Matricula, Seccion

        seccion = Seccion.objects.get(pk=seccion_id)
        componentes = ComponenteEvaluacion.objects.filter(
            curso=seccion.curso
        ).order_by('orden')

        progreso = []

        for componente in componentes:
            notas = Nota.objects.filter(
                matricula__seccion=seccion,
                componente=componente,
                valor__isnull=False
            )

            if notas.exists():
                promedio = sum(float(n.valor) for n in notas) / len(notas)
                progreso.append((componente.nombre, round(promedio, 2)))
            else:
                progreso.append((componente.nombre, 0))

        return progreso
