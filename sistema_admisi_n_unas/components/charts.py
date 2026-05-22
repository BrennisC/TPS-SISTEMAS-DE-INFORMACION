import reflex as rx

from ..states.dashboard_state import DashboardState


def grafico_postulantes_vs_ingresantes():
    return rx.el.div(
        rx.el.h3(
            "Postulantes vs Ingresantes por Carrera",
            class_name="text-sm font-bold text-gray-700 mb-4",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3", vertical=False),
            rx.recharts.x_axis(data_key="carrera", custom_attrs={"fontSize": "9px"}),
            rx.recharts.y_axis(custom_attrs={"fontSize": "11px"}),
            rx.recharts.graphing_tooltip(),
            rx.recharts.legend(),
            rx.recharts.bar(
                data_key="Postulantes", fill="#228B22", radius=[4, 4, 0, 0]
            ),
            rx.recharts.bar(
                data_key="Ingresantes", fill="#FFB020", radius=[4, 4, 0, 0]
            ),
            data=DashboardState.chart_postulantes_vs_ingresantes,
            height=220,
            width="100%",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2",
    )


def grafico_rendimiento_areas():
    return rx.el.div(
        rx.el.h3(
            "Rendimiento Promedio por Facultad",
            class_name="text-sm font-bold text-gray-700 mb-4",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.x_axis(data_key="area", custom_attrs={"fontSize": "10px"}),
            rx.recharts.y_axis(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.area(
                data_key="avg_score", fill="#E8F5E9", stroke="#228B22", stroke_width=2
            ),
            data=DashboardState.chart_rendimiento_areas,
            height=200,
            width="100%",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1 lg:col-span-2",
    )


def grafico_evolucion_historica():
    return rx.el.div(
        rx.el.h3(
            "Tendencia de Postulantes por Convocatoria",
            class_name="text-sm font-bold text-gray-700 mb-4",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.x_axis(data_key="year", custom_attrs={"fontSize": "11px"}),
            rx.recharts.y_axis(),
            rx.recharts.graphing_tooltip(),
            rx.recharts.area(
                data_key="Postulantes", fill="#E1F5FE", stroke="#0288D1", stroke_width=2
            ),
            data=DashboardState.chart_evolucion_historica,
            height=200,
            width="100%",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )


def grafico_distribucion_colegios():
    return rx.el.div(
        rx.el.h3(
            "Procedencia de Postulantes (Colegio)",
            class_name="text-sm font-bold text-gray-700 mb-4",
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=DashboardState.chart_genero,  # Contiene la data procesada de tipo_colegio
                    data_key="value",
                    name_key="name",
                    inner_radius=55,
                    outer_radius=80,
                    padding_angle=2,
                ),
                rx.recharts.graphing_tooltip(),
                height=160,
                width="100%",
            ),
            class_name="relative flex items-center justify-center h-40",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm col-span-1",
    )
