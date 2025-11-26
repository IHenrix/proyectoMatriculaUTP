"""
URLs del módulo academic_system
"""

from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Administrador
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/usuarios/', views.admin_usuarios_list, name='admin_usuarios_list'),
    path('admin/usuarios/crear/', views.admin_usuario_create, name='admin_usuario_create'),

    # Profesor
    path('profesor/dashboard/', views.profesor_dashboard, name='profesor_dashboard'),
    path('profesor/seccion/<int:seccion_id>/', views.profesor_seccion_detalle, name='profesor_seccion_detalle'),
    path('profesor/nota/<int:matricula_id>/<int:componente_id>/', views.profesor_registrar_nota, name='profesor_registrar_nota'),
    path('profesor/exportar/alumnos/<int:seccion_id>/<str:formato>/', views.profesor_exportar_lista_alumnos, name='profesor_exportar_lista_alumnos'),
    path('profesor/exportar/notas/<int:seccion_id>/<str:formato>/', views.profesor_exportar_notas, name='profesor_exportar_notas'),

    # Alumno
    path('alumno/dashboard/', views.alumno_dashboard, name='alumno_dashboard'),
    path('alumno/matricula/', views.alumno_matricula, name='alumno_matricula'),
    path('alumno/matricular/<int:seccion_id>/', views.alumno_matricular_seccion, name='alumno_matricular_seccion'),
    path('alumno/desmatricular/<int:matricula_id>/', views.alumno_desmatricular, name='alumno_desmatricular'),
    path('alumno/mis-cursos/', views.alumno_mis_cursos, name='alumno_mis_cursos'),

    # API para gráficos
    path('api/estadisticas/<int:seccion_id>/', views.api_estadisticas_seccion, name='api_estadisticas_seccion'),
]
