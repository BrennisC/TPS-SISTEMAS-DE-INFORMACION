import reflex as rx
from typing import TypedDict
from datetime import datetime
from sistema_admisi_n_unas.utils.csv_loader import (
    cargar_postulantes,
    append_postulante,
)


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
    convocatoria: str


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
]

FACULTAD_POR_CARRERA: dict[str, str] = {
    "Ingeniería Forestal": "Fac. Recursos Naturales Renovables",
    "Agronomía": "Fac. Agronomía",
    "Administración de Empresas": "Fac. Ciencias Económicas y Administrativas",
    "Ingeniería en Industrias Alimentarias": "Fac. Ingeniería en Industrias Alimentarias",
    "Ingeniería en Recursos Naturales Renovables": "Fac. Recursos Naturales Renovables",
    "Ingeniería en Conservación de Suelos y Agua": "Fac. Recursos Naturales Renovables",
    "Economía": "Fac. Ciencias Económicas y Administrativas",
    "Contabilidad": "Fac. Ciencias Económicas y Administrativas",
    "Ingeniería de Sistemas e Informática": "Fac. Ingeniería en Informática y Sistemas",
}


class PostulantesState(rx.State):
    postulantes: list[Postulante] = []

    # Form fields
    f_nombres: str = ""
    f_apellidos: str = ""
    f_dni: str = ""
    f_carrera: str = ""
    f_tipo_colegio: str = "Estatal"
    f_voucher: str = ""

    search_query: str = ""
    filter_carrera: str = "Todas"
    filter_convocatoria: str = "Todas"
    current_page: int = 1
    page_size: int = 10

    carreras: list[str] = CARRERAS
    tipos_colegio: list[str] = ["Estatal", "Privado"]

    show_success: bool = False

    next_id: int = 6
    

    @rx.event
    def cargar_datos(self):
        "Carga los datos de los postulantes desde el archivo CSV"
        datos = cargar_postulantes()
        self.postulantes = datos
        self.current_page = 1
        if datos:
            self.next_id = max(p["id"] for p in datos) + 1
        else:
            self.next_id = 1

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
    def admitted_count(self) -> int:
        return len(
            [
                p
                for p in self.postulantes
                if p["estado"].strip().lower() == "ingresante"
            ]
        )

    @rx.var
    def general_avg(self) -> float:
        puntajes = [
            float(p.get("puntaje", 0))
            for p in self.postulantes
            if float(p.get("puntaje", 0)) > 0
        ]
        if not puntajes:
            return 0.0
        return sum(puntajes) / len(puntajes)

    @rx.var
    def top_career(self) -> str:
        if not self.postulantes:
            return "N/D"
        counts: dict[str, int] = {}
        for p in self.postulantes:
            carrera = p["carrera"]
            counts[carrera] = counts.get(carrera, 0) + 1
        return max(counts.items(), key=lambda item: item[1])[0]

    @rx.var
    def convocatorias_disponibles(self) -> list[str]:
        """Obtiene todas las convocatorias únicas del CSV"""
        convocatorias = set()
        for p in self.postulantes:
            if "convocatoria" in p:
                convocatorias.add(p["convocatoria"])
        return sorted(list(convocatorias), reverse=True)

    @rx.var
    def filtered_postulantes(self) -> list[Postulante]:
        result = self.postulantes
        if self.filter_carrera != "Todas":
            result = [p for p in result if p["carrera"] == self.filter_carrera]
        if self.filter_convocatoria != "Todas":
            result = [p for p in result if p.get("convocatoria") == self.filter_convocatoria]
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

    @rx.var
    def total_pages(self) -> int:
        total = len(self.filtered_postulantes)
        if total == 0:
            return 1
        return (total + self.page_size - 1) // self.page_size

    @rx.var
    def paginated_postulantes(self) -> list[Postulante]:
        page = min(max(self.current_page, 1), self.total_pages)
        start = (page - 1) * self.page_size
        end = start + self.page_size
        return self.filtered_postulantes[start:end]

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
        self.current_page = 1

    @rx.event
    def set_filter_carrera(self, v: str):
        self.filter_carrera = v
        self.current_page = 1

    @rx.event
    def set_filter_convocatoria(self, v: str):
        self.filter_convocatoria = v
        self.current_page = 1

    @rx.event
    def set_page(self, page: int):
        if page < 1:
            self.current_page = 1
        elif page > self.total_pages:
            self.current_page = self.total_pages
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
    def submit_form(self):
        if not self.form_valido:
            return rx.toast(
                "Por favor completa todos los campos correctamente",
                duration=3000,
            )
        fecha_actual = datetime.now()
        convocatoria = (
            f"{fecha_actual.year}-I"
            if fecha_actual.month <= 6
            else f"{fecha_actual.year}-II"
        )
        facultad = FACULTAD_POR_CARRERA.get(
            self.f_carrera, "Otras Escuelas"
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
            "fecha": fecha_actual.strftime("%Y-%m-%d"),
            "estado": "Inscrito",
            "puntaje": 0.0,
        }
        self.postulantes.append(nuevo)
        self.next_id += 1
        append_postulante(
            {
                **nuevo,
                "convocatoria": convocatoria,
                "facultad": facultad,
                "puntaje": 0,
            }
        )
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
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        return rx.toast("Postulante eliminado", duration=2000)

    @rx.event
    def toggle_estado(self, pid: int):
        for p in self.postulantes:
            if p["id"] == pid:
                p["estado"] = (
                    "Inscrito" if p["estado"] == "Pendiente" else "Pendiente"
                )
        self.postulantes = list(self.postulantes)
