"""
Views del Sistema de Matrículas y Notas

Patrones de Diseño:
- MVC/MVT Pattern (Django)
- GRASP - Controller Pattern
- Facade Pattern (servicios simplifican operaciones)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .decorators import admin_required, profesor_required, alumno_required
from .models import Usuario, Curso, Ciclo, Seccion, ComponenteEvaluacion, Matricula, Nota
from .services import UsuarioService, MatriculaService, NotaService, ReporteService
from academic_system.services.reporte_service import ResponseAdapter
from academic_system.services.vacante_proxy import SeccionVacanteProxy


# ==============================================================================
# VISTAS DE AUTENTICACIÓN
# ==============================================================================

def login_view(request):
    """
    Vista de login del sistema.

    Controller Pattern: Maneja la lógica de autenticación.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.get_full_name()}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Tu cuenta está inactiva. Contacta al administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    """Vista de logout"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Dashboard principal que redirige según el rol del usuario.

    Strategy Pattern: Diferentes dashboards según rol.
    """
    user = request.user

    if user.rol == 'administrador':
        return redirect('admin_dashboard')
    elif user.rol == 'profesor':
        return redirect('profesor_dashboard')
    elif user.rol == 'alumno':
        return redirect('alumno_dashboard')
    else:
        messages.error(request, 'Rol no reconocido.')
        return redirect('login')


# ==============================================================================
# VISTAS DE ADMINISTRADOR
# ==============================================================================

@admin_required
def admin_dashboard(request):
    """Dashboard del administrador"""
    context = {
        'total_usuarios': Usuario.objects.filter(is_active=True).count(),
        'total_alumnos': Usuario.objects.filter(rol='alumno', is_active=True).count(),
        'total_profesores': Usuario.objects.filter(rol='profesor', is_active=True).count(),
        'total_cursos': Curso.objects.filter(is_active=True).count(),
        'total_secciones': Seccion.objects.filter(is_active=True).count(),
    }
    return render(request, 'admin/dashboard.html', context)


@admin_required
def admin_usuarios_list(request):
    """Lista de usuarios"""
    rol_filter = request.GET.get('rol', '')
    search = request.GET.get('search', '')

    usuarios = Usuario.objects.filter(is_active=True)

    if rol_filter:
        usuarios = usuarios.filter(rol=rol_filter)

    if search:
        usuarios = usuarios.filter(
            Q(codigo__icontains=search) |
            Q(first_name__icontains=search) |
            Q(apellido_paterno__icontains=search) |
            Q(apellido_materno__icontains=search) |
            Q(numero_documento__icontains=search)
        )

    context = {
        'usuarios': usuarios.order_by('-created_at'),
        'rol_filter': rol_filter,
        'search': search,
    }
    return render(request, 'admin/usuarios_list.html', context)


@admin_required
def admin_usuario_create(request):
    """Crear nuevo usuario"""
    if request.method == 'POST':
        try:
            datos = {
                'nombre': request.POST.get('nombre'),
                'apellido_paterno': request.POST.get('apellido_paterno'),
                'apellido_materno': request.POST.get('apellido_materno'),
                'tipo_documento': request.POST.get('tipo_documento'),
                'numero_documento': request.POST.get('numero_documento'),
                'email': request.POST.get('email'),
                'telefono': request.POST.get('telefono'),
                'direccion': request.POST.get('direccion'),
                'fecha_nacimiento': request.POST.get('fecha_nacimiento') or None,
                'sexo': request.POST.get('sexo'),
                'rol': request.POST.get('rol'),
                'username': request.POST.get('username'),
                'password': request.POST.get('password') or request.POST.get('numero_documento'),
            }

            usuario = UsuarioService.crear_usuario(datos)
            messages.success(request, f'Usuario {usuario.codigo} creado exitosamente.')
            return redirect('admin_usuarios_list')

        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')

    return render(request, 'admin/usuario_form.html')


# ==============================================================================
# VISTAS DE PROFESOR
# ==============================================================================

