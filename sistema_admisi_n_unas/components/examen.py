import reflex as rx
from sistema_admisi_n_unas.states.examen_state import ExamenState


def intro_screen() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("file-pen", class_name="h-8 w-8 text-[#228B22]"),
                class_name="p-4 rounded-2xl bg-green-50 w-fit mb-6",
            ),
            rx.el.h2(
                "Simulacro de Examen de Admisión",
                class_name="text-2xl font-bold text-[#003366] mb-2",
            ),
            rx.el.p(
                "Pon a prueba tus conocimientos antes del examen oficial",
                class_name="text-sm text-gray-500 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("clock", class_name="h-5 w-5 text-blue-600"),
                    rx.el.div(
                        rx.el.p(
                            "Duración",
                            class_name="text-xs font-medium text-gray-500",
                        ),
                        rx.el.p(
                            "180 minutos",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3 p-4 bg-blue-50/50 border border-blue-100 rounded-xl",
                ),
                rx.el.div(
                    rx.icon("list-checks", class_name="h-5 w-5 text-green-600"),
                    rx.el.div(
                        rx.el.p(
                            "Preguntas",
                            class_name="text-xs font-medium text-gray-500",
                        ),
                        rx.el.p(
                            f"{ExamenState.total_preguntas} preguntas",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3 p-4 bg-green-50/50 border border-green-100 rounded-xl",
                ),
                rx.el.div(
                    rx.icon("award", class_name="h-5 w-5 text-amber-600"),
                    rx.el.div(
                        rx.el.p(
                            "Aprobación",
                            class_name="text-xs font-medium text-gray-500",
                        ),
                        rx.el.p(
                            "Más de 51 puntos",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3 p-4 bg-amber-50/50 border border-amber-100 rounded-xl",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Instrucciones",
                    class_name="text-sm font-bold text-[#003366] uppercase tracking-wide mb-3",
                ),
                rx.el.ul(
                    rx.el.li(
                        "Lee cuidadosamente cada pregunta antes de responder.",
                        class_name="text-sm text-gray-600 flex items-start gap-2",
                    ),
                    rx.el.li(
                        "Cada respuesta correcta vale 1 punto.",
                        class_name="text-sm text-gray-600 flex items-start gap-2",
                    ),
                    rx.el.li(
                        "Puedes navegar entre preguntas y modificar respuestas.",
                        class_name="text-sm text-gray-600 flex items-start gap-2",
                    ),
                    rx.el.li(
                        "El examen finaliza automáticamente al agotar el tiempo.",
                        class_name="text-sm text-gray-600 flex items-start gap-2",
                    ),
                    class_name="flex flex-col gap-2 list-disc list-inside",
                ),
                class_name="bg-gray-50 border border-gray-100 rounded-xl p-5 mb-8",
            ),
            rx.el.button(
                rx.icon("play", class_name="h-4 w-4 mr-2"),
                "Iniciar Examen",
                on_click=ExamenState.iniciar_examen,
                class_name="flex items-center justify-center w-full px-6 py-3.5 bg-[#228B22] hover:bg-[#1a6b1a] text-white text-sm font-bold rounded-xl transition-colors shadow-sm",
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm",
        ),
        class_name="max-w-3xl mx-auto",
    )


def timer_display() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "clock",
                class_name=rx.cond(
                    ExamenState.tiempo_critico,
                    "h-5 w-5 text-red-600",
                    "h-5 w-5 text-[#003366]",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Tiempo restante",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.p(
                    ExamenState.tiempo_formateado,
                    class_name=rx.cond(
                        ExamenState.tiempo_critico,
                        "text-2xl font-bold text-red-600 font-mono",
                        "text-2xl font-bold text-[#003366] font-mono",
                    ),
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-3",
        ),
        class_name=rx.cond(
            ExamenState.tiempo_critico,
            "px-5 py-3 bg-red-50 border-2 border-red-200 rounded-xl animate-pulse",
            "px-5 py-3 bg-white border border-gray-200 rounded-xl",
        ),
    )


def alternativa_button(idx: int, texto: str) -> rx.Component:
    is_selected = ExamenState.respuesta_actual == idx
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    is_selected,
                    rx.icon("check", class_name="h-4 w-4 text-white"),
                    rx.el.span(""),
                ),
                class_name=rx.cond(
                    is_selected,
                    "h-6 w-6 rounded-full bg-[#228B22] flex items-center justify-center flex-shrink-0",
                    "h-6 w-6 rounded-full border-2 border-gray-300 flex items-center justify-center flex-shrink-0",
                ),
            ),
            rx.el.span(
                texto, class_name="text-sm text-gray-800 text-left flex-1"
            ),
            class_name="flex items-center gap-3 w-full",
        ),
        type="button",
        on_click=lambda: ExamenState.seleccionar_respuesta(idx),
        class_name=rx.cond(
            is_selected,
            "p-4 rounded-xl border-2 border-[#228B22] bg-green-50/50 transition-all hover:bg-green-50 w-full",
            "p-4 rounded-xl border-2 border-gray-200 bg-white hover:border-gray-300 transition-all w-full",
        ),
    )


