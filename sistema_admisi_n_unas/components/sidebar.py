import reflex as rx

from sistema_admisi_n_unas.states.auth_state import AuthState
from sistema_admisi_n_unas.states.dashboard_state import DashboardState

SIDEBAR_ITEMS = [
    {"label": "Dashboard", "icon": "layout-dashboard", "href": "/"},
    {
        "label": "Admisión",
        "icon": "users",
        "children": [
            {"label": "Postulantes", "icon": "users", "href": "/postulantes"},
            {"label": "Inscripción", "icon": "user-plus", "href": "/inscripcion"},
            {"label": "Examen", "icon": "file-pen", "href": "/examen"},
            {"label": "Resultados", "icon": "trophy", "href": "/resultados"},
            {"label": "Ingresantes", "icon": "bar-chart-3", "href": "/ingresantes"},
        ],
    },
    {
        "label": "Finanzas",
        "icon": "wallet",
        "children": [
            {"label": "Recaudación", "icon": "wallet", "href": "/recaudacion"},
            {"label": "Tesorería", "icon": "receipt", "href": "/tesoreria"},
        ],
    },
    {
        "label": "Servicios",
        "icon": "book-open",
        "children": [
            {"label": "Biblioteca", "icon": "book-open", "href": "/biblioteca"},
            {
                "label": "Retroalimentación",
                "icon": "message-square",
                "href": "/retroalimentacion",
            },
        ],
    },
]


def nav_item(item: dict) -> rx.Component:
    """Navigation item with hover effects and active state."""
    if item.get("children"):
        label = item["label"]
        is_expanded = DashboardState.expanded_sidebar.contains(label)
        return rx.vstack(
            rx.el.button(
                rx.hstack(
                    rx.hstack(
                        rx.icon(item["icon"], color="black"),
                        rx.text(item["label"], color="black"),
                        align="center",
                        spacing="3",
                    ),
                    rx.icon(
                        rx.cond(is_expanded, "chevron-down", "chevron-right"),
                        size=16,
                        color="black",
                    ),
                    width="100%",
                    align="center",
                    justify="between",
                ),
                on_click=DashboardState.toggle_sidebar_section(label),
                class_name="w-full rounded-lg px-2 py-2 hover:bg-gray-100 transition-colors",
            ),
            rx.cond(
                is_expanded,
                rx.vstack(
                    *[
                        rx.link(
                            rx.hstack(
                                rx.icon(child["icon"], size=16, color="black"),
                                rx.text(child["label"], color="black"),
                                padding="10px 12px",
                                margin_left="20px",
                                border_radius="8px",
                                _hover={"background": "#f0f0f0"},
                                spacing="3",
                            ),
                            href=child["href"],
                            width="100%",
                        )
                        for child in item["children"]
                    ],
                    width="100%",
                    spacing="2",
                ),
            ),
            width="100%",
            align_items="start",
            spacing="2",
        )

    return rx.link(
        rx.hstack(
            rx.icon(item["icon"], color="black"),
            rx.text(item["label"], color="black"),
            padding="12px",
            border_radius="8px",
            _hover={"background": "#0000"},
            spacing="3",
        ),
        href=item["href"],
        width="100%",
    )


def render_sidebar_items() -> list[rx.Component]:
    """Render static sidebar items without Reflex foreach typing issues."""
    return [nav_item(item) for item in SIDEBAR_ITEMS]


