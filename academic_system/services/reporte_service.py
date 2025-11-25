"""
ReporteService - Servicio para generación de reportes

Patrones de Diseño:
- Service Layer Pattern
- Factory Pattern: Creación de reportes según tipo
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


class ReporteFactory:
    """
    Factory Pattern: Crea reportes según el tipo solicitado.
    """

    @staticmethod
    def crear_reporte(tipo, formato, **kwargs):
        """
        Factory Method: Crea un reporte según tipo y formato.

        Args:
            tipo: 'lista_alumnos' o 'notas_seccion'
            formato: 'excel' o 'pdf'
            **kwargs: Parámetros adicionales según el tipo

        Returns:
            BytesIO: Buffer con el reporte generado
        """
        if tipo == 'lista_alumnos':
            if formato == 'excel':
                return ReporteBuilder.build_lista_alumnos_excel(kwargs['seccion_id'])
            elif formato == 'pdf':
                return ReporteBuilder.build_lista_alumnos_pdf(kwargs['seccion_id'])

        elif tipo == 'notas_seccion':
            if formato == 'excel':
                return ReporteBuilder.build_notas_excel(kwargs['seccion_id'])
            elif formato == 'pdf':
                return ReporteBuilder.build_notas_pdf(kwargs['seccion_id'])

        raise ValueError(f'Tipo de reporte no soportado: {tipo} en formato {formato}')


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

        data = [headers]

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

            data.append(row)

        # Crear tabla con anchos proporcionales
        col_widths = [0.3 * inch, 0.7 * inch, 1.8 * inch]
        for _ in componentes:
            col_widths.append(0.5 * inch)
        col_widths.append(0.6 * inch)

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
