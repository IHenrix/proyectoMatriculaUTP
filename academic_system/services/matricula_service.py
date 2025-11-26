"""
MatriculaService - Servicio para gestión de matrículas

Patrones de Diseño:
- Service Layer Pattern
- Strategy Pattern: Validaciones de matrícula
- Command Pattern: Acciones de matrícula
- GRASP - Information Expert
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from academic_system.models import Matricula, Seccion, Usuario, Ciclo, Nota, ComponenteEvaluacion


class MatriculaService:
    """
    Servicio para gestión de matrículas.

    Implementa Strategy Pattern para diferentes validaciones.
    Command Pattern para ejecutar comandos de matrícula.
    """

    @staticmethod
    def validar_matricula(alumno, seccion):
        """
        Strategy Pattern: Validación de matrícula.

        Args:
            alumno: Usuario alumno
            seccion: Sección a matricular

        Raises:
            ValidationError: Si la matrícula no es válida
        """
        # Validación 1: El ciclo debe permitir matrícula
        if not seccion.ciclo.puede_matricularse():
            raise ValidationError('El ciclo no está en periodo de matrícula')

        # Validación 2: Debe haber vacantes
        if not seccion.tiene_vacantes:
            raise ValidationError('No hay vacantes disponibles en esta sección')

        # Validación 3: El alumno no debe estar ya matriculado en esta sección
        if Matricula.objects.filter(alumno=alumno, seccion=seccion, is_active=True).exists():
            raise ValidationError('Ya estás matriculado en esta sección')

        # Validación 4: El alumno no puede matricularse en dos secciones del mismo curso en el mismo ciclo
        matriculas_curso = Matricula.objects.filter(
            alumno=alumno,
            seccion__curso=seccion.curso,
            seccion__ciclo=seccion.ciclo,
            is_active=True
        )
        if matriculas_curso.exists():
            raise ValidationError(f'Ya estás matriculado en otra sección de {seccion.curso.nombre}')

        return True

    @staticmethod
    @transaction.atomic
    def matricular_alumno(alumno_id, seccion_id):
        """
        Command Pattern: Ejecuta el comando de matricular alumno.

        Args:
            alumno_id: ID del alumno
            seccion_id: ID de la sección

        Returns:
            Matricula: Matrícula creada o reactivada

        Raises:
            ValidationError: Si la matrícula no es válida
        """
        alumno = Usuario.objects.get(pk=alumno_id, rol='alumno')
        seccion = Seccion.objects.get(pk=seccion_id)

        # Validar matrícula
        MatriculaService.validar_matricula(alumno, seccion)

        # Verificar si existe una matrícula inactiva (alumno que se desmatriculó antes)
        matricula_existente = Matricula.objects.filter(
            alumno=alumno,
            seccion=seccion,
            is_active=False
        ).first()

        if matricula_existente:
            # Reactivar matrícula existente
            matricula_existente.is_active = True
            matricula_existente.save()

            matricula = matricula_existente
        else:
            # Crear nueva matrícula
            matricula = Matricula.objects.create(
                alumno=alumno,
                seccion=seccion
            )

            # Crear notas vacías para cada componente de evaluación
            componentes = ComponenteEvaluacion.objects.filter(curso=seccion.curso)
            for componente in componentes:
                Nota.objects.create(
                    matricula=matricula,
                    componente=componente
                )

        return matricula

    @staticmethod
    @transaction.atomic
    def cambiar_seccion(matricula_id, nueva_seccion_id):
        """
        Command Pattern: Cambia un alumno de una sección a otra.

        Args:
            matricula_id: ID de la matrícula actual
            nueva_seccion_id: ID de la nueva sección

        Returns:
            Matricula: Nueva matrícula

        Raises:
            ValidationError: Si el cambio no es válido
        """
        matricula_actual = Matricula.objects.get(pk=matricula_id)
        nueva_seccion = Seccion.objects.get(pk=nueva_seccion_id)

        # Validar que sea del mismo curso y ciclo
        if matricula_actual.seccion.curso != nueva_seccion.curso:
            raise ValidationError('Solo puedes cambiar a otra sección del mismo curso')

        if matricula_actual.seccion.ciclo != nueva_seccion.ciclo:
            raise ValidationError('Solo puedes cambiar a otra sección del mismo ciclo')

        # Validar que el ciclo permita cambios
        if not nueva_seccion.ciclo.puede_matricularse():
            raise ValidationError('El periodo de matrícula ha cerrado')

        # Validar que haya vacantes
        if not nueva_seccion.tiene_vacantes:
            raise ValidationError('No hay vacantes disponibles en la nueva sección')

        # Eliminar matrícula actual (libera vacante)
        alumno = matricula_actual.alumno
        matricula_actual.delete()

        # Crear nueva matrícula
        return MatriculaService.matricular_alumno(alumno.id, nueva_seccion_id)

    @staticmethod
    @transaction.atomic
    def desmatricular_alumno(matricula_id):
        """
        Command Pattern: Desmatricula un alumno.

        Args:
            matricula_id: ID de la matrícula

        Raises:
            ValidationError: Si no se puede desmatricular
        """
        matricula = Matricula.objects.get(pk=matricula_id)

        # Validar que el ciclo permita desmatrícula
        if not matricula.seccion.ciclo.puede_matricularse():
            raise ValidationError('El periodo de matrícula ha cerrado')

        # Eliminar matrícula (las notas se eliminan en cascada)
        matricula.delete()

    @staticmethod
    def obtener_matriculas_alumno(alumno_id, ciclo_id=None):
        """
        Obtiene las matrículas de un alumno.

        Args:
            alumno_id: ID del alumno
            ciclo_id: ID del ciclo (opcional)

        Returns:
            QuerySet: Matrículas del alumno
        """
        query = Matricula.objects.filter(alumno_id=alumno_id, is_active=True)

        if ciclo_id:
            query = query.filter(seccion__ciclo_id=ciclo_id)

        return query.select_related('seccion', 'seccion__curso', 'seccion__ciclo')

    @staticmethod
    def calcular_creditos_totales(alumno_id, ciclo_id):
        """
        Information Expert: Calcula créditos totales de un alumno en un ciclo.

        Args:
            alumno_id: ID del alumno
            ciclo_id: ID del ciclo

        Returns:
            int: Total de créditos matriculados
        """
        matriculas = MatriculaService.obtener_matriculas_alumno(alumno_id, ciclo_id)
        return sum(m.creditos for m in matriculas)

    @staticmethod
    def obtener_secciones_disponibles(ciclo_id):
        """
        Obtiene secciones disponibles para matrícula.

        Args:
            ciclo_id: ID del ciclo

        Returns:
            QuerySet: Secciones con vacantes
        """
        from django.db.models import F

        return Seccion.objects.filter(
            ciclo_id=ciclo_id,
            is_active=True
        ).filter(
            vacantes_ocupadas__lt=F('vacantes_totales')
        ).select_related(
            'curso', 'ciclo'
        ).prefetch_related('profesores').order_by('curso__nombre')

    @staticmethod
    def obtener_alumnos_por_seccion(seccion_id):
        """
        Obtiene todos los alumnos matriculados en una sección.

        Args:
            seccion_id: ID de la sección

        Returns:
            QuerySet: Matrículas de la sección
        """
        return Matricula.objects.filter(
            seccion_id=seccion_id,
            is_active=True
        ).select_related('alumno').order_by('alumno__apellido_paterno')
