import reflex as rx
from sistema_admisi_n_unas.states.postulantes_state import PostulantesState


def field_label(label: str, required: bool = True) -> rx.Component:
    return rx.el.label(
        label,
        rx.cond(
            required, rx.el.span(" *", class_name="text-red-500"), rx.fragment()
        ),
        class_name="block text-sm font-semibold text-gray-700 mb-2",
    )


def text_field(
    label: str,
    placeholder: str,
    value: rx.Var,
    error: rx.Var,
    on_change,
    icon: str = "",
    input_type: str = "text",
) -> rx.Component:
    return rx.el.div(
        field_label(label),
        rx.el.div(
            rx.cond(
                icon != "",
                rx.icon(
                    icon,
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                ),
                rx.fragment(),
            ),
            rx.el.input(
                placeholder=placeholder,
                default_value=value,
                on_change=on_change.debounce(300),
                type=input_type,
                class_name=rx.cond(
                    icon != "",
                    "w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all",
                    "w-full px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all",
                ),
            ),
            class_name="relative",
        ),
        rx.cond(
            error != "",
            rx.el.div(
                rx.icon("circle-alert", class_name="h-3.5 w-3.5"),
                rx.el.span(error),
                class_name="flex items-center gap-1.5 mt-1.5 text-xs text-red-600 font-medium",
            ),
            rx.fragment(),
        ),
        class_name="flex flex-col",
    )


def carrera_select() -> rx.Component:
    return rx.el.div(
        field_label("Carrera profesional"),
        rx.el.div(
            rx.icon(
                "graduation-cap",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
            ),
            rx.el.select(
                rx.el.option(
                    "Selecciona una carrera...", value="", disabled=True
                ),
                rx.foreach(
                    PostulantesState.carreras,
                    lambda c: rx.el.option(c, value=c),
                ),
                value=PostulantesState.f_carrera,
                on_change=PostulantesState.set_carrera,
                class_name="w-full pl-10 pr-10 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 appearance-none cursor-pointer focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all",
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
            ),
            class_name="relative",
        ),
        rx.cond(
            PostulantesState.err_carrera != "",
            rx.el.div(
                rx.icon("circle-alert", class_name="h-3.5 w-3.5"),
                rx.el.span(PostulantesState.err_carrera),
                class_name="flex items-center gap-1.5 mt-1.5 text-xs text-red-600 font-medium",
            ),
            rx.fragment(),
        ),
        class_name="flex flex-col",
    )


def colegio_card(
    tipo: str, costo: str, descripcion: str, icon: str
) -> rx.Component:
    is_selected = PostulantesState.f_tipo_colegio == tipo
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    icon,
                    class_name=rx.cond(
                        is_selected,
                        "h-5 w-5 text-[#228B22]",
                        "h-5 w-5 text-gray-400",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        tipo,
                        class_name=rx.cond(
                            is_selected,
                            "text-sm font-bold text-[#003366]",
                            "text-sm font-bold text-gray-900",
                        ),
                    ),
                    rx.el.p(descripcion, class_name="text-xs text-gray-500"),
                    class_name="flex flex-col text-left",
                ),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.span(
                    "S/ ", class_name="text-xs text-gray-500 font-medium"
                ),
                rx.el.span(
                    costo,
                    class_name=rx.cond(
                        is_selected,
                        "text-xl font-bold text-[#228B22]",
                        "text-xl font-bold text-gray-700",
                    ),
                ),
                class_name="flex items-baseline",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        type="button",
        on_click=lambda: PostulantesState.set_tipo_colegio(tipo),
        class_name=rx.cond(
            is_selected,
            "p-4 rounded-xl border-2 border-[#228B22] bg-green-50/50 transition-all w-full",
            "p-4 rounded-xl border-2 border-gray-200 bg-white hover:border-gray-300 transition-all w-full",
        ),
    )


