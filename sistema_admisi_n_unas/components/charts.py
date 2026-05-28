import reflex as rx

from ..states.dashboard_state import DashboardState
from .chart_utils import TOOLTIP_PROPS, chart_legend


def grafico_postulantes_vs_ingresantes():
    """Gráfico mejorado de Postulantes vs Ingresantes por Carrera."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Postulantes vs Ingresantes por Carrera",
                class_name="text-sm font-bold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(class_name="h-3 w-3 rounded-full bg-[#228B22] inline-block mr-1"),
                    rx.el.span("Postulantes", class_name="text-xs text-gray-500 mr-4"),
                ),
                rx.el.div(
                    rx.el.span(class_name="h-3 w-3 rounded-full bg-[#FFB020] inline-block mr-1"),
                    rx.el.span("Ingresantes", class_name="text-xs text-gray-500"),
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        # Chart
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                vertical=False,
                class_name="opacity-30"
            ),
            rx.recharts.x_axis(
                data_key="carrera",
                custom_attrs={"fontSize": "9px", "fontWeight": "500"},
                axis_line=False,
                tick_line=False,
            ),
            rx.recharts.y_axis(
                custom_attrs={"fontSize": "11px", "fontWeight": "500"},
                axis_line=False,
                tick_line=False,
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "white",
                    "border": "1px solid #e5e7eb",
                    "borderRadius": "8px",
                    "padding": "8px 12px",
                    "fontSize": "12px",
                    "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                },
                item_style={"fontWeight": "600"},
            ),
            rx.recharts.legend(
                wrapper_style={"fontSize": "12px", "paddingTop": "10px"},
            ),
            rx.recharts.bar(
                data_key="Postulantes",
                fill="#228B22",
                radius=[4, 4, 0, 0],
                bar_size=20,
                animation_duration=800,
                animation_easing="ease-out",
            ),
            rx.recharts.bar(
                data_key="Ingresantes",
                fill="#FFB020",
                radius=[4, 4, 0, 0],
                bar_size=20,
                animation_duration=800,
                animation_easing="ease-out",
            ),
            data=DashboardState.chart_postulantes_vs_ingresantes,
            height=250,
            width="100%",
            margin={"top": 10, "right": 10, "left": -10, "bottom": 0},
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2 hover:shadow-md transition-shadow",
    )


def grafico_rendimiento_areas():
    """Gráfico mejorado de Rendimiento Promedio por Facultad con gradiente."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Rendimiento Promedio por Facultad",
                class_name="text-sm font-bold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.span("Área", class_name="text-xs text-[#228B22] font-medium"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        # Chart
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                vertical=False,
                class_name="opacity-20"
            ),
            rx.recharts.x_axis(
                data_key="area",
                custom_attrs={"fontSize": "10px", "fontWeight": "500"},
                axis_line=False,
                tick_line=False,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs={"fontSize": "11px"},
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "white",
                    "border": "1px solid #e5e7eb",
                    "borderRadius": "8px",
                    "padding": "8px 12px",
                    "fontSize": "12px",
                },
            ),
            rx.recharts.area(
                type_="monotone",
                data_key="avg_score",
                stroke="#228B22",
                stroke_width=2.5,
                fill="#228B22",
                fill_opacity=0.25,
                animation_duration=1000,
                animation_easing="ease-out",
            ),
            data=DashboardState.chart_rendimiento_areas,
            height=220,
            width="100%",
            margin={"top": 10, "right": 10, "left": -10, "bottom": 0},
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2 hover:shadow-md transition-shadow",
    )


