import reflex as rx


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    is_authenticated: bool = False

    @rx.var
    def form_valid(self) -> bool:
        return self.username.strip() != "" and self.password.strip() != ""

    @rx.event
    def set_username(self, v: str):
        self.username = v

    @rx.event
    def set_password(self, v: str):
        self.password = v

    @rx.event
    def login(self):
        if self.username == "admin" and self.password == "admin123":
            self.is_authenticated = True
            self.password = ""
            return rx.redirect("/")
        return rx.toast("Usuario o contraseña incorrectos", duration=3000)

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        return rx.redirect("/login")