def inscripcion_form() -> rx.Component:
    return rx.el.div(
        # Header card
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user-plus", class_name="h-5 w-5 text-[#228B22]"),
                    class_name="p-2.5 rounded-xl bg-green-50 w-fit",
                ),
                rx.el.div(
                    rx.el.h2(
                        "Nueva Inscripción",
                        class_name="text-xl font-bold text-[#003366]",
                    ),
                    rx.el.p(
                        "Completa los datos del postulante para registrarlo en el proceso de admisión",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-start gap-4 mb-8",
            ),
            # Form
            rx.el.form(
                # Personal info section
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "01",
                            class_name="text-xs font-bold text-[#228B22]",
                        ),
                        rx.el.h3(
                            "Datos personales",
                            class_name="text-sm font-bold text-[#003366] uppercase tracking-wide",
                        ),
                        class_name="flex items-center gap-2 mb-4 pb-3 border-b border-gray-100",
                    ),
                    rx.el.div(
                        text_field(
                            "Nombres",
                            "Ej: María Fernanda",
                            PostulantesState.f_nombres,
                            PostulantesState.err_nombres,
                            PostulantesState.set_nombres,
                            "user",
                        ),
                        text_field(
                            "Apellidos",
                            "Ej: Quispe Huamán",
                            PostulantesState.f_apellidos,
                            PostulantesState.err_apellidos,
                            PostulantesState.set_apellidos,
                            "user",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-5",
                    ),
                    rx.el.div(
                        text_field(
                            "DNI",
                            "8 dígitos",
                            PostulantesState.f_dni,
                            PostulantesState.err_dni,
                            PostulantesState.set_dni,
                            "id-card",
                        ),
                        carrera_select(),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-5 mt-5",
                    ),
                    class_name="mb-8",
                ),
                # Colegio section
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "02",
                            class_name="text-xs font-bold text-[#228B22]",
                        ),
                        rx.el.h3(
                            "Tipo de colegio de procedencia",
                            class_name="text-sm font-bold text-[#003366] uppercase tracking-wide",
                        ),
                        class_name="flex items-center gap-2 mb-4 pb-3 border-b border-gray-100",
                    ),
                    rx.el.div(
                        colegio_card(
                            "Estatal",
                            "220",
                            "Colegio público nacional",
                            "school",
                        ),
                        colegio_card(
                            "Privado",
                            "240",
                            "Institución educativa privada",
                            "building-2",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                    class_name="mb-8",
                ),
                # Voucher section
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "03",
                            class_name="text-xs font-bold text-[#228B22]",
                        ),
                        rx.el.h3(
                            "Comprobante de pago",
                            class_name="text-sm font-bold text-[#003366] uppercase tracking-wide",
                        ),
                        class_name="flex items-center gap-2 mb-4 pb-3 border-b border-gray-100",
                    ),
                    rx.el.div(
                        text_field(
                            "Número de Voucher",
                            "Ej: V-001250",
                            PostulantesState.f_voucher,
                            PostulantesState.err_voucher,
                            PostulantesState.set_voucher,
                            "receipt",
                        ),
                        rx.el.div(
                            field_label("Total a pagar", required=False),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.span(
                                        "S/",
                                        class_name="text-sm text-gray-500 font-medium",
                                    ),
                                    rx.el.span(
                                        f"{PostulantesState.costo_actual:.2f}",
                                        class_name="text-2xl font-bold text-[#003366]",
                                    ),
                                    class_name="flex items-baseline gap-1",
                                ),
                                rx.el.span(
                                    f"Tarifa para colegio {PostulantesState.f_tipo_colegio}",
                                    class_name="text-xs text-gray-500 font-medium",
                                ),
                                class_name="flex flex-col gap-1 px-4 py-2.5 bg-blue-50/50 border border-blue-100 rounded-xl",
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-5",
                    ),
                    class_name="mb-8",
                ),
                # Action buttons
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "info",
                            class_name="h-4 w-4 text-gray-400",
                        ),
                        rx.el.span(
                            "Verifica que todos los datos sean correctos antes de enviar",
                            class_name="text-xs text-gray-500 font-medium",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.el.a(
                            "Cancelar",
                            href="/postulantes",
                            class_name="px-5 py-2.5 rounded-xl text-sm font-semibold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.button(
                            rx.icon("check", class_name="h-4 w-4 mr-2"),
                            "Registrar Postulante",
                            type="submit",
                            disabled=~PostulantesState.form_valido,
                            class_name=rx.cond(
                                PostulantesState.form_valido,
                                "flex items-center px-5 py-2.5 rounded-xl text-sm font-semibold text-white bg-[#228B22] hover:bg-[#1a6b1a] transition-colors shadow-sm",
                                "flex items-center px-5 py-2.5 rounded-xl text-sm font-semibold text-white bg-gray-300 cursor-not-allowed",
                            ),
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center md:justify-between gap-4 pt-6 border-t border-gray-100",
                ),
                on_submit=PostulantesState.submit_form,
                reset_on_submit=False,
            ),
            class_name="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm",
        ),
        class_name="max-w-4xl mx-auto w-full",
    )