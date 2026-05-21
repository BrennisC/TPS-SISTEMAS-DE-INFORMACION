import reflex as rx
from typing import TypedDict
from datetime import datetime


class Postulante(TypedDict):
    id: int
    nombres: str
    apellidos: str
    dni: str
    carrera: str
    tipo_colegio: str
    costo: float
    voucher: str
    fecha: str
    estado: str


CARRERAS: list[str] = [
    "Ingeniería Forestal",
    "Agronomía",
    "Administración de Empresas",
    "Ingeniería en Industrias Alimentarias",
    "Ingeniería en Recursos Naturales Renovables",
    "Medicina Veterinaria",
    "Ingeniería en Conservación de Suelos y Agua",
    "Economía",
    "Contabilidad",
    "Ingeniería de Sistemas e Informática",
    "Educación Básica",
    "Enfermería",
]


class PostulantesState(rx.State):
    # Form fields
    f_nombres: str = ""
    f_apellidos: str = ""
    f_dni: str = ""
    f_carrera: str = ""
    f_tipo_colegio: str = "Estatal"
    f_voucher: str = ""

    search_query: str = ""
    filter_carrera: str = "Todas"

    carreras: list[str] = CARRERAS
    tipos_colegio: list[str] = ["Estatal", "Privado"]

    show_success: bool = False

    postulantes: list[Postulante] = [
        {
            "id": 1,
            "nombres": "María Fernanda",
            "apellidos": "Quispe Huamán",
            "dni": "73829145",
            "carrera": "Ingeniería Forestal",
            "tipo_colegio": "Estatal",
            "costo": 220.0,
            "voucher": "V-001245",
            "fecha": "2024-03-12",
            "estado": "Inscrito",
        },
        {
            "id": 2,
            "nombres": "Carlos Andrés",
            "apellidos": "Rojas Ventura",
            "dni": "74512893",
            "carrera": "Agronomía",
            "tipo_colegio": "Privado",
            "costo": 240.0,
            "voucher": "V-001246",
            "fecha": "2024-03-13",
            "estado": "Inscrito",
        },
        {
            "id": 3,
            "nombres": "Diana Lucía",
            "apellidos": "Mendoza Paredes",
            "dni": "72938174",
            "carrera": "Ingeniería de Sistemas e Informática",
            "tipo_colegio": "Estatal",
            "costo": 220.0,
            "voucher": "V-001247",
            "fecha": "2024-03-14",
            "estado": "Pendiente",
        },
        {
            "id": 4,
            "nombres": "Jorge Luis",
            "apellidos": "Salazar Cárdenas",
            "dni": "75829341",
            "carrera": "Administración de Empresas",
            "tipo_colegio": "Privado",
            "costo": 240.0,
            "voucher": "V-001248",
            "fecha": "2024-03-15",
            "estado": "Inscrito",
        },
        {
            "id": 5,
            "nombres": "Andrea Sofía",
            "apellidos": "Campos Lazo",
            "dni": "76123498",
            "carrera": "Medicina Veterinaria",
            "tipo_colegio": "Estatal",
            "costo": 220.0,
            "voucher": "V-001249",
            "fecha": "2024-03-16",
            "estado": "Pendiente",
        },
    ]
    next_id: int = 6

    # Validation computed vars
    @rx.var
    def err_nombres(self) -> str:
        if self.f_nombres == "":
            return ""
        if len(self.f_nombres.strip()) < 2:
            return "Mínimo 2 caracteres"
        return ""

    @rx.var
    def err_apellidos(self) -> str:
        if self.f_apellidos == "":
            return ""
        if len(self.f_apellidos.strip()) < 2:
            return "Mínimo 2 caracteres"
        return ""

    @rx.var
    def err_dni(self) -> str:
        if self.f_dni == "":
            return ""
        if not self.f_dni.isdigit():
            return "El DNI debe contener solo números"
        if len(self.f_dni) != 8:
            return "El DNI debe tener 8 dígitos"
        for p in self.postulantes:
            if p["dni"] == self.f_dni:
                return "Este DNI ya está registrado"
        return ""

    @rx.var
    def err_carrera(self) -> str:
        if self.f_carrera == "":
            return ""
        if self.f_carrera not in CARRERAS:
            return "Carrera inválida"
        return ""

    @rx.var
    def err_voucher(self) -> str:
        if self.f_voucher == "":
            return ""
        if len(self.f_voucher.strip()) < 4:
            return "Voucher inválido"
        for p in self.postulantes:
            if p["voucher"].lower() == self.f_voucher.lower():
                return "Este voucher ya fue utilizado"
        return ""

    @rx.var
    def costo_actual(self) -> float:
        return 220.0 if self.f_tipo_colegio == "Estatal" else 240.0

    @rx.var
    def form_valido(self) -> bool:
        return (
            len(self.f_nombres.strip()) >= 2
            and len(self.f_apellidos.strip()) >= 2
            and self.f_dni.isdigit()
            and len(self.f_dni) == 8
            and self.f_carrera in CARRERAS
            and self.f_tipo_colegio in ["Estatal", "Privado"]
            and len(self.f_voucher.strip()) >= 4
            and self.err_dni == ""
            and self.err_voucher == ""
        )

    @rx.var
    def total_postulantes(self) -> int:
        return len(self.postulantes)

    @rx.var
    def total_estatal(self) -> int:
        return len(
            [p for p in self.postulantes if p["tipo_colegio"] == "Estatal"]
        )

    @rx.var
    def total_privado(self) -> int:
        return len(
            [p for p in self.postulantes if p["tipo_colegio"] == "Privado"]
        )

    @rx.var
    def total_recaudado(self) -> float:
        return sum(p["costo"] for p in self.postulantes)

    @rx.var
    def filtered_postulantes(self) -> list[Postulante]:
        result = self.postulantes
        if self.filter_carrera != "Todas":
            result = [p for p in result if p["carrera"] == self.filter_carrera]
        if self.search_query.strip():
            q = self.search_query.lower().strip()
            result = [
                p
                for p in result
                if q in p["nombres"].lower()
                or q in p["apellidos"].lower()
                or q in p["dni"]
                or q in p["voucher"].lower()
            ]
        return result

    @rx.event
    def set_nombres(self, v: str):
        self.f_nombres = v

    @rx.event
    def set_apellidos(self, v: str):
        self.f_apellidos = v

    @rx.event
    def set_dni(self, v: str):
        self.f_dni = v[:8]

    @rx.event
    def set_carrera(self, v: str):
        self.f_carrera = v

    @rx.event
    def set_tipo_colegio(self, v: str):
        self.f_tipo_colegio = v

    @rx.event
    def set_voucher(self, v: str):
        self.f_voucher = v

    @rx.event
    def set_search_query(self, v: str):
        self.search_query = v

    @rx.event
    def set_filter_carrera(self, v: str):
        self.filter_carrera = v

    @rx.event
    def submit_form(self):
        if not self.form_valido:
            return rx.toast(
                "Por favor completa todos los campos correctamente",
                duration=3000,
            )
        nuevo: Postulante = {
            "id": self.next_id,
            "nombres": self.f_nombres.strip().title(),
            "apellidos": self.f_apellidos.strip().title(),
            "dni": self.f_dni.strip(),
            "carrera": self.f_carrera,
            "tipo_colegio": self.f_tipo_colegio,
            "costo": self.costo_actual,
            "voucher": self.f_voucher.strip().upper(),
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "estado": "Inscrito",
        }
        self.postulantes.append(nuevo)
        self.next_id += 1
        # Reset fields
        self.f_nombres = ""
        self.f_apellidos = ""
        self.f_dni = ""
        self.f_carrera = ""
        self.f_tipo_colegio = "Estatal"
        self.f_voucher = ""
        self.show_success = True
        return rx.toast(
            f"Postulante {nuevo['nombres']} registrado con éxito",
            duration=3000,
        )

    @rx.event
    def delete_postulante(self, pid: int):
        self.postulantes = [p for p in self.postulantes if p["id"] != pid]
        return rx.toast("Postulante eliminado", duration=2000)

    @rx.event
    def toggle_estado(self, pid: int):
        for p in self.postulantes:
            if p["id"] == pid:
                p["estado"] = (
                    "Inscrito" if p["estado"] == "Pendiente" else "Pendiente"
                )
        self.postulantes = list(self.postulantes)