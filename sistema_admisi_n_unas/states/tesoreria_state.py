from datetime import date
from typing import TypedDict

import reflex as rx

from ..utils.csv_loader import cargar_pagos, cargar_postulantes, guardar_pagos


class Pago(TypedDict):
    id: int
    postulante_id: int
    postulante: str
    dni: str
    convocatoria: str
    concepto: str
    monto: float
    voucher: str
    fecha_pago: str
    estado_pago: str
    observacion: str


class TesoreriaState(rx.State):
    pagos: list[Pago] = []
    postulantes: list[dict] = []
    total_recaudado: float = 0.0
    pagos_validados: int = 0
    pagos_pendientes: int = 0
    pagos_observados: int = 0
    f_dni: str = ""
    f_voucher: str = ""
    f_monto: str = ""
    f_concepto: str = "Derecho de admision"
    f_observacion: str = ""
    mensaje: str = ""
    show_payment_modal: bool = False

    @rx.event
    def cargar_pagos(self):
        self.postulantes = cargar_postulantes()
        self.pagos = cargar_pagos()
        self._actualizar_resumen()

    def _actualizar_resumen(self):
        self.total_recaudado = round(
            sum(pago["monto"] for pago in self.pagos if pago["estado_pago"] == "Validado"), 2
        )
        self.pagos_validados = sum(1 for pago in self.pagos if pago["estado_pago"] == "Validado")
        self.pagos_pendientes = sum(1 for pago in self.pagos if pago["estado_pago"] == "Pendiente")
        self.pagos_observados = sum(1 for pago in self.pagos if pago["estado_pago"] == "Observado")

    def _buscar_postulante(self, dni: str) -> dict | None:
        for postulante in self.postulantes:
            if postulante["dni"] == dni:
                return postulante
        return None

    @rx.event
    def set_dni(self, value: str):
        self.f_dni = value.strip()
        if not self.postulantes:
            self.postulantes = cargar_postulantes()
        postulante = self._buscar_postulante(self.f_dni)
        if postulante:
            self.f_monto = str(postulante["costo"])
            self.f_voucher = postulante["voucher"]
            self.mensaje = "Datos del postulante cargados."

    @rx.event
    def set_voucher(self, value: str):
        self.f_voucher = value.strip()

    @rx.event
    def set_monto(self, value: str):
        self.f_monto = value.strip()

    @rx.event
    def set_concepto(self, value: str):
        self.f_concepto = value.strip()

    @rx.event
    def set_observacion(self, value: str):
        self.f_observacion = value.strip()

    @rx.event
    def open_payment_modal(self):
        if not self.postulantes:
            self.postulantes = cargar_postulantes()
        self.mensaje = ""
        self.show_payment_modal = True

    @rx.event
    def close_payment_modal(self):
        self.show_payment_modal = False

    @rx.event
    def registrar_pago(self):
        if not self.postulantes:
            self.postulantes = cargar_postulantes()
        postulante = self._buscar_postulante(self.f_dni)
        if postulante is None:
            self.mensaje = "No se encontró un postulante con ese DNI."
            return
        if any(pago["voucher"].lower() == self.f_voucher.lower() for pago in self.pagos):
            self.mensaje = "Ese voucher ya fue registrado."
            return
        try:
            monto = float(self.f_monto)
        except ValueError:
            self.mensaje = "El monto debe ser numérico."
            return

        pago: Pago = {
            "id": max([p["id"] for p in self.pagos], default=0) + 1,
            "postulante_id": postulante["id"],
            "dni": postulante["dni"],
            "postulante": f"{postulante['nombres']} {postulante['apellidos']}",
            "convocatoria": postulante["convocatoria"],
            "concepto": self.f_concepto or "Derecho de admision",
            "monto": monto,
            "voucher": self.f_voucher,
            "fecha_pago": date.today().isoformat(),
            "estado_pago": "Pendiente",
            "observacion": self.f_observacion,
        }
        self.pagos.append(pago)
        guardar_pagos(self.pagos)
        self._actualizar_resumen()
        self.f_dni = ""
        self.f_voucher = ""
        self.f_monto = ""
        self.f_concepto = "Derecho de admision"
        self.f_observacion = ""
        self.mensaje = "Pago registrado como pendiente."
        self.show_payment_modal = False

    @rx.event
    def validar_pago(self, pago_id: int):
        for pago in self.pagos:
            if pago["id"] == pago_id:
                pago["estado_pago"] = "Validado"
                pago["observacion"] = ""
                break
        guardar_pagos(self.pagos)
        self._actualizar_resumen()
        self.mensaje = "Pago validado."

    @rx.event
    def observar_pago(self, pago_id: int):
        for pago in self.pagos:
            if pago["id"] == pago_id:
                pago["estado_pago"] = "Observado"
                pago["observacion"] = self.f_observacion or "Requiere revisión de Tesorería"
                break
        guardar_pagos(self.pagos)
        self._actualizar_resumen()
        self.mensaje = "Pago observado."

    @rx.var
    def total_pagos(self) -> int:
        return len(self.pagos)

    @rx.var
    def monto_pendiente(self) -> float:
        return round(
            sum(pago["monto"] for pago in self.pagos if pago["estado_pago"] == "Pendiente"), 2
        )

    @rx.var
    def pagos_recientes(self) -> list[Pago]:
        return list(reversed(self.pagos[-12:]))

    @rx.var
    def estudiante_encontrado(self) -> bool:
        return self._buscar_postulante(self.f_dni) is not None

    @rx.var
    def estudiante_nombre(self) -> str:
        postulante = self._buscar_postulante(self.f_dni)
        if not postulante:
            return "Sin estudiante seleccionado"
        return f"{postulante['nombres']} {postulante['apellidos']}"

    @rx.var
    def estudiante_carrera(self) -> str:
        postulante = self._buscar_postulante(self.f_dni)
        return postulante["carrera"] if postulante else "-"

    @rx.var
    def estudiante_convocatoria(self) -> str:
        postulante = self._buscar_postulante(self.f_dni)
        return postulante["convocatoria"] if postulante else "-"

    @rx.var
    def estudiante_estado(self) -> str:
        postulante = self._buscar_postulante(self.f_dni)
        return postulante["estado"] if postulante else "-"
