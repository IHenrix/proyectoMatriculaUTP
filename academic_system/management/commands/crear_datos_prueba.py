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
                'nombre': 'Hernan Francisco',
                'apellido_paterno': 'Peña',
                'apellido_materno': 'Carnero',
                'tipo_documento': 'DNI',
                'numero_documento': '43745890',
                'email': 'hernan.pena@utp.edu.pe',
                'telefono': '987345678',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Pedro1415@'
            },
            {
                'nombre': 'Ecmias Eduardo',
                'apellido_paterno': 'Fernandez',
                'apellido_materno': 'Galvez',
                'tipo_documento': 'DNI',
                'numero_documento': '44856901',
                'email': 'ecmias.fernandez@utp.edu.pe',
                'telefono': '987456789',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Pedro1415@'
            },
            {
                'nombre': 'Miguel Angel',
                'apellido_paterno': 'Farfan',
                'apellido_materno': 'Leyva',
                'tipo_documento': 'DNI',
                'numero_documento': '45967012',
                'email': 'miguel.farfan@utp.edu.pe',
                'telefono': '987567890',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Pedro1415@'
            },
            {
                'nombre': 'Jose Carlos',
                'apellido_paterno': 'Gallardo',
                'apellido_materno': 'Montero',
                'tipo_documento': 'DNI',
                'numero_documento': '46078123',
                'email': 'jose.gallardo@utp.edu.pe',
                'telefono': '987678901',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Pedro1415@'
            },
            {
                'nombre': 'Oscar Efrain',
                'apellido_paterno': 'Capuñay',
                'apellido_materno': 'Uceda',
                'tipo_documento': 'DNI',
                'numero_documento': '47189234',
                'email': 'oscar.capunay@utp.edu.pe',
                'telefono': '987789012',
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
            {'nombre': 'Juan Jose', 'apellido_paterno': 'Morales', 'apellido_materno': 'Velasquez', 'dni': 'U236265087', 'anio': 1998},
            {'nombre': 'Kelvin Jesus', 'apellido_paterno': 'Acevedo', 'apellido_materno': 'Huarachi', 'dni': 'U2330980', 'anio': 1999},
            {'nombre': 'Angel', 'apellido_paterno': 'Campusano', 'apellido_materno': 'Solis', 'dni': 'U23317595', 'anio': 1997},
            {'nombre': 'Joel Anthony', 'apellido_paterno': 'Saldaña', 'apellido_materno': 'Chavez', 'dni': 'U232650077', 'anio': 2000}
        ]

        alumnos = []
        for i, alumno_data in enumerate(alumnos_data):
            dni_num = alumno_data['dni'].replace('U', '')
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

        today = date.today()
        if not Ciclo.objects.filter(nombre='2025-1').exists():
            ciclo = Ciclo.objects.create(
                nombre='2025-1',
                fecha_inicio_matricula=today - timedelta(days=15),
                fecha_fin_matricula=today + timedelta(days=30),
                matricula_abierta=True
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Ciclo: {ciclo.nombre}'))
        else:
            ciclo = Ciclo.objects.get(nombre='2025-1')
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
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Participacion en clase (PA)', Decimal('10.00')),
                ('Examen final (EXFN)', Decimal('30.00'))
            ],
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Proyecto final (PROY)', Decimal('40.00'))
            ],
            [
                ('Avance de proyecto final 1 (APF1)', Decimal('20.00')),
                ('Avance de proyecto final 2 (APF2)', Decimal('20.00')),
                ('Avance de proyecto final 3 (APF3)', Decimal('20.00')),
                ('Proyecto final (PROY)', Decimal('40.00'))
            ],
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Trabajo final (TF)', Decimal('40.00'))
            ],
            [
                ('Practica calificada 1 (PC1)', Decimal('20.00')),
                ('Practica calificada 2 (PC2)', Decimal('20.00')),
                ('Practica calificada 3 (PC3)', Decimal('20.00')),
                ('Proyecto final (PROY)', Decimal('40.00'))
            ],
            [
                ('Tarea academica 1 (TA1)', Decimal('30.00')),
                ('Tarea academica 2 (TA2)', Decimal('30.00')),
                ('Examen final (EXFN)', Decimal('40.00'))
            ],
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

        modalidades = ['presencial', 'virtual', 'remoto']
        turnos = ['mañana', 'tarde', 'noche']

        secciones_info = [
            ('Lunes 20:15-21:45, Miércoles 20:15-21:45', time(20, 15), time(21, 45)),
            ('Martes 20:15-21:45, Jueves 20:15-21:45', time(20, 15), time(21, 45)),
            ('Jueves 11:00-13:15', time(11, 0), time(13, 15)),
            ('Miércoles 18:30-20:00, Jueves 18:30-20:00', time(18, 30), time(20, 0)),
            ('Sábado 15:45-18:00', time(15, 45), time(18, 0)),
            ('Viernes 20:15-21:45', time(20, 15), time(21, 45)),
            ('Disponible 24/7', time(0, 0), time(23, 59))
        ]

        secciones = []
        for i, curso in enumerate(cursos):
            codigo_seccion = ['11366', '16305', '28531', '16307', '16309', '28977', '38377'][i]
            if not Seccion.objects.filter(codigo=codigo_seccion, curso=curso, ciclo=ciclo).exists():
                dias, hora_inicio, hora_fin = secciones_info[i]
                modalidad = 'virtual' if i == 6 else 'presencial'
                turno = 'noche' if i in [0, 1, 5] else 'tarde' if i in [2, 3] else 'mañana'

                seccion = Seccion.objects.create(
                    codigo=codigo_seccion,
                    curso=curso,
                    ciclo=ciclo,
                    modalidad=modalidad,
                    turno=turno,
                    dias_semana=dias,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    vacantes_totales=30,
                    vacantes_ocupadas=0
                )
                seccion.profesores.add(profesores[i])
                secciones.append(seccion)
                self.stdout.write(self.style.SUCCESS(f'[OK] Sección: {seccion.codigo} - {curso.nombre}'))
            else:
                seccion = Seccion.objects.get(codigo=codigo_seccion, curso=curso, ciclo=ciclo)
                secciones.append(seccion)
                self.stdout.write(self.style.WARNING(f'Sección {seccion.codigo} ya existe'))

        for seccion in secciones:
            for alumno in alumnos:
                if not Matricula.objects.filter(alumno=alumno, seccion=seccion).exists():
                    try:
                        MatriculaService.matricular_alumno(alumno.id, seccion.id)
                        self.stdout.write(self.style.SUCCESS(f'[OK] {alumno.get_full_name()} en {seccion.curso.nombre}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('\nRegistrando notas...'))
        for matricula in Matricula.objects.all():
            componentes = ComponenteEvaluacion.objects.filter(curso=matricula.seccion.curso)
            for componente in componentes:
                if not Nota.objects.filter(matricula=matricula, componente=componente).exists():
                    if random.random() > 0.3:
                        nota_valor = Decimal(str(round(random.uniform(12, 20), 2)))
                        NotaService.registrar_nota(matricula.id, componente.id, nota_valor)

        self.stdout.write(self.style.SUCCESS('\n[OK] Datos creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS('\nCredenciales (Usuario/Password):'))
        self.stdout.write(self.style.SUCCESS(f'  Admin: 75911772 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Profesor: 41523678 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Alumno: 236265087 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS('\nAccede a http://localhost:8000'))
