from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academic_system.models import Curso, Ciclo, Seccion, ComponenteEvaluacion, Matricula, Nota
from academic_system.services import UsuarioService, CuotaService
from datetime import date, time
from decimal import Decimal
import random

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema de matrículas y notas SENATI'

    def _crear_matricula_directa(self, alumno, seccion):
        """Crea matrícula directamente (para ciclos cerrados/terminados)."""
        matricula, created = Matricula.objects.get_or_create(
            alumno=alumno,
            seccion=seccion,
            defaults={'is_active': True}
        )
        return matricula, created

    def _registrar_notas(self, matricula, notas_valores):
        """Crea o actualiza notas de una matrícula."""
        componentes = ComponenteEvaluacion.objects.filter(
            curso=matricula.seccion.curso
        ).order_by('orden')

        for i, componente in enumerate(componentes):
            if i < len(notas_valores):
                Nota.objects.update_or_create(
                    matricula=matricula,
                    componente=componente,
                    defaults={'valor': Decimal(str(notas_valores[i]))}
                )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creando datos de prueba SENATI...'))

        # ========================================
        # ADMINISTRADOR
        # ========================================
        if not Usuario.objects.filter(numero_documento='75933651').exists():
            admin = Usuario.objects.create_superuser(
                username='75933651',
                password='Marco1415@',
                codigo='U75933651',
                first_name='Edson Aldahir',
                apellido_paterno='Asencio',
                apellido_materno='Arcos',
                rol='administrador',
                tipo_documento='DNI',
                numero_documento='75933651',
                email='edson.ascencio@senati.edu.pe',
                telefono='912000001',
                fecha_nacimiento=date(2000, 1, 1),
                sexo='M'
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Admin: {admin.codigo} / Marco1415@'))
        else:
            admin = Usuario.objects.get(numero_documento='75933651')
            self.stdout.write(self.style.WARNING('Admin ya existe'))

        # ========================================
        # PROFESORES
        # ========================================
        profesores_data = [
            {   # índice 0
                'nombre': 'Nahui',
                'apellido_paterno': 'Xesppe',
                'apellido_materno': 'Clive',
                'tipo_documento': 'DNI',
                'numero_documento': '41523678',
                'email': 'nahui.xesppe@senati.edu.pe',
                'telefono': '987123456',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Marco1415@'
            },
            {   # índice 1
                'nombre': 'Rayme',
                'apellido_paterno': 'Serrano',
                'apellido_materno': 'Ruben Alejandro',
                'tipo_documento': 'DNI',
                'numero_documento': '42634789',
                'email': 'rayme.serrano@senati.edu.pe',
                'telefono': '987234567',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Marco1415@'
            },
            {   # índice 2
                'nombre': 'Ecmias Eduardo',
                'apellido_paterno': 'Fernandez',
                'apellido_materno': 'Galvez',
                'tipo_documento': 'DNI',
                'numero_documento': '43745890',
                'email': 'ecmias.fernandez@senati.edu.pe',
                'telefono': '987345678',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Marco1415@'
            },
            {   # índice 3
                'nombre': 'Miguel Angel',
                'apellido_paterno': 'Farfan',
                'apellido_materno': 'Leyva',
                'tipo_documento': 'DNI',
                'numero_documento': '44856901',
                'email': 'miguel.farfan@senati.edu.pe',
                'telefono': '987456789',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Marco1415@'
            },
            {   # índice 4
                'nombre': 'Arce',
                'apellido_paterno': 'Holgado',
                'apellido_materno': 'Adrian Guillermo',
                'tipo_documento': 'DNI',
                'numero_documento': '45967823',
                'email': 'arce.holgado@senati.edu.pe',
                'telefono': '987567890',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Marco1415@'
            },
            {   # índice 5 - nuevo para VERANO 2026
                'nombre': 'Luis Rolando',
                'apellido_paterno': 'Garcia',
                'apellido_materno': 'Moran',
                'tipo_documento': 'DNI',
                'numero_documento': '46078934',
                'email': 'luis.garcia@senati.edu.pe',
                'telefono': '987678901',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Marco1415@'
            },
            {   # índice 6 - Análisis y diseño (2026-1)
                'nombre': 'Oscar Enrique',
                'apellido_paterno': 'Osores',
                'apellido_materno': 'Granda',
                'tipo_documento': 'DNI',
                'numero_documento': '47189045',
                'email': 'oscar.osores@senati.edu.pe',
                'telefono': '987789012',
                'sexo': 'M',
                'rol': 'profesor',
                'password': 'Marco1415@'
            },
            {   # índice 7 - Diseño de productos y servicios (2026-1)
                'nombre': 'Jessica Katherin',
                'apellido_paterno': 'Carrasco',
                'apellido_materno': 'Zena',
                'tipo_documento': 'DNI',
                'numero_documento': '48290156',
                'email': 'jessica.carrasco@senati.edu.pe',
                'telefono': '987890123',
                'sexo': 'F',
                'rol': 'profesor',
                'password': 'Marco1415@'
            },
        ]

        profesores = []
        for prof_data in profesores_data:
            if not Usuario.objects.filter(numero_documento=prof_data['numero_documento']).exists():
                profesor = UsuarioService.crear_usuario(prof_data)
                profesores.append(profesor)
                self.stdout.write(self.style.SUCCESS(f'[OK] Profesor: {profesor.get_full_name()} / Marco1415@'))
            else:
                profesor = Usuario.objects.get(numero_documento=prof_data['numero_documento'])
                profesores.append(profesor)
                self.stdout.write(self.style.WARNING(f'Profesor {profesor.get_full_name()} ya existe'))

        # ========================================
        # ALUMNOS
        # ========================================
        alumnos_data = [
            # índice 0
            {'nombre': 'Juan Jose',    'apellido_paterno': 'Morales',   'apellido_materno': 'Velasquez', 'dni': '72365087', 'anio': 1998},
            # índice 1
            {'nombre': 'Kelvin Jesus', 'apellido_paterno': 'Acevedo',   'apellido_materno': 'Huarachi',  'dni': '76603529', 'anio': 1999},
            # índice 2
            {'nombre': 'Angel',        'apellido_paterno': 'Campusano', 'apellido_materno': 'Solis',     'dni': '74317595', 'anio': 1997},
            # índice 3
            {'nombre': 'Joel Anthony', 'apellido_paterno': 'Saldaña',   'apellido_materno': 'Chavez',    'dni': '75650077', 'anio': 2000},
        ]

        alumnos = []
        for i, alumno_data in enumerate(alumnos_data):
            dni_num = alumno_data['dni']
            if not Usuario.objects.filter(numero_documento=dni_num).exists():
                mes = random.randint(1, 12)
                dia = random.randint(1, 28)
                password = 'Marco1415@'
                data = {
                    'nombre': alumno_data['nombre'],
                    'apellido_paterno': alumno_data['apellido_paterno'],
                    'apellido_materno': alumno_data['apellido_materno'],
                    'tipo_documento': 'DNI',
                    'numero_documento': dni_num,
                    'email': f"{alumno_data['nombre'].lower().replace(' ', '.')}.{alumno_data['apellido_paterno'].lower()}@senati.edu.pe",
                    'telefono': f'9{random.randint(10000000, 99999999)}',
                    'sexo': 'M',
                    'rol': 'alumno',
                    'fecha_nacimiento': date(alumno_data['anio'], mes, dia),
                    'password': password
                }
                alumno = UsuarioService.crear_usuario(data)
                alumnos.append(alumno)
                self.stdout.write(self.style.SUCCESS(f'[OK] Alumno: {alumno.get_full_name()} / {password}'))
            else:
                alumno = Usuario.objects.get(numero_documento=dni_num)
                alumnos.append(alumno)
                self.stdout.write(self.style.WARNING(f'Alumno {alumno.get_full_name()} ya existe'))

        # Enrique como alumno de demostración para VERANO 2026
        if not Usuario.objects.filter(numero_documento='75911772').exists():
            enrique = UsuarioService.crear_usuario({
                'nombre': 'Ricardo Enrique',
                'apellido_paterno': 'Prada',
                'apellido_materno': 'Guerra',
                'tipo_documento': 'DNI',
                'numero_documento': '75911772',
                'email': 'enrique.prada@senati.edu.pe',
                'telefono': '912016161',
                'sexo': 'M',
                'rol': 'alumno',
                'fecha_nacimiento': date(1999, 5, 29),
                'password': 'Marco1415@'
            })
            self.stdout.write(self.style.SUCCESS(f'[OK] Alumno demo: {enrique.get_full_name()} / Marco1415@'))
        else:
            enrique = Usuario.objects.get(numero_documento='75911772')
            self.stdout.write(self.style.WARNING(f'Alumno demo {enrique.get_full_name()} ya existe'))

        # ========================================
        # CICLOS ACADÉMICOS
        # ========================================

        # Ciclo 2025-2 (HISTÓRICO - TERMINADO)
        if not Ciclo.objects.filter(nombre='2025-2').exists():
            ciclo_2025_2 = Ciclo.objects.create(
                nombre='2025-2',
                fecha_inicio_ciclo=date(2025, 8, 12),
                fecha_fin_ciclo=date(2025, 12, 20),
                fecha_inicio_matricula=date(2025, 8, 1),
                fecha_fin_matricula=date(2025, 11, 30),
                matricula_abierta=False,
                ciclo_terminado=True
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Ciclo histórico: {ciclo_2025_2.nombre}'))
        else:
            ciclo_2025_2 = Ciclo.objects.get(nombre='2025-2')
            self.stdout.write(self.style.WARNING(f'Ciclo {ciclo_2025_2.nombre} ya existe'))

        # Ciclo VERANO 2026 (HISTÓRICO - TERMINADO)
        if not Ciclo.objects.filter(nombre='VERANO 2026').exists():
            ciclo_verano = Ciclo.objects.create(
                nombre='VERANO 2026',
                fecha_inicio_ciclo=date(2026, 1, 16),
                fecha_fin_ciclo=date(2026, 3, 6),
                fecha_inicio_matricula=date(2026, 1, 6),
                fecha_fin_matricula=date(2026, 1, 15),
                matricula_abierta=False,
                ciclo_terminado=True
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Ciclo histórico: {ciclo_verano.nombre}'))
        else:
            ciclo_verano = Ciclo.objects.get(nombre='VERANO 2026')
            self.stdout.write(self.style.WARNING(f'Ciclo {ciclo_verano.nombre} ya existe'))

        # ========================================
        # CURSOS Y COMPONENTES DE EVALUACIÓN
        # ========================================
        cursos_data = [
            {'nombre': 'Redes y comunicación de datos I',   'creditos': 4, 'codigo': '1I41N'},  # idx 0
            {'nombre': 'Algoritmos y estructuras de datos', 'creditos': 3, 'codigo': '1I53N'},  # idx 1
            {'nombre': 'Taller de programación web',        'creditos': 2, 'codigo': '1SI45'},  # idx 2
            {'nombre': 'Base de datos II',                  'creditos': 4, 'codigo': '1SI46'},  # idx 3
            {'nombre': 'Diseño de patrones',                'creditos': 2, 'codigo': '1SI47'},  # idx 4
            {'nombre': 'Negociación y narrativa',           'creditos': 2, 'codigo': '1S76T'},  # idx 5
            {'nombre': 'Sistemas operativos',               'creditos': 3, 'codigo': '1TV74'},  # idx 6
            {'nombre': 'Programación orientada a objetos',  'creditos': 3, 'codigo': '1I55N'},  # idx 7
            {'nombre': 'Desarrollo de software',            'creditos': 3, 'codigo': '1IF70'},  # idx 8
            {'nombre': 'Teoría en computación',             'creditos': 3, 'codigo': '1S70F'},  # idx 9
            {'nombre': 'Curso integrador I: sistemas - software', 'creditos': 4, 'codigo': '1I58N'},  # idx 10
            {'nombre': 'Javascript avanzado',               'creditos': 3, 'codigo': '1SI56'},  # idx 11
            {'nombre': 'Marcos de desarrollo web',          'creditos': 3, 'codigo': '1SI57'},  # idx 12
            {'nombre': 'Hojas de estilo en cascada avanzado', 'creditos': 2, 'codigo': '1SI58'},  # idx 13
            {'nombre': 'Análisis y diseño de sistemas de información', 'creditos': 4, 'codigo': '1I60N'},  # idx 14
            {'nombre': 'Diseño de productos y servicios',             'creditos': 3, 'codigo': '1S64V'},  # idx 15
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
            # idx 0 - Redes y comunicación de datos I
            [('Practica calificada 1 (PC1)', Decimal('20.00')),
             ('Practica calificada 2 (PC2)', Decimal('20.00')),
             ('Practica calificada 3 (PC3)', Decimal('20.00')),
             ('Participacion en clase (PA)',  Decimal('10.00')),
             ('Examen final (EXFN)',          Decimal('30.00'))],
            # idx 1 - Algoritmos y estructuras de datos
            [('Practica calificada 1 (PC1)', Decimal('20.00')),
             ('Practica calificada 2 (PC2)', Decimal('20.00')),
             ('Practica calificada 3 (PC3)', Decimal('20.00')),
             ('Trabajo final (TF)',           Decimal('40.00'))],
            # idx 2 - Taller de programación web
            [('Avance de proyecto final 1 (APF1)', Decimal('20.00')),
             ('Avance de proyecto final 2 (APF2)', Decimal('20.00')),
             ('Avance de proyecto final 3 (APF3)', Decimal('20.00')),
             ('Proyecto final (PROY)',              Decimal('40.00'))],
            # idx 3 - Base de datos II
            [('Practica calificada 1 (PC1)', Decimal('20.00')),
             ('Practica calificada 2 (PC2)', Decimal('20.00')),
             ('Practica calificada 3 (PC3)', Decimal('20.00')),
             ('Trabajo final (TF)',           Decimal('40.00'))],
            # idx 4 - Diseño de patrones
            [('Practica calificada 1 (PC1)', Decimal('20.00')),
             ('Practica calificada 2 (PC2)', Decimal('20.00')),
             ('Practica calificada 3 (PC3)', Decimal('20.00')),
             ('Participacion en clase (PA)',  Decimal('10.00')),
             ('Examen final (EXFN)',          Decimal('30.00'))],
            # idx 5 - Negociación y narrativa
            [('Tarea academica 1 (TA1)', Decimal('30.00')),
             ('Tarea academica 2 (TA2)', Decimal('30.00')),
             ('Examen final (EXFN)',      Decimal('40.00'))],
            # idx 6 - Sistemas operativos
            [('Practica calificada 1 (PC1)', Decimal('20.00')),
             ('Practica calificada 2 (PC2)', Decimal('20.00')),
             ('Practica calificada 3 (PC3)', Decimal('20.00')),
             ('Participacion en clase (PA)',  Decimal('10.00')),
             ('Examen final (EXFN)',          Decimal('30.00'))],
            # idx 7 - Programación orientada a objetos
            [('Practica calificada 1 (PC1)', Decimal('20.00')),
             ('Practica calificada 2 (PC2)', Decimal('20.00')),
             ('Practica calificada 3 (PC3)', Decimal('20.00')),
             ('Proyecto final (PROY)',        Decimal('40.00'))],
            # idx 8 - Desarrollo de software
            [('Practica calificada 1 (PC1)', Decimal('25.00')),
             ('Practica calificada 2 (PC2)', Decimal('25.00')),
             ('Proyecto final (PROY)',        Decimal('50.00'))],
            # idx 9 - Teoría en computación
            [('Practica calificada 1 (PC1)', Decimal('25.00')),
             ('Practica calificada 2 (PC2)', Decimal('25.00')),
             ('Examen final (EXFN)',          Decimal('50.00'))],
            # idx 10 - Curso integrador I: sistemas - software
            [('Avance de proyecto final 1 (APF1)', Decimal('20.00')),
             ('Avance de proyecto final 2 (APF2)', Decimal('20.00')),
             ('Avance de proyecto final 3 (APF3)', Decimal('20.00')),
             ('Participacion en clase (PA)',        Decimal('10.00')),
             ('Proyecto final (PROY)',              Decimal('30.00'))],
            # idx 11 - Javascript avanzado
            [('Practica calificada 1 (PC1)', Decimal('20.00')),
             ('Practica calificada 2 (PC2)', Decimal('20.00')),
             ('Practica calificada 3 (PC3)', Decimal('20.00')),
             ('Trabajo final (TF)',           Decimal('40.00'))],
            # idx 12 - Marcos de desarrollo web
            [('Practica calificada 1 (PC1)', Decimal('20.00')),
             ('Practica calificada 2 (PC2)', Decimal('20.00')),
             ('Practica calificada 3 (PC3)', Decimal('20.00')),
             ('Participacion en clase (PA)',  Decimal('10.00')),
             ('Examen final (EXFN)',          Decimal('30.00'))],
            # idx 13 - Hojas de estilo en cascada avanzado
            [('Avance de proyecto final 1 (APF1)', Decimal('20.00')),
             ('Avance de proyecto final 2 (APF2)', Decimal('20.00')),
             ('Avance de proyecto final 3 (APF3)', Decimal('20.00')),
             ('Proyecto final (PROY)',              Decimal('40.00'))],
            # idx 14 - Análisis y diseño de sistemas de información (estructura exacta de imagen)
            [('Avance de proyecto final 1 (APF1)', Decimal('20.00')),
             ('Avance de proyecto final 2 (APF2)', Decimal('20.00')),
             ('Avance de proyecto final 3 (APF3)', Decimal('20.00')),
             ('Participacion en clase (PA)',        Decimal('10.00')),
             ('Proyecto final (PROY)',              Decimal('30.00'))],
            # idx 15 - Diseño de productos y servicios (estructura exacta de imagen)
            [('Avance de proyecto final 1 (APF1)', Decimal('20.00')),
             ('Avance de proyecto final 2 (APF2)', Decimal('20.00')),
             ('Avance de proyecto final 3 (APF3)', Decimal('20.00')),
             ('Participacion en clase (PA)',        Decimal('10.00')),
             ('Proyecto final (PROY)',              Decimal('30.00'))],
        ]

        for i, curso in enumerate(cursos):
            if not ComponenteEvaluacion.objects.filter(curso=curso).exists():
                componentes = []
                for orden, (nombre, porcentaje) in enumerate(componentes_por_curso[i], 1):
                    componentes.append(ComponenteEvaluacion(
                        curso=curso, nombre=nombre, porcentaje=porcentaje, orden=orden
                    ))
                ComponenteEvaluacion.objects.bulk_create(componentes)
                self.stdout.write(self.style.SUCCESS(f'[OK] Componentes: {curso.nombre}'))
            else:
                self.stdout.write(self.style.WARNING(f'Componentes de {curso.nombre} ya existen'))

        # ========================================
        # SECCIONES - CICLO HISTÓRICO 2025-2
        # ========================================
        # profesores[0]=Nahui, [1]=Rayme, [2]=Ecmias, [3]=Farfan, [4]=Arce, [5]=Garcia

        secciones_2025_2_config = [
            # Diseño de patrones (curso_idx=4)
            {'curso_idx': 4, 'codigo': '16309', 'prof': 3, 'dias': 'Sábado 15:45-18:00',          'h_ini': time(15,45), 'h_fin': time(18,0),  'mod': 'presencial', 'turno': 'tarde'},
            {'curso_idx': 4, 'codigo': '16310', 'prof': 1, 'dias': 'Martes 18:30-20:00',           'h_ini': time(18,30), 'h_fin': time(20,0),  'mod': 'presencial', 'turno': 'noche'},
            {'curso_idx': 4, 'codigo': '16311', 'prof': 2, 'dias': 'Jueves 20:15-21:45',           'h_ini': time(20,15), 'h_fin': time(21,45), 'mod': 'presencial', 'turno': 'noche'},
            # Taller de programación web (curso_idx=2)
            {'curso_idx': 2, 'codigo': '28531', 'prof': 3, 'dias': 'Jueves 11:00-13:15',           'h_ini': time(11,0),  'h_fin': time(13,15), 'mod': 'presencial', 'turno': 'mañana'},
            # Algoritmos y estructuras de datos (curso_idx=1)
            {'curso_idx': 1, 'codigo': '16305', 'prof': 3, 'dias': 'Lunes 08:00-10:15',            'h_ini': time(8,0),   'h_fin': time(10,15), 'mod': 'presencial', 'turno': 'mañana'},
            {'curso_idx': 1, 'codigo': '16306', 'prof': 2, 'dias': 'Miércoles 18:30-20:45',        'h_ini': time(18,30), 'h_fin': time(20,45), 'mod': 'presencial', 'turno': 'noche'},
            # Redes y comunicación (curso_idx=0)
            {'curso_idx': 0, 'codigo': '11366', 'prof': 0, 'dias': 'Lun/Mié 20:15-21:45',         'h_ini': time(20,15), 'h_fin': time(21,45), 'mod': 'presencial', 'turno': 'noche'},
            # Base de datos II (curso_idx=3)
            {'curso_idx': 3, 'codigo': '16308', 'prof': 2, 'dias': 'Mié/Jue 18:30-20:00',         'h_ini': time(18,30), 'h_fin': time(20,0),  'mod': 'presencial', 'turno': 'noche'},
        ]

        secciones_2025_2 = {}
        for cfg in secciones_2025_2_config:
            curso = cursos[cfg['curso_idx']]
            if not Seccion.objects.filter(codigo=cfg['codigo'], curso=curso, ciclo=ciclo_2025_2).exists():
                sec = Seccion.objects.create(
                    codigo=cfg['codigo'], curso=curso, ciclo=ciclo_2025_2,
                    modalidad=cfg['mod'], turno=cfg['turno'], dias_semana=cfg['dias'],
                    hora_inicio=cfg['h_ini'], hora_fin=cfg['h_fin'],
                    vacantes_totales=30, vacantes_ocupadas=0
                )
                sec.profesores.add(profesores[cfg['prof']])
                self.stdout.write(self.style.SUCCESS(f'[OK] Sección 2025-2: {sec.codigo} - {curso.nombre}'))
            else:
                sec = Seccion.objects.get(codigo=cfg['codigo'], curso=curso, ciclo=ciclo_2025_2)
                self.stdout.write(self.style.WARNING(f'Sección {sec.codigo} ya existe'))
            secciones_2025_2[cfg['codigo']] = sec

        # ========================================
        # MATRÍCULAS Y NOTAS - CICLO 2025-2 (TODOS APROBADOS)
        # ========================================
        # Angel (alumnos[2]) - 4 cursos
        matriculas_notas_angel = [
            # (codigo_seccion, notas por componente en orden)
            ('16309', [16, 15, 17, 18, 14]),   # Diseño patrones: PC1,PC2,PC3,PA,EXFN
            ('28531', [15, 16, 17, 18]),        # Taller web: APF1,APF2,APF3,PROY
            ('16305', [14, 16, 15, 17]),        # Algoritmos: PC1,PC2,PC3,TF
            ('11366', [16, 14, 15, 18, 13]),    # Redes: PC1,PC2,PC3,PA,EXFN
        ]

        for codigo_sec, notas in matriculas_notas_angel:
            sec = secciones_2025_2[codigo_sec]
            mat, created = self._crear_matricula_directa(alumnos[2], sec)
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Angel matriculado en {sec.curso.nombre}'))
            self._registrar_notas(mat, notas)
            self.stdout.write(self.style.SUCCESS(f'[OK] Notas Angel - {sec.curso.nombre}: {notas}'))

        # Joel (alumnos[3]) - 4 cursos
        matriculas_notas_joel = [
            ('16310', [17, 16, 14, 16, 15]),   # Diseño patrones: PC1,PC2,PC3,PA,EXFN
            ('28531', [14, 17, 16, 18]),        # Taller web: APF1,APF2,APF3,PROY
            ('16306', [15, 16, 17, 15]),        # Algoritmos: PC1,PC2,PC3,TF
            ('11366', [14, 15, 16, 18, 14]),    # Redes: PC1,PC2,PC3,PA,EXFN
        ]

        for codigo_sec, notas in matriculas_notas_joel:
            sec = secciones_2025_2[codigo_sec]
            mat, created = self._crear_matricula_directa(alumnos[3], sec)
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Joel matriculado en {sec.curso.nombre}'))
            self._registrar_notas(mat, notas)
            self.stdout.write(self.style.SUCCESS(f'[OK] Notas Joel - {sec.curso.nombre}: {notas}'))

        # Ricardo (enrique) - 4 cursos en 2025-2 (con 1 desaprobado)
        matriculas_notas_ricardo = [
            ('16311', [9, 8, 7, 12, 8]),    # Diseño patrones: PC1,PC2,PC3,PA,EXFN → DESAPROBADO
            ('28531', [13, 14, 12, 15]),     # Taller web: APF1,APF2,APF3,PROY → APROBADO
            ('16306', [12, 13, 11, 14]),     # Algoritmos: PC1,PC2,PC3,TF → APROBADO
            ('16308', [14, 12, 13, 15]),     # BD II: PC1,PC2,PC3,TF → APROBADO
        ]

        for codigo_sec, notas in matriculas_notas_ricardo:
            sec = secciones_2025_2[codigo_sec]
            mat, created = self._crear_matricula_directa(enrique, sec)
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] Ricardo matriculado en {sec.curso.nombre}'))
            self._registrar_notas(mat, notas)
            self.stdout.write(self.style.SUCCESS(f'[OK] Notas Ricardo - {sec.curso.nombre}: {notas}'))

        # ========================================
        # CUOTAS - CICLO 2025-2 (HISTÓRICO - PAGADAS)
        # ========================================
        for alumno_cuota in [alumnos[2], alumnos[3], enrique]:  # Angel, Joel, Ricardo
            CuotaService.generar_cuotas(alumno_cuota, ciclo_2025_2)
            CuotaService.marcar_pagadas(alumno_cuota, ciclo_2025_2)
            self.stdout.write(self.style.SUCCESS(f'[OK] Cuotas 2025-2 PAGADAS: {alumno_cuota.get_full_name()}'))

        # ========================================
        # SECCIONES - CICLO VERANO 2026 (VIRTUAL)
        # ========================================
        # 2 cursos: Desarrollo de software (idx=8) y Teoría en computación (idx=9)
        # Docente: Garcia Moran (profesores[5])

        secciones_verano_config = [
            {'curso_idx': 8, 'codigo': '17804', 'prof': 5},  # Desarrollo de software
            {'curso_idx': 9, 'codigo': '17805', 'prof': 5},  # Teoría en computación
        ]

        secciones_verano = {}
        for cfg in secciones_verano_config:
            curso = cursos[cfg['curso_idx']]
            if not Seccion.objects.filter(codigo=cfg['codigo'], curso=curso, ciclo=ciclo_verano).exists():
                sec = Seccion.objects.create(
                    codigo=cfg['codigo'], curso=curso, ciclo=ciclo_verano,
                    modalidad='virtual', turno=None, dias_semana='Disponible 24/7',
                    hora_inicio=None, hora_fin=None,
                    vacantes_totales=40, vacantes_ocupadas=0
                )
                sec.profesores.add(profesores[cfg['prof']])
                self.stdout.write(self.style.SUCCESS(f'[OK] Sección VERANO 2026: {sec.codigo} - {curso.nombre}'))
            else:
                sec = Seccion.objects.get(codigo=cfg['codigo'], curso=curso, ciclo=ciclo_verano)
                self.stdout.write(self.style.WARNING(f'Sección {sec.codigo} ya existe'))
            secciones_verano[cfg['codigo']] = sec

        # ========================================
        # MATRÍCULAS Y NOTAS - CICLO VERANO 2026 (TODOS APROBADOS)
        # ========================================
        # Todos los alumnos + Enrique (admin) como alumno de demostración

        alumnos_verano = [
            # (usuario, notas_dev_software, notas_teoria)
            (alumnos[0], [15, 14, 16], [14, 15, 15]),   # Juan
            (alumnos[1], [13, 15, 14], [15, 13, 14]),   # Kelvin
            (alumnos[2], [17, 16, 18], [16, 17, 17]),   # Angel
            (alumnos[3], [14, 15, 16], [15, 14, 15]),   # Joel
            (enrique,    [19, 20, 20], [18, 20, 19]),   # Enrique (admin - alumno demo)
        ]

        sec_dev  = secciones_verano['17804']  # Desarrollo de software
        sec_teo  = secciones_verano['17805']  # Teoría en computación

        nombres_demo = ['Juan', 'Kelvin', 'Angel', 'Joel', 'Enrique (demo)']

        for idx, (usuario, notas_dev, notas_teo) in enumerate(alumnos_verano):
            nombre_display = nombres_demo[idx]

            # Desarrollo de software
            mat_dev, created = self._crear_matricula_directa(usuario, sec_dev)
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] {nombre_display} matriculado en {sec_dev.curso.nombre}'))
            self._registrar_notas(mat_dev, notas_dev)
            self.stdout.write(self.style.SUCCESS(f'[OK] Notas {nombre_display} - Desarrollo de software: {notas_dev}'))

            # Teoría en computación
            mat_teo, created = self._crear_matricula_directa(usuario, sec_teo)
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] {nombre_display} matriculado en {sec_teo.curso.nombre}'))
            self._registrar_notas(mat_teo, notas_teo)
            self.stdout.write(self.style.SUCCESS(f'[OK] Notas {nombre_display} - Teoría en computación: {notas_teo}'))

        # ========================================
        # CUOTAS - CICLO VERANO 2026 (HISTÓRICO - PAGADAS)
        # ========================================
        for usuario, _, _ in alumnos_verano:
            CuotaService.generar_cuotas(usuario, ciclo_verano)
            CuotaService.marcar_pagadas(usuario, ciclo_verano)
            self.stdout.write(self.style.SUCCESS(f'[OK] Cuotas VERANO 2026 PAGADAS: {usuario.get_full_name()}'))

        # ========================================
        # CICLO 2026-1 (ACTIVO - EN CURSO)
        # ========================================
        if not Ciclo.objects.filter(nombre='2026-1').exists():
            ciclo_2026_1 = Ciclo.objects.create(
                nombre='2026-1',
                fecha_inicio_ciclo=date(2026, 3, 28),
                fecha_fin_ciclo=date(2026, 7, 26),
                fecha_inicio_matricula=date(2026, 2, 16),
                fecha_fin_matricula=date(2026, 3, 5),
                matricula_abierta=True,
                ciclo_terminado=False
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Ciclo activo: {ciclo_2026_1.nombre}'))
        else:
            ciclo_2026_1 = Ciclo.objects.get(nombre='2026-1')
            self.stdout.write(self.style.WARNING(f'Ciclo {ciclo_2026_1.nombre} ya existe'))

        # Secciones 2026-1 (virtual)
        # profesores[0]=Nahui, [1]=Rayme, [2]=Ecmias, [3]=Farfan, [4]=Arce, [5]=Garcia
        secciones_2026_1_config = [
            {'curso_idx': 10, 'codigo': '18001', 'prof': 3},  # Curso integrador I - Farfan
            {'curso_idx': 11, 'codigo': '18002', 'prof': 2},  # Javascript avanzado - Ecmias
            {'curso_idx': 12, 'codigo': '18003', 'prof': 1},  # Marcos de desarrollo web - Rayme
            {'curso_idx': 13, 'codigo': '18004', 'prof': 4},  # Hojas de estilo - Arce
            {'curso_idx': 14, 'codigo': '18005', 'prof': 6},  # Análisis y diseño - Osores Granda
            {'curso_idx': 15, 'codigo': '48398', 'prof': 6},  # Diseño de productos - Osores Granda
        ]

        secciones_2026_1 = {}
        for cfg in secciones_2026_1_config:
            curso = cursos[cfg['curso_idx']]
            if not Seccion.objects.filter(codigo=cfg['codigo'], curso=curso, ciclo=ciclo_2026_1).exists():
                sec = Seccion.objects.create(
                    codigo=cfg['codigo'], curso=curso, ciclo=ciclo_2026_1,
                    modalidad='virtual', turno=None, dias_semana='Disponible 24/7',
                    hora_inicio=None, hora_fin=None,
                    vacantes_totales=40, vacantes_ocupadas=0
                )
                sec.profesores.add(profesores[cfg['prof']])
                self.stdout.write(self.style.SUCCESS(f'[OK] Sección 2026-1: {sec.codigo} - {curso.nombre}'))
            else:
                sec = Seccion.objects.get(codigo=cfg['codigo'], curso=curso, ciclo=ciclo_2026_1)
                self.stdout.write(self.style.WARNING(f'Sección {sec.codigo} ya existe'))
            secciones_2026_1[cfg['codigo']] = sec

        # Matrículas 2026-1: Juan, Kelvin, Angel, Joel
        # Van a: 18001, 18002, 18003, 18004, 48398 (NO a 18005 Análisis - esos son solo los 4 extra)
        # Enrique NO se matricula (servirá para demo en vivo)
        alumnos_2026_1 = [alumnos[0], alumnos[1], alumnos[2], alumnos[3]]
        nombres_2026_1 = ['Juan', 'Kelvin', 'Angel', 'Joel']
        secciones_generales = {k: v for k, v in secciones_2026_1.items() if k != '18005'}

        for alumno, nombre in zip(alumnos_2026_1, nombres_2026_1):
            for codigo_sec, sec in secciones_generales.items():
                mat, created = self._crear_matricula_directa(alumno, sec)
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'[OK] {nombre} matriculado en {sec.curso.nombre} (sin notas)'
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'{nombre} ya estaba matriculado en {sec.curso.nombre}'
                    ))

        # ========================================
        # CUOTAS - CICLO 2026-1 (ACTIVO - PENDIENTES)
        # ========================================
        for alumno_cuota in alumnos_2026_1:  # Juan, Kelvin, Angel, Joel
            CuotaService.generar_cuotas(alumno_cuota, ciclo_2026_1)
            self.stdout.write(self.style.SUCCESS(f'[OK] Cuotas 2026-1 PENDIENTES: {alumno_cuota.get_full_name()}'))

        # ========================================
        # ALUMNOS EXTRA - SOLO ANÁLISIS Y DISEÑO (2026-1)
        # Para que el docente Osores vea alumnos en su sección
        # ========================================
        alumnos_extra_analisis = [
            {'nombre': 'David',        'apellido_paterno': 'Chavez',     'apellido_materno': 'Suarez',  'codigo': 'U20200477', 'dni': '20200477'},
            {'nombre': 'Jean Brandon', 'apellido_paterno': 'Loayza',     'apellido_materno': 'Almonte', 'codigo': 'U22235164', 'dni': '22235164'},
            {'nombre': 'Yuri Reiner',  'apellido_paterno': 'Mujica',     'apellido_materno': 'Arroyo',  'codigo': 'U23255063', 'dni': '23255063'},
            {'nombre': 'Abel',         'apellido_paterno': 'Pariacuri',  'apellido_materno': 'Huaman',  'codigo': 'U20235453', 'dni': '20235453'},
        ]

        sec_analisis = secciones_2026_1['18005']  # Análisis y diseño

        for extra in alumnos_extra_analisis:
            if not Usuario.objects.filter(numero_documento=extra['dni']).exists():
                alumno_extra = UsuarioService.crear_usuario({
                    'nombre': extra['nombre'],
                    'apellido_paterno': extra['apellido_paterno'],
                    'apellido_materno': extra['apellido_materno'],
                    'tipo_documento': 'DNI',
                    'numero_documento': extra['dni'],
                    'email': f"{extra['nombre'].lower().replace(' ', '.')}.{extra['apellido_paterno'].lower()}@senati.edu.pe",
                    'telefono': f'9{random.randint(10000000, 99999999)}',
                    'sexo': 'M',
                    'rol': 'alumno',
                    'fecha_nacimiento': date(2000, 1, 1),
                    'password': 'Marco1415@'
                })
                self.stdout.write(self.style.SUCCESS(f'[OK] Alumno extra: {alumno_extra.get_full_name()} / Marco1415@'))
            else:
                alumno_extra = Usuario.objects.get(numero_documento=extra['dni'])
                self.stdout.write(self.style.WARNING(f'Alumno {alumno_extra.get_full_name()} ya existe'))

            mat, created = self._crear_matricula_directa(alumno_extra, sec_analisis)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'[OK] {alumno_extra.get_full_name()} matriculado en Análisis y diseño (sin notas)'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'{alumno_extra.get_full_name()} ya estaba matriculado en Análisis y diseño'
                ))

        # ========================================
        # RESUMEN FINAL
        # ========================================
        self.stdout.write(self.style.SUCCESS('\n========================================'))
        self.stdout.write(self.style.SUCCESS('[OK] Datos creados exitosamente! - SENATI'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(self.style.SUCCESS('\nCREDENCIALES (DNI / Password):'))
        self.stdout.write(self.style.SUCCESS('  Admin Edson:      75933651  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Profesor Nahui:   41523678  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Profesor Rayme:   42634789  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Profesor Ecmias:  43745890  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Profesor Farfan:  44856901  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Profesor Arce:    45967823  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Profesor Garcia:  46078934  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Profesor Osores:  47189045  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Profesor Carrasco:48290156  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Alumno Juan:      72365087  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Alumno Kelvin:    76603529  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Alumno Angel:     74317595  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Alumno Joel:      75650077  / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('  Alumno Enrique:   75911772  / Marco1415@  [demo VERANO 2026]'))
        self.stdout.write(self.style.SUCCESS('\n--- CICLO 2025-2 (HISTÓRICO/TERMINADO) ---'))
        self.stdout.write(self.style.SUCCESS('  Angel y Joel: 4 cursos c/u - TODOS APROBADOS'))
        self.stdout.write(self.style.SUCCESS('  Ricardo: 4 cursos - 1 DESAPROBADO (Diseño de patrones)'))
        self.stdout.write(self.style.SUCCESS('  Juan y Kelvin: sin matrícula en este ciclo'))
        self.stdout.write(self.style.SUCCESS('  Cuotas 2025-2: Angel, Joel, Ricardo → PAGADAS (5 cuotas)'))
        self.stdout.write(self.style.SUCCESS('\n--- CICLO VERANO 2026 (HISTÓRICO/TERMINADO) ---'))
        self.stdout.write(self.style.SUCCESS('  Matrícula:  06/01/2026 - 15/01/2026'))
        self.stdout.write(self.style.SUCCESS('  Ciclo:      16/01/2026 - 06/03/2026'))
        self.stdout.write(self.style.SUCCESS('  Cursos:     Desarrollo de software (17804)'))
        self.stdout.write(self.style.SUCCESS('              Teoría en computación (17805)'))
        self.stdout.write(self.style.SUCCESS('  Docente:    Luis Rolando Garcia Moran'))
        self.stdout.write(self.style.SUCCESS('  Alumnos:    Juan, Kelvin, Angel, Joel + Ricardo (demo)'))
        self.stdout.write(self.style.SUCCESS('  Estado:     TODOS APROBADOS'))
        self.stdout.write(self.style.SUCCESS('  Cuotas VERANO: todos → PAGADAS (2 cuotas)'))
        self.stdout.write(self.style.SUCCESS('\n--- CICLO 2026-1 (ACTIVO - EN CURSO) ---'))
        self.stdout.write(self.style.SUCCESS('  Matrícula:  16/02/2026 - 05/03/2026'))
        self.stdout.write(self.style.SUCCESS('  Ciclo:      28/03/2026 - 26/07/2026'))
        self.stdout.write(self.style.SUCCESS('  Cursos:     Curso integrador I (18001) - Farfan'))
        self.stdout.write(self.style.SUCCESS('              Javascript avanzado (18002) - Ecmias'))
        self.stdout.write(self.style.SUCCESS('              Marcos de desarrollo web (18003) - Rayme'))
        self.stdout.write(self.style.SUCCESS('              Hojas de estilo en cascada avanzado (18004) - Arce'))
        self.stdout.write(self.style.SUCCESS('              Análisis y diseño de sistemas (18005) - Osores Granda'))
        self.stdout.write(self.style.SUCCESS('              Diseño de productos y servicios (48398) - Osores Granda'))
        self.stdout.write(self.style.SUCCESS('  Alumnos generales (18001-18004+48398): Juan, Kelvin, Angel, Joel'))
        self.stdout.write(self.style.SUCCESS('  Alumnos Análisis (18005): David, Jean Brandon, Yuri Reiner, Abel'))
        self.stdout.write(self.style.SUCCESS('  Ricardo:    NO matriculado en 2026-1 (demo en vivo de matrícula)'))
        self.stdout.write(self.style.SUCCESS('  Cuotas 2026-1: Juan, Kelvin, Angel, Joel → PENDIENTES (5 cuotas)'))
        self.stdout.write(self.style.SUCCESS('\n  [DEMO MATRÍCULA] Login: 75911772 / Marco1415@'))
        self.stdout.write(self.style.SUCCESS('\nAccede a: http://localhost:8000'))
