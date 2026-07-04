import reflex as rx
from ..states.recaudacion_state import RecaudacionState

def stat_card(label: str, value: str, subtext: str = "", icon: str = "wallet", color: str = "blue") -> rx.Component:
    """Tarjeta de KPI minimalista"""
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 text-{color}-600"),
            class_name=f"p-3 rounded-lg bg-{color}-100",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
            rx.el.p(subtext, class_name="text-xs text-gray-400 mt-1") if subtext else rx.el.span(),
            class_name="flex flex-col flex-1",
        ),
        class_name="flex items-center gap-4 bg-white p-4 rounded-xl border border-gray-100 shadow-sm transition-all hover:shadow-md",
    )

def chart_card(title: str, chart: rx.Component, col_span: int = 1) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-base font-bold text-gray-800 mb-4"),
        chart,
        class_name=f"bg-white p-5 rounded-xl border border-gray-100 shadow-sm col-span-1 lg:col-span-{col_span}"
    )

def gauge_half_donut(data: list, title: str) -> rx.Component:
    return chart_card(
        title,
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="75%",
                start_angle=180,
                end_angle=0,
                inner_radius=50,
                outer_radius=70,
                padding_angle=2,
                label=True
            ),
            rx.recharts.tooltip(),
            height=220,
        )
    )

def panel_alertas() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Alertas Financieras", class_name="text-base font-bold text-gray-800 mb-4 flex items-center gap-2"),
        rx.foreach(
            RecaudacionState.alertas_financieras,
            lambda alerta: rx.el.div(
                rx.icon(alerta.icono, class_name=f"h-5 w-5 mt-0.5 flex-shrink-0 text-{alerta.tipo}-600"),
                rx.el.p(alerta.mensaje, class_name="text-sm text-gray-700"),
                class_name=f"flex items-start gap-3 p-3 mb-3 rounded-lg bg-{alerta.tipo}-50 border border-{alerta.tipo}-100"
            )
        ),
        class_name="bg-white p-5 rounded-xl border border-gray-100 shadow-sm h-full"
    )

def panel_filtros() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label("Año", class_name="block text-xs font-medium text-gray-500 mb-1"),
            rx.select(
                RecaudacionState.opciones_años,
                value=RecaudacionState.filtro_año,
                on_change=RecaudacionState.set_filtro_año,
                class_name="w-full bg-gray-50 border border-gray-200 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2"
            ),
            class_name="w-48"
        ),
        rx.el.div(
            rx.el.label("Mes", class_name="block text-xs font-medium text-gray-500 mb-1"),
            rx.select(
                RecaudacionState.opciones_meses,
                value=RecaudacionState.filtro_mes,
                on_change=RecaudacionState.set_filtro_mes,
                class_name="w-full bg-gray-50 border border-gray-200 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2"
            ),
            class_name="w-48"
        ),
        rx.el.div(
            rx.el.label("Convocatoria", class_name="block text-xs font-medium text-gray-500 mb-1"),
            rx.select(
                RecaudacionState.opciones_convocatorias,
                value=RecaudacionState.filtro_convocatoria,
                on_change=RecaudacionState.set_filtro_convocatoria,
                class_name="w-full bg-gray-50 border border-gray-200 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2"
            ),
            class_name="w-48"
        ),
        rx.el.button(
            rx.icon("refresh-cw", class_name="h-4 w-4 mr-2"),
            "Recargar",
            on_click=RecaudacionState.cargar_datos_recaudacion,
            class_name="ml-auto flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium text-sm transition-colors mt-5",
        ),
        class_name="flex flex-wrap items-center gap-4 bg-white p-4 rounded-xl border border-gray-100 shadow-sm mb-6"
    )

def calendario_heatmap() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="w-12"),
            rx.foreach(
                RecaudacionState.heatmap_dias,
                lambda dia: rx.el.div(dia, class_name="flex-1 text-center text-xs font-bold text-gray-400")
            ),
            class_name="flex w-full mb-2",
        ),
        rx.foreach(
            RecaudacionState.data_heatmap,
            lambda fila: rx.el.div(
                rx.el.div(fila.hora, class_name="w-12 text-xs font-medium text-gray-400 text-right pr-2"),
                rx.foreach(
                    fila.celdas,
                    lambda celda: rx.el.div(
                        rx.el.div(
                            class_name="w-full h-full rounded-md bg-green-500 hover:opacity-100 transition-all cursor-pointer hover:scale-105",
                            style={"opacity": celda.opacity},
                            title=celda.valor + " pagos",
                        ),
                        class_name="flex-1 p-[3px] h-8",
                    )
                ),
                class_name="flex w-full items-center mb-1",
            )
        ),
        class_name="w-full flex flex-col mt-2",
    )