def grafico_evolucion_historica():
    """Gráfico mejorado de Tendencia de Postulantes con gradiente azul."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Tendencia de Postulantes por Convocatoria",
                class_name="text-sm font-bold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.span(class_name="w-8 h-1 rounded bg-[#0288D1] inline-block mr-1"),
                rx.el.span("Postulantes", class_name="text-xs text-gray-500"),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        # Chart
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                vertical=False,
                class_name="opacity-20"
            ),
            rx.recharts.x_axis(
                data_key="year",
                custom_attrs={"fontSize": "11px", "fontWeight": "600"},
                axis_line=False,
                tick_line=False,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs={"fontSize": "11px"},
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "#0288D1",
                    "color": "white",
                    "border": "none",
                    "borderRadius": "6px",
                    "padding": "6px 10px",
                    "fontSize": "12px",
                    "fontWeight": "600",
                },
                cursor={"stroke": "#0288D1", "strokeWidth": 1},
            ),
            rx.recharts.area(
                type_="monotone",
                data_key="Postulantes",
                stroke="#0288D1",
                stroke_width=2.5,
                fill="#0288D1",
                fill_opacity=0.25,
                animation_duration=1000,
                animation_easing="ease-out",
            ),
            data=DashboardState.chart_evolucion_historica,
            height=220,
            width="100%",
            margin={"top": 10, "right": 10, "left": -10, "bottom": 0},
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 hover:shadow-md transition-shadow",
    )


def grafico_distribucion_colegios():
    """Gráfico mejorado de Distribución de Colegio con leyenda mejorada."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Procedencia de Postulantes",
                class_name="text-sm font-bold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.span("Tipo de Colegio", class_name="text-xs text-gray-400"),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        # Chart with center label
        rx.el.div(
            rx.el.div(
                rx.recharts.pie_chart(
                    rx.recharts.pie(
                        data=DashboardState.chart_genero,
                        data_key="value",
                        name_key="name",
                        inner_radius=55,
                        outer_radius=75,
                        padding_angle=3,
                        data_legend=True,
                        animation_begin=0,
                        animation_duration=800,
                        animation_easing="ease-out",
                    ),
                    rx.recharts.graphing_tooltip(
                        content_style={
                            "backgroundColor": "white",
                            "border": "1px solid #e5e7eb",
                            "borderRadius": "8px",
                            "padding": "8px 12px",
                            "fontSize": "12px",
                        },
                    ),
                    height=160,
                    width="100%",
                ),
                class_name="w-1/2",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.tbody(
                        rx.foreach(
                            DashboardState.chart_genero,
                            lambda item: rx.el.tr(
                                rx.el.td(
                                    rx.el.span(
                                        class_name="h-3 w-3 rounded-full inline-block mr-2",
                                        style={"backgroundColor": item["fill"]},
                                    ),
                                    class_name="w-3",
                                ),
                                rx.el.td(
                                    item["name"],
                                    class_name="text-sm font-medium text-gray-700 pr-4",
                                ),
                                rx.el.td(
                                    item["value"],
                                    class_name="text-sm font-bold text-gray-900",
                                ),
                                rx.el.td(
                                    rx.el.span("%", class_name="text-xs text-gray-400"),
                                    class_name="text-xs text-gray-400",
                                ),
                                class_name="hover:bg-gray-50 transition-colors",
                            ),
                        ),
                    ),
                    class_name="table-auto",
                ),
                class_name="w-1/2 flex flex-col justify-center",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 hover:shadow-md transition-shadow",
    )


