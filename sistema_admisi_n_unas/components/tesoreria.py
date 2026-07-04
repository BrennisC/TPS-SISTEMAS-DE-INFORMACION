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
                                        rx.el.div(estado_badge(pago["estado"]), class_name="flex justify-center border-b border-gray-100 py-3"),
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
