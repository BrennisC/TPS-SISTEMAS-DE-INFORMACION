import reflex as rx


def stats_card(
    title: str, value: str, icon: str, color: str, subtitle: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name=f"h-6 w-6 text-{color}-600"),
                class_name=f"p-3 rounded-xl bg-{color}-50",
            ),
            rx.el.div(
                rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
                rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.span(
                subtitle, class_name="text-xs text-gray-400 font-medium"
            ),
            class_name="mt-4 pt-4 border-t border-gray-50",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )