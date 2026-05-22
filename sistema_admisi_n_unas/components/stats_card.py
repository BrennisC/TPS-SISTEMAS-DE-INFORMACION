import reflex as rx


def stats_card(
    title: str, value: str, subtext: str, icon_name: str, color_hex: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    title,
                    class_name="text-xs font-medium text-gray-500 uppercase tracking-wider",
                ),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mt-1"),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.icon(icon_name, size=20, color=color_hex),
                class_name=f"p-3 rounded-xl bg-gray-50",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.p(
            subtext,
            class_name="text-xs text-green-600 font-medium mt-4 flex items-center gap-1",
        ),
        class_name="bg-white p-5 rounded-2xl border border-gray-100 shadow-sm flex flex-col justify-between",
    )
