import reflex as rx

from sistema_admisi_n_unas.components.chart_utils import TOOLTIP_PROPS, chart_legend
from sistema_admisi_n_unas.components.biblioteca import biblioteca_view
from sistema_admisi_n_unas.components.examen import examen_view
from sistema_admisi_n_unas.components.feedback import feedback_view
from sistema_admisi_n_unas.components.ingresantes import ingresantes_view
from sistema_admisi_n_unas.components.inscripcion_form import inscripcion_form
from sistema_admisi_n_unas.components.login_form import login_form
from sistema_admisi_n_unas.components.page_layout import page_header
from sistema_admisi_n_unas.components.postulantes_table import postulantes_table
from sistema_admisi_n_unas.components.recaudacion import recaudacion_view
from sistema_admisi_n_unas.components.resultados import resultados_view
from sistema_admisi_n_unas.components.sidebar import mobile_sidebar, sidebar
from sistema_admisi_n_unas.components.stats_card import stats_card
from sistema_admisi_n_unas.components.tesoreria import tesoreria_view
from sistema_admisi_n_unas.states.auth_state import AuthState
from sistema_admisi_n_unas.states.biblioteca_state import BibliotecaState
from sistema_admisi_n_unas.states.dashboard_state import DashboardState
from sistema_admisi_n_unas.states.feedback_state import FeedbackState
from sistema_admisi_n_unas.states.ingresantes_state import IngresantesState
from sistema_admisi_n_unas.states.postulantes_state import PostulantesState
from sistema_admisi_n_unas.states.recaudacion_state import RecaudacionState
from sistema_admisi_n_unas.states.resultados_state import ResultadosState
from sistema_admisi_n_unas.states.tesoreria_state import TesoreriaState

from .components.charts import (
    grafico_distribucion_colegios,
    grafico_distribucion_puntajes,
    grafico_evolucion_historica,
    grafico_postulantes_vs_ingresantes,
    grafico_promedio_convocatoria,
    grafico_rendimiento_areas,
    grafico_top_carreras_puntaje,
)
from .components.tables import panel_preguntas_errores, tabla_ultimos_registrados


def mobile_header() -> rx.Component:
    """Header con botón hamburguesa para móvil"""
    return rx.el.div(
        rx.el.button(
            rx.icon("menu", class_name="h-6 w-6 text-slate-700"),
            on_click=DashboardState.toggle_mobile_menu,
            class_name="md:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors",
        ),
        class_name="md:hidden flex items-center gap-4 p-4 bg-white border-b border-gray-200",
    )


def dashboard_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Panel de Control",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Resumen general del proceso de admisión actual",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("download", class_name="h-4 w-4 mr-2"),
                    "Reporte PDF",
                    class_name="flex items-center px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-4 w-4 mr-2"),
                    "Nueva Inscripción",
                    class_name="flex items-center px-4 py-2 bg-[#228B22] rounded-xl text-sm font-semibold text-white hover:bg-[#1a6b1a] transition-colors shadow-sm",
                    on_click=rx.redirect("/inscripcion"),
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 w-full",
        ),
        class_name="mb-8",
    )


def scores_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Puntajes Promedio por Área",
                    class_name="text-lg font-bold text-[#003366]",
                ),
                rx.el.p(
                    "Basado en el último simulacro realizado",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            chart_legend("#228B22", "Puntaje Promedio"),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                horizontal=True, vertical=False, class_name="opacity-20"
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="area",
                axis_line=False,
                tick_line=False,
                custom_attrs={"fontSize": "12px", "fontWeight": "500"},
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs={"fontSize": "12px", "fontWeight": "500"},
            ),
            rx.recharts.bar(
                data_key="avg_score",
                fill="#228B22",
                radius=[6, 6, 0, 0],
                bar_size=40,
            ),
            data=DashboardState.area_scores,
            height=300,
            width="100%",
            margin={"top": 10, "right": 10, "left": -20, "bottom": 0},
            class_name="[&_.recharts-tooltip-item-value]:!text-[#003366] [&_.recharts-tooltip-item-value]:!font-bold",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2",
    )


