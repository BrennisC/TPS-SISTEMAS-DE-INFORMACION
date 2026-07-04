"""
Componentes UI para el Dashboard Ejecutivo de Biblioteca.
"""
import reflex as rx

from .chart_utils import TOOLTIP_PROPS, chart_legend
from .stats_card import stats_card, trend_indicator
from ..states.biblioteca_dashboard_state import BibliotecaDashboardState


def kpi_card(
    title: str,
    value: str,
    trend_val: str,
    trend_positive: bool,
    subtext: str,
    icon: str,
    color: str,
) -> rx.Component:
    """Tarjeta KPI con indicador de tendencia para el dashboard ejecutivo."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(title, class_name="text-xs font-medium text-gray-500 uppercase tracking-wider"),
                rx.el.p(value, class_name="text-2xl font-extrabold text-gray-900 mt-1"),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.icon(icon, size=24, color="white"),
                class_name="p-3 rounded-xl shadow-sm flex items-center justify-center",
                style={"backgroundColor": color},
            ),
            class_name="flex items-start justify-between w-full mb-4",
        ),
        rx.el.div(
            trend_indicator(value=" " + subtext, trend=trend_val, positive=trend_positive),
            class_name="w-full",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow cursor-default",
    )


def panel_alertas() -> rx.Component:
    """Panel de alertas inteligentes."""
    return rx.el.div(
        rx.el.h3("Alertas del Sistema", class_name="text-lg font-bold text-gray-900 mb-4"),
        rx.el.div(
            rx.foreach(
                BibliotecaDashboardState.alertas,
                lambda alerta: rx.el.div(
                    rx.el.div(
                        rx.match(
                            alerta["icono"],
                            ("triangle-alert", rx.icon("triangle-alert", class_name=rx.cond(alerta["tipo"] == "critico", "h-5 w-5 text-red-600", rx.cond(alerta["tipo"] == "advertencia", "h-5 w-5 text-amber-600", "h-5 w-5 text-green-600")))),
                            ("clock", rx.icon("clock", class_name=rx.cond(alerta["tipo"] == "critico", "h-5 w-5 text-red-600", rx.cond(alerta["tipo"] == "advertencia", "h-5 w-5 text-amber-600", "h-5 w-5 text-green-600")))),
                            ("book-x", rx.icon("book-x", class_name=rx.cond(alerta["tipo"] == "critico", "h-5 w-5 text-red-600", rx.cond(alerta["tipo"] == "advertencia", "h-5 w-5 text-amber-600", "h-5 w-5 text-green-600")))),
                            ("trending-up", rx.icon("trending-up", class_name=rx.cond(alerta["tipo"] == "critico", "h-5 w-5 text-red-600", rx.cond(alerta["tipo"] == "advertencia", "h-5 w-5 text-amber-600", "h-5 w-5 text-green-600")))),
                            ("package-x", rx.icon("package-x", class_name=rx.cond(alerta["tipo"] == "critico", "h-5 w-5 text-red-600", rx.cond(alerta["tipo"] == "advertencia", "h-5 w-5 text-amber-600", "h-5 w-5 text-green-600")))),
                            ("wrench", rx.icon("wrench", class_name=rx.cond(alerta["tipo"] == "critico", "h-5 w-5 text-red-600", rx.cond(alerta["tipo"] == "advertencia", "h-5 w-5 text-amber-600", "h-5 w-5 text-green-600")))),
                            ("circle-check", rx.icon("circle-check", class_name=rx.cond(alerta["tipo"] == "critico", "h-5 w-5 text-red-600", rx.cond(alerta["tipo"] == "advertencia", "h-5 w-5 text-amber-600", "h-5 w-5 text-green-600")))),
                            rx.icon("circle-help", class_name=rx.cond(alerta["tipo"] == "critico", "h-5 w-5 text-red-600", rx.cond(alerta["tipo"] == "advertencia", "h-5 w-5 text-amber-600", "h-5 w-5 text-green-600")))
                        ),
                        class_name=rx.cond(
                            alerta["tipo"] == "critico",
                            "p-2 bg-red-50 rounded-lg",
                            rx.cond(
                                alerta["tipo"] == "advertencia",
                                "p-2 bg-amber-50 rounded-lg",
                                "p-2 bg-green-50 rounded-lg"
                            )
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(alerta["titulo"], class_name="text-sm font-bold text-gray-900"),
                        rx.el.p(alerta["desc"], class_name="text-xs text-gray-500"),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-start gap-3 p-3 rounded-xl border border-gray-100 bg-white shadow-sm mb-3",
                )
            ),
            class_name="flex flex-col max-h-[300px] overflow-y-auto pr-2",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )


def grafico_estado_catalogo() -> rx.Component:
    """Gráfico de Dona: Estado del catálogo."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Estado del Catálogo", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Distribución actual de ejemplares", class_name="text-sm text-gray-500"),
            class_name="mb-4",
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=BibliotecaDashboardState.chart_estado_catalogo,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                inner_radius="60%",
                outer_radius="80%",
                padding_angle=5,
                stroke="none",
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.legend(vertical_align="bottom", height=36),
            height=250,
            width="100%",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )


def grafico_evolucion_prestamos() -> rx.Component:
    """Gráfico de Líneas: Evolución de préstamos."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Evolución de Préstamos", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Tendencia histórica por mes", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(horizontal=True, vertical=False, class_name="opacity-20"),
            rx.recharts.x_axis(data_key="mes", axis_line=False, tick_line=False),
            rx.recharts.y_axis(axis_line=False, tick_line=False),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.line(
                data_key="prestamos",
                type_="monotone",
                stroke="#3b82f6",
                stroke_width=3,
                dot={"r": 4, "fill": "#3b82f6", "strokeWidth": 0},
                active_dot={"r": 6, "strokeWidth": 0},
            ),
            data=BibliotecaDashboardState.chart_evolucion_prestamos,
            height=300,
            width="100%",
            margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm lg:col-span-2",
    )


def grafico_top_libros() -> rx.Component:
    """Gráfico de Barras horizontales: Top 10 libros."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Libros Más Solicitados", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Top 10 material con mayor rotación", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(horizontal=False, vertical=True, class_name="opacity-20"),
            rx.recharts.x_axis(type_="number", axis_line=False, tick_line=False),
            rx.recharts.y_axis(data_key="titulo", type_="category", width=150, axis_line=False, tick_line=False, custom_attrs={"fontSize": "11px"}),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.bar(
                data_key="prestamos",
                fill="#22c55e",
                radius=[0, 4, 4, 0],
                bar_size=15,
            ),
            data=BibliotecaDashboardState.chart_top_libros,
            layout="vertical",
            height=350,
            width="100%",
            margin={"top": 10, "right": 10, "left": 0, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm lg:col-span-2",
    )


def grafico_lectores_carrera() -> rx.Component:
    """Gráfico de Barras verticales: Lectores por carrera."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Lectores por Carrera", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Distribución de usuarios activos", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(horizontal=True, vertical=False, class_name="opacity-20"),
            rx.recharts.x_axis(data_key="carrera", axis_line=False, tick_line=False, tick=False),
            rx.recharts.y_axis(axis_line=False, tick_line=False),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.bar(
                data_key="lectores",
                fill="#8b5cf6",
                radius=[4, 4, 0, 0],
            ),
            data=BibliotecaDashboardState.chart_lectores_carrera,
            height=300,
            width="100%",
            margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )


def grafico_prestamos_facultad() -> rx.Component:
    """Gráfico de Barras agrupadas: Préstamos por facultad."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Préstamos por Facultad", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Estado de préstamos agrupado por facultad", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(horizontal=True, vertical=False, class_name="opacity-20"),
            rx.recharts.x_axis(data_key="facultad", axis_line=False, tick_line=False, custom_attrs={"fontSize": "11px"}),
            rx.recharts.y_axis(axis_line=False, tick_line=False),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.legend(vertical_align="top", height=36),
            rx.recharts.bar(data_key="Activos", fill="#3b82f6", radius=[4, 4, 0, 0]),
            rx.recharts.bar(data_key="Devueltos", fill="#22c55e", radius=[4, 4, 0, 0]),
            rx.recharts.bar(data_key="Vencidos", fill="#ef4444", radius=[4, 4, 0, 0]),
            data=BibliotecaDashboardState.chart_prestamos_facultad,
            height=350,
            width="100%",
            margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm lg:col-span-2",
    )


