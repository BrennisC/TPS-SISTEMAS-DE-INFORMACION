import reflex as rx

from ..components.stats_card import stats_card
from ..states.tesoreria_state import TesoreriaState


def estado_badge(estado: str) -> rx.Component:
    classes = {
        "Validado": "bg-green-50 text-green-700 border-green-200",
        "Pendiente": "bg-amber-50 text-amber-700 border-amber-200",
        "Observado": "bg-red-50 text-red-700 border-red-200",
    }
    return rx.el.span(
        estado,
        class_name=f"px-3 py-1 rounded-full text-xs font-semibold border {classes.get(estado, 'bg-gray-50 text-gray-700 border-gray-200')}",
    )


def tesoreria_input(label: str, placeholder: str, value: rx.Var, on_change, input_type: str = "text") -> rx.Component:
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


def payment_modal() -> rx.Component:
    return rx.cond(
        TesoreriaState.show_payment_modal,
        rx.el.div(
            rx.el.div(
                on_click=TesoreriaState.close_payment_modal,
                class_name="fixed inset-0 bg-slate-950/50 backdrop-blur-sm z-40",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2("Registrar pago", class_name="text-xl font-bold text-gray-900"),
                            rx.el.p(
                                "Ingresa el DNI y Tesorería rellenará los datos desde postulantes.csv.",
                                class_name="text-sm text-gray-500 mt-1",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-5 w-5"),
                            on_click=TesoreriaState.close_payment_modal,
                            class_name="p-2 rounded-xl text-gray-500 hover:bg-gray-100",
                        ),
                        class_name="flex items-start justify-between gap-4 mb-6",
                    ),
                    rx.el.div(
                        tesoreria_input("DNI", "Ej: 73698379", TesoreriaState.f_dni, TesoreriaState.set_dni),
                        tesoreria_input("Voucher", "Ej: V-2026A00001", TesoreriaState.f_voucher, TesoreriaState.set_voucher),
                        tesoreria_input("Monto", "Ej: 220.00", TesoreriaState.f_monto, TesoreriaState.set_monto),
                        tesoreria_input("Concepto", "Derecho de admision", TesoreriaState.f_concepto, TesoreriaState.set_concepto),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Estudiante", class_name="text-xs font-bold text-gray-400 uppercase tracking-widest"),
                            rx.el.h3(TesoreriaState.estudiante_nombre, class_name="text-lg font-bold text-gray-900 mt-1"),
                            class_name="md:col-span-2",
                        ),
                        rx.el.div(
                            rx.el.p("Carrera", class_name="text-xs font-bold text-gray-400 uppercase tracking-widest"),
                            rx.el.p(TesoreriaState.estudiante_carrera, class_name="text-sm font-semibold text-gray-700 mt-1"),
                        ),
                        rx.el.div(
                            rx.el.p("Convocatoria", class_name="text-xs font-bold text-gray-400 uppercase tracking-widest"),
                            rx.el.p(TesoreriaState.estudiante_convocatoria, class_name="text-sm font-semibold text-gray-700 mt-1"),
                        ),
                        rx.el.div(
                            rx.el.p("Estado", class_name="text-xs font-bold text-gray-400 uppercase tracking-widest"),
                            rx.el.p(TesoreriaState.estudiante_estado, class_name="text-sm font-semibold text-gray-700 mt-1"),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-50 border border-slate-100 rounded-2xl p-4 mt-5",
                    ),
                    rx.el.div(
                        tesoreria_input("Observación", "Opcional", TesoreriaState.f_observacion, TesoreriaState.set_observacion),
                        class_name="mt-5",
                    ),
                    rx.cond(
                        TesoreriaState.mensaje != "",
                        rx.el.p(TesoreriaState.mensaje, class_name="text-sm font-medium text-[#003366] mt-4"),
                        rx.fragment(),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            on_click=TesoreriaState.close_payment_modal,
                            class_name="px-5 py-2.5 rounded-xl border border-gray-200 text-sm font-semibold text-gray-700 hover:bg-gray-50",
                        ),
                        rx.el.button(
                            "Registrar pago",
                            on_click=TesoreriaState.registrar_pago,
                            class_name="px-5 py-2.5 rounded-xl bg-[#228B22] text-white text-sm font-semibold hover:opacity-90",
                        ),
                        class_name="flex justify-end gap-3 mt-6",
                    ),
                    class_name="bg-white rounded-3xl border border-gray-100 shadow-2xl p-6 w-full max-w-3xl max-h-[90vh] overflow-y-auto",
                ),
                class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
            ),
        ),
        rx.fragment(),
    )


def tesoreria_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                stats_card(
                    "Pagos Validados",
                    f"{TesoreriaState.pagos_validados}",
                    "Comprobantes conformes",
                    "receipt",
                    "#228B22",
                ),
                stats_card(
                    "Pagos Pendientes",
                    f"{TesoreriaState.pagos_pendientes}",
                    f"Monto por revisar: S/. {TesoreriaState.monto_pendiente:,.2f}",
                    "clock-3",
                    "#d97706",
                ),
                stats_card(
                    "Pagos Observados",
                    f"{TesoreriaState.pagos_observados}",
                    "Requieren regularizacion",
                    "triangle-alert",
                    "#dc2626",
                ),
                stats_card(
                    "Total Validado",
                    f"S/. {TesoreriaState.total_recaudado:,.2f}",
                    f"Operaciones: {TesoreriaState.total_pagos}",
                    "wallet",
                    "#003366",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Proceso sugerido de tesoreria",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Este modulo se conecta con admision para validar pagos, observar vouchers y liberar la inscripcion.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-5",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span("1", class_name="w-8 h-8 rounded-full bg-blue-50 text-[#003366] font-bold flex items-center justify-center"),
                        rx.el.div(
                            rx.el.h3("Registro de pago", class_name="font-semibold text-gray-900"),
                            rx.el.p("El postulante genera o entrega el voucher.", class_name="text-sm text-gray-500"),
                        ),
                        class_name="flex items-start gap-3",
                    ),
                    rx.el.div(
                        rx.el.span("2", class_name="w-8 h-8 rounded-full bg-green-50 text-[#228B22] font-bold flex items-center justify-center"),
                        rx.el.div(
                            rx.el.h3("Validacion", class_name="font-semibold text-gray-900"),
                            rx.el.p("Tesoreria revisa monto, fecha, convocatoria y estado.", class_name="text-sm text-gray-500"),
                        ),
                        class_name="flex items-start gap-3",
                    ),
                    rx.el.div(
                        rx.el.span("3", class_name="w-8 h-8 rounded-full bg-amber-50 text-amber-700 font-bold flex items-center justify-center"),
                        rx.el.div(
                            rx.el.h3("Liberacion del proceso", class_name="font-semibold text-gray-900"),
                            rx.el.p("Admisión continúa solo con pagos validados.", class_name="text-sm text-gray-500"),
                        ),
                        class_name="flex items-start gap-3",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-4",
                ),
                class_name="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2("Acciones de tesoreria", class_name="text-lg font-bold text-gray-900"),
                    rx.el.p(
                        "Registra pagos desde un modal conectado con la base de postulantes.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("plus", class_name="h-4 w-4 mr-2"),
                        "Registrar pago",
                        on_click=TesoreriaState.open_payment_modal,
                        class_name="flex items-center px-5 py-2.5 rounded-xl bg-[#228B22] text-white text-sm font-semibold hover:opacity-90",
                    ),
                    class_name="flex flex-col sm:flex-row gap-3",
                ),
                rx.cond(
                    TesoreriaState.mensaje != "",
                    rx.el.p(TesoreriaState.mensaje, class_name="text-sm font-medium text-[#003366] mt-4"),
                    rx.fragment(),
                ),
                class_name="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm mb-8 flex flex-col lg:flex-row lg:items-center justify-between gap-4",
            ),
            payment_modal(),
            rx.el.div(
                rx.el.div(
                    rx.el.h2("Operaciones recientes", class_name="text-lg font-bold text-gray-900"),
                    rx.el.button(
                        "Actualizar pagos",
                        on_click=TesoreriaState.cargar_pagos,
                        class_name="px-4 py-2 rounded-xl bg-[#003366] text-white text-sm font-semibold hover:opacity-90",
                    ),
                    class_name="flex items-center justify-between gap-3 mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th("Postulante", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                                rx.el.th("DNI", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                                rx.el.th("Convocatoria", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                                rx.el.th("Concepto", class_name="px-4 py-3 text-left text-sm font-bold text-gray-600 bg-gray-50"),
                                rx.el.th("Monto", class_name="px-4 py-3 text-right text-sm font-bold text-gray-600 bg-gray-50"),
                                rx.el.th("Estado", class_name="px-4 py-3 text-center text-sm font-bold text-gray-600 bg-gray-50"),
                                rx.el.th("Acciones", class_name="px-4 py-3 text-center text-sm font-bold text-gray-600 bg-gray-50"),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                TesoreriaState.pagos_recientes,
                                lambda pago: rx.el.tr(
                                    rx.el.td(pago["postulante"], class_name="px-4 py-3 text-sm font-medium text-gray-900 border-b border-gray-100"),
                                    rx.el.td(pago["dni"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                    rx.el.td(pago["convocatoria"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                    rx.el.td(pago["concepto"], class_name="px-4 py-3 text-sm text-gray-600 border-b border-gray-100"),
                                    rx.el.td(f"S/. {pago['monto']:,.2f}", class_name="px-4 py-3 text-sm text-right font-semibold text-gray-900 border-b border-gray-100"),
                                    rx.el.td(
                                        rx.el.div(estado_badge(pago["estado_pago"]), class_name="flex justify-center border-b border-gray-100 py-3"),
                                    ),
                                    rx.el.td(
                                        rx.el.div(
                                            rx.el.button(
                                                "Validar",
                                                on_click=lambda: TesoreriaState.validar_pago(pago["id"]),
                                                class_name="px-3 py-1.5 rounded-lg bg-green-50 text-green-700 text-xs font-semibold",
                                            ),
                                            rx.el.button(
                                                "Observar",
                                                on_click=lambda: TesoreriaState.observar_pago(pago["id"]),
                                                class_name="px-3 py-1.5 rounded-lg bg-red-50 text-red-700 text-xs font-semibold",
                                            ),
                                            class_name="flex justify-center gap-2 border-b border-gray-100 py-3",
                                        ),
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
    )
