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


def biblioteca_input(label: str, placeholder: str, value: rx.Var, on_change, input_type: str = "text") -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-semibold text-gray-700 mb-2"),
        rx.el.input(
            placeholder=placeholder,
            default_value=value,
            on_change=on_change.debounce(300),
            type=input_type,
            class_name="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10",
        ),
    )


def modal_shell(title: str, description: str, close_event, *children: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            on_click=close_event,
            class_name="fixed inset-0 bg-slate-950/50 backdrop-blur-sm z-40",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(title, class_name="text-xl font-bold text-gray-900"),
                        rx.el.p(description, class_name="text-sm text-gray-500 mt-1"),
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-5 w-5"),
                        on_click=close_event,
                        class_name="p-2 rounded-xl text-gray-500 hover:bg-gray-100",
                    ),
                    class_name="flex items-start justify-between gap-4 mb-6",
                ),
                *children,
                class_name="bg-white rounded-3xl border border-gray-100 shadow-2xl p-6 w-full max-w-3xl max-h-[90vh] overflow-y-auto",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
    )


def add_book_modal() -> rx.Component:
    return rx.cond(
        BibliotecaState.show_add_book_modal,
        modal_shell(
            "Agregar libro",
            "Registra material bibliográfico y su stock disponible.",
            BibliotecaState.close_add_book_modal,
            rx.el.div(
                biblioteca_input("Código", "Ej: LIB-051", BibliotecaState.f_codigo, BibliotecaState.set_codigo),
                biblioteca_input("Título", "Nombre del libro", BibliotecaState.f_titulo, BibliotecaState.set_titulo),
                biblioteca_input("Autor", "Autor", BibliotecaState.f_autor, BibliotecaState.set_autor),
                biblioteca_input("Categoría", "Ej: Informática", BibliotecaState.f_categoria, BibliotecaState.set_categoria),
                biblioteca_input("Editorial", "Editorial", BibliotecaState.f_editorial, BibliotecaState.set_editorial),
                biblioteca_input("Stock", "Ej: 3", BibliotecaState.f_stock, BibliotecaState.set_stock),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
            ),
            rx.cond(
                BibliotecaState.mensaje != "",
                rx.el.p(BibliotecaState.mensaje, class_name="text-sm font-medium text-[#003366] mt-4"),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.button(
                    "Cancelar",
                    on_click=BibliotecaState.close_add_book_modal,
                    class_name="px-5 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold text-gray-700 hover:bg-gray-50",
                ),
                rx.el.button(
                    "Guardar libro",
                    on_click=BibliotecaState.agregar_libro,
                    class_name="px-5 py-2.5 rounded-xl bg-[#003366] text-white text-sm font-semibold hover:opacity-90",
                ),
                class_name="flex justify-end gap-3 mt-6",
            ),
        ),
        rx.fragment(),
    )


def loan_modal() -> rx.Component:
    return rx.cond(
        BibliotecaState.show_loan_modal,
        modal_shell(
            "Registrar préstamo",
            "El lector debe existir como ingresante en postulantes.csv.",
            BibliotecaState.close_loan_modal,
            rx.el.div(
                biblioteca_input("DNI lector", "DNI del ingresante", BibliotecaState.f_dni_lector, BibliotecaState.set_dni_lector),
                biblioteca_input("Código de libro", "Ej: LIB-001", BibliotecaState.f_libro_codigo, BibliotecaState.set_libro_codigo),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
            ),
            rx.cond(
                BibliotecaState.mensaje != "",
                rx.el.p(BibliotecaState.mensaje, class_name="text-sm font-medium text-[#003366] mt-4"),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.button(
                    "Cancelar",
                    on_click=BibliotecaState.close_loan_modal,
                    class_name="px-5 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold text-gray-700 hover:bg-gray-50",
                ),
                rx.el.button(
                    "Registrar préstamo",
                    on_click=BibliotecaState.registrar_prestamo,
                    class_name="px-5 py-2.5 rounded-xl bg-[#228B22] text-white text-sm font-semibold hover:opacity-90",
                ),
                class_name="flex justify-end gap-3 mt-6",
            ),
        ),
        rx.fragment(),
    )