def question_navigator() -> rx.Component:
    return rx.el.div(
        rx.el.h4(
            "Navegación",
            class_name="text-xs font-bold text-gray-600 uppercase tracking-wide mb-3",
        ),
        rx.el.div(
            rx.foreach(
                ExamenState.preguntas,
                lambda p, i: rx.el.button(
                    f"{i + 1}",
                    type="button",
                    on_click=lambda: ExamenState.ir_pregunta(i),
                    class_name=rx.cond(
                        ExamenState.indice_actual == i,
                        "h-10 w-10 rounded-lg bg-[#003366] text-white text-sm font-bold flex items-center justify-center transition-all",
                        rx.cond(
                            ExamenState.respuestas.contains(i),
                            "h-10 w-10 rounded-lg bg-green-100 text-[#228B22] text-sm font-bold flex items-center justify-center hover:bg-green-200 transition-all",
                            "h-10 w-10 rounded-lg bg-gray-100 text-gray-600 text-sm font-bold flex items-center justify-center hover:bg-gray-200 transition-all",
                        ),
                    ),
                ),
            ),
            class_name="grid grid-cols-5 gap-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    class_name="h-3 w-3 rounded bg-[#003366] inline-block"
                ),
                rx.el.span("Actual", class_name="text-xs text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.span(
                    class_name="h-3 w-3 rounded bg-green-100 inline-block"
                ),
                rx.el.span("Respondida", class_name="text-xs text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.span(
                    class_name="h-3 w-3 rounded bg-gray-100 inline-block"
                ),
                rx.el.span("Pendiente", class_name="text-xs text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col gap-2 mt-4 pt-4 border-t border-gray-100",
        ),
        class_name="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm",
    )


def exam_in_progress() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        f"Pregunta {ExamenState.indice_actual + 1} de {ExamenState.total_preguntas}",
                        class_name="text-sm font-semibold text-gray-500",
                    ),
                    rx.el.div(
                        rx.el.div(
                            class_name="h-2 bg-[#228B22] rounded-full transition-all",
                            style={"width": f"{ExamenState.progreso}%"},
                        ),
                        class_name="h-2 bg-gray-100 rounded-full w-48 mt-2",
                    ),
                    class_name="flex flex-col",
                ),
                timer_display(),
                class_name="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            ExamenState.pregunta_actual["area"],
                            class_name="px-2.5 py-1 rounded-md text-xs font-bold bg-blue-50 text-blue-700",
                        ),
                        rx.el.span(
                            ExamenState.pregunta_actual["tipo"],
                            class_name="px-2.5 py-1 rounded-md text-xs font-bold bg-purple-50 text-purple-700",
                        ),
                        class_name="flex items-center gap-2 mb-4",
                    ),
                    rx.el.h3(
                        ExamenState.pregunta_actual["enunciado"],
                        class_name="text-lg font-bold text-[#003366] leading-relaxed mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ExamenState.pregunta_actual["alternativas"],
                            lambda alt, i: alternativa_button(i, alt),
                        ),
                        class_name="flex flex-col gap-3",
                    ),
                    class_name="bg-white border border-gray-200 rounded-2xl p-6 md:p-8 shadow-sm mb-4",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                        "Anterior",
                        on_click=ExamenState.anterior,
                        disabled=ExamenState.indice_actual == 0,
                        class_name="flex items-center px-4 py-2.5 rounded-xl text-sm font-semibold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("flag", class_name="h-4 w-4 mr-2"),
                            "Finalizar",
                            on_click=ExamenState.finalizar_examen,
                            class_name="flex items-center px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-red-500 hover:bg-red-600 transition-colors shadow-sm",
                        ),
                        rx.el.button(
                            "Siguiente",
                            rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                            on_click=ExamenState.siguiente,
                            disabled=ExamenState.indice_actual
                            >= ExamenState.total_preguntas - 1,
                            class_name="flex items-center px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-[#003366] hover:bg-[#002244] disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    class_name="flex items-center justify-between",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                question_navigator(),
                rx.el.div(
                    rx.el.p(
                        "Progreso",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    rx.el.p(
                        f"{ExamenState.respondidas}/{ExamenState.total_preguntas}",
                        class_name="text-2xl font-bold text-[#003366]",
                    ),
                    rx.el.p(
                        "preguntas respondidas",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm mt-4",
                ),
                class_name="w-full lg:w-72 flex-shrink-0",
            ),
            class_name="flex flex-col lg:flex-row gap-6",
        ),
        class_name="max-w-7xl mx-auto",
    )


