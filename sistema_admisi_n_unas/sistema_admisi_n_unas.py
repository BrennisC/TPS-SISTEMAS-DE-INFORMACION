import reflex as rx
from sistema_admisi_n_unas.states.dashboard_state import DashboardState
from sistema_admisi_n_unas.states.postulantes_state import PostulantesState
from sistema_admisi_n_unas.components.sidebar import sidebar
from sistema_admisi_n_unas.components.stats_card import stats_card
from sistema_admisi_n_unas.components.chart_utils import TOOLTIP_PROPS, chart_legend
from sistema_admisi_n_unas.components.inscripcion_form import inscripcion_form
from sistema_admisi_n_unas.components.postulantes_table import postulantes_table
from sistema_admisi_n_unas.components.page_layout import page_header
from sistema_admisi_n_unas.components.examen import examen_view
from sistema_admisi_n_unas.components.resultados import resultados_view
from sistema_admisi_n_unas.components.feedback import feedback_view


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
                    on_click=rx.redirect("/inscripcion")
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


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                dashboard_header(),
                # Stats Grid
                rx.el.div(
                    stats_card(
                        "Postulantes",
                        f"{PostulantesState.total_postulantes}",
                        "users",
                        "blue",
                        "Total inscritos 2024-II",
                    ),
                    stats_card(
                        "Ingresantes",
                        f"{PostulantesState.admitted_count}",
                        "user-check",
                        "green",
                        "Vacantes cubiertas al 85%",
                    ),
                    stats_card(
                        "Promedio General",
                        f"{PostulantesState.general_avg:.1f}",
                        "trending-up",
                        "amber",
                        "Supera el 13.8 del 2023",
                    ),
                    stats_card(
                        "Carrera Top",
                        f"{PostulantesState.top_career}",
                        "award",
                        "purple",
                        "Mayor número de postulantes",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
                ),
                # Content Grid
                rx.el.div(
                    scores_chart(),
                    recent_activity(),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
                ),
                class_name="max-w-7xl mx-auto",
            ),
            class_name="flex-1 bg-gray-50/50 p-6 md:p-10 overflow-y-auto",
        ),
        class_name="flex min-h-screen bg-white font-['Inter']",
    )


def inscripcion_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
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
        class_name="flex min-h-screen bg-white font-['Inter']",
    )


def postulantes_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
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
        class_name="flex min-h-screen bg-white font-['Inter']",
    )


def examen_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
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
        class_name="flex min-h-screen bg-white font-['Inter']",
    )


def resultados_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
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
        class_name="flex min-h-screen bg-white font-['Inter']",
    )


def retroalimentacion_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
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
        class_name="flex min-h-screen bg-white font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    on_load=PostulantesState.cargar_datos,
)
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
app.add_page(resultados_page, route="/resultados")
app.add_page(retroalimentacion_page, route="/retroalimentacion")