def recent_activity() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Carreras con Mayor Demanda",
            class_name="text-lg font-bold text-[#003366] mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        "1",
                        class_name="w-8 h-8 rounded-lg bg-blue-50 text-[#003366] flex items-center justify-center font-bold text-xs",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Ingeniería Forestal",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Facultad de Rec. Nat. Renovables",
                            class_name="text-xs text-gray-500",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.span(
                    "452 post.",
                    class_name="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded-md",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        "2",
                        class_name="w-8 h-8 rounded-lg bg-green-50 text-[#228B22] flex items-center justify-center font-bold text-xs",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Agronomía",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Facultad de Agronomía",
                            class_name="text-xs text-gray-500",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.span(
                    "389 post.",
                    class_name="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded-md",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        "3",
                        class_name="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center font-bold text-xs",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Admin. de Empresas",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Facultad de C. Económicas",
                            class_name="text-xs text-gray-500",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.span(
                    "312 post.",
                    class_name="text-xs font-bold text-amber-600 bg-amber-50 px-2 py-1 rounded-md",
                ),
                class_name="flex items-center justify-between",
            ),
            class_name="flex flex-col gap-6",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm",
    )


def login_view() -> rx.Component:
    return rx.el.div(
        login_form(),
        class_name="w-full max-w-md",
    )


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.main(
            rx.el.div(
                login_view(),
                class_name="flex items-center justify-center min-h-screen bg-gray-50 p-6",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen bg-white font-['Inter']",
    )


def require_auth(content: rx.Component) -> rx.Component:
    return rx.cond(AuthState.is_authenticated, content, login_page())


def index() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        dashboard_header(),
                        # 1. FILA SUPERIOR: Cards de control con datos reales del CSV
                        rx.el.div(
                            stats_card(
                                "Total Postulantes",
                                f"{DashboardState.total_postulantes}",
                                "Registrados en CSV",
                                "users",
                                "#228B22",
                            ),
                            stats_card(
                                "Total Ingresantes",
                                f"{DashboardState.admitted_count}",
                                "Vacantes validadas",
                                "user-check",
                                "#228B22",
                            ),
                            stats_card(
                                "Total Recaudado",
                                f"S/. {DashboardState.total_recaudado:,.2f}",
                                f"Estatal: {DashboardState.total_estatal} | Priv.: {DashboardState.total_privado}",
                                "circle-dollar-sign",
                                "#228B22",
                            ),
                            stats_card(
                                "Carrera Más Demandada",
                                f"{DashboardState.top_career}",
                                "Mayor N° de registros",
                                "graduation-cap",
                                "#003366",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
                        ),
                        # 2. SEGUNDA FILA: Calibrador Promedio + Gráfico Barras Doble
                        rx.el.div(
                            rx.el.div(
                                rx.el.h3(
                                    "Rendimiento General del Examen",
                                    class_name="text-sm font-bold text-gray-700 mb-4",
                                ),
                                rx.el.div(
                                    rx.el.h1(
                                        rx.cond(
                                            DashboardState.general_avg > 0,
                                            f"{DashboardState.general_avg:.2f}",
                                            "0.00",
                                        ),
                                        class_name="text-4xl font-extrabold text-gray-900",
                                    ),
                                    rx.el.p(
                                        "Promedio General Real (Data CSV)",
                                        class_name="text-xs text-gray-500 mt-1",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-48 border-2 border-dashed border-gray-100 rounded-xl",
                                ),
                                class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1",
                            ),
                            grafico_postulantes_vs_ingresantes(),
                            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6",
                        ),
                        # 3. TERCERA FILA (¡AÑADIDA!): Evolución de Años + Gráfico de Torta de Colegios
                        rx.el.div(
                            grafico_evolucion_historica(),
                            grafico_distribucion_colegios(),
                            recent_activity(),  # Mantiene tu componente lateral original
                            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6",
                        ),
                        # 4. CUARTA FILA: Áreas Analíticas + Top Errores Fijos
                        rx.el.div(
                            grafico_rendimiento_areas(),
                            panel_preguntas_errores(),
                            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6",
                        ),
                        # 5. QUINTA FILA: Análisis de puntajes
                        rx.el.div(
                            grafico_distribucion_puntajes(),
                            grafico_promedio_convocatoria(),
                            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6",
                        ),
                        rx.el.div(
                            grafico_top_carreras_puntaje(),
                            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6",
                        ),
                        # 6. SEXTA FILA: Tabla de alumnos del CSV
                        rx.el.div(
                            tabla_ultimos_registrados(),
                            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
                        ),
                        class_name="max-w-7xl mx-auto",
                    ),
                    class_name="flex-1 bg-gray-50/40 p-6 md:p-8 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def inscripcion_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Inscripción de Postulantes",
                            "Registra un nuevo postulante en el proceso de admisión 2024-II",
                            "user-plus",
                        ),
                        inscripcion_form(),
                        class_name="max-w-7xl mx-auto",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def postulantes_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Gestión de Postulantes",
                            "Administra y consulta a todos los postulantes registrados",
                            "users",
                        ),
                        postulantes_table(),
                        class_name="max-w-7xl mx-auto",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def examen_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Simulador de Examen",
                            "Practica con un examen de admisión simulado",
                            "file-pen",
                        ),
                        examen_view(),
                        class_name="max-w-7xl mx-auto",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def resultados_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Ranking de Resultados",
                            "Consulta el ranking ordenado de postulantes según puntaje",
                            "trophy",
                        ),
                        resultados_view(),
                        class_name="max-w-7xl mx-auto",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def retroalimentacion_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Retroalimentación y Apelaciones",
                            "Análisis de errores frecuentes y gestión de reclamos",
                            "message-square",
                        ),
                        feedback_view(),
                        class_name="max-w-7xl mx-auto",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def recaudacion_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Dashboard de Recaudación",
                            "Análisis de monto recaudado por examen, año y carrera",
                            "wallet",
                        ),
                        recaudacion_view(),
                        class_name="max-w-full",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def ingresantes_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Ingresantes por Período",
                            "Análisis de ingresantes desde 2023-I hasta 2026-I",
                            "bar-chart-3",
                        ),
                        ingresantes_view(),
                        class_name="max-w-full",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def tesoreria_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Tesorería",
                            "Validación de pagos y control operativo para el proceso de admisión",
                            "receipt",
                        ),
                        tesoreria_view(),
                        class_name="max-w-full",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


