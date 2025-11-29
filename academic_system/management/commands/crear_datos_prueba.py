from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academic_system.models import Curso, Ciclo, Seccion, ComponenteEvaluacion, Matricula, Nota
from academic_system.services import UsuarioService, MatriculaService, NotaService
from datetime import date, timedelta, time
from decimal import Decimal
import random

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema de matrículas y notas'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creando datos de prueba...'))

        if not Usuario.objects.filter(numero_documento='75911772').exists():
            admin = Usuario.objects.create_superuser(
                username='75911772',
                password='Pedro1415@',
                codigo='U75911772',
                first_name='Ricardo Enrique',
                apellido_paterno='Prada',
                apellido_materno='Guerra',
                rol='administrador',
                tipo_documento='DNI',
                numero_documento='75911772',
                email='enrique.pdg@gmail.com',
                telefono='912016161',
                fecha_nacimiento=date(1999, 5, 29),
                sexo='M'
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Admin creado: {admin.codigo} / Pedro1415@'))
        else:
            admin = Usuario.objects.get(numero_documento='75911772')
            self.stdout.write(self.style.WARNING('Admin ya existe'))

        profesores_data = [
            {
                'nombre': 'Nahui',
                'apellido_paterno': 'Xesppe',
                'apellido_materno': 'Clive',
                'tipo_documento': 'DNI',
                'numero_documento': '41523678',
                'email': 'nahui.xesppe@utp.edu.pe',
                'telefono': '987123456',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Pedro1415@'
            },
            {
                'nombre': 'Rayme',
                'apellido_paterno': 'Serrano',
                'apellido_materno': 'Ruben Alejandro',
                'tipo_documento': 'DNI',
                'numero_documento': '42634789',
                'email': 'rayme.serrano@utp.edu.pe',
                'telefono': '987234567',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Pedro1415@'
            },
            {
                'nombre': 'Ecmias Eduardo',
                'apellido_paterno': 'Fernandez',
                'apellido_materno': 'Galvez',
                'tipo_documento': 'DNI',
                'numero_documento': '43745890',
                'email': 'ecmias.fernandez@utp.edu.pe',
                'telefono': '987345678',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Pedro1415@'
            },
            {
                'nombre': 'Miguel Angel',
                'apellido_paterno': 'Farfan',
                'apellido_materno': 'Leyva',
                'tipo_documento': 'DNI',
                'numero_documento': '44856901',
                'email': 'miguel.farfan@utp.edu.pe',
                'telefono': '987456789',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Pedro1415@'
            }
        ]

        profesores = []
        for prof_data in profesores_data:
            if not Usuario.objects.filter(numero_documento=prof_data['numero_documento']).exists():
                profesor = UsuarioService.crear_usuario(prof_data)
                profesores.append(profesor)
                self.stdout.write(self.style.SUCCESS(f'[OK] Profesor: {profesor.codigo} / Pedro1415@'))
            else:
                profesor = Usuario.objects.get(numero_documento=prof_data['numero_documento'])
                profesores.append(profesor)
                self.stdout.write(self.style.WARNING(f'Profesor {profesor.codigo} ya existe'))

        alumnos_data = [
            {'nombre': 'Juan Jose', 'apellido_paterno': 'Morales', 'apellido_materno': 'Velasquez', 'dni': '72365087', 'anio': 1998},
            {'nombre': 'Kelvin Jesus', 'apellido_paterno': 'Acevedo', 'apellido_materno': 'Huarachi', 'dni': '73309801', 'anio': 1999},
            {'nombre': 'Angel', 'apellido_paterno': 'Campusano', 'apellido_materno': 'Solis', 'dni': '74317595', 'anio': 1997},
            {'nombre': 'Joel Anthony', 'apellido_paterno': 'Saldaña', 'apellido_materno': 'Chavez', 'dni': '75650077', 'anio': 2000}
        ]

        alumnos = []
        for i, alumno_data in enumerate(alumnos_data):
            dni_num = alumno_data['dni']
            if not Usuario.objects.filter(numero_documento=dni_num).exists():
                mes = random.randint(1, 12)
                dia = random.randint(1, 28)
                data = {
                    'nombre': alumno_data['nombre'],
                    'apellido_paterno': alumno_data['apellido_paterno'],
                    'apellido_materno': alumno_data['apellido_materno'],
                    'tipo_documento': 'DNI',
                    'numero_documento': dni_num,
                    'email': f"{alumno_data['nombre'].lower().replace(' ', '.')}.{alumno_data['apellido_paterno'].lower()}@utp.edu.pe",
                    'telefono': f'9{random.randint(10000000, 99999999)}',
                    'sexo': 'M',
                    'rol': 'alumno',
                    'fecha_nacimiento': date(alumno_data['anio'], mes, dia),
                    'password': 'Pedro1415@'
                }
                alumno = UsuarioService.crear_usuario(data)
                alumnos.append(alumno)
                self.stdout.write(self.style.SUCCESS(f'[OK] Alumno: {alumno.codigo} / Pedro1415@'))
            else:
                alumno = Usuario.objects.get(numero_documento=dni_num)
                alumnos.append(alumno)
                self.stdout.write(self.style.WARNING(f'Alumno {alumno.codigo} ya existe'))

        if not Ciclo.objects.filter(nombre='2025-2').exists():
            ciclo = Ciclo.objects.create(
                nombre='2025-2',
                fecha_inicio_ciclo=date(2025, 8, 12),
                fecha_fin_ciclo=date(2025, 12, 20),
                fecha_inicio_matricula=date(2025, 8, 1),
                fecha_fin_matricula=date(2025, 11, 30),
                matricula_abierta=True
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Ciclo: {ciclo.nombre}'))
        else:
            ciclo = Ciclo.objects.get(nombre='2025-2')
            self.stdout.write(self.style.WARNING(f'Ciclo {ciclo.nombre} ya existe'))

        cursos_data = [
            {'nombre': 'Redes y comunicación de datos I', 'creditos': 4, 'codigo': '1I41N'},
            {'nombre': 'Algoritmos y estructuras de datos', 'creditos': 3, 'codigo': '1I53N'},
            {'nombre': 'Taller de programación web', 'creditos': 2, 'codigo': '1SI45'},
            {'nombre': 'Base de datos II', 'creditos': 4, 'codigo': '1SI46'},
            {'nombre': 'Diseño de patrones', 'creditos': 2, 'codigo': '1SI47'},
            {'nombre': 'Negociación y narrativa', 'creditos': 2, 'codigo': '1S76T'},
            {'nombre': 'Sistemas operativos', 'creditos': 3, 'codigo': '1TV74'}
        ]

        cursos = []
        for curso_data in cursos_data:
            if not Curso.objects.filter(nombre=curso_data['nombre']).exists():
                curso = Curso.objects.create(
                    nombre=curso_data['nombre'],
                    creditos=curso_data['creditos'],
                    descripcion=f"Curso {curso_data['codigo']}"
                )
                cursos.append(curso)
                self.stdout.write(self.style.SUCCESS(f'[OK] Curso: {curso.nombre}'))
            else:
                curso = Curso.objects.get(nombre=curso_data['nombre'])
                cursos.append(curso)
                self.stdout.write(self.style.WARNING(f'Curso {curso.nombre} ya existe'))

        componentes_por_curso = [
            # Redes y comunicación de datos I
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Participacion en clase (PA)', Decimal('10.00')),
                ('Examen final (EXFN)', Decimal('30.00'))
            ],
            # Algoritmos y estructuras de datos
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Trabajo final (TF)', Decimal('40.00'))
            ],
            # Taller de programación web
            [
                ('Avance de proyecto final 1 (APF1)', Decimal('20.00')),
                ('Avance de proyecto final 2 (APF2)', Decimal('20.00')),
                ('Avance de proyecto final 3 (APF3)', Decimal('20.00')),
                ('Proyecto final (PROY)', Decimal('40.00'))
            ],
            # Base de datos II
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Trabajo final (TF)', Decimal('40.00'))
            ],
            # Diseño de patrones
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Participacion en clase (PA)', Decimal('10.00')),
                ('Examen final (EXFN)', Decimal('30.00'))
            ],
            # Negociación y narrativa
            [
                ('Tarea academica 1 (TA1)', Decimal('30.00')),
                ('Tarea academica 2 (TA2)', Decimal('30.00')),
                ('Examen final (EXFN)', Decimal('40.00'))
            ],
            # Sistemas operativos
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Participacion en clase (PA)', Decimal('10.00')),
                ('Examen final (EXFN)', Decimal('30.00'))
            ]
        ]

        for i, curso in enumerate(cursos):
            if not ComponenteEvaluacion.objects.filter(curso=curso).exists():
                componentes = []
                for orden, (nombre, porcentaje) in enumerate(componentes_por_curso[i], 1):
                    componentes.append(ComponenteEvaluacion(
                        curso=curso,
                        nombre=nombre,
                        porcentaje=porcentaje,
                        orden=orden
                    ))
                ComponenteEvaluacion.objects.bulk_create(componentes)
                self.stdout.write(self.style.SUCCESS(f'[OK] Componentes para {curso.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'Componentes de {curso.nombre} ya existen'))

        # Configuración de secciones:
        # profesores[0] = Nahui Xesppe
        # profesores[1] = Rayme Serrano
        # profesores[2] = Ecmias Fernandez
        # profesores[3] = Miguel Angel Farfan

        secciones_config = [
            # Diseño de patrones - 3 secciones (curso_idx = 4)
            {'curso_idx': 4, 'codigo': '16309', 'profesor_idx': 3, 'dias': 'Sábado 15:45-18:00', 'hora_inicio': time(15, 45), 'hora_fin': time(18, 0), 'modalidad': 'presencial', 'turno': 'tarde'},
            {'curso_idx': 4, 'codigo': '16310', 'profesor_idx': 1, 'dias': 'Martes 18:30-20:00', 'hora_inicio': time(18, 30), 'hora_fin': time(20, 0), 'modalidad': 'presencial', 'turno': 'noche'},
            {'curso_idx': 4, 'codigo': '16311', 'profesor_idx': 2, 'dias': 'Jueves 20:15-21:45', 'hora_inicio': time(20, 15), 'hora_fin': time(21, 45), 'modalidad': 'presencial', 'turno': 'noche'},

            # Taller de programación web - 1 sección (curso_idx = 2)
            {'curso_idx': 2, 'codigo': '28531', 'profesor_idx': 3, 'dias': 'Jueves 11:00-13:15', 'hora_inicio': time(11, 0), 'hora_fin': time(13, 15), 'modalidad': 'presencial', 'turno': 'mañana'},

            # Algoritmos y estructuras de datos - 2 secciones (curso_idx = 1)
            {'curso_idx': 1, 'codigo': '16305', 'profesor_idx': 3, 'dias': 'Lunes 08:00-10:15', 'hora_inicio': time(8, 0), 'hora_fin': time(10, 15), 'modalidad': 'presencial', 'turno': 'mañana'},
            {'curso_idx': 1, 'codigo': '16306', 'profesor_idx': 2, 'dias': 'Miércoles 18:30-20:45', 'hora_inicio': time(18, 30), 'hora_fin': time(20, 45), 'modalidad': 'presencial', 'turno': 'noche'},

            # Redes y comunicación de datos I - 1 sección (curso_idx = 0)
            {'curso_idx': 0, 'codigo': '11366', 'profesor_idx': 0, 'dias': 'Lunes 20:15-21:45, Miércoles 20:15-21:45', 'hora_inicio': time(20, 15), 'hora_fin': time(21, 45), 'modalidad': 'presencial', 'turno': 'noche'}
        ]

        secciones = []
        for seccion_data in secciones_config:
            curso = cursos[seccion_data['curso_idx']]
            codigo = seccion_data['codigo']

            if not Seccion.objects.filter(codigo=codigo, curso=curso, ciclo=ciclo).exists():
                seccion = Seccion.objects.create(
                    codigo=codigo,
                    curso=curso,
                    ciclo=ciclo,
                    modalidad=seccion_data['modalidad'],
                    turno=seccion_data['turno'],
                    dias_semana=seccion_data['dias'],
                    hora_inicio=seccion_data['hora_inicio'],
                    hora_fin=seccion_data['hora_fin'],
                    vacantes_totales=30,
                    vacantes_ocupadas=0
                )

                profesor = profesores[seccion_data['profesor_idx']]
                seccion.profesores.add(profesor)
                secciones.append(seccion)

                self.stdout.write(self.style.SUCCESS(f'[OK] Sección: {seccion.codigo} - {curso.nombre} (Prof: {profesor.get_full_name()})'))
            else:
                seccion = Seccion.objects.get(codigo=codigo, curso=curso, ciclo=ciclo)
                secciones.append(seccion)
                self.stdout.write(self.style.WARNING(f'Sección {seccion.codigo} ya existe'))

        # Matricular alumnos excepto Juan (índice 0) y Kelvin (índice 1)
        # Angel: índice 2, Joel: índice 3

        # Matrícula de Angel - una sección por curso
        matriculas_angel = [
            {'curso_idx': 4, 'seccion_codigo': '16309'},  # Diseño patrones con Farfan (sábado)
            {'curso_idx': 2, 'seccion_codigo': '28531'},  # Taller web con Farfan
            {'curso_idx': 1, 'seccion_codigo': '16305'},  # Algoritmos con Farfan (lunes)
            {'curso_idx': 0, 'seccion_codigo': '11366'}   # Redes con Nahui
        ]

        # Matrícula de Joel - una sección por curso (diferentes a Angel donde haya opciones)
        matriculas_joel = [
            {'curso_idx': 4, 'seccion_codigo': '16310'},  # Diseño patrones con Rayme (martes)
            {'curso_idx': 2, 'seccion_codigo': '28531'},  # Taller web con Farfan
            {'curso_idx': 1, 'seccion_codigo': '16306'},  # Algoritmos con Ecmias (miércoles)
            {'curso_idx': 0, 'seccion_codigo': '11366'}   # Redes con Nahui
        ]

        # Matricular Angel
        for matricula_data in matriculas_angel:
            curso = cursos[matricula_data['curso_idx']]
            seccion = Seccion.objects.get(codigo=matricula_data['seccion_codigo'], curso=curso, ciclo=ciclo)
            if not Matricula.objects.filter(alumno=alumnos[2], seccion=seccion).exists():
                try:
                    MatriculaService.matricular_alumno(alumnos[2].id, seccion.id)
                    self.stdout.write(self.style.SUCCESS(f'[OK] {alumnos[2].get_full_name()} matriculado en {seccion.curso.nombre} - {seccion.codigo}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

        # Matricular Joel
        for matricula_data in matriculas_joel:
            curso = cursos[matricula_data['curso_idx']]
            seccion = Seccion.objects.get(codigo=matricula_data['seccion_codigo'], curso=curso, ciclo=ciclo)
            if not Matricula.objects.filter(alumno=alumnos[3], seccion=seccion).exists():
                try:
                    MatriculaService.matricular_alumno(alumnos[3].id, seccion.id)
                    self.stdout.write(self.style.SUCCESS(f'[OK] {alumnos[3].get_full_name()} matriculado en {seccion.curso.nombre} - {seccion.codigo}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n[INFO] Juan y Kelvin NO fueron matriculados (para demostración de flujo de matrícula)'))

        self.stdout.write(self.style.SUCCESS('\n========================================'))
        self.stdout.write(self.style.SUCCESS('✓ Datos creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(self.style.SUCCESS('\nCredenciales (Usuario/Password):'))
        self.stdout.write(self.style.SUCCESS(f'  Admin: 75911772 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Profesor Nahui: 41523678 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Profesor Farfan: 44856901 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Alumno Juan (sin matrícula): 72365087 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Alumno Angel (matriculado): 74317595 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS('\nCursos con secciones disponibles:'))
        self.stdout.write(self.style.SUCCESS('  - Diseño de patrones (3 secciones)'))
        self.stdout.write(self.style.SUCCESS('  - Taller de programación web (1 sección)'))
        self.stdout.write(self.style.SUCCESS('  - Algoritmos y estructuras de datos (2 secciones)'))
        self.stdout.write(self.style.SUCCESS('  - Redes y comunicación de datos I (1 sección)'))
        self.stdout.write(self.style.SUCCESS('\nCursos sin secciones (en sistema pero no matriculables):'))
        self.stdout.write(self.style.SUCCESS('  - Base de datos II'))
        self.stdout.write(self.style.SUCCESS('  - Negociación y narrativa'))
        self.stdout.write(self.style.SUCCESS('  - Sistemas operativos'))
        self.stdout.write(self.style.SUCCESS('\nAccede a: http://localhost:8000'))
