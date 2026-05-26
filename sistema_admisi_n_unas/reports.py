"""PDF Report generation for Sistema Admisión UNAS."""
import io
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import get_sample_style_sheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    HRFlowable,
)
from reportlab.pdfgen import canvas

from sistema_admisi_n_unas.config import (
    UNAS_BLUE,
    UNAS_GREEN,
    REPORT_DIR,
    EXPORT_DIR,
)


def get_report_filename(prefix: str = "reporte") -> str:
    """Generate a unique filename for reports."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.pdf"


def get_export_filename(prefix: str = "export") -> str:
    """Generate a unique filename for exports."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.csv"


class ReportStyles:
    """Custom styles for PDF reports."""

    @staticmethod
    def get_styles():
        styles = get_sample_style_sheet()

        # Title style
        styles.add(
            ParagraphStyle(
                name="ReportTitle",
                parent=styles["Heading1"],
                fontSize=24,
                textColor=colors.HexColor("#003366"),
                alignment=TA_CENTER,
                spaceAfter=12,
                fontName="Helvetica-Bold",
            )
        )

        # Subtitle style
        styles.add(
            ParagraphStyle(
                name="ReportSubtitle",
                parent=styles["Normal"],
                fontSize=12,
                textColor=colors.HexColor("#228B22"),
                alignment=TA_CENTER,
                spaceAfter=20,
            )
        )

        # Section header
        styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=styles["Heading2"],
                fontSize=14,
                textColor=colors.HexColor("#003366"),
                spaceAfter=8,
                spaceBefore=16,
                fontName="Helvetica-Bold",
                borderColor=colors.HexColor("#228B22"),
                borderWidth=2,
                borderPadding=5,
            )
        )

        # Normal text
        styles.add(
            ParagraphStyle(
                name="ReportNormal",
                parent=styles["Normal"],
                fontSize=10,
                textColor=colors.black,
                spaceAfter=6,
                alignment=TA_JUSTIFY,
            )
        )

        # Footer
        styles.add(
            ParagraphStyle(
                name="Footer",
                parent=styles["Normal"],
                fontSize=8,
                textColor=colors.gray,
                alignment=TA_CENTER,
            )
        )

        return styles


def add_header_footer(canvas_obj, doc):
    """Add header and footer to each page."""
    canvas_obj.saveState()

    # Header line
    canvas_obj.setStrokeColor(colors.HexColor("#003366"))
    canvas_obj.setLineWidth(2)
    canvas_obj.line(50, A4[1] - 50, A4[0] - 50, A4[1] - 50)

    # Footer
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.gray)
    canvas_obj.drawString(
        50, 30, f"Sistema de Admisión UNAS - {datetime.now().strftime('%Y')}"
    )
    canvas_obj.drawRightString(
        A4[0] - 50, 30, f"Página {doc.page}"
    )

    canvas_obj.restoreState()


def generate_postulantes_report(postulantes: List[Dict], filters: Dict = None) -> str:
    """Generate a PDF report of postulants.

    Args:
        postulantes: List of postulant dictionaries
        filters: Optional filters applied (search, career, etc.)

    Returns:
        Path to the generated PDF file
    """
    if not REPORT_DIR.exists():
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

    filename = get_report_filename("postulantes")
    filepath = REPORT_DIR / filename

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=70,
        bottomMargin=50,
    )

    styles = ReportStyles.get_styles()
    story = []

    # Title
    story.append(Paragraph("REPORTE DE POSTULANTES", styles["ReportTitle"]))
    story.append(
        Paragraph(
            f"Sistema de Admisión - Universidad Nacional Agraria de la Selva",
            styles["ReportSubtitle"],
        )
    )
    story.append(
        Paragraph(
            f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles["ReportNormal"],
        )
    )

    # Filters applied
    if filters:
        filter_text = " | ".join([f"{k}: {v}" for k, v in filters.items() if v])
        story.append(Paragraph(f"Filtros aplicados: {filter_text}", styles["ReportNormal"]))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#228B22")))
    story.append(Spacer(1, 20))

    # Summary statistics
    total = len(postulantes)
    estatal = len([p for p in postulantes if p.get("tipo_colegio") == "Estatal"])
    privado = len([p for p in postulantes if p.get("tipo_colegio") == "Privado"])
    ingresantes = len(
        [p for p in postulantes if str(p.get("estado", "")).lower() == "ingresante"]
    )
    total_recaudado = sum(p.get("costo", 0) for p in postulantes)

    summary_data = [
        ["MÉTRICA", "VALOR"],
        ["Total Postulantes", str(total)],
        ["Estatales", str(estatal)],
        ["Privados", str(privado)],
        ["Total Ingresantes", str(ingresantes)],
        ["Total Recaudado", f"S/. {total_recaudado:,.2f}"],
    ]

    summary_table = Table(summary_data, colWidths=[200, 120])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f5f5f5")),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#228B22")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e8f5e9")]),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 30))

    # Detailed table
    story.append(Paragraph("LISTA DETALLADA DE POSTULANTES", styles["SectionHeader"]))

    # Table headers
    headers = ["DNI", "Apellidos", "Nombres", "Carrera", "Colegio", "Estado"]
    col_widths = [60, 90, 90, 130, 60, 60]

    table_data = [headers]

    for p in postulantes[:100]:  # Limit to 100 for performance
        row = [
            p.get("dni", ""),
            p.get("apellidos", ""),
            p.get("nombres", ""),
            p.get("carrera", "")[:25],  # Truncate long names
            p.get("tipo_colegio", ""),
            p.get("estado", ""),
        ]
        table_data.append(row)

    main_table = Table(table_data, colWidths=col_widths)
    main_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
            ]
        )
    )
    story.append(main_table)

    if len(postulantes) > 100:
        story.append(Spacer(1, 10))
        story.append(
            Paragraph(
                f"<i>Mostrando los primeros 100 de {len(postulantes)} registros.</i>",
                styles["ReportNormal"],
            )
        )

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    return str(filepath)