def grafico_distribucion_puntajes():
    """Gráfico mejorado de Distribución de Puntajes con colores gradientes."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Distribución de Puntajes (0-20)",
                class_name="text-sm font-bold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.span(
                    DashboardState.chart_puntajes_rango.length().to_string()
                    + " total",
                    class_name="text-xs text-gray-500 font-medium",
                ),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        # Chart
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                vertical=False,
                class_name="opacity-20"
            ),
            rx.recharts.x_axis(
                data_key="rango",
                custom_attrs={"fontSize": "11px", "fontWeight": "600"},
                axis_line=False,
                tick_line=False,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs={"fontSize": "11px"},
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "white",
                    "border": "1px solid #e5e7eb",
                    "borderRadius": "8px",
                    "padding": "8px 12px",
                    "fontSize": "12px",
                },
            ),
            rx.recharts.bar(
                data_key="cantidad",
                fill="#228B22",
                radius=[4, 4, 0, 0],
                bar_size=30,
                animation_duration=800,
                animation_easing="ease-out",
            ),
            data=DashboardState.chart_puntajes_rango,
            height=250,
            width="100%",
            margin={"top": 10, "right": 10, "left": -10, "bottom": 0},
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 hover:shadow-md transition-shadow",
    )


def grafico_promedio_convocatoria():
    """Gráfico mejorado de Promedio de Puntajes con gradiente verde."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Promedio de Puntajes por Convocatoria",
                class_name="text-sm font-bold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.span(
                    "Convocatorias: "
                    + DashboardState.chart_promedio_convocatoria.length().to_string(),
                    class_name="text-xs text-gray-400",
                ),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        # Chart
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                vertical=False,
                class_name="opacity-20"
            ),
            rx.recharts.x_axis(
                data_key="convocatoria",
                custom_attrs={"fontSize": "11px", "fontWeight": "600"},
                axis_line=False,
                tick_line=False,
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs={"fontSize": "11px"},
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "white",
                    "border": "1px solid #e5e7eb",
                    "borderRadius": "8px",
                    "padding": "8px 12px",
                    "fontSize": "12px",
                },
            ),
            rx.recharts.area(
                type_="monotone",
                data_key="avg_score",
                stroke="#228B22",
                stroke_width=2.5,
                fill="#228B22",
                fill_opacity=0.25,
                dot={"fill": "#228B22", "strokeWidth": 2, "r": 4},
                active_dot={"r": 6, "fill": "#003366"},
                animation_duration=1000,
                animation_easing="ease-out",
            ),
            data=DashboardState.chart_promedio_convocatoria,
            height=250,
            width="100%",
            margin={"top": 10, "right": 20, "left": -10, "bottom": 0},
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2 hover:shadow-md transition-shadow",
    )


def grafico_top_carreras_puntaje():
    """Gráfico mejorado de Top Carreras por Puntaje con barras horizontales."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Top Carreras por Puntaje Promedio",
                class_name="text-sm font-bold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.span("Top 5", class_name="text-xs text-[#0288D1] font-medium bg-blue-50 px-2 py-1 rounded"),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        # Chart
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
                horizontal=True,
                vertical=False,
                class_name="opacity-20",
            ),
            rx.recharts.x_axis(
                type_="number",
                axis_line=False,
                tick_line=False,
                custom_attrs={"fontSize": "11px"},
            ),
            rx.recharts.y_axis(
                data_key="carrera",
                type_="category",
                custom_attrs={"fontSize": "10px", "fontWeight": "500"},
                width=120,
            ),
            rx.recharts.graphing_tooltip(
                content_style={
                    "backgroundColor": "white",
                    "border": "1px solid #e5e7eb",
                    "borderRadius": "8px",
                    "padding": "8px 12px",
                    "fontSize": "12px",
                },
            ),
            rx.recharts.bar(
                data_key="avg_score",
                fill="#0288D1",
                radius=[0, 4, 4, 0],
                bar_size=25,
                animation_duration=800,
                animation_easing="ease-out",
            ),
            layout="vertical",
            data=DashboardState.chart_top_carreras_puntaje,
            height=220,
            width="100%",
            margin={"top": 5, "right": 10, "left": -20, "bottom": 0},
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2 hover:shadow-md transition-shadow",
    )


def chart_summary_card(icon: str, title: str, value: str, subtitle: str, color: str) -> rx.Component:
    """Componente de tarjeta resumen paraDashboard."""
    color_map = {
        "green": "bg-green-50 text-green-600 border-green-100",
        "blue": "bg-blue-50 text-blue-600 border-blue-100",
        "amber": "bg-amber-50 text-amber-600 border-amber-100",
        "purple": "bg-purple-50 text-purple-600 border-purple-100",
    }
    active_color = color_map.get(color, color_map["green"])
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-5 w-5 {active_color.split()[1]}"),
            class_name=f"p-3 rounded-xl {active_color}",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-xs font-medium text-gray-500"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(subtitle, class_name="text-xs text-gray-400"),
        ),
        class_name="flex items-start gap-3 bg-white rounded-xl border border-gray-100 p-4 shadow-sm hover:shadow-md transition-shadow",
    )
