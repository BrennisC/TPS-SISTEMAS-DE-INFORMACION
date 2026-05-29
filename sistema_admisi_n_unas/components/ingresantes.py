import reflex as rx
from ..states.ingresantes_state import IngresantesState


def stat_card(label: str, value: str, subtext: str = "", icon: str = "users", color: str = "blue") -> rx.Component:
    """Tarjeta de estadística"""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 text-{color}-600"),
            class_name=f"p-3 rounded-lg bg-{color}-100",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-600"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
            rx.el.p(subtext, class_name="text-xs text-gray-500 mt-1") if subtext else rx.el.span(),
            class_name="flex flex-col flex-1",
        ),
        class_name="flex items-start gap-4 bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def chart_bar_ingresantes_por_convocatoria() -> rx.Component:
    """Gráfico de barras: Ingresantes por convocatoria (2023-I a 2026-I)"""
    return rx.el.div(
        rx.el.h3(
            "Ingresantes por Período de Examen (2023-I a 2026-I)",
            class_name="text-lg font-bold text-gray-900 mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="cantidad",
                fill="#06b6d4",
                name="Ingresantes",
            ),
            rx.recharts.x_axis(data_key="convocatoria", angle=-45, height=80),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            data=IngresantesState.ingresantes_por_convocatoria,
            height=350,
            margin={"top": 5, "right": 30, "left": 0, "bottom": 80},
        ),
        class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def chart_line_ingresantes_por_año() -> rx.Component:
    """Gráfico de línea: Tendencia de ingresantes por año"""
    return rx.el.div(
        rx.el.h3(
            "Tendencia de Ingresantes por Año",
            class_name="text-lg font-bold text-gray-900 mb-6",
        ),
        rx.recharts.line_chart(
            rx.recharts.line(
                data_key="cantidad",
                stroke="#8b5cf6",
                name="Ingresantes",
                stroke_width=3,
                dot={"fill": "#8b5cf6", "r": 6},
            ),
            rx.recharts.x_axis(data_key="año"),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            data=IngresantesState.ingresantes_por_año,
            height=300,
            margin={"top": 5, "right": 30, "left": 0, "bottom": 5},
        ),
        class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def chart_pie_ingresantes_por_colegio() -> rx.Component:
    """Gráfico pastel: Distribución de ingresantes por tipo de colegio"""
    return rx.el.div(
        rx.el.h3(
            "Ingresantes por Tipo de Colegio",
            class_name="text-lg font-bold text-gray-900 mb-6",
        ),

        rx.recharts.pie_chart(
            rx.recharts.pie(
                rx.foreach(
                    IngresantesState.ingresantes_por_colegio,
                    lambda item: rx.recharts.cell(fill=item["fill"]),
                ),

                data=IngresantesState.ingresantes_por_colegio,
                data_key="cantidad",
                name_key="tipo",
                cx="50%",
                cy="50%",
                label=True,
            ),

            rx.recharts.tooltip(),
            rx.recharts.legend(),
            height=350,
        ),

        class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def chart_bar_ingresantes_por_carrera() -> rx.Component:
    """Gráfico de barras: Top carreras con más ingresantes"""
    return rx.el.div(
        rx.el.h3(
            "Top Carreras por Ingresantes",
            class_name="text-lg font-bold text-gray-900 mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="cantidad",
                fill="#f59e0b",
                name="Ingresantes",
            ),
            rx.recharts.x_axis(data_key="carrera", angle=-45, height=100),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            data=IngresantesState.ingresantes_por_carrera,
            height=400,
            margin={"top": 5, "right": 30, "left": 0, "bottom": 100},
        ),
        class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def ingresantes_view() -> rx.Component:
    """Vista principal del dashboard de ingresantes"""
    return rx.el.div(
        # Botón para cargar datos
        rx.el.div(
            rx.el.button(
                "Cargar Datos de Ingresantes",
                on_click=IngresantesState.cargar_datos_ingresantes,
                class_name="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium mb-6",
            ),
            class_name="max-w-7xl mx-auto",
        ),
        
        # Tarjetas de estadísticas principales
        rx.el.div(
            stat_card(
                "Total Ingresantes",
                f"{IngresantesState.total_ingresantes}",
                "Desde 2023-I a 2026-I",
                "users",
                "green"
            ),
            stat_card(
                "Año Mayor Ingreso",
                IngresantesState.año_mayor_ingreso,
                "Período con más ingresantes",
                "trend-up",
                "blue"
            ),
            stat_card(
                "Carrera Destacada",
                IngresantesState.carrera_mas_ingresantes,
                "Carrera con más ingresantes",
                "graduation-cap",
                "purple"
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto mb-8",
        ),
        
        # Fila 1: Gráficos principales
        rx.el.div(
            # Gráfico de línea: Tendencia por año
            rx.el.div(
                chart_line_ingresantes_por_año(),
                class_name="flex-1",
            ),
            # Gráfico pastel: Por tipo de colegio
            rx.el.div(
                chart_pie_ingresantes_por_colegio(),
                class_name="flex-1",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-7xl mx-auto mb-8",
        ),
        
        # Fila 2: Gráfico de barras por convocatoria
        rx.el.div(
            chart_bar_ingresantes_por_convocatoria(),
            class_name="max-w-7xl mx-auto mb-8",
        ),
        
        # Fila 3: Top carreras
        rx.el.div(
            chart_bar_ingresantes_por_carrera(),
            class_name="max-w-7xl mx-auto mb-8",
        ),
        
        # Tabla detallada por convocatoria
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Detalles de Ingresantes por Convocatoria",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Convocatoria",
                                    class_name="px-6 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50",
                                ),
                                rx.el.th(
                                    "Cantidad de Ingresantes",
                                    class_name="px-6 py-3 text-center text-sm font-bold text-gray-600 bg-gray-50",
                                ),
                            ),
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                IngresantesState.ingresantes_por_convocatoria,
                                lambda item: rx.el.tr(
                                    rx.el.td(
                                        rx.el.span(
                                            item["convocatoria"],
                                            class_name="px-6 py-3 font-semibold text-gray-900 bg-cyan-50 inline-block rounded",
                                        ),
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            item["cantidad"],
                                            class_name="px-6 py-3 text-center text-gray-900 font-bold text-cyan-600",
                                        ),
                                    ),
                                    class_name="border-b border-gray-100 hover:bg-gray-50",
                                ),
                            ),
                        ),
                        class_name="w-full",
                    ),
                    class_name="overflow-x-auto",
                ),
                class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm max-w-7xl mx-auto",
            ),
            class_name="mb-8",
        ),
        
        class_name="space-y-6 pb-8",
    )
