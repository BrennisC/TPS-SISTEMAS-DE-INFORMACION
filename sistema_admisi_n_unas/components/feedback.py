import reflex as rx
from sistema_admisi_n_unas.states.feedback_state import FeedbackState, Apelacion
from sistema_admisi_n_unas.components.chart_utils import TOOLTIP_PROPS


def stat_card_fb(label: str, value: str, color: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-5 w-5 text-{color}-600"),
            class_name=f"p-2.5 rounded-xl bg-{color}-50",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-xs font-medium text-gray-500"),
            rx.el.h3(value, class_name="text-xl font-bold text-gray-900"),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-3 bg-white rounded-2xl border border-gray-200 p-4 shadow-sm",
    )


def error_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Preguntas con Mayor Índice de Error",
                    class_name="text-lg font-bold text-[#003366]",
                ),
                rx.el.p(
                    "Porcentaje de respuestas incorrectas por pregunta",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.span(
                    class_name="w-3 h-3 inline-block mr-2 rounded-full bg-red-500"
                ),
                rx.el.span(
                    "% Error", class_name="text-sm font-medium text-gray-600"
                ),
                class_name="flex items-center",
            ),
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
                custom_attrs={"fontSize": "11px", "fontWeight": "500"},
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs={"fontSize": "11px", "fontWeight": "500"},
                unit="%",
            ),
            rx.recharts.bar(
                data_key="indice_error",
                fill="#EF4444",
                radius=[6, 6, 0, 0],
                bar_size=36,
                name="% Error",
            ),
            data=FeedbackState.preguntas_error,
            height=320,
            width="100%",
            margin={"top": 10, "right": 10, "left": -10, "bottom": 0},
            class_name="[&_.recharts-tooltip-item-value]:!text-red-600 [&_.recharts-tooltip-item-value]:!font-bold",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
    )


def error_question_row(p: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                p["area"],
                class_name="px-2.5 py-1 rounded-md text-xs font-bold bg-blue-50 text-blue-700 w-fit",
            ),
            rx.el.p(
                p["enunciado"],
                class_name="text-sm font-semibold text-gray-900 mt-2",
            ),
            class_name="flex flex-col flex-1",
        ),
        rx.el.div(
            rx.el.p(
                f"{p['indice_error']:.1f}%",
                class_name="text-xl font-bold text-red-600",
            ),
            rx.el.p(
                f"{p['total_respuestas']} respuestas",
                class_name="text-xs text-gray-500",
            ),
            class_name="flex flex-col items-end",
        ),
        class_name="flex items-center justify-between gap-4 p-4 bg-white border border-gray-100 rounded-xl hover:border-gray-200 transition-colors",
    )


def estado_apelacion_badge(estado: rx.Var) -> rx.Component:
    return rx.cond(
        estado == "Pendiente",
        rx.el.span(
            rx.el.span(class_name="w-1.5 h-1.5 rounded-full bg-amber-500"),
            "Pendiente",
            class_name="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-700 w-fit",
        ),
        rx.el.span(
            rx.el.span(class_name="w-1.5 h-1.5 rounded-full bg-green-500"),
            "Resuelto",
            class_name="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-green-50 text-green-700 w-fit",
        ),
    )


def apelacion_row(a: Apelacion) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    a["postulante"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(f"DNI: {a['dni']}", class_name="text-xs text-gray-500"),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                a["pregunta"],
                class_name="text-xs font-mono font-semibold text-gray-700 bg-gray-50 px-2 py-1 rounded-md",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.p(
                a["motivo"],
                class_name="text-sm text-gray-600 max-w-md",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                a["fecha"], class_name="text-xs text-gray-500 font-medium"
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(estado_apelacion_badge(a["estado"]), class_name="px-6 py-4"),
        rx.el.td(
            rx.cond(
                a["estado"] == "Pendiente",
                rx.el.button(
                    rx.icon("check", class_name="h-4 w-4 mr-1.5"),
                    "Resolver",
                    on_click=lambda: FeedbackState.resolver_apelacion(a["id"]),
                    class_name="flex items-center px-3 py-1.5 rounded-lg text-xs font-semibold text-white bg-[#228B22] hover:bg-[#1a6b1a] transition-colors",
                ),
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="h-4 w-4 mr-1.5"),
                    "Reabrir",
                    on_click=lambda: FeedbackState.reabrir_apelacion(a["id"]),
                    class_name="flex items-center px-3 py-1.5 rounded-lg text-xs font-semibold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 transition-colors",
                ),
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50/50 transition-colors",
    )


def feedback_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_card_fb(
                "Total Apelaciones",
                f"{FeedbackState.total_apelaciones}",
                "blue",
                "message-square",
            ),
            stat_card_fb(
                "Pendientes",
                f"{FeedbackState.total_pendientes}",
                "amber",
                "clock",
            ),
            stat_card_fb(
                "Resueltas",
                f"{FeedbackState.total_resueltas}",
                "green",
                "circle-check",
            ),
            stat_card_fb(
                "Error Promedio",
                f"{FeedbackState.promedio_error:.1f}%",
                "red",
                "trending-down",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
        ),
        # Chart and top errors
        rx.el.div(
            error_chart(),
            rx.el.div(
                rx.el.h3(
                    "Top Preguntas con Mayor Error",
                    class_name="text-lg font-bold text-[#003366] mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        FeedbackState.preguntas_error,
                        error_question_row,
                    ),
                    class_name="flex flex-col gap-3 max-h-[320px] overflow-y-auto",
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6",
        ),
        # Apelaciones section
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Tabla de Apelaciones",
                        class_name="text-lg font-bold text-[#003366]",
                    ),
                    rx.el.p(
                        "Reclamos formales presentados por los postulantes",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.icon(
                        "filter",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                    ),
                    rx.el.select(
                        rx.el.option("Todas", value="Todas"),
                        rx.el.option("Pendiente", value="Pendiente"),
                        rx.el.option("Resuelto", value="Resuelto"),
                        value=FeedbackState.filter_estado,
                        on_change=FeedbackState.set_filter_estado,
                        class_name="pl-10 pr-10 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 appearance-none cursor-pointer focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all min-w-[180px]",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                class_name="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                rx.el.div(
                                    rx.icon("user", class_name="h-3.5 w-3.5"),
                                    "Postulante",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon(
                                        "file-question",
                                        class_name="h-3.5 w-3.5",
                                    ),
                                    "Pregunta",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon(
                                        "message-circle",
                                        class_name="h-3.5 w-3.5",
                                    ),
                                    "Motivo",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon(
                                        "calendar", class_name="h-3.5 w-3.5"
                                    ),
                                    "Fecha",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                "Estado",
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                "Acciones",
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                        ),
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            FeedbackState.apelaciones_filtradas, apelacion_row
                        ),
                    ),
                    class_name="table-auto w-full",
                ),
                class_name="overflow-x-auto bg-white rounded-2xl border border-gray-200 shadow-sm",
            ),
            class_name="",
        ),
        class_name="max-w-7xl mx-auto w-full",
    )