def biblioteca_page() -> rx.Component:
    return require_auth(
        rx.el.div(
            mobile_sidebar(),
            sidebar(),
            rx.el.div(
                mobile_header(),
                rx.el.main(
                    rx.el.div(
                        page_header(
                            "Biblioteca",
                            "Catálogo y préstamos iniciales vinculados al flujo académico",
                            "book-open",
                        ),
                        biblioteca_view(),
                        class_name="max-w-full",
                    ),
                    class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
                ),
                class_name="flex-1 flex flex-col",
            ),
            class_name="flex min-h-screen bg-white font-['Inter']",
        )
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    on_load=DashboardState.cargar_datos_csv,
)
app.add_page(login_page, route="/login")
app.add_page(
    inscripcion_page,
    route="/inscripcion",
    on_load=PostulantesState.cargar_datos,
)
app.add_page(
    postulantes_page,
    route="/postulantes",
    on_load=PostulantesState.cargar_datos,
)
app.add_page(examen_page, route="/examen")
app.add_page(
    resultados_page,
    route="/resultados",
    on_load=ResultadosState.cargar_resultados,
)
app.add_page(
    retroalimentacion_page,
    route="/retroalimentacion",
    on_load=FeedbackState.cargar_datos,
)
app.add_page(
    recaudacion_page,
    route="/recaudacion",
    on_load=RecaudacionState.cargar_datos_recaudacion,
)
app.add_page(
    ingresantes_page,
    route="/ingresantes",
    on_load=IngresantesState.cargar_datos_ingresantes,
)
app.add_page(
    tesoreria_page,
    route="/tesoreria",
    on_load=TesoreriaState.cargar_pagos,
)
app.add_page(
    biblioteca_page,
    route="/biblioteca",
    on_load=BibliotecaState.cargar_biblioteca,
)
