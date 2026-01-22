"""
Django Admin Configuration

Configuración del panel de administración de Django.
Permite gestionar los modelos desde la interfaz web.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Curso, Ciclo, Seccion, ComponenteEvaluacion, Matricula, Nota

# Personaliza los textos del panel de administración
admin.site.site_header = "Panel de Matrículas SENATI"
admin.site.site_title = "Panel de Matrículas SENATI"
admin.site.index_title = "Administración del sistema"


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """Admin para el modelo Usuario personalizado"""

    list_display = ('codigo', 'get_full_name', 'email', 'rol', 'is_active', 'created_at')
    list_filter = ('rol', 'is_active', 'tipo_documento', 'sexo')
    search_fields = ('codigo', 'first_name', 'apellido_paterno', 'apellido_materno', 'numero_documento', 'email')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {
            'fields': (
                'codigo', 'first_name', 'apellido_paterno', 'apellido_materno',
                'tipo_documento', 'numero_documento', 'email', 'telefono', 'direccion',
                'fecha_nacimiento', 'sexo'
            )
        }),
        ('Rol y Permisos', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 'first_name', 'apellido_paterno',
                'apellido_materno', 'numero_documento', 'rol'
            ),
        }),
    )


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    """Admin para el modelo Curso"""

    list_display = ('nombre', 'creditos', 'is_active', 'created_at')
    list_filter = ('is_active', 'creditos')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


@admin.register(Ciclo)
class CicloAdmin(admin.ModelAdmin):
    """Admin para el modelo Ciclo"""

    list_display = (
        'nombre', 'fecha_inicio_ciclo', 'fecha_fin_ciclo',
        'matricula_abierta', 'ciclo_terminado', 'created_at'
    )
    list_filter = ('ciclo_terminado', 'matricula_abierta')
    search_fields = ('nombre',)
    ordering = ('-nombre',)

    fieldsets = (
        ('Información del Ciclo', {
            'fields': ('nombre', 'fecha_inicio_ciclo', 'fecha_fin_ciclo'),
            'description': 'Rango de fechas del ciclo académico'
        }),
        ('Período de Matrícula', {
            'fields': ('fecha_inicio_matricula', 'fecha_fin_matricula', 'matricula_abierta'),
            'description': 'Configuración del período de matrícula'
        }),
        ('Estado del Ciclo', {
            'fields': ('ciclo_terminado',),
            'description': 'Marque esta opción cuando el ciclo haya finalizado. Las notas quedarán bloqueadas.'
        }),
    )


@admin.register(Seccion)
class SeccionAdmin(admin.ModelAdmin):
    """Admin para el modelo Seccion"""

    list_display = (
        'codigo', 'curso', 'ciclo', 'modalidad', 'turno',
        'vacantes_disponibles', 'vacantes_totales', 'is_active'
    )
    list_filter = ('ciclo', 'modalidad', 'turno', 'is_active')
    search_fields = ('codigo', 'curso__nombre')
    filter_horizontal = ('profesores',)
    ordering = ('-ciclo__nombre', 'curso__nombre', 'codigo')

    def vacantes_disponibles(self, obj):
        return obj.vacantes_disponibles
    vacantes_disponibles.short_description = 'Vacantes Disponibles'


@admin.register(ComponenteEvaluacion)
class ComponenteEvaluacionAdmin(admin.ModelAdmin):
    """Admin para el modelo ComponenteEvaluacion"""

    list_display = ('nombre', 'curso', 'porcentaje', 'orden', 'created_at')
    list_filter = ('curso',)
    search_fields = ('nombre', 'curso__nombre')
    ordering = ('curso', 'orden')


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    """Admin para el modelo Matricula"""

    list_display = ('alumno', 'seccion', 'creditos', 'fecha_matricula', 'is_active')
    list_filter = ('seccion__ciclo', 'seccion__curso', 'is_active')
    search_fields = (
        'alumno__codigo', 'alumno__first_name', 'alumno__apellido_paterno',
        'seccion__codigo', 'seccion__curso__nombre'
    )
    ordering = ('-created_at',)
    raw_id_fields = ('alumno', 'seccion')


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    """Admin para el modelo Nota"""

    list_display = ('matricula', 'componente', 'valor', 'updated_at')
    list_filter = ('componente__curso', 'matricula__seccion__ciclo')
    search_fields = (
        'matricula__alumno__codigo', 'matricula__alumno__first_name',
        'matricula__alumno__apellido_paterno', 'componente__nombre'
    )
    ordering = ('-updated_at',)
    raw_id_fields = ('matricula', 'componente')
