import reflex as rx
from sistema_admisi_n_unas.components.sidebar import sidebar


def page_header(title: str, subtitle: str, icon: str) -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-5 w-5 text-[#228B22]"),
                class_name="p-2.5 rounded-xl bg-green-50 w-fit",
            ),
            rx.el.div(
                rx.el.h1(title, class_name="text-2xl font-bold text-gray-900"),
                rx.el.p(subtitle, class_name="text-sm text-gray-500"),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="mb-8",
    )