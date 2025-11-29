"""
ReporteService - Servicio para generación de reportes

Patrones de Diseño:
- Service Layer Pattern
- Factory Pattern: Creación de reportes según tipo
- Strategy Pattern: Diferentes estrategias de generación de reportes
- Builder Pattern: Construcción de reportes complejos
"""

from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.conf import settings
from academic_system.models import Matricula, Nota
from django.http import HttpResponse

# ============================================================
# Abstract Factory
# ============================================================


class ReporteAbstractFactory:
    """Abstract Factory para estrategias de reporte."""

    def crear_lista_alumnos(self):
        raise NotImplementedError

    def crear_reporte_notas(self):
        raise NotImplementedError


class ReporteExcelFactory(ReporteAbstractFactory):
    def crear_lista_alumnos(self):
        return ListaAlumnosExcelStrategy()

    def crear_reporte_notas(self):
        return NotasSeccionExcelStrategy()


class ReportePDFFactory(ReporteAbstractFactory):
    def crear_lista_alumnos(self):
        return ListaAlumnosPDFStrategy()

    def crear_reporte_notas(self):
        return NotasSeccionPDFStrategy()


# ============================================================
# Adapter
# ============================================================


class ResponseAdapter:
    """Adapter para transformar buffers en HttpResponse."""

    @staticmethod
    def from_buffer(buffer, content_type, filename):
        response = HttpResponse(buffer.getvalue(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename=\"{filename}\"'
        return response


# ============================================================
# Bridge
# ============================================================


class FormatoImplementor:
    """Implementor que delega a factories por formato."""

    def __init__(self, formato):
        self.formato = formato
        self.factory = ReporteExcelFactory() if formato == 'excel' else ReportePDFFactory()

    def generar(self, tipo, **kwargs):
        if tipo == 'lista_alumnos':
            estrategia = self.factory.crear_lista_alumnos()
        else:
            estrategia = self.factory.crear_reporte_notas()
        return estrategia.generar(**kwargs)


class ReporteBridge:
    """Abstracción que separa tipo de reporte de formato (Bridge Pattern)."""

    def __init__(self, formato):
        self.implementor = FormatoImplementor(formato)

    def generar(self, tipo, **kwargs):
        return self.implementor.generar(tipo, **kwargs)


# ============================================================
# Composite
# ============================================================


class TablaComposite:
    """Composite simple para construir tablas (listas de filas)."""

    def __init__(self):
        self.filas = []

    def agregar(self, fila):
        self.filas.append(fila)

    def to_rows(self):
        return self.filas


class ReporteStrategy:
    """
    STRATEGY PATTERN: Interfaz base para estrategias de generación de reportes.

    Cada estrategia concreta implementa el método generar() para
    producir un reporte específico en un formato específico.
    """

    def generar(self, **kwargs):
        """
        Genera el reporte según la estrategia.

        Args:
            **kwargs: Parámetros necesarios para generar el reporte

        Returns:
            BytesIO: Buffer con el reporte generado

        Raises:
            NotImplementedError: Si no se implementa en subclase
        """
        raise NotImplementedError("Las estrategias deben implementar el método generar()")


class ListaAlumnosExcelStrategy(ReporteStrategy):
    """STRATEGY PATTERN: Estrategia para generar lista de alumnos en Excel"""

    def generar(self, **kwargs):
        return ReporteBuilder.build_lista_alumnos_excel(kwargs['seccion_id'])


class ListaAlumnosPDFStrategy(ReporteStrategy):
    """STRATEGY PATTERN: Estrategia para generar lista de alumnos en PDF"""

    def generar(self, **kwargs):
        return ReporteBuilder.build_lista_alumnos_pdf(kwargs['seccion_id'])


class NotasSeccionExcelStrategy(ReporteStrategy):
    """STRATEGY PATTERN: Estrategia para generar notas de sección en Excel"""

    def generar(self, **kwargs):
        return ReporteBuilder.build_notas_excel(kwargs['seccion_id'])


class NotasSeccionPDFStrategy(ReporteStrategy):
    """STRATEGY PATTERN: Estrategia para generar notas de sección en PDF"""

    def generar(self, **kwargs):
        return ReporteBuilder.build_notas_pdf(kwargs['seccion_id'])


class ReporteFactory:
    """
    FACTORY + STRATEGY PATTERN: Selecciona y ejecuta la estrategia apropiada.

    El Factory mantiene un registro de estrategias disponibles y
    delega la generación a la estrategia correspondiente.

    Ventajas:
    - Open/Closed Principle: Agregar nuevas estrategias sin modificar el Factory
    - Fácil extensión: Registrar nuevas estrategias en el diccionario
    - Sin condicionales anidados: Usa lookup de diccionario
    """

    # Registro de estrategias disponibles
    _estrategias = {
        ('lista_alumnos', 'excel'): ListaAlumnosExcelStrategy(),
        ('lista_alumnos', 'pdf'): ListaAlumnosPDFStrategy(),
        ('notas_seccion', 'excel'): NotasSeccionExcelStrategy(),
        ('notas_seccion', 'pdf'): NotasSeccionPDFStrategy(),
    }

    @classmethod
    def registrar_estrategia(cls, tipo, formato, estrategia):
        """
        Registra una nueva estrategia de reporte.

        Esto permite extender el sistema con nuevos tipos de reportes
        sin modificar el código existente (Open/Closed Principle).

        Args:
            tipo (str): Tipo de reporte
            formato (str): Formato del reporte
            estrategia (ReporteStrategy): Instancia de la estrategia

        Ejemplo:
            ReporteFactory.registrar_estrategia(
                'estadisticas_curso',
                'excel',
                EstadisticasCursoExcelStrategy()
            )
        """
        cls._estrategias[(tipo, formato)] = estrategia

    @classmethod
    def crear_reporte(cls, tipo, formato, **kwargs):
        """
        FACTORY + STRATEGY PATTERN: Crea un reporte usando la estrategia apropiada.
        ABSTRACT FACTORY + BRIDGE: Selecciona familia por formato y tipo.

        Args:
            tipo (str): 'lista_alumnos' o 'notas_seccion'
            formato (str): 'excel' o 'pdf'
            **kwargs: Parámetros adicionales según el tipo

        Returns:
            BytesIO: Buffer con el reporte generado

        Raises:
            ValueError: Si no existe estrategia para el tipo/formato solicitado
        """
        # Bridge + Abstract Factory: delegar en implementor de formato
        try:
            return ReporteBridge(formato).generar(tipo, **kwargs)
        except Exception:
            # STRATEGY PATTERN: fallback al registro clásico
            estrategia = cls._estrategias.get((tipo, formato))

            if estrategia is None:
                tipos_disponibles = ', '.join(
                    f"{t}/{f}" for t, f in cls._estrategias.keys()
                )
                raise ValueError(
                    f'Tipo de reporte no soportado: {tipo}/{formato}. '
                    f'Disponibles: {tipos_disponibles}'
                )

            return estrategia.generar(**kwargs)


class ReporteBuilder:
    """
    Builder Pattern: Construye reportes complejos paso a paso.
    """

    @staticmethod
    def build_lista_alumnos_excel(seccion_id):
        """
        Construye un reporte Excel con la lista de alumnos.

        Args:
            seccion_id: ID de la sección

        Returns:
            BytesIO: Buffer con el archivo Excel
        """
        from academic_system.models import Seccion

        seccion = Seccion.objects.select_related('curso', 'ciclo').get(pk=seccion_id)
        matriculas = Matricula.objects.filter(
            seccion=seccion,
            is_active=True
        ).select_related('alumno').order_by('alumno__apellido_paterno')

        # Crear workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Lista de Alumnos"

        # Estilos
        header_font = Font(bold=True, color="FFFFFF", size=12)
        header_fill = PatternFill(start_color="DC143C", end_color="DC143C", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")

        # Título
        ws.merge_cells('A1:F1')
        title_cell = ws['A1']
        title_cell.value = settings.UNIVERSITY_NAME
        title_cell.font = Font(bold=True, size=14)
        title_cell.alignment = Alignment(horizontal="center")

        # Subtítulo
        ws.merge_cells('A2:F2')
        subtitle_cell = ws['A2']
        subtitle_cell.value = f"Lista de Alumnos - {seccion.curso.nombre} - Sección {seccion.codigo}"
        subtitle_cell.font = Font(size=11)
        subtitle_cell.alignment = Alignment(horizontal="center")

        ws.merge_cells('A3:F3')
        ciclo_cell = ws['A3']
        ciclo_cell.value = f"Ciclo: {seccion.ciclo.nombre}"
        ciclo_cell.alignment = Alignment(horizontal="center")

        # Headers
        headers = ['N°', 'Código', 'Apellido Paterno', 'Apellido Materno', 'Nombres', 'Email']
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=5, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment

        # Datos
        for row_num, matricula in enumerate(matriculas, 6):
            ws.cell(row=row_num, column=1, value=row_num - 5)
            ws.cell(row=row_num, column=2, value=matricula.alumno.codigo)
            ws.cell(row=row_num, column=3, value=matricula.alumno.apellido_paterno)
            ws.cell(row=row_num, column=4, value=matricula.alumno.apellido_materno)
            ws.cell(row=row_num, column=5, value=matricula.alumno.first_name)
            ws.cell(row=row_num, column=6, value=matricula.alumno.email)

        # Ajustar anchos de columna
        ws.column_dimensions['A'].width = 5
        ws.column_dimensions['B'].width = 12
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['D'].width = 20
        ws.column_dimensions['E'].width = 20
        ws.column_dimensions['F'].width = 30

        # Guardar en buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer

    @staticmethod
    def build_notas_excel(seccion_id):
        """
        Construye un reporte Excel con las notas de una sección.

        Args:
            seccion_id: ID de la sección

        Returns:
            BytesIO: Buffer con el archivo Excel
        """
        from academic_system.models import Seccion, ComponenteEvaluacion
        from academic_system.services import NotaService

        seccion = Seccion.objects.select_related('curso', 'ciclo').get(pk=seccion_id)
        matriculas = Matricula.objects.filter(
            seccion=seccion,
            is_active=True
        ).select_related('alumno').order_by('alumno__apellido_paterno')

        componentes = ComponenteEvaluacion.objects.filter(
            curso=seccion.curso
        ).order_by('orden')

        # Crear workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Notas"

        # Estilos
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_fill = PatternFill(start_color="DC143C", end_color="DC143C", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")

        # Título
        col_count = 5 + len(componentes) + 1  # Código, Apellidos, Nombres + componentes + Promedio
        ws.merge_cells(f'A1:{chr(64 + col_count)}1')
        title_cell = ws['A1']
        title_cell.value = settings.UNIVERSITY_NAME
        title_cell.font = Font(bold=True, size=14)
        title_cell.alignment = Alignment(horizontal="center")

        ws.merge_cells(f'A2:{chr(64 + col_count)}2')
        subtitle_cell = ws['A2']
        subtitle_cell.value = f"Acta de Notas - {seccion.curso.nombre} - Sección {seccion.codigo}"
        subtitle_cell.font = Font(size=11)
        subtitle_cell.alignment = Alignment(horizontal="center")

        ws.merge_cells(f'A3:{chr(64 + col_count)}3')
        ciclo_cell = ws['A3']
        ciclo_cell.value = f"Ciclo: {seccion.ciclo.nombre}"
        ciclo_cell.alignment = Alignment(horizontal="center")

        # Headers
        headers = ['N°', 'Código', 'Apellido Paterno', 'Apellido Materno', 'Nombres']
        for comp in componentes:
            headers.append(f"{comp.nombre}\n({comp.porcentaje}%)")
        headers.append('Promedio\nFinal')

        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=5, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment

        # Datos
        for row_num, matricula in enumerate(matriculas, 6):
            ws.cell(row=row_num, column=1, value=row_num - 5)
            ws.cell(row=row_num, column=2, value=matricula.alumno.codigo)
            ws.cell(row=row_num, column=3, value=matricula.alumno.apellido_paterno)
            ws.cell(row=row_num, column=4, value=matricula.alumno.apellido_materno)
            ws.cell(row=row_num, column=5, value=matricula.alumno.first_name)

            # Notas
            col = 6
            for componente in componentes:
                try:
                    nota = Nota.objects.get(matricula=matricula, componente=componente)
                    valor = float(nota.valor) if nota.valor is not None else '-'
                except Nota.DoesNotExist:
                    valor = '-'

                ws.cell(row=row_num, column=col, value=valor)
                col += 1

            # Promedio
            resultado = NotaService.calcular_promedio_matricula(matricula.id)
            promedio = float(resultado['promedio']) if resultado['promedio'] else '-'
            ws.cell(row=row_num, column=col, value=promedio)

        # Ajustar anchos
        ws.column_dimensions['A'].width = 5
        ws.column_dimensions['B'].width = 12
        ws.column_dimensions['C'].width = 18
        ws.column_dimensions['D'].width = 18
        ws.column_dimensions['E'].width = 18

        for i in range(len(componentes)):
            ws.column_dimensions[chr(70 + i)].width = 10

        # Guardar en buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer

    @staticmethod
    def build_lista_alumnos_pdf(seccion_id):
        """
        Construye un reporte PDF con la lista de alumnos.

        Args:
            seccion_id: ID de la sección

        Returns:
            BytesIO: Buffer con el archivo PDF
        """
        from academic_system.models import Seccion

        seccion = Seccion.objects.select_related('curso', 'ciclo').get(pk=seccion_id)
        matriculas = Matricula.objects.filter(
            seccion=seccion,
            is_active=True
        ).select_related('alumno').order_by('alumno__apellido_paterno')

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#DC143C'),
            alignment=TA_CENTER,
            spaceAfter=12
        )

        # Título
        elements.append(Paragraph(settings.UNIVERSITY_NAME, title_style))
        elements.append(Paragraph(
            f"Lista de Alumnos - {seccion.curso.nombre} - Sección {seccion.codigo}",
            styles['Heading2']
        ))
        elements.append(Paragraph(f"Ciclo: {seccion.ciclo.nombre}", styles['Normal']))
        elements.append(Spacer(1, 0.3 * inch))

        # Tabla
        data = [['N°', 'Código', 'Apellido Paterno', 'Apellido Materno', 'Nombres']]

        for idx, matricula in enumerate(matriculas, 1):
            data.append([
                str(idx),
                matricula.alumno.codigo,
                matricula.alumno.apellido_paterno,
                matricula.alumno.apellido_materno,
                matricula.alumno.first_name
            ])

        table = Table(data, colWidths=[0.5 * inch, 1 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC143C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer

    @staticmethod
    def build_notas_pdf(seccion_id):
        """
        Construye un reporte PDF con las notas de una sección.

        Args:
            seccion_id: ID de la sección

        Returns:
            BytesIO: Buffer con el archivo PDF
        """
        from academic_system.models import Seccion, ComponenteEvaluacion
        from academic_system.services import NotaService

        seccion = Seccion.objects.select_related('curso', 'ciclo').get(pk=seccion_id)
        matriculas = Matricula.objects.filter(
            seccion=seccion,
            is_active=True
        ).select_related('alumno').order_by('alumno__apellido_paterno')

        componentes = ComponenteEvaluacion.objects.filter(
            curso=seccion.curso
        ).order_by('orden')

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=14,
            textColor=colors.HexColor('#DC143C'),
            alignment=TA_CENTER,
            spaceAfter=10
        )

        # Título
        elements.append(Paragraph(settings.UNIVERSITY_NAME, title_style))
        elements.append(Paragraph(
            f"Acta de Notas - {seccion.curso.nombre} - Sección {seccion.codigo}",
            styles['Heading3']
        ))
        elements.append(Paragraph(f"Ciclo: {seccion.ciclo.nombre}", styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

        # Headers de tabla
        headers = ['N°', 'Código', 'Apellidos y Nombres']
        for comp in componentes:
            headers.append(f"{comp.nombre[:10]}\n({comp.porcentaje}%)")
        headers.append('Promedio')

        tabla = TablaComposite()
        tabla.agregar(headers)

        # Datos
        for idx, matricula in enumerate(matriculas, 1):
            row = [
                str(idx),
                matricula.alumno.codigo,
                f"{matricula.alumno.apellido_paterno} {matricula.alumno.apellido_materno}, {matricula.alumno.first_name}"
            ]

            for componente in componentes:
                try:
                    nota = Nota.objects.get(matricula=matricula, componente=componente)
                    valor = str(nota.valor) if nota.valor is not None else '-'
                except Nota.DoesNotExist:
                    valor = '-'
                row.append(valor)

            resultado = NotaService.calcular_promedio_matricula(matricula.id)
            promedio = str(resultado['promedio']) if resultado['promedio'] else '-'
            row.append(promedio)

            tabla.agregar(row)

        # Crear tabla con anchos proporcionales
        col_widths = [0.3 * inch, 0.7 * inch, 1.8 * inch]
        for _ in componentes:
            col_widths.append(0.5 * inch)
        col_widths.append(0.6 * inch)

        data = tabla.to_rows()

        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC143C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer


class ReporteService:
    """
    Facade Pattern: Simplifica el acceso a la generación de reportes.
    """

    @staticmethod
    def generar_lista_alumnos(seccion_id, formato='excel'):
        """
        Genera una lista de alumnos en el formato especificado.

        Args:
            seccion_id: ID de la sección
            formato: 'excel' o 'pdf'

        Returns:
            BytesIO: Buffer con el reporte
        """
        return ReporteFactory.crear_reporte('lista_alumnos', formato, seccion_id=seccion_id)

    @staticmethod
    def generar_reporte_notas(seccion_id, formato='excel'):
        """
        Genera un reporte de notas en el formato especificado.

        Args:
            seccion_id: ID de la sección
            formato: 'excel' o 'pdf'

        Returns:
            BytesIO: Buffer con el reporte
        """
        return ReporteFactory.crear_reporte('notas_seccion', formato, seccion_id=seccion_id)
