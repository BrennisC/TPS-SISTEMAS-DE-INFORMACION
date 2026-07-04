import reflex as rx

from ..components.stats_card import stats_card
from ..states.biblioteca_state import BibliotecaState


def prestamo_badge(estado: str) -> rx.Component:
    classes = {
        "Prestado": "bg-blue-50 text-blue-700 border-blue-200",
        "Devuelto": "bg-green-50 text-green-700 border-green-200",
        "Vencido": "bg-red-50 text-red-700 border-red-200",
    }
    return rx.el.span(
        estado,
        class_name=f"px-3 py-1 rounded-full text-xs font-semibold border {classes.get(estado, 'bg-gray-50 text-gray-700 border-gray-200')}",
    )


def biblioteca_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stats_card(
                "Catalogo Base",
                f"{BibliotecaState.total_libros}",
                f"Stock total: {BibliotecaState.total_stock}",
                "book-open",
                "#003366",
            ),
            stats_card(
                "Lectores Vinculados",
                f"{BibliotecaState.total_lectores}",
                "Ingresantes vinculados al modulo",
                "users",
                "#228B22",
            ),
            stats_card(
                "Prestamos Activos",
                f"{BibliotecaState.prestamos_activos}",
                "Material pendiente de devolucion",
                "book-open",
                "#2563eb",
            ),
            stats_card(
                "Prestamos Vencidos",
                f"{BibliotecaState.prestamos_vencidos}",
                "Seguimiento requerido",
                "triangle-alert",
                "#dc2626",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2("Integracion ERP con biblioteca", class_name="text-lg font-bold text-gray-900"),
                rx.el.p(
                    "Biblioteca reaprovecha datos de admision para habilitar lectores, controlar prestamos y preparar futuras integraciones con matricula.",
                    class_name="text-sm text-gray-500 mt-1",
                ),
                class_name="mb-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Entradas" , class_name="font-semibold text-gray-900 mb-2"),
                    rx.el.p("Ingresantes, DNI, carreras y estado academico.", class_name="text-sm text-gray-500"),
                    class_name="bg-slate-50 rounded-2xl p-4 border border-slate-100",
                ),
                rx.el.div(
                    rx.el.h3("Proceso" , class_name="font-semibold text-gray-900 mb-2"),
                    rx.el.p("Alta de lector, prestamos, devoluciones y alertas.", class_name="text-sm text-gray-500"),
                    class_name="bg-slate-50 rounded-2xl p-4 border border-slate-100",
                ),
                rx.el.div(
                    rx.el.h3("Salida" , class_name="font-semibold text-gray-900 mb-2"),
                    rx.el.p("Historial de uso y control de material por estudiante.", class_name="text-sm text-gray-500"),
                    class_name="bg-slate-50 rounded-2xl p-4 border border-slate-100",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-4",
            ),
            class_name="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2("Catalogo inicial", class_name="text-lg font-bold text-gray-900"),
                rx.el.button(
                    "Actualizar biblioteca",
                    on_click=BibliotecaState.cargar_biblioteca,
                    class_name="px-4 py-2 rounded-xl bg-[#003366] text-white text-sm font-semibold hover:opacity-90",
                ),
                class_name="flex items-center justify-between gap-3 mb-4",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Codigo", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                            rx.el.th("Titulo", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                            rx.el.th("Categoria", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                            rx.el.th("Stock", class_name="px-4 py-3 text-center text-sm font-bold text-gray-600 bg-gray-50"),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            BibliotecaState.catalogo,
                            lambda libro: rx.el.tr(
                                rx.el.td(libro["codigo"], class_name="px-4 py-3 text-sm font-medium text-gray-900 border-b border-gray-100"),
                                rx.el.td(libro["titulo"], class_name="px-4 py-3 text-sm text-gray-700 border-b border-gray-100"),
                                rx.el.td(libro["categoria"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(libro["stock"], class_name="px-4 py-3 text-sm text-center font-semibold text-gray-900 border-b border-gray-100"),
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm mb-8",
        ),
        rx.el.div(
            rx.el.h2("Prestamos vinculados", class_name="text-lg font-bold text-gray-900 mb-4"),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Lector", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                            rx.el.th("DNI", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                            rx.el.th("Libro", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                            rx.el.th("Prestamo", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                            rx.el.th("Devolucion", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                            rx.el.th("Estado", class_name="px-4 py-3 text-center text-sm font-bold text-gray-600 bg-gray-50"),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            BibliotecaState.prestamos,
                            lambda prestamo: rx.el.tr(
                                rx.el.td(prestamo["lector"], class_name="px-4 py-3 text-sm font-medium text-gray-900 border-b border-gray-100"),
                                rx.el.td(prestamo["dni"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(prestamo["libro"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(prestamo["fecha_prestamo"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(prestamo["fecha_devolucion"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(
                                    rx.el.div(prestamo_badge(prestamo["estado"]), class_name="flex justify-center border-b border-gray-100 py-3"),
                                ),
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm",
        ),
        class_name="max-w-7xl mx-auto",
    )
