import reflex as rx

from ..states.dashboard_state import DashboardState


def tabla_ultimos_registrados():
    return rx.el.div(
        rx.el.h3(
            "Últimos Alumnos Registrados en Sistema (CSV)",
            class_name="text-sm font-bold text-gray-800 mb-3",
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "DNI",
                        class_name="text-left p-3 text-xs text-gray-500 font-semibold",
                    ),
                    rx.el.th(
                        "Apellidos y Nombres",
                        class_name="text-left p-3 text-xs text-gray-500 font-semibold",
                    ),
                    rx.el.th(
                        "Carrera",
                        class_name="text-left p-3 text-xs text-gray-500 font-semibold",
                    ),
                    rx.el.th(
                        "Estado",
                        class_name="text-left p-3 text-xs text-gray-500 font-semibold",
                    ),
                ),
                class_name="bg-gray-50/70",
            ),
            rx.el.tbody(
                rx.foreach(
                    DashboardState.paginated_postulantes,
                    lambda p: rx.el.tr(
                        rx.el.td(
                            p["dni"], class_name="p-3 text-sm text-gray-600 font-mono"
                        ),
                        rx.el.td(
                            f"{p['apellidos']}, {p['nombres']}",
                            class_name="p-3 text-sm font-medium text-gray-700",
                        ),
                        rx.el.td(p["carrera"], class_name="p-3 text-sm text-gray-500"),
                        rx.el.td(
                            rx.el.span(
                                p["estado"],
                                class_name=rx.cond(
                                    p["estado"].strip().lower() == "ingresante",
                                    "px-2 py-0.5 rounded-md text-xs font-bold bg-green-50 text-green-700 capitalize",
                                    "px-2 py-0.5 rounded-md text-xs font-bold bg-blue-50 text-blue-700 capitalize",
                                ),
                            ),
                            class_name="p-3",
                        ),
                    ),
                )
            ),
            class_name="w-full min-w-full divide-y divide-gray-100",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2 overflow-x-auto",
    )


def panel_preguntas_errores():
    return rx.el.div(
        rx.el.h3(
            "Preguntas con Mayor Índice de Error",
            class_name="text-sm font-bold text-gray-700 mb-4",
        ),
        rx.el.div(
            # Barra de Error 1
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Matemática - P. 45",
                        class_name="text-xs font-bold text-gray-700",
                    ),
                    rx.el.p(
                        "78% de error", class_name="text-xs font-medium text-red-500"
                    ),
                    class_name="flex justify-between mb-1",
                ),
                rx.el.div(
                    rx.el.div(class_name="bg-red-500 h-2 rounded-full w-[78%]"),
                    class_name="w-full bg-gray-100 h-2 rounded-full",
                ),
                class_name="mb-4",
            ),
            # Barra de Error 2
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Ciencia y Tecnología - P. 62",
                        class_name="text-xs font-bold text-gray-700",
                    ),
                    rx.el.p(
                        "71% de error", class_name="text-xs font-medium text-red-500"
                    ),
                    class_name="flex justify-between mb-1",
                ),
                rx.el.div(
                    rx.el.div(class_name="bg-red-400 h-2 rounded-full w-[71%]"),
                    class_name="w-full bg-gray-100 h-2 rounded-full",
                ),
            ),
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )
