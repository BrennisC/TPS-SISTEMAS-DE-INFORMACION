from datetime import date, timedelta
from typing import TypedDict

import reflex as rx

from ..utils.csv_loader import (
    cargar_libros,
    cargar_postulantes,
    cargar_prestamos,
    guardar_libros,
    guardar_prestamos,
)


class Libro(TypedDict):
    id: int
    codigo: str
    titulo: str
    autor: str
    categoria: str
    editorial: str
    stock: int
    disponibles: int
    estado: str
    prestamos_total: int


class Prestamo(TypedDict):
    id: int
    dni_lector: str
    lector: str
    libro_codigo: str
    libro: str
    fecha_prestamo: str
    fecha_devolucion: str
    estado: str


class BibliotecaState(rx.State):
    catalogo: list[Libro] = []
    prestamos: list[Prestamo] = []
    lectores: list[dict] = []
    total_lectores: int = 0
    prestamos_activos: int = 0
    prestamos_vencidos: int = 0
    f_codigo: str = ""
    f_titulo: str = ""
    f_autor: str = ""
    f_categoria: str = ""
    f_editorial: str = ""
    f_stock: str = "1"
    f_dni_lector: str = ""
    f_libro_codigo: str = ""
    mensaje: str = ""
    show_add_book_modal: bool = False
    show_loan_modal: bool = False
    catalogo_page: int = 1
    prestamos_page: int = 1
    page_size: int = 8

    @rx.event
    def cargar_biblioteca(self):
        postulantes = cargar_postulantes()
        self.lectores = [
            postulante
            for postulante in postulantes
            if postulante["estado"].strip().lower() == "ingresante"
        ]
        self.catalogo = cargar_libros()
        self.prestamos = cargar_prestamos()
        self.catalogo_page = 1
        self.prestamos_page = 1
        self._actualizar_resumen()

    def _actualizar_resumen(self):
        self.total_lectores = len({prestamo["dni_lector"] for prestamo in self.prestamos})
        self.prestamos_activos = sum(
            1 for prestamo in self.prestamos if prestamo["estado"] == "Prestado"
        )
        self.prestamos_vencidos = sum(
            1 for prestamo in self.prestamos if prestamo["estado"] == "Vencido"
        )

    def _buscar_lector(self, dni: str) -> dict | None:
        for lector in self.lectores:
            if lector["dni"] == dni:
                return lector
        return None

    def _buscar_libro(self, codigo: str) -> Libro | None:
        for libro in self.catalogo:
            if libro["codigo"].lower() == codigo.lower():
                return libro
        return None

    @rx.event
    def set_codigo(self, value: str):
        self.f_codigo = value.strip()

    @rx.event
    def set_titulo(self, value: str):
        self.f_titulo = value.strip()

    @rx.event
    def set_autor(self, value: str):
        self.f_autor = value.strip()

    @rx.event
    def set_categoria(self, value: str):
        self.f_categoria = value.strip()

    @rx.event
    def set_editorial(self, value: str):
        self.f_editorial = value.strip()

    @rx.event
    def set_stock(self, value: str):
        self.f_stock = value.strip()

    @rx.event
    def set_dni_lector(self, value: str):
        self.f_dni_lector = value.strip()

    @rx.event
    def set_libro_codigo(self, value: str):
        self.f_libro_codigo = value.strip()

    @rx.event
    def open_add_book_modal(self):
        self.mensaje = ""
        self.show_add_book_modal = True

    @rx.event
    def close_add_book_modal(self):
        self.show_add_book_modal = False

    @rx.event
    def open_loan_modal(self):
        self.mensaje = ""
        self.show_loan_modal = True

    @rx.event
    def close_loan_modal(self):
        self.show_loan_modal = False

    @rx.event
    def agregar_libro(self):
        if any(libro["codigo"].lower() == self.f_codigo.lower() for libro in self.catalogo):
            self.mensaje = "Ya existe un libro con ese código."
            return
        try:
            stock = int(self.f_stock)
        except ValueError:
            self.mensaje = "El stock debe ser numérico."
            return
        if stock < 1 or not self.f_codigo or not self.f_titulo:
            self.mensaje = "Completa código, título y stock válido."
            return

        libro: Libro = {
            "id": max([libro["id"] for libro in self.catalogo], default=0) + 1,
            "codigo": self.f_codigo,
            "titulo": self.f_titulo,
            "autor": self.f_autor,
            "categoria": self.f_categoria or "General",
            "editorial": self.f_editorial,
            "stock": stock,
            "disponibles": stock,
            "estado": "Disponible",
            "prestamos_total": 0,
        }
        self.catalogo.append(libro)
        guardar_libros(self.catalogo)
        self.f_codigo = ""
        self.f_titulo = ""
        self.f_autor = ""
        self.f_categoria = ""
        self.f_editorial = ""
        self.f_stock = "1"
        self.mensaje = "Libro agregado al catálogo."
        self.show_add_book_modal = False
        self.catalogo_page = self.catalogo_total_pages

    @rx.event
    def registrar_prestamo(self):
        if not self.lectores:
            postulantes = cargar_postulantes()
            self.lectores = [
                postulante
                for postulante in postulantes
                if postulante["estado"].strip().lower() == "ingresante"
            ]
        lector = self._buscar_lector(self.f_dni_lector)
        libro = self._buscar_libro(self.f_libro_codigo)
        if lector is None:
            self.mensaje = "Solo los ingresantes pueden registrarse como lectores."
            return
        if libro is None:
            self.mensaje = "No se encontró un libro con ese código."
            return
        if libro["disponibles"] < 1:
            self.mensaje = "El libro no tiene ejemplares disponibles."
            return

        prestamo: Prestamo = {
            "id": max([p["id"] for p in self.prestamos], default=0) + 1,
            "dni_lector": lector["dni"],
            "lector": f"{lector['nombres']} {lector['apellidos']}",
            "libro_codigo": libro["codigo"],
            "libro": libro["titulo"],
            "fecha_prestamo": date.today().isoformat(),
            "fecha_devolucion": (date.today() + timedelta(days=7)).isoformat(),
            "estado": "Prestado",
        }
        libro["disponibles"] -= 1
        libro["prestamos_total"] += 1
        libro["estado"] = "Prestado" if libro["disponibles"] == 0 else "Disponible"
        self.prestamos.append(prestamo)
        guardar_libros(self.catalogo)
        guardar_prestamos(self.prestamos)
        self._actualizar_resumen()
        self.f_dni_lector = ""
        self.f_libro_codigo = ""
        self.mensaje = "Préstamo registrado."
        self.show_loan_modal = False
        self.prestamos_page = self.prestamos_total_pages

    @rx.event
    def devolver_prestamo(self, prestamo_id: int):
        for prestamo in self.prestamos:
            if prestamo["id"] == prestamo_id and prestamo["estado"] == "Prestado":
                prestamo["estado"] = "Devuelto"
                libro = self._buscar_libro(prestamo["libro_codigo"])
                if libro:
                    libro["disponibles"] = min(libro["stock"], libro["disponibles"] + 1)
                    libro["estado"] = "Disponible"
                break
        guardar_libros(self.catalogo)
        guardar_prestamos(self.prestamos)
        self._actualizar_resumen()
        self.mensaje = "Libro devuelto."

    @rx.event
    def next_catalogo_page(self):
        if self.catalogo_page < self.catalogo_total_pages:
            self.catalogo_page += 1

    @rx.event
    def prev_catalogo_page(self):
        if self.catalogo_page > 1:
            self.catalogo_page -= 1

    @rx.event
    def next_prestamos_page(self):
        if self.prestamos_page < self.prestamos_total_pages:
            self.prestamos_page += 1

    @rx.event
    def prev_prestamos_page(self):
        if self.prestamos_page > 1:
            self.prestamos_page -= 1

    @rx.var
    def total_libros(self) -> int:
        return len(self.catalogo)

    @rx.var
    def total_stock(self) -> int:
        return sum(libro["stock"] for libro in self.catalogo)

    @rx.var
    def total_disponibles(self) -> int:
        return sum(libro["disponibles"] for libro in self.catalogo)

    @rx.var
    def catalogo_total_pages(self) -> int:
        if not self.catalogo:
            return 1
        return (len(self.catalogo) + self.page_size - 1) // self.page_size

    @rx.var
    def prestamos_total_pages(self) -> int:
        if not self.prestamos:
            return 1
        return (len(self.prestamos) + self.page_size - 1) // self.page_size

    @rx.var
    def paginated_catalogo(self) -> list[Libro]:
        start = (self.catalogo_page - 1) * self.page_size
        end = start + self.page_size
        return self.catalogo[start:end]

    @rx.var
    def paginated_prestamos(self) -> list[Prestamo]:
        start = (self.prestamos_page - 1) * self.page_size
        end = start + self.page_size
        return self.prestamos[start:end]
