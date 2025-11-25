"""
Modelos del Sistema de Matrículas y Notas

Patrones de Diseño Aplicados:
- Active Record Pattern (Django ORM)
- Repository Pattern (mediante Django ORM)
- Factory Pattern (en métodos de creación)
- GRASP - Information Expert (lógica de negocio en modelos)
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
import random
import string


class Usuario(AbstractUser):
    """
    Modelo de Usuario personalizado que extiende AbstractUser.

    Patrones aplicados:
    - Template Method Pattern (AbstractUser)
    - Factory Pattern (crear usuarios según rol)
    - Single Responsibility Principle (maneja solo datos de usuario)
    """

    ROLES = (
        ('administrador', 'Administrador'),
        ('profesor', 'Profesor'),
        ('alumno', 'Alumno'),
    )

    TIPO_DOCUMENTO = (
        ('DNI', 'DNI'),
        ('CE', 'Carnet de Extranjería'),
        ('PASAPORTE', 'Pasaporte'),
    )

    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    # Código único del usuario (ej: U23316357)
    codigo = models.CharField(max_length=10, unique=True, db_index=True)

    # Información personal
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO, default='DNI')
    numero_documento = models.CharField(max_length=20, unique=True)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO, blank=True, null=True)

    # Rol del usuario
    rol = models.CharField(max_length=20, choices=ROLES)

    # Flag para inactivar usuarios (Soft Delete Pattern)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.codigo} - {self.get_full_name()}"

    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.apellido_paterno} {self.apellido_materno}"

    @staticmethod
    def generar_codigo():
        """
        Factory Method para generar código único de usuario.
        Formato: U + 8 dígitos aleatorios
        """
        while True:
            codigo = 'U' + ''.join(random.choices(string.digits, k=8))
            if not Usuario.objects.filter(codigo=codigo).exists():
                return codigo

    def save(self, *args, **kwargs):
        """Override save para generar código automáticamente"""
        if not self.codigo:
            self.codigo = self.generar_codigo()
        if not self.username:
            self.username = self.codigo
        super().save(*args, **kwargs)


class Curso(models.Model):
    """
    Modelo que representa un curso académico.

    Principios SOLID:
    - SRP: Solo maneja información del curso
    """
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    creditos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'curso'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.creditos} créditos)"


class Ciclo(models.Model):
    """
    Modelo que representa un ciclo académico.

    Patrón Strategy: Diferentes estrategias de validación de matrícula.
    """
    nombre = models.CharField(max_length=50, unique=True)  # Ej: 2025-2
    fecha_inicio_matricula = models.DateField()
    fecha_fin_matricula = models.DateField()
    matricula_abierta = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ciclo'
        verbose_name = 'Ciclo'
        verbose_name_plural = 'Ciclos'
        ordering = ['-nombre']

    def __str__(self):
        return self.nombre

    def puede_matricularse(self):
        """
        Strategy Pattern: Validación de si se puede matricular.
        Information Expert: El ciclo conoce su estado de matrícula.
        """
        from datetime import date
        hoy = date.today()
        return (
            self.matricula_abierta and
            self.fecha_inicio_matricula <= hoy <= self.fecha_fin_matricula
        )

    def clean(self):
        """Validación de fechas"""
        if self.fecha_inicio_matricula and self.fecha_fin_matricula:
            if self.fecha_inicio_matricula > self.fecha_fin_matricula:
                raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin')


class Seccion(models.Model):
    """
    Modelo que representa una sección de un curso en un ciclo.

    Patrones:
    - Composite Pattern: Sección contiene curso, ciclo, profesores
    - GRASP Creator: Sección crea relación con profesores
    """

    MODALIDAD = (
        ('virtual', 'Virtual'),
        ('remoto', 'Remoto'),
        ('presencial', 'Presencial'),
    )

    TURNO = (
        ('mañana', 'Mañana'),
        ('tarde', 'Tarde'),
    )

    codigo = models.CharField(max_length=10)  # Ej: 15000
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='secciones')
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, related_name='secciones')
    modalidad = models.CharField(max_length=20, choices=MODALIDAD)
    turno = models.CharField(max_length=10, choices=TURNO, blank=True, null=True)

    # Horario (solo para modalidad no virtual)
    dias_semana = models.CharField(max_length=100, blank=True, null=True,
                                    help_text="Ej: Lunes, Miércoles")
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    # Vacantes
    vacantes_totales = models.IntegerField(validators=[MinValueValidator(1)])
    vacantes_ocupadas = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Relación N:N con profesores
    profesores = models.ManyToManyField(
        Usuario,
        limit_choices_to={'rol': 'profesor', 'is_active': True},
        related_name='secciones_profesor'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'seccion'
        verbose_name = 'Sección'
        verbose_name_plural = 'Secciones'
        unique_together = ['codigo', 'curso', 'ciclo']
        ordering = ['ciclo', 'curso', 'codigo']

    def __str__(self):
        return f"{self.curso.nombre} - {self.codigo} ({self.ciclo.nombre})"

    @property
    def vacantes_disponibles(self):
        """Information Expert: La sección conoce sus vacantes disponibles"""
        return self.vacantes_totales - self.vacantes_ocupadas

    @property
    def tiene_vacantes(self):
        """Strategy Pattern: Validación de vacantes"""
        return self.vacantes_disponibles > 0

    @property
    def pocas_vacantes(self):
        """Alerta de pocas vacantes (≤5)"""
        return 0 < self.vacantes_disponibles <= 5

    @property
    def ultima_vacante(self):
        """Alerta de última vacante"""
        return self.vacantes_disponibles == 1

    def get_modalidad_icon(self):
        """Retorna icono de Font Awesome según modalidad"""
        icons = {
            'presencial': 'school',
            'virtual': 'laptop',
            'remoto': 'video',
        }
        return icons.get(self.modalidad, 'book')

    def get_turno_icon(self):
        """Retorna icono de Font Awesome según turno"""
        icons = {
            'mañana': 'sun',
            'tarde': 'cloud-sun',
            'noche': 'moon',
        }
        return icons.get(self.turno, 'clock')

    @property
    def horario_display(self):
        """Template Method Pattern: Formato de horario según modalidad"""
        if self.modalidad == 'virtual':
            return '24/7'
        elif self.hora_inicio and self.hora_fin:
            return f"{self.dias_semana} {self.hora_inicio.strftime('%H:%M')}-{self.hora_fin.strftime('%H:%M')}"
        return 'Sin horario definido'

    def clean(self):
        """Validaciones del modelo"""
        if self.modalidad != 'virtual':
            if not self.turno:
                raise ValidationError('Debe especificar el turno para modalidad no virtual')
            if not self.hora_inicio or not self.hora_fin:
                raise ValidationError('Debe especificar horario para modalidad no virtual')

        if self.vacantes_ocupadas > self.vacantes_totales:
            raise ValidationError('Las vacantes ocupadas no pueden superar las vacantes totales')


class ComponenteEvaluacion(models.Model):
    """
    Modelo que representa un componente de evaluación de un curso.

    Patrón Composite: Curso compuesto por componentes de evaluación.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='componentes')
    nombre = models.CharField(max_length=200)  # Ej: Práctica Calificada 1
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    orden = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'componente_evaluacion'
        verbose_name = 'Componente de Evaluación'
        verbose_name_plural = 'Componentes de Evaluación'
        ordering = ['curso', 'orden']
        unique_together = ['curso', 'nombre']

    def __str__(self):
        return f"{self.curso.nombre} - {self.nombre} ({self.porcentaje}%)"

    @staticmethod
    def validar_porcentajes_curso(curso):
        """
        Validación de que los porcentajes de un curso sumen 100%.
        Strategy Pattern: Estrategia de validación.
        """
        total = ComponenteEvaluacion.objects.filter(curso=curso).aggregate(
            total=models.Sum('porcentaje')
        )['total'] or Decimal('0')

        return total == Decimal('100.00')