def pagination_controls(current_page: rx.Var, total_pages: rx.Var, prev_event, next_event) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Anterior",
            on_click=prev_event,
            class_name="px-4 py-2 rounded-xl border border-gray-200 text-sm font-semibold text-gray-700 hover:bg-gray-50",
        ),
        rx.el.span(
            f"Página {current_page} de {total_pages}",
            class_name="text-sm font-semibold text-gray-600",
        ),
        rx.el.button(
            "Siguiente",
            on_click=next_event,
            class_name="px-4 py-2 rounded-xl border border-gray-200 text-sm font-semibold text-gray-700 hover:bg-gray-50",
        ),
        class_name="flex items-center justify-end gap-3 mt-4",
    )


def biblioteca_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stats_card(
                "Catalogo Base",
                f"{BibliotecaState.total_libros}",
                f"Disponibles: {BibliotecaState.total_disponibles}",
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
                rx.el.h2("Acciones de biblioteca", class_name="text-lg font-bold text-gray-900"),
                rx.el.p("Agrega libros y registra préstamos desde ventanas modales.", class_name="text-sm text-gray-500 mt-1"),
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("plus", class_name="h-4 w-4 mr-2"),
                    "Agregar libro",
                    on_click=BibliotecaState.open_add_book_modal,
                    class_name="flex items-center px-5 py-2.5 rounded-xl bg-[#003366] text-white text-sm font-semibold hover:opacity-90",
                ),
                rx.el.button(
                    rx.icon("book-open", class_name="h-4 w-4 mr-2"),
                    "Registrar préstamo",
                    on_click=BibliotecaState.open_loan_modal,
                    class_name="flex items-center px-5 py-2.5 rounded-xl bg-[#228B22] text-white text-sm font-semibold hover:opacity-90",
                ),
                class_name="flex flex-col sm:flex-row gap-3",
            ),
            rx.cond(
                BibliotecaState.mensaje != "",
                rx.el.p(BibliotecaState.mensaje, class_name="text-sm font-medium text-[#003366] mt-4"),
                rx.fragment(),
            ),
            class_name="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm mb-8 flex flex-col lg:flex-row lg:items-center justify-between gap-4",
        ),
        add_book_modal(),
        loan_modal(),
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
                            rx.el.th("Disponibles", class_name="px-4 py-3 text-center text-sm font-bold text-gray-600 bg-gray-50"),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            BibliotecaState.paginated_catalogo,
                            lambda libro: rx.el.tr(
                                rx.el.td(libro["codigo"], class_name="px-4 py-3 text-sm font-medium text-gray-900 border-b border-gray-100"),
                                rx.el.td(libro["titulo"], class_name="px-4 py-3 text-sm text-gray-700 border-b border-gray-100"),
                                rx.el.td(libro["categoria"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(libro["stock"], class_name="px-4 py-3 text-sm text-center font-semibold text-gray-900 border-b border-gray-100"),
                                rx.el.td(libro["disponibles"], class_name="px-4 py-3 text-sm text-center font-semibold text-green-700 border-b border-gray-100"),
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto",
            ),
            pagination_controls(
                BibliotecaState.catalogo_page,
                BibliotecaState.catalogo_total_pages,
                BibliotecaState.prev_catalogo_page,
                BibliotecaState.next_catalogo_page,
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
                            rx.el.th("Acciones", class_name="px-4 py-3 text-center text-sm font-bold text-gray-600 bg-gray-50"),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            BibliotecaState.paginated_prestamos,
                            lambda prestamo: rx.el.tr(
                                rx.el.td(prestamo["lector"], class_name="px-4 py-3 text-sm font-medium text-gray-900 border-b border-gray-100"),
                                rx.el.td(prestamo["dni_lector"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(prestamo["libro"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(prestamo["fecha_prestamo"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(prestamo["fecha_devolucion"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                rx.el.td(
                                    rx.el.div(prestamo_badge(prestamo["estado"]), class_name="flex justify-center border-b border-gray-100 py-3"),
                                ),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.button(
                                            "Devolver",
                                            on_click=lambda: BibliotecaState.devolver_prestamo(prestamo["id"]),
                                            class_name="px-3 py-1.5 rounded-lg bg-green-50 text-green-700 text-xs font-semibold",
                                        ),
                                        class_name="flex justify-center border-b border-gray-100 py-3",
                                    ),
                                ),
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto",
            ),
            pagination_controls(
                BibliotecaState.prestamos_page,
                BibliotecaState.prestamos_total_pages,
                BibliotecaState.prev_prestamos_page,
                BibliotecaState.next_prestamos_page,
            ),
            class_name="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm",
        ),
        class_name="max-w-7xl mx-auto",
    )