def exam_results() -> rx.Component:
    ingresó = ExamenState.condicion == "INGRESÓ"
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    ingresó,
                    rx.icon(
                        "circle-check", class_name="h-12 w-12 text-[#228B22]"
                    ),
                    rx.icon("circle-x", class_name="h-12 w-12 text-red-500"),
                ),
                class_name=rx.cond(
                    ingresó,
                    "p-4 rounded-2xl bg-green-50 w-fit mx-auto mb-6",
                    "p-4 rounded-2xl bg-red-50 w-fit mx-auto mb-6",
                ),
            ),
            rx.el.h2(
                ExamenState.condicion,
                class_name=rx.cond(
                    ingresó,
                    "text-3xl font-bold text-[#228B22] text-center mb-2",
                    "text-3xl font-bold text-red-600 text-center mb-2",
                ),
            ),
            rx.el.p(
                rx.cond(
                    ingresó,
                    "¡Felicitaciones! Has alcanzado el puntaje requerido para ingresar.",
                    "No alcanzaste el puntaje mínimo requerido. Sigue preparándote.",
                ),
                class_name="text-sm text-gray-500 text-center mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Puntaje obtenido",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    rx.el.p(
                        f"{ExamenState.puntaje}",
                        class_name="text-3xl font-bold text-[#003366]",
                    ),
                    rx.el.p("puntos", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col items-center p-5 bg-blue-50/50 border border-blue-100 rounded-xl",
                ),
                rx.el.div(
                    rx.el.p(
                        "Respuestas correctas",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    rx.el.p(
                        f"{ExamenState.correctas}/{ExamenState.total_preguntas}",
                        class_name="text-3xl font-bold text-[#228B22]",
                    ),
                    rx.el.p("aciertos", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col items-center p-5 bg-green-50/50 border border-green-100 rounded-xl",
                ),
                rx.el.div(
                    rx.el.p(
                        "Tiempo usado",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    rx.el.p(
                        ExamenState.tiempo_formateado,
                        class_name="text-3xl font-bold text-amber-600 font-mono",
                    ),
                    rx.el.p("restante", class_name="text-xs text-gray-500"),
                    class_name="flex flex-col items-center p-5 bg-amber-50/50 border border-amber-100 rounded-xl",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="h-4 w-4 mr-2"),
                    "Volver a Intentar",
                    on_click=ExamenState.reiniciar,
                    class_name="flex items-center px-5 py-2.5 rounded-xl text-sm font-semibold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 transition-colors",
                ),
                rx.el.a(
                    rx.icon("trophy", class_name="h-4 w-4 mr-2"),
                    "Ver Ranking",
                    href="/resultados",
                    class_name="flex items-center px-5 py-2.5 rounded-xl text-sm font-semibold text-white bg-[#003366] hover:bg-[#002244] transition-colors shadow-sm",
                ),
                class_name="flex items-center justify-center gap-3",
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm",
        ),
        class_name="max-w-3xl mx-auto",
    )


def examen_view() -> rx.Component:
    return rx.cond(
        ExamenState.examen_finalizado,
        exam_results(),
        rx.cond(
            ExamenState.examen_iniciado,
            exam_in_progress(),
            intro_screen(),
        ),
    )