def grafico_tipo_usuario() -> rx.Component:
    """Gráfico de Pie: Distribución por tipo de usuario."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Distribución de Préstamos", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Por tipo de usuario", class_name="text-sm text-gray-500"),
            class_name="mb-4",
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=BibliotecaDashboardState.chart_tipo_usuario,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                outer_radius="80%",
                stroke="none",
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.legend(vertical_align="bottom", height=36),
            height=250,
            width="100%",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )


def grafico_material_categoria() -> rx.Component:
    """Gráfico de Barras: Material por Categoría (Alternativa a Treemap)."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Material por Categoría", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Préstamos agrupados por área", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(horizontal=True, vertical=False, class_name="opacity-20"),
            rx.recharts.x_axis(data_key="categoria", axis_line=False, tick_line=False, tick=False),
            rx.recharts.y_axis(axis_line=False, tick_line=False),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.bar(
                data_key="prestamos",
                fill="#f59e0b",
                radius=[4, 4, 0, 0],
            ),
            data=BibliotecaDashboardState.chart_material_categoria,
            height=300,
            width="100%",
            margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )


def grafico_tiempo_promedio() -> rx.Component:
    """Gráfico Comparativo: Tiempo Real vs Permitido."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Tiempo de Préstamo", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Promedio Real vs Permitido por categoría", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(horizontal=True, vertical=False, class_name="opacity-20"),
            rx.recharts.x_axis(data_key="categoria", axis_line=False, tick_line=False, custom_attrs={"fontSize": "11px"}),
            rx.recharts.y_axis(axis_line=False, tick_line=False),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.legend(vertical_align="top", height=36),
            rx.recharts.bar(data_key="real", fill="#ec4899", radius=[4, 4, 0, 0]),
            rx.recharts.bar(data_key="permitido", fill="#94a3b8", radius=[4, 4, 0, 0]),
            data=BibliotecaDashboardState.chart_tiempo_comparativo,
            height=300,
            width="100%",
            margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2",
    )


def grafico_uso_horario() -> rx.Component:
    """Heatmap simulado con grilla HTML."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Horas de Mayor Uso", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Tráfico de lectores en la biblioteca", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.el.div(
            # Cabecera de días
            rx.el.div(
                rx.el.div(class_name="w-12"),  # Espacio esquina
                rx.foreach(
                    BibliotecaDashboardState.heatmap_dias,
                    lambda dia: rx.el.div(dia, class_name="flex-1 text-center text-xs font-bold text-gray-500")
                ),
                class_name="flex w-full mb-2",
            ),
            # Filas de horas
            rx.foreach(
                BibliotecaDashboardState.heatmap_data,
                lambda fila: rx.el.div(
                    rx.el.div(fila.hora, class_name="w-12 text-xs font-medium text-gray-500 text-right pr-2"),
                    rx.foreach(
                        fila.celdas,
                        lambda celda: rx.el.div(
                            rx.el.div(
                                class_name="w-full h-full rounded-sm bg-blue-500 hover:opacity-100 transition-opacity",
                                style={"opacity": celda.opacity},
                                title=celda.valor + " lectores",
                            ),
                            class_name="flex-1 p-[2px] h-6",
                        )
                    ),
                    class_name="flex w-full items-center",
                )
            ),
            class_name="w-full flex flex-col",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm lg:col-span-2",
    )


def grafico_libros_retraso() -> rx.Component:
    """Gráfico de Barras horizontales: Top 10 libros con retraso."""
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Libros con Mayor Retraso", class_name="text-lg font-bold text-gray-900"),
            rx.el.p("Días acumulados de mora", class_name="text-sm text-gray-500"),
            class_name="mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(horizontal=False, vertical=True, class_name="opacity-20"),
            rx.recharts.x_axis(type_="number", axis_line=False, tick_line=False),
            rx.recharts.y_axis(data_key="titulo", type_="category", width=150, axis_line=False, tick_line=False, custom_attrs={"fontSize": "11px"}),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.bar(
                data_key="dias_retraso",
                fill="#ef4444",
                radius=[0, 4, 4, 0],
                bar_size=15,
            ),
            data=BibliotecaDashboardState.chart_libros_retraso,
            layout="vertical",
            height=300,
            width="100%",
            margin={"top": 10, "right": 10, "left": 0, "bottom": 0},
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm lg:col-span-2",
    )


def biblioteca_executive_dashboard() -> rx.Component:
    """Dashboard Ejecutivo Completo de Biblioteca."""
    return rx.el.div(
        # Fila 1: KPIs Principales
        rx.el.div(
            kpi_card(
                "Total Libros", f"{BibliotecaDashboardState.total_libros}",
                f"{BibliotecaDashboardState.tend_libros}", True, "vs mes anterior",
                "book", "#003366"
            ),
            kpi_card(
                "Ejemplares Disp.", f"{BibliotecaDashboardState.total_ejemplares_disponibles}",
                f"{BibliotecaDashboardState.tend_disponibles}", False, "vs mes anterior",
                "circle-check", "#228B22"
            ),
            kpi_card(
                "Total Lectores", f"{BibliotecaDashboardState.total_lectores}",
                f"{BibliotecaDashboardState.tend_lectores}", True, "vs mes anterior",
                "users", "#3b82f6"
            ),
            kpi_card(
                "Préstamos Activos", f"{BibliotecaDashboardState.prestamos_activos}",
                f"{BibliotecaDashboardState.tend_activos}", True, "vs mes anterior",
                "book-open", "#8b5cf6"
            ),
            kpi_card(
                "Préstamos Vencidos", f"{BibliotecaDashboardState.prestamos_vencidos}",
                f"{BibliotecaDashboardState.tend_vencidos}", False, "vs mes anterior",
                "triangle-alert", "#ef4444"
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6",
        ),
        
        # Fila 2: KPIs Secundarios
        rx.el.div(
            kpi_card(
                "Devoluciones Día", f"{BibliotecaDashboardState.devoluciones_dia}",
                f"{BibliotecaDashboardState.tend_devoluciones}", True, "vs mes anterior",
                "undo-2", "#14b8a6"
            ),
            kpi_card(
                "En Mantenimiento", f"{BibliotecaDashboardState.libros_mantenimiento}",
                f"{BibliotecaDashboardState.tend_mantenimiento}", False, "vs mes anterior",
                "wrench", "#f59e0b"
            ),
            kpi_card(
                "Ocupación Catálogo", f"{BibliotecaDashboardState.ocupacion_catalogo}%",
                f"{BibliotecaDashboardState.tend_ocupacion}", True, "vs mes anterior",
                "pie-chart", "#ec4899"
            ),
            kpi_card(
                "Tiempo Promedio", f"{BibliotecaDashboardState.tiempo_promedio_prestamo} d",
                f"{BibliotecaDashboardState.tend_tiempo}", True, "vs mes anterior",
                "clock", "#64748b"
            ),
            kpi_card(
                "Morosidad", f"{BibliotecaDashboardState.indice_morosidad}%",
                f"{BibliotecaDashboardState.tend_morosidad}", False, "vs mes anterior",
                "circle-alert", "#f43f5e"
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6",
        ),
        
        # Fila 3: Gráficos de Estado y Alertas
        rx.el.div(
            grafico_estado_catalogo(),
            grafico_tipo_usuario(),
            panel_alertas(),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6",
        ),
        
        # Fila 4: Evolución y Lectores
        rx.el.div(
            grafico_evolucion_prestamos(),
            grafico_lectores_carrera(),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6",
        ),
        
        # Fila 5: Top Libros y Préstamos por Facultad
        rx.el.div(
            grafico_top_libros(),
            grafico_prestamos_facultad(),
            class_name="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6",
        ),
        
        # Fila 6: Tiempo Promedio y Material por Categoría
        rx.el.div(
            grafico_tiempo_promedio(),
            grafico_material_categoria(),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6",
        ),
        
        # Fila 7: HeatMap y Top Libros con Retraso
        rx.el.div(
            grafico_uso_horario(),
            grafico_libros_retraso(),
            class_name="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6",
        ),
    )