def tabla_ejecutiva() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Facultad", class_name="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50/50 rounded-tl-lg"),
                    rx.el.th("Recaudado (S/)", class_name="px-4 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50/50"),
                    rx.el.th("Validados", class_name="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50/50"),
                    rx.el.th("Pend. / Obs.", class_name="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50/50"),
                    rx.el.th("Efectividad", class_name="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50/50 rounded-tr-lg"),
                ),
            ),
            rx.el.tbody(
                rx.foreach(
                    RecaudacionState.data_tabla_ejecutiva,
                    lambda row: rx.el.tr(
                        rx.el.td(rx.el.span(row.facultad, class_name="font-semibold text-gray-800"), class_name="px-4 py-3 border-b border-gray-50 text-sm"),
                        rx.el.td(rx.el.span(f"S/ {row.total_recaudado}", class_name="font-bold text-green-600"), class_name="px-4 py-3 border-b border-gray-50 text-right text-sm"),
                        rx.el.td(rx.el.span(row.pagos_validados, class_name="text-gray-600"), class_name="px-4 py-3 border-b border-gray-50 text-center text-sm"),
                        rx.el.td(
                            rx.el.span(f"{row.pagos_pendientes} / {row.pagos_observados}", class_name="text-orange-500 font-medium"), 
                            class_name="px-4 py-3 border-b border-gray-50 text-center text-sm"
                        ),
                        rx.el.td(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.div(class_name="h-2 bg-blue-500 rounded-full", style={"width": f"{row.porcentaje_validado}%"}),
                                    class_name="w-full bg-gray-100 rounded-full h-2 mt-1 mr-2"
                                ),
                                rx.el.span(f"{row.porcentaje_validado}%", class_name="text-xs text-gray-500 font-medium w-8"),
                                class_name="flex items-center"
                            ),
                            class_name="px-4 py-3 border-b border-gray-50 text-sm min-w-[120px]"
                        ),
                        class_name="hover:bg-gray-50/30 transition-colors",
                    ),
                ),
            ),
            class_name="w-full text-left border-collapse",
        ),
        class_name="overflow-x-auto"
    )

