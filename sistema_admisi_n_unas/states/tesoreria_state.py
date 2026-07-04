from typing import TypedDict

import reflex as rx

from ..utils.csv_loader import cargar_postulantes


class Pago(TypedDict):
    id: int
    postulante: str
    dni: str
    convocatoria: str
    concepto: str
    monto: float
    fecha: str
    estado: str


class TesoreriaState(rx.State):
    pagos: list[Pago] = []
    total_recaudado: float = 0.0
    pagos_validados: int = 0
    pagos_pendientes: int = 0
    pagos_observados: int = 0

    @rx.event
    def cargar_pagos(self):
        postulantes = cargar_postulantes()

        pagos: list[Pago] = []
        for postulante in postulantes:
            estado_pago = "Validado"
            if postulante["id"] % 7 == 0:
                estado_pago = "Observado"
            elif postulante["id"] % 4 == 0:
                estado_pago = "Pendiente"

            pagos.append(
                {
                    "id": postulante["id"],
                    "postulante": f"{postulante['nombres']} {postulante['apellidos']}",
                    "dni": postulante["dni"],
                    "convocatoria": postulante["convocatoria"],
                    "concepto": "Derecho de admision",
                    "monto": float(postulante["costo"]),
                    "fecha": postulante["fecha"],
                    "estado": estado_pago,
                }
            )

        self.pagos = pagos
        self.total_recaudado = round(
            sum(pago["monto"] for pago in pagos if pago["estado"] == "Validado"), 2
        )
        self.pagos_validados = sum(1 for pago in pagos if pago["estado"] == "Validado")
        self.pagos_pendientes = sum(1 for pago in pagos if pago["estado"] == "Pendiente")
        self.pagos_observados = sum(1 for pago in pagos if pago["estado"] == "Observado")

    @rx.var
    def total_pagos(self) -> int:
        return len(self.pagos)

    @rx.var
    def monto_pendiente(self) -> float:
        return round(
            sum(pago["monto"] for pago in self.pagos if pago["estado"] == "Pendiente"), 2
        )

    @rx.var
    def pagos_recientes(self) -> list[Pago]:
        return list(reversed(self.pagos[-12:]))