@profesor_required
def profesor_dashboard(request):
    """Dashboard del profesor con selector de ciclo"""
    profesor = request.user

    # Obtener todos los ciclos donde el profesor tiene secciones asignadas
    ciclos_disponibles = Ciclo.objects.filter(
        secciones__profesores=profesor,
        secciones__is_active=True
    ).distinct().order_by('-nombre')

    # Obtener el ciclo seleccionado (desde query param o el más reciente)
    ciclo_id = request.GET.get('ciclo_id')
    if ciclo_id:
        try:
            ciclo_seleccionado = Ciclo.objects.get(pk=ciclo_id)
        except Ciclo.DoesNotExist:
            ciclo_seleccionado = ciclos_disponibles.first() if ciclos_disponibles.exists() else None
    else:
        ciclo_seleccionado = ciclos_disponibles.first() if ciclos_disponibles.exists() else None

    # Filtrar secciones por ciclo seleccionado
    if ciclo_seleccionado:
        secciones = Seccion.objects.filter(
            profesores=profesor,
            ciclo=ciclo_seleccionado,
            is_active=True
        ).select_related('curso', 'ciclo').prefetch_related('matriculas')
    else:
        secciones = Seccion.objects.none()

    context = {
        'secciones': secciones,
        'ciclos_disponibles': ciclos_disponibles,
        'ciclo_seleccionado': ciclo_seleccionado,
    }
    return render(request, 'profesor/dashboard.html', context)


@profesor_required
def profesor_seccion_detalle(request, seccion_id):
    """Detalle de una sección con lista de alumnos y notas"""
    seccion = get_object_or_404(Seccion, pk=seccion_id, profesores=request.user)
    matriculas = MatriculaService.obtener_alumnos_por_seccion(seccion_id)
    componentes = ComponenteEvaluacion.objects.filter(curso=seccion.curso).order_by('orden')

    # Obtener estadísticas
    estadisticas = NotaService.obtener_estadisticas_seccion(seccion_id)

    # Preparar datos de notas para cada matrícula
    for matricula in matriculas:
        # Obtener notas
        notas = Nota.objects.filter(matricula=matricula).select_related('componente')
        notas_dict = {nota.componente.id: nota for nota in notas}

        # Crear lista de notas en el orden de componentes
        matricula.notas_ordenadas = []
        for componente in componentes:
            nota = notas_dict.get(componente.id)
            # Si no existe la nota, crear una instancia temporal (sin guardar en BD)
            if nota is None:
                nota = Nota(matricula=matricula, componente=componente, valor=None)
            matricula.notas_ordenadas.append(nota)

        # Calcular promedio
        resultado = NotaService.calcular_promedio_matricula(matricula.id)
        matricula.promedio_final = resultado['promedio']
        matricula.estado_final = resultado['estado'] if resultado['notas_completas'] else 'PENDIENTE'
        matricula.notas_completas = resultado['notas_completas']

    context = {
        'seccion': seccion,
        'matriculas': matriculas,
        'componentes': componentes,
        'estadisticas': estadisticas,
        'ciclo_terminado': seccion.ciclo.ciclo_terminado,
    }
    return render(request, 'profesor/seccion_detalle.html', context)


@profesor_required
def profesor_registrar_nota(request, matricula_id, componente_id):
    """Registrar o actualizar una nota"""
    if request.method == 'POST':
        try:
            # Verificar si el ciclo está terminado
            matricula = get_object_or_404(Matricula, pk=matricula_id)
            if matricula.seccion.ciclo.ciclo_terminado:
                error_msg = 'El ciclo ha finalizado. No se pueden editar las notas.'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/x-www-form-urlencoded':
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    }, status=403)
                messages.error(request, error_msg)
                return redirect('profesor_seccion_detalle', seccion_id=matricula.seccion.id)

            valor = request.POST.get('valor')
            if valor:
                valor = float(valor)
            else:
                valor = None

            nota = NotaService.registrar_nota(matricula_id, componente_id, valor)

            # Si es petición AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/x-www-form-urlencoded':
                return JsonResponse({
                    'success': True,
                    'message': 'Nota registrada exitosamente',
                    'valor': str(nota.valor) if nota.valor is not None else None
                })

            messages.success(request, 'Nota registrada exitosamente.')

        except Exception as e:
            # Si es petición AJAX, devolver error JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/x-www-form-urlencoded':
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                }, status=400)

            messages.error(request, f'Error al registrar nota: {str(e)}')

    # Redirigir de vuelta a la sección (solo si no es AJAX)
    matricula = get_object_or_404(Matricula, pk=matricula_id)
    return redirect('profesor_seccion_detalle', seccion_id=matricula.seccion.id)


