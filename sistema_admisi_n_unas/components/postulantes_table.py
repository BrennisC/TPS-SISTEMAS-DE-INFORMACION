import reflex as rx
from sistema_admisi_n_unas.states.postulantes_state import PostulantesState, Postulante


def stat_pill(label: str, value: str, color: str, icon: str) -> rx.Component:
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


def estado_badge(estado: rx.Var) -> rx.Component:
    return rx.cond(
        estado == "Inscrito",
        rx.el.span(
            rx.el.span(class_name="w-1.5 h-1.5 rounded-full bg-green-500"),
            "Inscrito",
            class_name="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-green-50 text-green-700 w-fit",
        ),
        rx.el.span(
            rx.el.span(class_name="w-1.5 h-1.5 rounded-full bg-amber-500"),
            "Pendiente",
            class_name="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-700 w-fit",
        ),
    )


def colegio_badge(tipo: rx.Var) -> rx.Component:
    return rx.cond(
        tipo == "Estatal",
        rx.el.span(
            "Estatal",
            class_name="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-blue-50 text-blue-700 w-fit",
        ),
        rx.el.span(
            "Privado",
            class_name="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-purple-50 text-purple-700 w-fit",
        ),
    )


def get_initials(nombres: rx.Var, apellidos: rx.Var) -> rx.Var:
    return f"{nombres.split(' ')[0][0]}{apellidos.split(' ')[0][0]}"


def table_row(p: Postulante) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    get_initials(p["nombres"], p["apellidos"]),
                    class_name="h-9 w-9 rounded-full bg-[#003366] text-white flex items-center justify-center text-xs font-bold flex-shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        f"{p['nombres']} {p['apellidos']}",
                        class_name="text-sm font-semibold text-gray-900 leading-tight",
                    ),
                    rx.el.p(
                        f"DNI: {p['dni']}",
                        class_name="text-xs text-gray-500 font-medium",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.p(
                p["carrera"], class_name="text-sm font-medium text-gray-700"
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(colegio_badge(p["tipo_colegio"]), class_name="px-6 py-4"),
        rx.el.td(
            rx.el.span(
                f"S/ {p['costo']:.2f}",
                class_name="text-sm font-bold text-[#228B22]",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                p["voucher"],
                class_name="text-xs font-mono font-semibold text-gray-700 bg-gray-50 px-2 py-1 rounded-md",
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.span(
                p["fecha"], class_name="text-xs text-gray-500 font-medium"
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(estado_badge(p["estado"]), class_name="px-6 py-4"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("refresh-cw", class_name="h-4 w-4"),
                    on_click=lambda: PostulantesState.toggle_estado(p["id"]),
                    title="Cambiar estado",
                    class_name="p-2 rounded-lg text-gray-500 hover:bg-blue-50 hover:text-blue-600 transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: PostulantesState.delete_postulante(
                        p["id"]
                    ),
                    title="Eliminar",
                    class_name="p-2 rounded-lg text-gray-500 hover:bg-red-50 hover:text-red-600 transition-colors",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="px-6 py-4",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50/50 transition-colors",
    )


def empty_state() -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("inbox", class_name="h-10 w-10 text-gray-300 mb-3"),
                rx.el.p(
                    "No se encontraron postulantes",
                    class_name="text-sm font-semibold text-gray-700",
                ),
                rx.el.p(
                    "Intenta ajustar los filtros o registra un nuevo postulante",
                    class_name="text-xs text-gray-500 mt-1",
                ),
                class_name="flex flex-col items-center justify-center py-16",
            ),
            col_span=8,
        ),
    )


def filters_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
            ),
            rx.el.input(
                placeholder="Buscar por nombre, DNI o voucher...",
                default_value=PostulantesState.search_query,
                on_change=PostulantesState.set_search_query.debounce(400),
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
                    PostulantesState.carreras,
                    lambda c: rx.el.option(c, value=c),
                ),
                value=PostulantesState.filter_carrera,
                on_change=PostulantesState.set_filter_carrera,
                class_name="pl-10 pr-10 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 appearance-none cursor-pointer focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all min-w-[220px]",
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
            ),
            class_name="relative",
        ),
        rx.el.a(
            rx.icon("plus", class_name="h-4 w-4 mr-2"),
            "Nueva Inscripción",
            href="/inscripcion",
            class_name="flex items-center px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-[#228B22] hover:bg-[#1a6b1a] transition-colors shadow-sm",
        ),
        class_name="flex flex-col md:flex-row md:items-center gap-3 mb-6",
    )


def postulantes_table() -> rx.Component:
    return rx.el.div(
        # Stats
        rx.el.div(
            stat_pill(
                "Total Postulantes",
                f"{PostulantesState.total_postulantes}",
                "blue",
                "users",
            ),
            stat_pill(
                "Colegio Estatal",
                f"{PostulantesState.total_estatal}",
                "green",
                "school",
            ),
            stat_pill(
                "Colegio Privado",
                f"{PostulantesState.total_privado}",
                "purple",
                "building-2",
            ),
            stat_pill(
                "Total Recaudado",
                f"S/ {PostulantesState.total_recaudado:.2f}",
                "amber",
                "wallet",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
        ),
        filters_bar(),
        # Table
        rx.el.div(
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
                                    rx.icon("school", class_name="h-3.5 w-3.5"),
                                    "Colegio",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon("wallet", class_name="h-3.5 w-3.5"),
                                    "Costo",
                                    class_name="flex items-center gap-2",
                                ),
                                class_name="px-6 py-3.5 text-left text-xs font-bold text-gray-600 uppercase tracking-wider bg-gray-50",
                            ),
                            rx.el.th(
                                rx.el.div(
                                    rx.icon(
                                        "receipt", class_name="h-3.5 w-3.5"
                                    ),
                                    "Voucher",
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
                        rx.cond(
                            PostulantesState.filtered_postulantes.length() > 0,
                            rx.foreach(
                                PostulantesState.paginated_postulantes,
                                table_row,
                            ),
                            empty_state(),
                        ),
                    ),
                    class_name="table-auto w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("chevron-left", class_name="h-4 w-4"),
                    "Anterior",
                    on_click=PostulantesState.prev_page,
                    disabled=PostulantesState.current_page == 1,
                    class_name=rx.cond(
                        PostulantesState.current_page == 1,
                        "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold text-gray-400 bg-gray-100 cursor-not-allowed",
                        "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50",
                    ),
                ),
                rx.el.span(
                    f"Página {PostulantesState.current_page} de {PostulantesState.total_pages}",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.button(
                    "Siguiente",
                    rx.icon("chevron-right", class_name="h-4 w-4"),
                    on_click=PostulantesState.next_page,
                    disabled=PostulantesState.current_page
                    == PostulantesState.total_pages,
                    class_name=rx.cond(
                        PostulantesState.current_page
                        == PostulantesState.total_pages,
                        "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold text-gray-400 bg-gray-100 cursor-not-allowed",
                        "flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-semibold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50",
                    ),
                ),
                class_name="flex items-center justify-center gap-4",
            ),
            class_name="mt-4",
        ),
        class_name="max-w-7xl mx-auto w-full",
    )