def sidebar() -> rx.Component:
    """Main sidebar component with improved styling."""
    return rx.el.aside(
        rx.el.div(
            # Logo Section
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                "./admision.jpg",
                                class_name="h-8 w-8 rounded-xl",
                            ),
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
                        class_name="flex items-center gap-3 p-4",
                    ),
                    href="/",
                    class_name="block",
                ),
                class_name="border-b border-gray-200",
            ),
            # Navigation
            rx.el.nav(
                rx.el.div(
                    rx.el.p(
                        "MENÚ PRINCIPAL",
                        class_name="px-4 text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2",
                    ),
                    *render_sidebar_items(),
                    class_name="flex flex-col gap-3 p-4",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            # Footer / User Info
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src="https://api.dicebear.com/9.x/notionists/svg?seed=Admin",
                            class_name="h-10 w-10 rounded-full bg-gray-200 border-2 border-gray-200",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Administrador",
                                class_name="text-sm font-bold text-gray-900",
                            ),
                            rx.el.p(
                                "Sistemas UNAS",
                                class_name="text-xs text-gray-500",
                            ),
                            class_name="flex flex-col",
                        ),
                        class_name="flex items-center gap-3 p-3 bg-gradient-to-r from-gray-50 to-white rounded-xl border border-gray-200 shadow-sm",
                    ),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4 mr-2"),
                        "Cerrar sesión",
                        on_click=AuthState.logout,
                        class_name="flex items-center justify-center w-full px-4 py-2.5 mt-2 rounded-xl text-sm font-semibold text-red-600 bg-red-50 hover:bg-red-100 border border-red-100 transition-colors",
                    ),
                ),
                class_name="p-4 border-t border-gray-100",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex flex-col w-72 h-screen sticky top-0 border-r border-gray-200 bg-gradient-to-b from-gray-50 to-white",
        style={"background": "linear-gradient(180deg, #fafbfd 0%, #ffffff 100%)"},
    )


def mobile_sidebar() -> rx.Component:
    """Sidebar para móvil que se abre en overlay con mejor estilo."""
    return rx.cond(
        DashboardState.mobile_menu_open,
        rx.el.div(
            # Overlay oscuro con blur
            rx.el.div(
                on_click=DashboardState.close_mobile_menu,
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40",
            ),
            # Sidebar móvil
            rx.el.div(
                rx.el.div(
                    # Logo Section
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "graduation-cap",
                                    class_name="h-8 w-8 text-white",
                                ),
                                class_name="p-2 rounded-xl bg-[#003366]",
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
                            rx.icon("x", class_name="h-6 w-6 text-gray-500"),
                            on_click=DashboardState.close_mobile_menu,
                            class_name="p-2 hover:bg-gray-200 rounded-lg transition-colors",
                        ),
                        class_name="flex items-center justify-between p-4 border-b border-gray-200",
                    ),
                    # Navigation
                    rx.el.nav(
                        rx.el.div(
                            *render_sidebar_items(),
                            class_name="flex flex-col gap-3 p-4",
                        ),
                        class_name="flex-1 overflow-y-auto",
                    ),
                    # Footer
                    rx.el.div(
                        rx.el.button(
                            rx.icon("log-out", class_name="h-4 w-4 mr-2"),
                            "Cerrar sesión",
                            on_click=AuthState.logout,
                            class_name="flex items-center justify-center w-full px-4 py-2.5 rounded-xl text-sm font-semibold text-red-600 bg-red-50 hover:bg-red-100 border border-red-100 transition-colors",
                        ),
                        class_name="p-4 border-t border-gray-200",
                    ),
                    class_name="flex flex-col h-full max-h-screen bg-white",
                ),
                class_name="fixed left-0 top-0 w-72 border-r border-gray-200 h-screen z-50 shadow-2xl overflow-y-auto",
            ),
        ),
    )


def mobile_header() -> rx.Component:
    """Header con botón hamburguesa mejorado para móvil."""
    return rx.el.div(
        rx.el.button(
            rx.icon(
                "menu",
                class_name="h-6 w-6 text-[#003366]",
            ),
            on_click=DashboardState.toggle_mobile_menu,
            class_name="p-2.5 hover:bg-gray-100 rounded-xl transition-colors border border-gray-200 bg-white shadow-sm",
        ),
        rx.el.div(
            rx.icon(
                "graduation-cap",
                class_name="h-6 w-6 text-[#003366]",
            ),
            rx.el.span(
                "UNAS Admisión",
                class_name="font-bold text-[#003366]",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.div(
            rx.image(
                src="https://api.dicebear.com/9.x/notionists/svg?seed=Admin",
                class_name="h-8 w-8 rounded-full border-2 border-gray-200",
            ),
            class_name="flex items-center",
        ),
        class_name="md:hidden flex items-center justify-between p-4 bg-white border-b border-gray-200 shadow-sm",
    )