# ==============================================================================
# VISTAS DE ALUMNO
# ==============================================================================

@alumno_required
def alumno_dashboard(request):
    """Dashboard del alumno con estadísticas completas"""
    alumno = request.user
    from decimal import Decimal

    # Obtener ciclo activo (cualquier ciclo, no solo con matrícula abierta)
    try:
        ciclo_activo = Ciclo.objects.latest('nombre')
    except Ciclo.DoesNotExist:
        ciclo_activo = None

    # Obtener matrículas del alumno en el ciclo activo
    if ciclo_activo:
        matriculas = MatriculaService.obtener_matriculas_alumno(alumno.id, ciclo_activo.id)
        creditos_totales = MatriculaService.calcular_creditos_totales(alumno.id, ciclo_activo.id)
    else:
        matriculas = []
        creditos_totales = 0

    # Calcular estadísticas avanzadas
    cursos_data = []
    total_promedio = Decimal('0')
    cursos_con_promedio = 0
    cursos_aprobados = 0
    cursos_desaprobados = 0
    cursos_pendientes = 0
    mejor_nota = None
    peor_nota = None

    for matricula in matriculas:
        # Obtener notas del curso
        notas = Nota.objects.filter(matricula=matricula).select_related('componente')

        # Calcular promedio
        promedio = Nota.calcular_promedio_ponderado(matricula)
        estado = Nota.estado_aprobacion(promedio)

        # Verificar si todas las notas están registradas
        total_componentes = notas.count()
        notas_registradas = notas.filter(valor__isnull=False).count()
        notas_completas = total_componentes == notas_registradas and total_componentes > 0

        # Obtener última nota registrada
        ultima_nota = notas.filter(valor__isnull=False).order_by('-updated_at').first()

        curso_info = {
            'matricula': matricula,
            'promedio': promedio,
            'estado': estado,
            'notas_completas': notas_completas,
            'ultima_nota': ultima_nota,
            'total_notas': notas_registradas,
            'total_componentes': total_componentes,
        }
        cursos_data.append(curso_info)

        # Actualizar estadísticas
        if promedio is not None:
            total_promedio += promedio
            cursos_con_promedio += 1

            # Mejor y peor nota
            if mejor_nota is None or promedio > mejor_nota:
                mejor_nota = promedio
            if peor_nota is None or promedio < peor_nota:
                peor_nota = promedio

        # Contar estados
        if notas_completas:
            if estado == 'APROBADO':
                cursos_aprobados += 1
            elif estado == 'DESAPROBADO':
                cursos_desaprobados += 1
        else:
            cursos_pendientes += 1

    # Calcular promedio general
    promedio_general = (total_promedio / cursos_con_promedio) if cursos_con_promedio > 0 else None

    # Preparar datos para gráfico
    cursos_labels = []
    cursos_promedios = []
    for curso_info in cursos_data:
        if curso_info['promedio'] is not None:
            cursos_labels.append(curso_info['matricula'].seccion.curso.nombre[:20])
            cursos_promedios.append(float(curso_info['promedio']))

    context = {
        'ciclo_activo': ciclo_activo,
        'matriculas': matriculas,
        'creditos_totales': creditos_totales,
        'cursos_data': cursos_data,
        'promedio_general': promedio_general,
        'cursos_aprobados': cursos_aprobados,
        'cursos_desaprobados': cursos_desaprobados,
        'cursos_pendientes': cursos_pendientes,
        'mejor_nota': mejor_nota,
        'peor_nota': peor_nota,
        'cursos_labels': cursos_labels,
        'cursos_promedios': cursos_promedios,
    }
    return render(request, 'alumno/dashboard.html', context)


