import reflex as rx

from ..states.dashboard_state import DashboardState


def tabla_ultimos_registrados():
    """Tabla mejorada de últimos alumnos registrados."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Últimos Alumnos Registrados en Sistema",
                class_name="text-sm font-bold text-gray-800 mb-1",
            ),
            rx.el.p(
                DashboardState.paginated_postulantes.length().to_string()
                + " registros recientes",
                class_name="text-xs text-gray-400",
            ),
            class_name="mb-4",
        ),
        # Table
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            rx.el.div(
                                rx.icon("hash", class_name="h-3 w-3"),
                                "DNI",
                                class_name="flex items-center gap-1.5 text-xs text-gray-500 font-semibold uppercase tracking-wider",
                            ),
                            class_name="text-left p-3 bg-gray-50/80",
                        ),
                        rx.el.th(
                            rx.el.div(
                                rx.icon("user", class_name="h-3 w-3"),
                                "Apellidos y Nombres",
                                class_name="flex items-center gap-1.5 text-xs text-gray-500 font-semibold uppercase tracking-wider",
                            ),
                            class_name="text-left p-3 bg-gray-50/80",
                        ),
                        rx.el.th(
                            rx.el.div(
                                rx.icon("graduation-cap", class_name="h-3 w-3"),
                                "Carrera",
                                class_name="flex items-center gap-1.5 text-xs text-gray-500 font-semibold uppercase tracking-wider",
                            ),
                            class_name="text-left p-3 bg-gray-50/80",
                        ),
                        rx.el.th(
                            rx.el.div(
                                rx.icon("check-circle", class_name="h-3 w-3"),
                                "Estado",
                                class_name="flex items-center gap-1.5 text-xs text-gray-500 font-semibold uppercase tracking-wider",
                            ),
                            class_name="text-left p-3 bg-gray-50/80",
                        ),
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.paginated_postulantes,
                        lambda p: rx.el.tr(
                            rx.el.td(
                                rx.el.span(
                                    p["dni"],
                                    class_name="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-mono font-medium",
                                ),
                                class_name="p-3",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.p(
                                        f"{p['apellidos']}, {p['nombres']}",
                                        class_name="text-sm font-semibold text-gray-800",
                                    ),
                                ),
                                class_name="p-3",
                            ),
                            rx.el.td(
                                rx.el.div(
                                    rx.el.span(
                                        p["carrera"],
                                        class_name="text-xs text-gray-600",
                                    ),
                                ),
                                class_name="p-3",
                            ),
                            rx.el.td(
                                rx.el.span(
                                    p["estado"],
                                    class_name=rx.cond(
                                        p["estado"].strip().lower() == "ingresante",
                                        "px-2.5 py-1 rounded-full text-xs font-bold bg-green-100 text-green-700",
                                        rx.cond(
                                            p["estado"].strip().lower() == "inscrito",
                                            "px-2.5 py-1 rounded-full text-xs font-bold bg-blue-100 text-blue-700",
                                            "px-2.5 py-1 rounded-full text-xs font-bold bg-gray-100 text-gray-600",
                                        ),
                                    ),
                                ),
                                class_name="p-3",
                            ),
                            class_name="border-b border-gray-100 hover:bg-gray-50/60 transition-colors",
                        ),
                    )
                ),
            ),
            class_name="w-full min-w-full overflow-hidden",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2 hover:shadow-md transition-shadow overflow-hidden",
    )


def panel_preguntas_errores():
    """Panel mejorado de preguntas con mayor índice de error."""
    return rx.el.div(
        # Header
        rx.el.div(
            rx.el.h3(
                "Preguntas con Mayor Índice de Error",
                class_name="text-sm font-bold text-gray-700 mb-1",
            ),
            rx.el.p(
                "Análisis de desempeño por área temática",
                class_name="text-xs text-gray-400",
            ),
            class_name="mb-4",
        ),
        # Bars
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("calculator", class_name="h-4 w-4 text-red-500"),
                        rx.el.p(
                            "Matemática - P. 45",
                            class_name="text-xs font-semibold text-gray-700",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "78%",
                            class_name="text-xs font-bold text-red-500",
                        ),
                        class_name="flex items-center gap-1",
                    ),
                    class_name="flex items-center justify-between mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="bg-gradient-to-r from-red-400 to-red-500 h-2 rounded-full transition-all",
                        style={"width": "78%"},
                    ),
                    class_name="w-full bg-gray-100 h-2 rounded-full overflow-hidden",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("flask-conical", class_name="h-4 w-4 text-red-400"),
                        rx.el.p(
                            "Ciencia y Tecnología - P. 62",
                            class_name="text-xs font-semibold text-gray-700",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "71%",
                            class_name="text-xs font-bold text-red-400",
                        ),
                        class_name="flex items-center gap-1",
                    ),
                    class_name="flex items-center justify-between mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="bg-gradient-to-r from-red-300 to-red-400 h-2 rounded-full transition-all",
                        style={"width": "71%"},
                    ),
                    class_name="w-full bg-gray-100 h-2 rounded-full overflow-hidden",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("book-open", class_name="h-4 w-4 text-amber-500"),
                        rx.el.p(
                            "Razonamiento Verbal - P. 28",
                            class_name="text-xs font-semibold text-gray-700",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "65%",
                            class_name="text-xs font-bold text-amber-500",
                        ),
                        class_name="flex items-center gap-1",
                    ),
                    class_name="flex items-center justify-between mb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="bg-gradient-to-r from-amber-300 to-amber-400 h-2 rounded-full transition-all",
                        style={"width": "65%"},
                    ),
                    class_name="w-full bg-gray-100 h-2 rounded-full overflow-hidden",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("globe", class_name="h-4 w-4 text-amber-400"),
                        rx.el.p(
                            "Humanidades - P. 88",
                            class_name="text-xs font-semibold text-gray-700",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "58%",
                            class_name="text-xs font-bold text-amber-400",
                        ),
                        class_name="flex items-center gap-1",
                    ),
                    class_name="flex items-center justify-between",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="bg-gradient-to-r from-amber-200 to-amber-300 h-2 rounded-full transition-all",
                        style={"width": "58%"},
                    ),
                    class_name="w-full bg-gray-100 h-2 rounded-full overflow-hidden",
                ),
            ),
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 hover:shadow-md transition-shadow",
    )


def summary_stats_card(title: str, value: str, subtitle: str, icon: str, color: str) -> rx.Component:
    """Tarjeta de resumen estadístico mejorada."""
    colors = {
        "green": ("bg-green-50 text-green-600", "text-green-600", "bg-green-100"),
        "blue": ("bg-blue-50 text-blue-600", "text-blue-600", "bg-blue-100"),
        "purple": ("bg-purple-50 text-purple-600", "text-purple-600", "bg-purple-100"),
        "amber": ("bg-amber-50 text-amber-600", "text-amber-600", "bg-amber-100"),
    }
    bg_icon, text_color, bg_badge = colors.get(color, colors["green"])
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-5 w-5 {text_color}"),
            class_name=f"p-3 rounded-xl {bg_icon}",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-xs font-medium text-gray-500"),
            rx.el.h3(value, class_name="text-xl font-bold text-gray-900"),
            rx.el.span(
                subtitle,
                class_name=f"inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium {bg_badge} {text_color}",
            ),
        ),
        class_name="flex items-start gap-3 bg-white rounded-xl border border-gray-100 p-4 shadow-sm hover:shadow-md transition-shadow cursor-default",
    )
