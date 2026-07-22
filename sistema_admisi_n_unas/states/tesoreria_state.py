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

    search_query: str = ""
    filter_estado: str = "Todos"
    filter_concepto: str = "Todos"
    filter_convocatoria: str = "Todos"
    current_page: int = 1
    page_size: int = 10

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
        else:
            self.mensaje = ""

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
    def set_search_query(self, value: str):
        self.search_query = value
        self.current_page = 1

    @rx.event
    def set_filter_estado(self, value: str):
        self.filter_estado = value
        self.current_page = 1

    @rx.event
    def set_filter_concepto(self, value: str):
        self.filter_concepto = value
        self.current_page = 1

    @rx.event
    def set_filter_convocatoria(self, value: str):
        self.filter_convocatoria = value
        self.current_page = 1

    @rx.event
    def set_page(self, page: int):
        total = self.total_pages
        if page < 1:
            self.current_page = 1
        elif page > total:
            self.current_page = total
        else:
            self.current_page = page

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

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
        if any(
            pago["dni"] == postulante["dni"]
            and pago["convocatoria"] == postulante["convocatoria"]
            for pago in self.pagos
        ):
            self.mensaje = "Ese postulante ya tiene un pago registrado para esta convocatoria."
            return
        try:
            monto = float(self.f_monto)
        except ValueError:
            self.mensaje = "El monto debe ser numérico."
            return

        costo_esperado = postulante["costo"]
        if monto != costo_esperado:
            self.mensaje = f"El monto S/. {monto:.2f} no coincide con el costo de inscripción S/. {costo_esperado:.2f}"
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

    @rx.var
    def filtered_pagos(self) -> list[Pago]:
        result = list(self.pagos)
        if self.filter_estado != "Todos":
            result = [p for p in result if p["estado_pago"] == self.filter_estado]
        if self.filter_concepto != "Todos":
            result = [p for p in result if p["concepto"] == self.filter_concepto]
        if self.filter_convocatoria != "Todos":
            result = [p for p in result if p["convocatoria"] == self.filter_convocatoria]
        if self.search_query.strip():
            q = self.search_query.lower().strip()
            result = [
                p for p in result
                if q in p["dni"]
                or q in p["postulante"].lower()
                or q in p["voucher"].lower()
                or q in p["convocatoria"].lower()
            ]
        return result

    @rx.var
    def total_pages(self) -> int:
        total = len(self.filtered_pagos)
        if total == 0:
            return 1
        return (total + self.page_size - 1) // self.page_size

    @rx.var
    def paginated_pagos(self) -> list[Pago]:
        page = min(max(self.current_page, 1), self.total_pages)
        start = (page - 1) * self.page_size
        end = start + self.page_size
        return self.filtered_pagos[start:end]

    @rx.var
    def recaudacion_admision(self) -> float:
        return round(sum(p["monto"] for p in self.pagos if p["estado_pago"] == "Validado" and p["concepto"] in ("Derecho de admision", "Derecho de admisión")), 2)

    @rx.var
    def recaudacion_comedor(self) -> float:
        return round(sum(p["monto"] for p in self.pagos if p["estado_pago"] == "Validado" and p.get("concepto", "") == "Comedor universitario"), 2)

    @rx.var
    def recaudacion_residencia(self) -> float:
        return round(sum(p["monto"] for p in self.pagos if p["estado_pago"] == "Validado" and p.get("concepto", "") == "Residencia universitaria"), 2)

    @rx.var
    def recaudacion_por_concepto(self) -> list[dict]:
        return [
            {"concepto": "Admisión", "monto": self.recaudacion_admision, "fill": "#228B22"},
            {"concepto": "Comedor", "monto": self.recaudacion_comedor, "fill": "#003366"},
            {"concepto": "Residencia", "monto": self.recaudacion_residencia, "fill": "#d97706"},
        ]

    @rx.var
    def convocatorias_disponibles(self) -> list[str]:
        convs: set[str] = set()
        for p in self.pagos:
            convs.add(p["convocatoria"])
        return sorted(convs, reverse=True)

    @rx.var
    def recaudacion_por_semestre(self) -> list[dict]:
        from collections import defaultdict
        semestres: dict[str, float] = defaultdict(float)
        for p in self.pagos:
            if p["estado_pago"] == "Validado":
                semestres[p["convocatoria"]] += p["monto"]
        return sorted(
            [{"semestre": k, "monto": round(v, 2)} for k, v in semestres.items()],
            key=lambda x: x["semestre"],
        )

    @rx.var
    def recaudacion_por_semestre_concepto(self) -> list[dict]:
        from collections import defaultdict
        data: dict[str, dict[str, float]] = defaultdict(lambda: {"Admisión": 0.0, "Comedor": 0.0, "Residencia": 0.0})
        for p in self.pagos:
            if p["estado_pago"] != "Validado":
                continue
            concepto = p.get("concepto", "")
            conv = p["convocatoria"]
            if concepto in ("Derecho de admision", "Derecho de admisión"):
                data[conv]["Admisión"] += p["monto"]
            elif concepto == "Comedor universitario":
                data[conv]["Comedor"] += p["monto"]
            elif concepto == "Residencia universitaria":
                data[conv]["Residencia"] += p["monto"]
        return sorted(
            [{"semestre": k, "Admisión": round(v["Admisión"], 2), "Comedor": round(v["Comedor"], 2), "Residencia": round(v["Residencia"], 2)}
             for k, v in data.items()],
            key=lambda x: x["semestre"],
        )
