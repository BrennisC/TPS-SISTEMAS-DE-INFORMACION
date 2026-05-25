import reflex as rx
from sistema_admisi_n_unas.states.auth_state import AuthState


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("graduation-cap", class_name="h-6 w-6 text-[#003366]"),
                class_name="p-2.5 rounded-xl bg-blue-50 w-fit",
            ),
            rx.el.div(
                rx.el.h2(
                    "UNAS Admisión",
                    class_name="text-xl font-bold text-[#003366]",
                ),
                rx.el.p(
                    "Ingresa tus credenciales para continuar",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-4 mb-6",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Usuario",
                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                ),
                rx.el.input(
                    placeholder="admin",
                    default_value=AuthState.username,
                    on_change=AuthState.set_username.debounce(300),
                    class_name="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.label(
                    "Contraseña",
                    class_name="block text-sm font-semibold text-gray-700 mb-2",
                ),
                rx.el.input(
                    placeholder="••••••••",
                    type="password",
                    default_value=AuthState.password,
                    on_change=AuthState.set_password.debounce(300),
                    class_name="w-full px-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-[#003366] focus:ring-2 focus:ring-[#003366]/10 transition-all",
                ),
                class_name="flex flex-col",
            ),
            rx.el.button(
                rx.icon("log-in", class_name="h-4 w-4 mr-2"),
                "Ingresar",
                type="submit",
                disabled=~AuthState.form_valid,
                class_name=rx.cond(
                    AuthState.form_valid,
                    "flex items-center justify-center w-full px-5 py-2.5 rounded-xl text-sm font-semibold text-white bg-[#228B22] hover:bg-[#1a6b1a] transition-colors shadow-sm",
                    "flex items-center justify-center w-full px-5 py-2.5 rounded-xl text-sm font-semibold text-white bg-gray-300 cursor-not-allowed",
                ),
            ),
            on_submit=AuthState.login,
            reset_on_submit=False,
            class_name="flex flex-col gap-4",
        ),
        class_name="bg-white rounded-2xl border border-gray-200 p-8 shadow-sm w-full",
    )