@alumno_required
def alumno_matricula(request):
    """Vista de matrícula del alumno"""
    alumno = request.user

    # Verificar si hay un ciclo activo con matrícula abierta
    from datetime import date
    hoy = date.today()

    ciclo_activo = Ciclo.objects.filter(
        matricula_abierta=True,
        fecha_inicio_matricula__lte=hoy,
        fecha_fin_matricula__gte=hoy
    ).first()

    if not ciclo_activo:
        messages.error(request, 'El período de matrícula no está disponible actualmente.')
        return redirect('alumno_dashboard')

    # Obtener secciones disponibles
    secciones = MatriculaService.obtener_secciones_disponibles(ciclo_activo.id)

    # Obtener matrículas actuales del alumno
    matriculas_actuales = MatriculaService.obtener_matriculas_alumno(alumno.id, ciclo_activo.id)
    creditos_actuales = MatriculaService.calcular_creditos_totales(alumno.id, ciclo_activo.id)

    # Agrupar secciones por curso
    cursos_disponibles = {}
    for seccion in secciones:
        curso_id = seccion.curso.id
        if curso_id not in cursos_disponibles:
            cursos_disponibles[curso_id] = {
                'curso': seccion.curso,
                'secciones': [],
                'matriculado': False,
                'matricula_actual': None
            }
        cursos_disponibles[curso_id]['secciones'].append(seccion)

    # Marcar cursos en los que ya está matriculado
    for matricula in matriculas_actuales:
        curso_id = matricula.seccion.curso.id
        if curso_id in cursos_disponibles:
            cursos_disponibles[curso_id]['matriculado'] = True
            cursos_disponibles[curso_id]['matricula_actual'] = matricula

    context = {
        'ciclo': ciclo_activo,
        'cursos_disponibles': cursos_disponibles.values(),
        'creditos_actuales': creditos_actuales,
        'total_cursos_matriculados': matriculas_actuales.count(),
    }
    return render(request, 'alumno/matricula.html', context)


@alumno_required
def alumno_matricular_seccion(request, seccion_id):
    """Matricular alumno en una sección"""
    if request.method == 'POST':
        try:
            alumno = request.user
            MatriculaService.matricular_alumno(alumno.id, seccion_id)
            messages.success(request, '¡Matrícula exitosa!')

        except Exception as e:
            messages.error(request, f'Error al matricular: {str(e)}')

    return redirect('alumno_matricula')


@alumno_required
def alumno_desmatricular(request, matricula_id):
    """Desmatricular alumno de una sección"""
    if request.method == 'POST':
        try:
            alumno = request.user
            matricula = Matricula.objects.get(id=matricula_id, alumno=alumno)

            # Verificar que el ciclo permite desmatricularse
            if not matricula.seccion.ciclo.puede_matricularse():
                messages.error(request, 'El periodo de matrícula ha finalizado. No puedes retirarte del curso.')
                return redirect('alumno_matricula')

            # Desactivar la matr??cula
            matricula.is_active = False
            matricula.save(update_fields=["is_active"])

            # Actualizar vacantes con Proxy (protege contadores)
            seccion = matricula.seccion
            SeccionVacanteProxy(seccion).liberar_vacante()

            messages.success(request, f'Te has retirado exitosamente del curso: {matricula.seccion.curso.nombre}')

        except Matricula.DoesNotExist:
            messages.error(request, 'Matrícula no encontrada.')
        except Exception as e:
            messages.error(request, f'Error al retirarse: {str(e)}')

    return redirect('alumno_matricula')


@alumno_required
def alumno_mis_cursos(request):
    """Ver cursos matriculados y notas con selector de ciclo"""
    alumno = request.user

    # Obtener TODOS los ciclos donde el alumno tiene matrículas O que tienen secciones activas
    ciclos_con_matriculas = Ciclo.objects.filter(
        secciones__matriculas__alumno=alumno,
        secciones__matriculas__is_active=True
    ).distinct()

    # Obtener ciclos con matrícula abierta (donde puede matricularse)
    ciclos_abiertos = Ciclo.objects.filter(matricula_abierta=True).distinct()

    # Combinar ambos conjuntos y ordenar
    ciclos_disponibles = (ciclos_con_matriculas | ciclos_abiertos).distinct().order_by('-nombre')

    # Obtener el ciclo seleccionado (desde query param o el más reciente)
    ciclo_id = request.GET.get('ciclo_id')
    if ciclo_id:
        try:
            ciclo_seleccionado = Ciclo.objects.get(pk=ciclo_id)
        except Ciclo.DoesNotExist:
            ciclo_seleccionado = ciclos_disponibles.first() if ciclos_disponibles.exists() else None
    else:
        ciclo_seleccionado = ciclos_disponibles.first() if ciclos_disponibles.exists() else None

    # Obtener matrículas del ciclo seleccionado
    if ciclo_seleccionado:
        matriculas = Matricula.objects.filter(
            alumno=alumno,
            seccion__ciclo=ciclo_seleccionado,
            is_active=True
        ).select_related(
            'seccion', 'seccion__curso', 'seccion__ciclo'
        ).prefetch_related('seccion__profesores').order_by('seccion__curso__nombre')
    else:
        matriculas = Matricula.objects.none()

    # Obtener notas y promedios
    cursos_data = []
    for matricula in matriculas:
        notas = NotaService.obtener_notas_matricula(matricula.id)
        resultado = NotaService.calcular_promedio_matricula(matricula.id)

        cursos_data.append({
            'matricula': matricula,
            'notas': notas,
            'promedio': resultado['promedio'],
            'estado': resultado['estado'],
            'notas_completas': resultado['notas_completas'],
        })

    # Verificar si puede matricularse en el ciclo seleccionado
    puede_matricularse = False
    if ciclo_seleccionado and ciclo_seleccionado.matricula_abierta:
        puede_matricularse = True

    context = {
        'ciclo_activo': ciclo_seleccionado,  # Mantener nombre para compatibilidad con template
        'ciclos_disponibles': ciclos_disponibles,
        'ciclo_seleccionado': ciclo_seleccionado,
        'cursos_data': cursos_data,
        'puede_matricularse': puede_matricularse,
    }
    return render(request, 'alumno/mis_cursos.html', context)


