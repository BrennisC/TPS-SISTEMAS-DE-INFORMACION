from typing import TypedDict

import reflex as rx

from ..utils.csv_loader import cargar_postulantes


CATALOGO_BASE = [
    {"codigo": "LIB-001", "titulo": "Matematica Basica", "categoria": "Ciencias", "stock": 5},
    {"codigo": "LIB-002", "titulo": "Comprension Lectora", "categoria": "Humanidades", "stock": 4},
    {"codigo": "LIB-003", "titulo": "Biologia General", "categoria": "Ciencias", "stock": 3},
    {"codigo": "LIB-004", "titulo": "Quimica Preuniversitaria", "categoria": "Ciencias", "stock": 6},
    {"codigo": "LIB-005", "titulo": "Historia del Peru", "categoria": "Sociales", "stock": 2},
]


class Libro(TypedDict):
    codigo: str
    titulo: str
    categoria: str
    stock: int


class Prestamo(TypedDict):
    id: int
    lector: str
    dni: str
    libro: str
    fecha_prestamo: str
    fecha_devolucion: str
    estado: str


class BibliotecaState(rx.State):
    catalogo: list[Libro] = []
    prestamos: list[Prestamo] = []
    total_lectores: int = 0
    prestamos_activos: int = 0
    prestamos_vencidos: int = 0

    @rx.event
    def cargar_biblioteca(self):
        postulantes = cargar_postulantes()
        ingresantes = [
            postulante
            for postulante in postulantes
            if postulante["estado"].strip().lower() == "ingresante"
        ]

        prestamos: list[Prestamo] = []
        for index, ingresante in enumerate(ingresantes[:10], start=1):
            libro = CATALOGO_BASE[(index - 1) % len(CATALOGO_BASE)]
            estado = "Prestado"
            if index % 5 == 0:
                estado = "Vencido"
            elif index % 3 == 0:
                estado = "Devuelto"

            prestamos.append(
                {
                    "id": index,
                    "lector": f"{ingresante['nombres']} {ingresante['apellidos']}",
                    "dni": ingresante["dni"],
                    "libro": libro["titulo"],
                    "fecha_prestamo": ingresante["fecha"],
                    "fecha_devolucion": "2026-12-15",
                    "estado": estado,
                }
            )

        self.catalogo = list(CATALOGO_BASE)
        self.prestamos = prestamos
        self.total_lectores = len({prestamo["dni"] for prestamo in prestamos})
        self.prestamos_activos = sum(
            1 for prestamo in prestamos if prestamo["estado"] == "Prestado"
        )
        self.prestamos_vencidos = sum(
            1 for prestamo in prestamos if prestamo["estado"] == "Vencido"
        )

    @rx.var
    def total_libros(self) -> int:
        return len(self.catalogo)

    @rx.var
    def total_stock(self) -> int:
        return sum(libro["stock"] for libro in self.catalogo)
