import reflex as rx
from ..states.aulas_state import AulasState


def aulas_view() -> rx.Component:
    """Vista principal del módulo de asignación de aulas"""
    return rx.el.div(
        # Sección de configuración
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Configuración de Aulas",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Número de Aulas por Piso",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.input(
                            type_="number",
                            value=AulasState.aulas_por_piso,
                            on_change=AulasState.set_aulas_por_piso,
                            class_name="px-3 py-2 border border-gray-300 rounded-lg w-full",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Capacidad por Aula",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.input(
                            type_="number",
                            value=AulasState.capacidad_por_aula,
                            on_change=AulasState.set_capacidad_por_aula,
                            class_name="px-3 py-2 border border-gray-300 rounded-lg w-full",
                        ),
                        class_name="mb-4",
                    ),
                    class_name="space-y-4",
                ),
                rx.el.button(
                    "Generar Asignaciones",
                    on_click=AulasState.generar_asignaciones,
                    class_name="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium",
                ),
                class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
            ),
            class_name="max-w-2xl mb-8",
        ),
        
        # Estadísticas
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Estadísticas",
                    class_name="text-lg font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Total Postulantes", class_name="text-sm text-gray-600"),
                        rx.el.p(AulasState.total_postulantes, class_name="text-2xl font-bold text-gray-900"),
                        class_name="p-4 bg-blue-50 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.p("Total Aulas", class_name="text-sm text-gray-600"),
                        rx.el.p(AulasState.total_aulas, class_name="text-2xl font-bold text-gray-900"),
                        class_name="p-4 bg-green-50 rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.p("Utilización Promedio", class_name="text-sm text-gray-600"),
                        rx.el.p(AulasState.promedio_utilizacion, class_name="text-2xl font-bold text-gray-900"),
                        class_name="p-4 bg-purple-50 rounded-lg",
                    ),
                    class_name="grid grid-cols-3 gap-4 mb-6",
                ),
                class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm",
            ),
            class_name="max-w-7xl mb-8",
        ),
        
        # Mensaje cuando no hay datos
        rx.cond(
            AulasState.total_aulas > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Distribución de Aulas por Carrera",
                        class_name="text-lg font-bold text-gray-900 mb-4",
                    ),
                    rx.el.p(
                        "Las aulas han sido generadas exitosamente.",
                        class_name="text-gray-600 text-sm"
                    ),
                    class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm max-w-7xl",
                ),
                class_name="",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Haz clic en 'Generar Asignaciones' para crear la distribución de aulas.",
                        class_name="text-gray-600 text-center py-8"
                    ),
                    class_name="bg-white p-6 rounded-lg border border-gray-200 shadow-sm max-w-7xl",
                ),
                class_name="",
            ),
        ),
        
        class_name="space-y-6 pb-8",
    )
