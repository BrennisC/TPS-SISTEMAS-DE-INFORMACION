import reflex as rx
from ..states.recaudacion_state import RecaudacionState


def stat_card(label: str, value: str, subtext: str = "", icon: str = "wallet", color: str = "blue") -> rx.Component:
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


def chart_bar_recaudacion_por_año() -> rx.Component:
    """Gráfico de barras: Recaudación por año"""
    return rx.el.div(
        rx.el.h3(
            "Recaudación por Año",
            class_name="text-lg font-bold text-gray-900 mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="monto",
                fill="#10b981",
                name="Monto (S/)",
            ),
            rx.recharts.x_axis(data_key="año"),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            data=RecaudacionState.recaudacion_por_año,
            height=300,
            margin={"top": 5, "right": 30, "left": 0, "bottom": 5},
        ),
        class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def chart_pie_recaudacion_por_colegio() -> rx.Component:
    """Gráfico pastel: Recaudación por tipo de colegio"""
    return rx.el.div(
        rx.el.h3(
            "Recaudación por Tipo de Colegio",
            class_name="text-lg font-bold text-gray-900 mb-6",
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=RecaudacionState.recaudacion_por_colegio,
                data_key="monto",
                name_key="tipo",
                cx="50%",
                cy="50%",
                label=True,
                fill="#8884d8",
            ),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            height=350,
        ),
        class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def chart_bar_recaudacion_por_convocatoria() -> rx.Component:
    """Gráfico de barras: Recaudación por convocatoria"""
    return rx.el.div(
        rx.el.h3(
            "Recaudación por Convocatoria (Examen)",
            class_name="text-lg font-bold text-gray-900 mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="monto",
                fill="#3b82f6",
                name="Monto (S/)",
            ),
            rx.recharts.x_axis(data_key="convocatoria", angle=-45, height=80),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            data=RecaudacionState.recaudacion_por_convocatoria,
            height=350,
            margin={"top": 5, "right": 30, "left": 0, "bottom": 80},
        ),
        class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )


def chart_bar_top_carreras() -> rx.Component:
    """Gráfico de barras: Top 10 carreras por recaudación"""
    return rx.el.div(
        rx.el.h3(
            "Top 10 Carreras por Recaudación",
            class_name="text-lg font-bold text-gray-900 mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.bar(
                data_key="monto",
                fill="#f59e0b",
                name="Monto (S/)",
            ),
            rx.recharts.x_axis(data_key="carrera", angle=-45, height=100),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            data=RecaudacionState.recaudacion_por_carrera,
            height=400,
            margin={"top": 5, "right": 30, "left": 0, "bottom": 100},
        ),
        class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
    )



def recaudacion_view() -> rx.Component:
    """Vista principal del dashboard de recaudación con gráficos"""
    return rx.el.div(
        # Fila 1: Gráficos principales
        rx.el.div(
            # Gráfico de barras: Recaudación por año
            rx.el.div(
                chart_bar_recaudacion_por_año(),
                class_name="flex-1",
            ),
            # Gráfico pastel: Recaudación por tipo de colegio
            rx.el.div(
                chart_pie_recaudacion_por_colegio(),
                class_name="flex-1",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-7xl mx-auto mb-8",
        ),

        # Fila 2: Gráfico de barras por convocatoria
        rx.el.div(
            chart_bar_recaudacion_por_convocatoria(),
            class_name="max-w-7xl mx-auto mb-8",
        ),

        # Fila 3: Gráfico de top carreras
        rx.el.div(
            chart_bar_top_carreras(),
            class_name="max-w-7xl mx-auto mb-8",
        ),

        # Tabla de recaudación por convocatoria (detalles)
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Detalles por Convocatoria",
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
                                    "Postulantes",
                                    class_name="px-6 py-3 text-center text-sm font-bold text-gray-600 bg-gray-50",
                                ),
                                rx.el.th(
                                    "Monto Total",
                                    class_name="px-6 py-3 text-right text-sm font-bold text-gray-600 bg-gray-50",
                                ),
                                rx.el.th(
                                    "Promedio",
                                    class_name="px-6 py-3 text-right text-sm font-bold text-gray-600 bg-gray-50",
                                ),
                            ),
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                RecaudacionState.recaudacion_por_convocatoria,
                                lambda item: rx.el.tr(
                                    rx.el.td(
                                        rx.el.span(
                                            item["convocatoria"],
                                            class_name="px-6 py-3 font-semibold text-gray-900 bg-blue-50 inline-block rounded",
                                        ),
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            item["cantidad"],
                                            class_name="px-6 py-3 text-center text-gray-700 font-medium",
                                        ),
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            f"S/ {item['monto']}",
                                            class_name="px-6 py-3 text-right text-gray-900 font-bold text-green-600",
                                        ),
                                    ),
                                    rx.el.td(
                                        rx.el.span(
                                            f"S/ {item['promedio']}",
                                            class_name="px-6 py-3 text-right text-gray-700",
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