def recaudacion_view() -> rx.Component:
    """Vista principal del Dashboard Ejecutivo Financiero"""
    return rx.el.div(
        panel_filtros(),
        
        # Grid Principal: Sidebar (KPIs/Alertas) + Main (Gráficos)
        rx.el.div(
            # Columna Izquierda: KPIs y Alertas
            rx.el.div(
                stat_card("Total Recaudado", f"S/ {RecaudacionState.kpi_total_recaudado}", "Ingreso global", "wallet", "green"),
                stat_card("Estatal", f"S/ {RecaudacionState.kpi_recaudacion_estatal}", "Colegios Estatales", "school", "blue"),
                stat_card("Privado", f"S/ {RecaudacionState.kpi_recaudacion_privada}", "Colegios Privados", "building", "orange"),
                panel_alertas(),
                class_name="flex flex-col gap-6 lg:col-span-1"
            ),
            
            # Columna Derecha: Gráficos
            rx.el.div(
                # Fila 1: Gauges y Dona
                rx.el.div(
                    gauge_half_donut(RecaudacionState.data_meta_recaudacion, "1. Meta de Recaudación"),
                    gauge_half_donut(RecaudacionState.data_morosidad, "2. Índice de Morosidad"),
                    chart_card(
                        "3. Estado de los Pagos",
                        rx.recharts.pie_chart(
                            rx.recharts.pie(
                                data=RecaudacionState.data_estado_pagos,
                                data_key="value", name_key="name", cx="50%", cy="40%",
                                inner_radius=25, outer_radius=45, label=True
                            ),
                            rx.recharts.tooltip(), 
                            rx.recharts.legend(vertical_align="bottom", height=40), 
                            height=220
                        )
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6"
                ),
                
                # Fila 2: Líneas y Área
                rx.el.div(
                    chart_card(
                        "4. Evolución de la Recaudación",
                        rx.recharts.line_chart(
                            rx.recharts.line(data_key="monto", type_="monotone", stroke="#10b981", stroke_width=3, dot=False),
                            rx.recharts.x_axis(data_key="fecha", tick_line=False, axis_line=False, min_tick_gap=20),
                            rx.recharts.y_axis(tick_line=False, axis_line=False),
                            rx.recharts.tooltip(),
                            rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
                            data=RecaudacionState.data_evolucion_recaudacion, height=280
                        ),
                        col_span=2
                    ),
                    chart_card(
                        "5. Evolución de Pagos",
                        rx.recharts.area_chart(
                            rx.recharts.area(data_key="cantidad", type_="monotone", stroke="#3b82f6", fill="#93c5fd"),
                            rx.recharts.x_axis(data_key="mes", tick_line=False, axis_line=False, min_tick_gap=15),
                            rx.recharts.y_axis(tick_line=False, axis_line=False),
                            rx.recharts.tooltip(),
                            data=RecaudacionState.data_evolucion_pagos, height=280
                        ),
                        col_span=1
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6"
                ),
                
                # Fila 3: Comparativas
                rx.el.div(
                    chart_card(
                        "6. Ingresos Estatales vs Privados",
                        rx.recharts.area_chart(
                            rx.recharts.area(data_key="estatal", stroke="#2563eb", fill="#2563eb", stack_id="1"),
                            rx.recharts.area(data_key="privado", stroke="#f59e0b", fill="#f59e0b", stack_id="1"),
                            rx.recharts.x_axis(data_key="mes"), rx.recharts.y_axis(),
                            rx.recharts.tooltip(), rx.recharts.legend(),
                            data=RecaudacionState.data_comparacion_colegio, height=300
                        ),
                        col_span=2
                    ),
                    chart_card(
                        "7. Comparación por Convocatoria",
                        rx.recharts.bar_chart(
                            rx.recharts.bar(data_key="estatal", fill="#2563eb", name="Estatal"),
                            rx.recharts.bar(data_key="privado", fill="#f59e0b", name="Privado"),
                            rx.recharts.x_axis(data_key="convocatoria"), rx.recharts.y_axis(),
                            rx.recharts.tooltip(), rx.recharts.legend(),
                            data=RecaudacionState.data_comparacion_convocatoria, height=300
                        ),
                        col_span=1
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6"
                ),
                
                # Fila 4: Facultades y Conceptos
                rx.el.div(
                    chart_card(
                        "8. Recaudación por Facultad",
                        rx.recharts.bar_chart(
                            rx.recharts.bar(data_key="monto", fill="#14b8a6", radius=[0, 4, 4, 0]),
                            rx.recharts.x_axis(type_="number"),
                            rx.recharts.y_axis(data_key="facultad", type_="category", width=120),
                            rx.recharts.tooltip(),
                            layout="vertical",
                            data=RecaudacionState.data_recaudacion_facultad, height=300
                        ),
                        col_span=2
                    ),
                    chart_card(
                        "9. Ingresos por Concepto",
                        rx.recharts.pie_chart(
                            rx.recharts.pie(
                                data=RecaudacionState.data_ingresos_concepto,
                                data_key="value", name_key="name", cx="50%", cy="50%",
                                inner_radius=50, outer_radius=80, label=True
                            ),
                            rx.recharts.tooltip(), rx.recharts.legend(vertical_align="bottom"), height=300
                        ),
                        col_span=1
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6"
                ),
                
                # Fila 5: Embudo y Promedio
                rx.el.div(
                    chart_card(
                        "10. Embudo Financiero",
                        rx.recharts.bar_chart(
                            rx.recharts.bar(data_key="value", fill="#8b5cf6", radius=[0, 4, 4, 0]),
                            rx.recharts.x_axis(type_="number"),
                            rx.recharts.y_axis(data_key="name", type_="category", width=100),
                            rx.recharts.tooltip(),
                            layout="vertical",
                            data=RecaudacionState.data_embudo, height=250
                        ),
                        col_span=1
                    ),
                    chart_card(
                        "11. Tendencia Promedio por Postulante",
                        rx.recharts.line_chart(
                            rx.recharts.line(data_key="promedio", type_="monotone", stroke="#8b5cf6", stroke_width=2),
                            rx.recharts.x_axis(data_key="mes"), rx.recharts.y_axis(domain=['auto', 'auto']),
                            rx.recharts.tooltip(), rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                            data=RecaudacionState.data_tendencia_promedio, height=250
                        ),
                        col_span=2
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6"
                ),
                
                # Fila 6: Heatmap y Ranking
                rx.el.div(
                    chart_card(
                        "12. Calendario de Pagos (HeatMap)",
                        calendario_heatmap(),
                        col_span=2
                    ),
                    chart_card(
                        "13. Top Carreras (Ranking)",
                        rx.recharts.bar_chart(
                            rx.recharts.bar(data_key="monto", fill="#ec4899", radius=[0, 4, 4, 0]),
                            rx.recharts.x_axis(type_="number"),
                            rx.recharts.y_axis(data_key="carrera", type_="category", width=120, tick={"fontSize": 10}),
                            rx.recharts.tooltip(),
                            layout="vertical",
                            data=RecaudacionState.data_ranking_carreras, height=300
                        ),
                        col_span=1
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6"
                ),
                
                # Fila 7: Tabla Ejecutiva
                chart_card(
                    "14. Tabla Ejecutiva de Facultades",
                    tabla_ejecutiva(),
                    col_span=3
                ),
                
                class_name="lg:col-span-3 flex flex-col"
            ),
            class_name="grid grid-cols-1 lg:grid-cols-4 gap-6"
        ),
        
        class_name="p-4 md:p-6 bg-gray-50/50 min-h-screen",
    )
