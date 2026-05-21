import reflex as rx
from sistema_admisi_n_unas.states.dashboard_state import DashboardState


def nav_item(item: dict) -> rx.Component:
    is_active = DashboardState.current_page == item["label"]
    return rx.el.a(
        rx.icon(
            item["icon"],
            class_name=rx.cond(
                is_active,
                "h-5 w-5 text-white",
                "h-5 w-5 text-gray-400 group-hover:text-[#228B22]",
            ),
        ),
        rx.el.span(item["label"]),
        href=item["href"],
        on_click=lambda: DashboardState.set_page(item["label"]),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-4 py-3 rounded-xl bg-[#003366] text-white font-semibold transition-all shadow-md",
            "flex items-center gap-3 px-4 py-3 rounded-xl text-gray-500 hover:bg-gray-50 hover:text-[#003366] font-medium transition-all group",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            # Logo Section
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "graduation-cap", class_name="h-8 w-8 text-[#228B22]"
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "UNAS",
                            class_name="text-xl font-bold text-[#003366] leading-none",
                        ),
                        rx.el.span(
                            "Admisión",
                            class_name="text-[10px] uppercase tracking-widest text-[#228B22] font-bold",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3 p-6",
                ),
                class_name="border-b border-gray-100",
            ),
            # Navigation
            rx.el.nav(
                rx.el.div(
                    rx.foreach(DashboardState.sidebar_items, nav_item),
                    class_name="flex flex-col gap-2 p-4",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            # Footer / User Info
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="https://api.dicebear.com/9.x/notionists/svg?seed=Admin",
                        class_name="h-10 w-10 rounded-full bg-gray-100",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Administrador",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Sistemas UNAS", class_name="text-xs text-gray-500"
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3 p-4 bg-gray-50 rounded-2xl border border-gray-100",
                ),
                class_name="p-4",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex flex-col w-72 bg-white border-r border-gray-200 h-screen sticky top-0",
    )