# ==============================================================================
# VISTAS DE REPORTES
# ==============================================================================

@profesor_required
def profesor_exportar_lista_alumnos(request, seccion_id, formato='excel'):
    """Exportar lista de alumnos en Excel o PDF"""
    seccion = get_object_or_404(Seccion, pk=seccion_id, profesores=request.user)

    try:
        buffer = ReporteService.generar_lista_alumnos(seccion_id, formato)

        if formato == 'excel':
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            filename = f'lista_alumnos_{seccion.codigo}.xlsx'
        else:  # pdf
            content_type = 'application/pdf'
            filename = f'lista_alumnos_{seccion.codigo}.pdf'

        return ResponseAdapter.from_buffer(buffer, content_type, filename)

    except Exception as e:
        messages.error(request, f'Error al generar reporte: {str(e)}')
        return redirect('profesor_seccion_detalle', seccion_id=seccion_id)


@profesor_required
def profesor_exportar_notas(request, seccion_id, formato='excel'):
    """Exportar notas en Excel o PDF"""
    seccion = get_object_or_404(Seccion, pk=seccion_id, profesores=request.user)

    try:
        buffer = ReporteService.generar_reporte_notas(seccion_id, formato)

        if formato == 'excel':
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            filename = f'notas_{seccion.codigo}.xlsx'
        else:  # pdf
            content_type = 'application/pdf'
            filename = f'notas_{seccion.codigo}.pdf'

        return ResponseAdapter.from_buffer(buffer, content_type, filename)

    except Exception as e:
        messages.error(request, f'Error al generar reporte: {str(e)}')
        return redirect('profesor_seccion_detalle', seccion_id=seccion_id)


# ==============================================================================
# API ENDPOINTS PARA GRÁFICOS (JSON)
# ==============================================================================

@profesor_required
def api_estadisticas_seccion(request, seccion_id):
    """API para obtener estadísticas de una sección (para gráficos)"""
    seccion = get_object_or_404(Seccion, pk=seccion_id, profesores=request.user)

    # Obtener datos para gráficos
    estadisticas = NotaService.obtener_estadisticas_seccion(seccion_id)
    top_alumnos = NotaService.obtener_top_alumnos(seccion_id, limite=5, orden='desc')
    peores_alumnos = NotaService.obtener_top_alumnos(seccion_id, limite=5, orden='asc')
    progreso = NotaService.obtener_progreso_evaluaciones(seccion_id)

    data = {
        'estadisticas': estadisticas,
        'top_alumnos': [
            {'nombre': alumno.get_full_name(), 'promedio': promedio}
            for alumno, promedio in top_alumnos
        ],
        'peores_alumnos': [
            {'nombre': alumno.get_full_name(), 'promedio': promedio}
            for alumno, promedio in peores_alumnos
        ],
        'progreso_evaluaciones': [
            {'componente': nombre, 'promedio': promedio}
            for nombre, promedio in progreso
        ],
    }

    return JsonResponse(data)
