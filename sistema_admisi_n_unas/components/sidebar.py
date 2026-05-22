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
                "h-5 w-5 text-gray-600 group-hover:text-[#003366]",
            ),
        ),
        rx.el.span(item["label"]),
        href=item["href"],
        on_click=[lambda: DashboardState.set_page(item["label"]), DashboardState.close_mobile_menu],
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-4 py-3 rounded-xl bg-[#003366] text-white font-semibold transition-all shadow-md",
            "flex items-center gap-3 px-4 py-3 rounded-xl text-gray-700 hover:bg-gray-100 hover:text-[#003366] font-semibold transition-all group",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            # Logo Section
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "graduation-cap", class_name="h-8 w-8 text-[#003366]"
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
                class_name="border-b border-gray-200",
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
                        class_name="h-10 w-10 rounded-full bg-gray-200",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Administrador",
                            class_name="text-sm font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Sistemas UNAS", class_name="text-xs text-gray-600"
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3 p-4 bg-gray-100 rounded-2xl border border-gray-300",
                ),
                class_name="p-4",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex flex-col w-72 h-screen sticky top-0 border-r border-gray-200",
        style={"backgroundColor": "#fafbfd"},
    )


def mobile_sidebar() -> rx.Component:
    """Sidebar para móvil que se abre en overlay"""
    return rx.cond(
        DashboardState.mobile_menu_open,
        rx.el.div(
            # Overlay oscuro
            rx.el.div(
                on_click=DashboardState.close_mobile_menu,
                class_name="fixed inset-0 bg-black/50 z-40",
            ),
            # Sidebar móvil
            rx.el.div(
                rx.el.div(
                    # Logo Section
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "graduation-cap", class_name="h-8 w-8 text-[#003366]"
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
                            class_name="flex items-center gap-3",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-6 w-6 text-gray-700"),
                            on_click=DashboardState.close_mobile_menu,
                            class_name="p-1 hover:bg-gray-200 rounded-lg transition-colors",
                        ),
                        class_name="flex items-center justify-between p-4 border-b border-gray-200",
                    ),
                    # Navigation
                    rx.el.nav(
                        rx.el.div(
                            rx.foreach(DashboardState.sidebar_items, nav_item),
                            class_name="flex flex-col gap-2 p-4",
                        ),
                        class_name="flex-1 overflow-y-auto",
                    ),
                    class_name="flex flex-col h-full max-h-screen",
                ),
                class_name="fixed left-0 top-0 w-64 border-r border-gray-200 h-screen z-50 shadow-lg overflow-y-auto",
                style={"backgroundColor": "#fafbfd"},
            ),
        ),
    )