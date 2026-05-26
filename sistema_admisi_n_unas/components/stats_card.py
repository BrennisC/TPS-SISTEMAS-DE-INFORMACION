import reflex as rx


def stats_card(
    title: str, value: str, subtext: str, icon_name: str, color_hex: str
) -> rx.Component:
    """Stats card mejorado con mejor diseño visual."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon_name, size=24, color="white"),
                class_name="p-3 rounded-xl shadow-sm",
                style={"backgroundColor": color_hex},
            ),
            rx.el.div(
                rx.el.p(
                    title,
                    class_name="text-xs font-medium text-gray-500 uppercase tracking-wider",
                ),
                rx.el.h3(value, class_name="text-2xl font-extrabold text-gray-900 mt-1"),
                class_name="flex flex-col flex-1",
            ),
            class_name="flex items-start justify-between gap-4",
        ),
        rx.el.div(
            rx.el.div(
                class_name="h-0.5 w-full rounded-full bg-gray-100 mb-3",
            ),
            rx.el.p(
                subtext,
                class_name="text-xs text-gray-500 font-medium flex items-center gap-1.5",
            ),
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow cursor-default group",
        style={"minHeight": "140px"},
    )


def mini_stat_card(title: str, value: str, icon: str, color: str) -> rx.Component:
    """Mini tarjeta de estadísticas para usar en espacios reducidos."""
    colors_map = {
        "green": "bg-green-50 text-green-600 border-green-100",
        "blue": "bg-blue-50 text-blue-600 border-blue-100",
        "amber": "bg-amber-50 text-amber-600 border-amber-100",
        "red": "bg-red-50 text-red-600 border-red-100",
        "purple": "bg-purple-50 text-purple-600 border-purple-100",
    }
    active = colors_map.get(color, colors_map["green"])
    return rx.el.div(
        rx.icon(icon, class_name=f"h-4 w-4 {active.split()[1]}"),
        rx.el.div(
            rx.el.p(title, class_name="text-xs text-gray-500"),
            rx.el.p(value, class_name="text-lg font-bold text-gray-900"),
        ),
        class_name=f"flex items-center gap-3 p-3 bg-white rounded-xl border {active} shadow-sm hover:shadow transition-shadow",
    )


def trend_indicator(value: str, trend: str, positive: bool = True) -> rx.Component:
    """Indicador de tendencia con flecha hacia arriba o abajo."""
    return rx.el.div(
        rx.icon(
            "trending-up" if positive else "trending-down",
            class_name=f"h-4 w-4 { 'text-green-500' if positive else 'text-red-500'}",
        ),
        rx.el.span(
            f"{trend}%",
            class_name=f"text-xs font-semibold { 'text-green-600' if positive else 'text-red-600'}",
        ),
        rx.el.span(
            value,
            class_name="text-xs text-gray-600 font-medium",
        ),
        class_name="flex items-center gap-2",
    )