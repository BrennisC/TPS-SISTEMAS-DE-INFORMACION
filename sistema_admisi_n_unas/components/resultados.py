import reflex as rx
from sistema_admisi_n_unas.states.resultados_state import ResultadosState, Resultado


def stat_card(label: str, value: str, color: str, icon: str) -> rx.Component:
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


def medalla(ranking: rx.Var) -> rx.Component:
    return rx.match(
        ranking,
        (
            1,
            rx.el.div(
                rx.icon("medal", class_name="h-4 w-4 text-yellow-500"),
                class_name="h-9 w-9 rounded-full bg-yellow-50 flex items-center justify-center",
            ),
        ),
        (
            2,
            rx.el.div(
                rx.icon("medal", class_name="h-4 w-4 text-gray-400"),
                class_name="h-9 w-9 rounded-full bg-gray-100 flex items-center justify-center",
            ),
        ),
        (
            3,
            rx.el.div(
                rx.icon("medal", class_name="h-4 w-4 text-amber-700"),
                class_name="h-9 w-9 rounded-full bg-amber-50 flex items-center justify-center",
            ),
        ),
        rx.el.div(
            rx.el.span(
                ranking.to_string(),
                class_name="text-xs font-bold text-gray-600",
            ),
            class_name="h-9 w-9 rounded-full bg-gray-50 border border-gray-200 flex items-center justify-center",
        ),
    )


def condicion_badge(cond: rx.Var) -> rx.Component:
    return rx.cond(
        cond == "INGRESÓ",
        rx.el.span(
            rx.el.span(class_name="w-1.5 h-1.5 rounded-full bg-green-500"),
            "INGRESÓ",
            class_name="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-green-50 text-green-700 w-fit",
        ),
        rx.el.span(
            rx.el.span(class_name="w-1.5 h-1.5 rounded-full bg-red-500"),
            "NO INGRESÓ",
            class_name="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-red-50 text-red-700 w-fit",
        ),
    )


def ranking_row(r: Resultado) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            medalla(r["ranking"]),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"{r['nombres']} {r['apellidos']}",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"DNI: {r['dni']}",
                    class_name="text-xs text-gray-500 font-medium",
                ),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.p(
                r["carrera"], class_name="text-sm font-medium text-gray-700"
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                f"{r['puntaje']:.1f}",
                class_name="text-base font-bold text-[#003366]",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                f"{r['correctas']}",
                class_name="text-sm font-semibold text-gray-700",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(condicion_badge(r["condicion"]), class_name="px-6 py-4"),
        class_name="border-b border-gray-100 hover:bg-gray-50/50 transition-colors",
    )


def resultados_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_card(
                "Total Postulantes",
                f"{ResultadosState.resultados.length()}",
                "blue",
                "users",
            ),
            stat_card(
                "Ingresantes",
                f"{ResultadosState.total_ingresantes}",
                "green",
                "circle-check",
            ),
            stat_card(
                "No Ingresantes",
                f"{ResultadosState.total_no_ingresantes}",
                "red",
                "circle-x",
            ),
            stat_card(
                "Promedio General",
                f"{ResultadosState.promedio_general:.1f}",
                "amber",
                "trending-up",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
        ),
        # Filters
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                ),
                rx.el.input(
                    placeholder="Buscar por nombre o DNI...",
                    default_value=ResultadosState.search_query,
                    on_change=ResultadosState.set_search_query.debounce(400),
                    class_name="w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all",
                ),
                class_name="relative flex-1 max-w-md",
            ),
            rx.el.div(
                rx.icon(
                    "graduation-cap",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                ),
                rx.el.select(
                    rx.el.option("Todas las carreras", value="Todas"),
                    rx.foreach(
                        ResultadosState.carreras,
                        lambda c: rx.el.option(c, value=c),
                    ),
                    value=ResultadosState.filter_carrera,
                    on_change=ResultadosState.set_filter_carrera,
                    class_name="pl-10 pr-10 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 appearance-none cursor-pointer focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all min-w-[260px]",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("file-text", class_name="h-4 w-4 mr-2"),
                    "PDF",
                    on_click=ResultadosState.exportar_pdf,
                    class_name="flex items-center px-4 py-2.5 rounded-xl text-sm font-semibold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 transition-colors",
                ),
                rx.el.button(
                    rx.icon("file-spreadsheet", class_name="h-4 w-4 mr-2"),
                    "Excel",
                    on_click=ResultadosState.exportar_excel,
                    class_name="flex items-center px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-[#228B22] hover:bg-[#1a6b1a] transition-colors shadow-sm",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex flex-col md:flex-row md:items-center gap-3 mb-6",
        ),
        # Table
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                rx.el.div(
                                    rx.icon("hash", class_name="h-3.5 w-3.5"),
                                    "Pos.",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
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
                                        "graduation-cap",
                                        class_name="h-3.5 w-3.5",
                                    ),
                                    "Carrera",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon(
                                        "trending-up", class_name="h-3.5 w-3.5"
                                    ),
                                    "Puntaje",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon("check", class_name="h-3.5 w-3.5"),
                                    "Aciertos",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                "Condición",
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                        ),
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            ResultadosState.ranking_ordenado, ranking_row
                        ),
                    ),
                    class_name="table-auto w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm",
        ),
        class_name="max-w-7xl mx-auto w-full",
    )