def generate_resultados_report(resultados: List[Dict]) -> str:
    """Generate a PDF report of exam results.

    Args:
        resultados: List of result dictionaries

    Returns:
        Path to the generated PDF file
    """
    if not REPORT_DIR.exists():
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

    filename = get_report_filename("resultados")
    filepath = REPORT_DIR / filename

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=70,
        bottomMargin=50,
    )

    styles = ReportStyles.get_styles()
    story = []

    # Title
    story.append(Paragraph("REPORTE DE RESULTADOS DEL EXAMEN", styles["ReportTitle"]))
    story.append(
        Paragraph(
            "Sistema de Admisión - Universidad Nacional Agraria de la Selva",
            styles["ReportSubtitle"],
        )
    )
    story.append(
        Paragraph(
            f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles["ReportNormal"],
        )
    )
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#228B22")))
    story.append(Spacer(1, 20))

    # Summary
    total_resultados = len(resultados)
    ingresos = len([r for r in resultados if r.get("condicion") == "Ingresante"])
    no_ingresos = total_resultados - ingresos
    promedio = (
        sum(r.get("puntaje", 0) for r in resultados) / total_resultados
        if total_resultados > 0
        else 0
    )

    summary_data = [
        ["MÉTRICA", "VALOR"],
        ["Total Postulantes", str(total_resultados)],
        ["Ingresantes", str(ingresos)],
        ["No Ingresantes", str(no_ingresos)],
        ["Promedio General", f"{promedio:.2f}"],
    ]

    summary_table = Table(summary_data, colWidths=[200, 120])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#228B22")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#003366")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e8f5e9")]),
            ]
        )
    )
    story.append(summary_table)
    story.append(Spacer(1, 30))

    # Results table
    story.append(Paragraph("RANKING DE RESULTADOS", styles["SectionHeader"]))

    headers = ["Posición", "DNI", "Apellidos", "Nombres", "Puntaje", "Condición"]
    col_widths = [50, 60, 90, 90, 60, 80]

    table_data = [headers]

    for idx, r in enumerate(resultados[:50]):  # Limit to top 50
        row = [
            str(idx + 1),
            r.get("dni", ""),
            r.get("apellidos", ""),
            r.get("nombres", ""),
            f"{r.get('puntaje', 0):.2f}",
            r.get("condicion", ""),
        ]
        table_data.append(row)

    results_table = Table(table_data, colWidths=col_widths)
    results_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#228B22")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),  # Position column centered
                ("ALIGN", (4, 0), (4, -1), "CENTER"),  # Score column centered
                ("ALIGN", (5, 0), (5, -1), "CENTER"),  # Condition column centered
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
                (
                    "BACKGROUND",
                    (5, 1),
                    (5, -1),
                    colors.HexColor("#e8f5e9"),
                ),  # Highlight condition
            ]
        )
    )
    story.append(results_table)

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    return str(filepath)


def generate_stats_report(stats: Dict) -> str:
    """Generate a PDF report with dashboard statistics.

    Args:
        stats: Dictionary with statistics data

    Returns:
        Path to the generated PDF file
    """
    if not REPORT_DIR.exists():
        REPORT_DIR.mkdir(parents=True, exist_ok=True)

    filename = get_report_filename("estadisticas")
    filepath = REPORT_DIR / filename

    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=70,
        bottomMargin=50,
    )

    styles = ReportStyles.get_styles()
    story = []

    # Title
    story.append(Paragraph("REPORTE ESTADÍSTICO DASHBOARD", styles["ReportTitle"]))
    story.append(
        Paragraph(
            "Sistema de Admisión - Universidad Nacional Agraria de la Selva",
            styles["ReportSubtitle"],
        )
    )
    story.append(
        Paragraph(
            f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            styles["ReportNormal"],
        )
    )
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#228B22")))
    story.append(Spacer(1, 20))

    # KPIs
    kpi_data = [
        ["INDICADOR", "VALOR"],
        ["Total Postulantes", str(stats.get("total_postulantes", 0))],
        ["Total Ingresantes", str(stats.get("admitted_count", 0))],
        ["Total Recaudado", f"S/. {stats.get('total_recaudado', 0):,.2f}"],
        ["Postulantes Estatales", str(stats.get("total_estatal", 0))],
        ["Postulantes Privados", str(stats.get("total_privado", 0))],
        ["Carrera Más Demandada", str(stats.get("top_career", "N/A"))],
        ["Promedio General", f"{stats.get('general_avg', 0):.2f}"],
    ]

    kpi_table = Table(kpi_data, colWidths=[200, 150])
    kpi_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#228B22")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#e8f5e9")]),
            ]
        )
    )
    story.append(kpi_table)

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    return str(filepath)


def export_to_csv(data: List[Dict], filename_prefix: str = "export") -> str:
    """Export data to CSV file.

    Args:
        data: List of dictionaries to export
        filename_prefix: Prefix for the filename

    Returns:
        Path to the generated CSV file
    """
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    filepath = EXPORT_DIR / filename

    if not data:
        return str(filepath)

    # Get all keys from first record
    headers = list(data[0].keys())

    import csv

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    return str(filepath)