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

        # ============================================
        # ADMIN
        # ============================================
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

        # ============================================
        # PROFESORES
        # ============================================
        profesores_data = [
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
                'nombre': 'Adrian Guillermo',
                'apellido_paterno': 'Arce',
                'apellido_materno': 'Holgado',
                'tipo_documento': 'DNI',
                'numero_documento': '45967823',
                'email': 'adrian.arce@utp.edu.pe',
                'telefono': '987567890',
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
                self.stdout.write(self.style.SUCCESS(f'[OK] Profesor: {profesor.get_full_name()} ({profesor.codigo}) / Pedro1415@'))
            else:
                profesor = Usuario.objects.get(numero_documento=prof_data['numero_documento'])
                profesores.append(profesor)
                self.stdout.write(self.style.WARNING(f'Profesor {profesor.codigo} ya existe'))

        # ============================================
        # ALUMNOS
        # ============================================
        alumnos_data = [
            {'nombre': 'Kelvin Jesus', 'apellido_paterno': 'Acevedo', 'apellido_materno': 'Huarachi', 'dni': '73309801', 'anio': 1999},
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
                self.stdout.write(self.style.SUCCESS(f'[OK] Alumno: {alumno.get_full_name()} ({alumno.codigo}) / Pedro1415@'))
            else:
                alumno = Usuario.objects.get(numero_documento=dni_num)
                alumnos.append(alumno)
                self.stdout.write(self.style.WARNING(f'Alumno {alumno.codigo} ya existe'))

        # ============================================
        # CICLOS
        # ============================================

        # Ciclo 2025-1 (TERMINADO)
        if not Ciclo.objects.filter(nombre='2025-1').exists():
            ciclo_2025_1 = Ciclo.objects.create(
                nombre='2025-1',
                fecha_inicio_ciclo=date(2025, 3, 1),
                fecha_fin_ciclo=date(2025, 6, 28),
                fecha_inicio_matricula=date(2025, 2, 15),
                fecha_fin_matricula=date(2025, 3, 7),
                matricula_abierta=False,
                ciclo_terminado=True
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Ciclo: {ciclo_2025_1.nombre} (TERMINADO)'))
        else:
            ciclo_2025_1 = Ciclo.objects.get(nombre='2025-1')
            self.stdout.write(self.style.WARNING(f'Ciclo {ciclo_2025_1.nombre} ya existe'))

        # Ciclo 2025-2 (ACTIVO)
        if not Ciclo.objects.filter(nombre='2025-2').exists():
            ciclo_2025_2 = Ciclo.objects.create(
                nombre='2025-2',
                fecha_inicio_ciclo=date(2025, 8, 12),
                fecha_fin_ciclo=date(2025, 12, 20),
                fecha_inicio_matricula=date(2025, 7, 29),
                fecha_fin_matricula=date(2025, 12, 30),  # Matrícula abierta
                matricula_abierta=True,
                ciclo_terminado=False
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Ciclo: {ciclo_2025_2.nombre} (ACTIVO - Matrícula abierta)'))
        else:
            ciclo_2025_2 = Ciclo.objects.get(nombre='2025-2')
            self.stdout.write(self.style.WARNING(f'Ciclo {ciclo_2025_2.nombre} ya existe'))

        # ============================================
        # CURSOS
        # ============================================
        cursos_data = [
            {'nombre': 'Base de datos II', 'creditos': 4, 'codigo': '1SI46'},
            {'nombre': 'Programación orientada a objetos', 'creditos': 3, 'codigo': '1I55N'}
        ]

        cursos = {}
        for curso_data in cursos_data:
            if not Curso.objects.filter(codigo=curso_data['codigo']).exists():
                curso = Curso.objects.create(
                    nombre=curso_data['nombre'],
                    creditos=curso_data['creditos'],
                    descripcion=f"Curso {curso_data['codigo']}"
                )
                cursos[curso_data['codigo']] = curso
                self.stdout.write(self.style.SUCCESS(f'[OK] Curso: {curso.nombre}'))
            else:
                curso = Curso.objects.get(codigo=curso_data['codigo'])
                cursos[curso_data['codigo']] = curso
                self.stdout.write(self.style.WARNING(f'Curso {curso.nombre} ya existe'))

        # ============================================
        # COMPONENTES DE EVALUACIÓN
        # ============================================

        # Base de datos II
        if not ComponenteEvaluacion.objects.filter(curso=cursos['1SI46']).exists():
            componentes_bd = [
                ComponenteEvaluacion(curso=cursos['1SI46'], nombre='Práctica calificada 1 (PC1)', porcentaje=Decimal('15.00'), orden=1),
                ComponenteEvaluacion(curso=cursos['1SI46'], nombre='Práctica calificada 2 (PC2)', porcentaje=Decimal('20.00'), orden=2),
                ComponenteEvaluacion(curso=cursos['1SI46'], nombre='Práctica calificada 3 (PC3)', porcentaje=Decimal('18.00'), orden=3),
                ComponenteEvaluacion(curso=cursos['1SI46'], nombre='Participación en clase (PA)', porcentaje=Decimal('20.00'), orden=4),
                ComponenteEvaluacion(curso=cursos['1SI46'], nombre='Examen final (EXFN)', porcentaje=Decimal('19.00'), orden=5),
            ]
            ComponenteEvaluacion.objects.bulk_create(componentes_bd)
            self.stdout.write(self.style.SUCCESS(f'[OK] Componentes para Base de datos II'))
        else:
            self.stdout.write(self.style.WARNING('Componentes de Base de datos II ya existen'))

        # Programación orientada a objetos
        if not ComponenteEvaluacion.objects.filter(curso=cursos['1I55N']).exists():
            componentes_poo = [
                ComponenteEvaluacion(curso=cursos['1I55N'], nombre='Práctica calificada 1 (PC1)', porcentaje=Decimal('19.00'), orden=1),
                ComponenteEvaluacion(curso=cursos['1I55N'], nombre='Práctica calificada 2 (PC2)', porcentaje=Decimal('20.00'), orden=2),
                ComponenteEvaluacion(curso=cursos['1I55N'], nombre='Práctica calificada 3 (PC3)', porcentaje=Decimal('20.00'), orden=3),
                ComponenteEvaluacion(curso=cursos['1I55N'], nombre='Proyecto final (PROY)', porcentaje=Decimal('20.00'), orden=4),
            ]
            ComponenteEvaluacion.objects.bulk_create(componentes_poo)
            self.stdout.write(self.style.SUCCESS(f'[OK] Componentes para Programación orientada a objetos'))
        else:
            self.stdout.write(self.style.WARNING('Componentes de Programación orientada a objetos ya existen'))

        # ============================================
        # SECCIONES
        # ============================================

        # profesores[0] = Miguel Angel Farfan
        # profesores[1] = Ecmias Fernandez
        # profesores[2] = Adrian Arce Holgado

        # CICLO 2025-1 (TERMINADO)
        # Base de datos II - Arce Holgado
        if not Seccion.objects.filter(codigo='44334', curso=cursos['1SI46'], ciclo=ciclo_2025_1).exists():
            seccion_bd_2025_1 = Seccion.objects.create(
                codigo='44334',
                curso=cursos['1SI46'],
                ciclo=ciclo_2025_1,
                modalidad='presencial',
                turno='noche',
                dias_semana='Miércoles 18:30-20:00, Jueves 18:30-20:00',
                hora_inicio=time(18, 30),
                hora_fin=time(20, 0),
                vacantes_totales=30,
                vacantes_ocupadas=0
            )
            seccion_bd_2025_1.profesores.add(profesores[2])  # Arce Holgado
            self.stdout.write(self.style.SUCCESS(f'[OK] Sección 2025-1: Base de datos II - {profesores[2].get_full_name()}'))
        else:
            seccion_bd_2025_1 = Seccion.objects.get(codigo='44334', curso=cursos['1SI46'], ciclo=ciclo_2025_1)
            self.stdout.write(self.style.WARNING('Sección 44334 ya existe'))

        # Programación orientada a objetos - Farfan
        if not Seccion.objects.filter(codigo='44337', curso=cursos['1I55N'], ciclo=ciclo_2025_1).exists():
            seccion_poo_2025_1 = Seccion.objects.create(
                codigo='44337',
                curso=cursos['1I55N'],
                ciclo=ciclo_2025_1,
                modalidad='presencial',
                turno='noche',
                dias_semana='Martes 18:30-20:00, Jueves 18:30-20:00',
                hora_inicio=time(18, 30),
                hora_fin=time(20, 0),
                vacantes_totales=30,
                vacantes_ocupadas=0
            )
            seccion_poo_2025_1.profesores.add(profesores[0])  # Farfan
            self.stdout.write(self.style.SUCCESS(f'[OK] Sección 2025-1: Programación orientada a objetos - {profesores[0].get_full_name()}'))
        else:
            seccion_poo_2025_1 = Seccion.objects.get(codigo='44337', curso=cursos['1I55N'], ciclo=ciclo_2025_1)
            self.stdout.write(self.style.WARNING('Sección 44337 ya existe'))

        # CICLO 2025-2 (ACTIVO)
        # Base de datos II - Ecmias
        if not Seccion.objects.filter(codigo='16307', curso=cursos['1SI46'], ciclo=ciclo_2025_2).exists():
            seccion_bd_2025_2 = Seccion.objects.create(
                codigo='16307',
                curso=cursos['1SI46'],
                ciclo=ciclo_2025_2,
                modalidad='presencial',
                turno='noche',
                dias_semana='Miércoles 18:30-20:00, Jueves 18:30-20:00',
                hora_inicio=time(18, 30),
                hora_fin=time(20, 0),
                vacantes_totales=30,
                vacantes_ocupadas=0
            )
            seccion_bd_2025_2.profesores.add(profesores[1])  # Ecmias
            self.stdout.write(self.style.SUCCESS(f'[OK] Sección 2025-2: Base de datos II - {profesores[1].get_full_name()} (DISPONIBLE PARA MATRÍCULA)'))
        else:
            seccion_bd_2025_2 = Seccion.objects.get(codigo='16307', curso=cursos['1SI46'], ciclo=ciclo_2025_2)
            self.stdout.write(self.style.WARNING('Sección 16307 ya existe'))

        # ============================================
        # MATRÍCULAS Y NOTAS - CICLO 2025-1
        # ============================================

        kelvin = alumnos[0]

        # Matricular Kelvin en Base de datos II (2025-1)
        if not Matricula.objects.filter(alumno=kelvin, seccion=seccion_bd_2025_1).exists():
            try:
                matricula_bd = MatriculaService.matricular_alumno(kelvin.id, seccion_bd_2025_1.id)
                self.stdout.write(self.style.SUCCESS(f'[OK] {kelvin.get_full_name()} matriculado en Base de datos II (2025-1)'))

                # Registrar notas DESAPROBADAS
                componentes_bd = ComponenteEvaluacion.objects.filter(curso=cursos['1SI46']).order_by('orden')
                notas_desaprobadas = [
                    Decimal('7.50'),   # PC1 (15%)
                    Decimal('8.00'),   # PC2 (20%)
                    Decimal('9.50'),   # PC3 (18%)
                    Decimal('10.00'),  # PA (20%)
                    Decimal('6.50'),   # EXFN (19%)
                ]

                for comp, nota_valor in zip(componentes_bd, notas_desaprobadas):
                    NotaService.registrar_nota(matricula_bd.id, comp.id, nota_valor)

                self.stdout.write(self.style.SUCCESS(f'[OK] Notas DESAPROBADAS registradas para {kelvin.get_full_name()} en Base de datos II'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

        # Matricular Kelvin en Programación orientada a objetos (2025-1)
        if not Matricula.objects.filter(alumno=kelvin, seccion=seccion_poo_2025_1).exists():
            try:
                matricula_poo = MatriculaService.matricular_alumno(kelvin.id, seccion_poo_2025_1.id)
                self.stdout.write(self.style.SUCCESS(f'[OK] {kelvin.get_full_name()} matriculado en Programación orientada a objetos (2025-1)'))

                # Registrar notas variadas
                componentes_poo = ComponenteEvaluacion.objects.filter(curso=cursos['1I55N']).order_by('orden')
                notas_variadas = [
                    Decimal('19.00'),  # PC1 (19%)
                    Decimal('20.00'),  # PC2 (20%)
                    Decimal('20.00'),  # PC3 (20%)
                    Decimal('14.00'),  # PROY (20%) - pendiente
                ]

                for comp, nota_valor in zip(componentes_poo, notas_variadas):
                    NotaService.registrar_nota(matricula_poo.id, comp.id, nota_valor)

                self.stdout.write(self.style.SUCCESS(f'[OK] Notas variadas registradas para {kelvin.get_full_name()} en Programación orientada a objetos'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

        # ============================================
        # RESUMEN FINAL
        # ============================================
        self.stdout.write(self.style.SUCCESS('\n========================================'))
        self.stdout.write(self.style.SUCCESS('Datos creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(self.style.SUCCESS('\nCredenciales (Usuario/Password):'))
        self.stdout.write(self.style.SUCCESS(f'  Admin: 75911772 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Profesor Farfan: 44856901 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Profesor Ecmias: 43745890 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Profesor Arce: 45967823 / Pedro1415@'))
        self.stdout.write(self.style.SUCCESS(f'  Alumno Kelvin: 73309801 / Pedro1415@'))

        self.stdout.write(self.style.SUCCESS('\nCICLO 2025-1 (TERMINADO - Solo lectura):'))
        self.stdout.write(self.style.SUCCESS('  - Base de datos II (Arce Holgado) - Kelvin DESAPROBADO'))
        self.stdout.write(self.style.SUCCESS('  - Programación orientada a objetos (Farfan) - Kelvin con notas'))

        self.stdout.write(self.style.SUCCESS('\nCICLO 2025-2 (ACTIVO - Matrícula abierta):'))
        self.stdout.write(self.style.SUCCESS('  - Base de datos II (Ecmias) - Sin matrículas'))

        self.stdout.write(self.style.SUCCESS('\nAccede a: http://localhost:8000'))