class Matricula(models.Model):
    """
    Modelo que representa la matrícula de un alumno en una sección.

    Patrones:
    - Command Pattern: Matrícula como comando que modifica estado
    - Observer Pattern: Puede notificar cambios
    """
    alumno = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'alumno'},
        related_name='matriculas'
    )
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='matriculas')

    fecha_matricula = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matricula'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = ['alumno', 'seccion']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.alumno.get_full_name()} - {self.seccion}"

    @property
    def creditos(self):
        """Information Expert: La matrícula conoce sus créditos"""
        return self.seccion.curso.creditos

    def save(self, *args, **kwargs):
        """
        Override save para incrementar vacantes ocupadas.
        Command Pattern: Ejecuta acciones al matricular.
        """
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.is_active:
            # Incrementar vacantes ocupadas
            self.seccion.vacantes_ocupadas += 1
            self.seccion.save()

    def delete(self, *args, **kwargs):
        """Override delete para decrementar vacantes ocupadas"""
        if self.is_active:
            self.seccion.vacantes_ocupadas -= 1
            self.seccion.save()
        super().delete(*args, **kwargs)


class Nota(models.Model):
    """
    Modelo que representa una nota de un alumno en un componente de evaluación.

    Patrones:
    - Strategy Pattern: Cálculo de promedios
    - Observer Pattern: Notifica cambios de nota
    """
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='notas')
    componente = models.ForeignKey(ComponenteEvaluacion, on_delete=models.CASCADE)

    # Nota en escala 0-20 (sistema peruano)
    valor = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nota'
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ['matricula', 'componente']
        ordering = ['matricula', 'componente__orden']

    def __str__(self):
        nota_str = self.valor if self.valor is not None else '-'
        return f"{self.matricula.alumno.get_full_name()} - {self.componente.nombre}: {nota_str}"

    @staticmethod
    def calcular_promedio_ponderado(matricula):
        """
        Strategy Pattern: Cálculo de promedio ponderado.
        Information Expert: Las notas conocen cómo calcularse.

        Args:
            matricula: Instancia de Matrícula

        Returns:
            Decimal: Promedio ponderado o None si no hay notas
        """
        notas = Nota.objects.filter(matricula=matricula, valor__isnull=False)

        if not notas.exists():
            return None

        total_ponderado = Decimal('0')
        total_porcentaje = Decimal('0')

        for nota in notas:
            if nota.valor is not None:
                total_ponderado += (nota.valor * nota.componente.porcentaje) / Decimal('100')
                total_porcentaje += nota.componente.porcentaje

        if total_porcentaje == Decimal('0'):
            return None

        # Si solo hay notas parciales, ajustar al 100%
        if total_porcentaje < Decimal('100'):
            promedio_parcial = (total_ponderado * Decimal('100')) / total_porcentaje
            return round(promedio_parcial, 2)

        return round(total_ponderado, 2)

    @staticmethod
    def estado_aprobacion(promedio):
        """
        Strategy Pattern: Determina estado de aprobación.

        Args:
            promedio: Decimal o None

        Returns:
            str: 'APROBADO', 'DESAPROBADO' o 'PENDIENTE'
        """
        if promedio is None:
            return 'PENDIENTE'

        NOTA_MINIMA_APROBACION = Decimal('11.6')

        if promedio >= NOTA_MINIMA_APROBACION:
            return 'APROBADO'
        else:
            return 'DESAPROBADO'

    def clean(self):
        """Validación: la nota debe pertenecer al curso de la matrícula"""
        if self.componente.curso != self.matricula.seccion.curso:
            raise ValidationError('El componente no pertenece al curso de la matrícula')
