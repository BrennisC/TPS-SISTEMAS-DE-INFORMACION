import reflex as rx
from typing import TypedDict

from datetime import datetime

from sistema_admisi_n_unas.utils.csv_loader import (
    append_apelacion,
    cargar_apelaciones,
    cargar_preguntas_error,
)


class PreguntaError(TypedDict):
    id: int
    area: str
    enunciado: str
    indice_error: float
    total_respuestas: int


class Apelacion(TypedDict):
    id: int
    postulante: str
    dni: str
    pregunta: str
    motivo: str
    fecha: str
    estado: str


PREGUNTAS_ERROR_DEMO: list[PreguntaError] = [
    {
        "id": 1,
        "area": "Matemática",
        "enunciado": "Pregunta 7: Función cuadrática",
        "indice_error": 78.5,
        "total_respuestas": 1250,
    },
    {
        "id": 2,
        "area": "Psicotécnico",
        "enunciado": "Pregunta 23: Series numéricas",
        "indice_error": 72.3,
        "total_respuestas": 1250,
    },
    {
        "id": 3,
        "area": "Comunicación",
        "enunciado": "Pregunta 45: Comprensión lectora",
        "indice_error": 65.1,
        "total_respuestas": 1250,
    },
    {
        "id": 4,
        "area": "Ciencias Naturales",
        "enunciado": "Pregunta 12: Genética mendeliana",
        "indice_error": 61.8,
        "total_respuestas": 1250,
    },
    {
        "id": 5,
        "area": "Cultura General",
        "enunciado": "Pregunta 89: Historia regional",
        "indice_error": 58.4,
        "total_respuestas": 1250,
    },
    {
        "id": 6,
        "area": "Matemática",
        "enunciado": "Pregunta 15: Trigonometría",
        "indice_error": 54.2,
        "total_respuestas": 1250,
    },
    {
        "id": 7,
        "area": "Psicotécnico",
        "enunciado": "Pregunta 31: Razonamiento lógico",
        "indice_error": 49.7,
        "total_respuestas": 1250,
    },
    {
        "id": 8,
        "area": "Comunicación",
        "enunciado": "Pregunta 52: Ortografía",
        "indice_error": 41.3,
        "total_respuestas": 1250,
    },
]


APELACIONES_DEMO: list[Apelacion] = [
    {
        "id": 1,
        "postulante": "María Fernanda Quispe",
        "dni": "73829145",
        "pregunta": "Pregunta 7 - Matemática",
        "motivo": "La pregunta tiene dos alternativas que pueden considerarse correctas según el enunciado.",
        "fecha": "2024-03-18",
        "estado": "Pendiente",
    },
    {
        "id": 2,
        "postulante": "Carlos Andrés Rojas",
        "dni": "74512893",
        "pregunta": "Pregunta 23 - Psicotécnico",
        "motivo": "Error en la formulación de la serie numérica presentada.",
        "fecha": "2024-03-18",
        "estado": "Resuelto",
    },
    {
        "id": 3,
        "postulante": "Diana Lucía Mendoza",
        "dni": "72938174",
        "pregunta": "Pregunta 45 - Comunicación",
        "motivo": "El texto de comprensión lectora presenta ambigüedad en la respuesta.",
        "fecha": "2024-03-19",
        "estado": "Pendiente",
    },
    {
        "id": 4,
        "postulante": "Jorge Luis Salazar",
        "dni": "75829341",
        "pregunta": "Pregunta 12 - Ciencias",
        "motivo": "Falta información para resolver el problema de genética mendeliana.",
        "fecha": "2024-03-19",
        "estado": "Pendiente",
    },
    {
        "id": 5,
        "postulante": "Andrea Sofía Campos",
        "dni": "76123498",
        "pregunta": "Pregunta 89 - Cultura",
        "motivo": "La fecha histórica indicada en la respuesta oficial es incorrecta.",
        "fecha": "2024-03-20",
        "estado": "Resuelto",
    },
    {
        "id": 6,
        "postulante": "Pedro Antonio Vargas",
        "dni": "77891234",
        "pregunta": "Pregunta 15 - Matemática",
        "motivo": "Falta especificar el cuadrante en la pregunta de trigonometría.",
        "fecha": "2024-03-20",
        "estado": "Pendiente",
    },
]


class FeedbackState(rx.State):
    preguntas_error: list[PreguntaError] = PREGUNTAS_ERROR_DEMO
    apelaciones: list[Apelacion] = APELACIONES_DEMO
    filter_estado: str = "Todas"
    current_page: int = 1
    page_size: int = 10

    f_postulante: str = ""
    f_dni: str = ""
    f_pregunta: str = ""
    f_motivo: str = ""

    @rx.event
    def cargar_datos(self):
        try:
            self.preguntas_error = cargar_preguntas_error()
            self.apelaciones = cargar_apelaciones()
        except Exception as exc:
            print(f"Error al leer retroalimentacion desde CSV: {exc}")
            return

    @rx.var
    def total_apelaciones(self) -> int:
        return len(self.apelaciones)

    @rx.var
    def total_pendientes(self) -> int:
        return len([a for a in self.apelaciones if a["estado"] == "Pendiente"])

    @rx.var
    def total_resueltas(self) -> int:
        return len([a for a in self.apelaciones if a["estado"] == "Resuelto"])

    @rx.var
    def promedio_error(self) -> float:
        if not self.preguntas_error:
            return 0.0
        return sum(p["indice_error"] for p in self.preguntas_error) / len(
            self.preguntas_error
        )

    @rx.var
    def apelaciones_filtradas(self) -> list[Apelacion]:
        if self.filter_estado == "Todas":
            return self.apelaciones
        return [
            a for a in self.apelaciones if a["estado"] == self.filter_estado
        ]

    @rx.var
    def total_pages(self) -> int:
        total = len(self.apelaciones_filtradas)
        if total == 0:
            return 1
        return (total + self.page_size - 1) // self.page_size

    @rx.var
    def paginated_apelaciones(self) -> list[Apelacion]:
        page = min(max(self.current_page, 1), self.total_pages)
        start = (page - 1) * self.page_size
        end = start + self.page_size
        return self.apelaciones_filtradas[start:end]

    @rx.event
    def set_filter_estado(self, v: str):
        self.filter_estado = v
        self.current_page = 1

    @rx.var
    def err_postulante(self) -> str:
        if self.f_postulante == "":
            return ""
        if len(self.f_postulante.strip()) < 4:
            return "Mínimo 4 caracteres"
        return ""

    @rx.var
    def err_dni(self) -> str:
        if self.f_dni == "":
            return ""
        if not self.f_dni.isdigit():
            return "El DNI debe contener solo números"
        if len(self.f_dni) != 8:
            return "El DNI debe tener 8 dígitos"
        return ""

    @rx.var
    def err_pregunta(self) -> str:
        if self.f_pregunta == "":
            return ""
        if len(self.f_pregunta.strip()) < 6:
            return "Mínimo 6 caracteres"
        return ""

    @rx.var
    def err_motivo(self) -> str:
        if self.f_motivo == "":
            return ""
        if len(self.f_motivo.strip()) < 10:
            return "Mínimo 10 caracteres"
        return ""

    @rx.var
    def form_valido(self) -> bool:
        return (
            len(self.f_postulante.strip()) >= 4
            and self.f_dni.isdigit()
            and len(self.f_dni) == 8
            and len(self.f_pregunta.strip()) >= 6
            and len(self.f_motivo.strip()) >= 10
            and self.err_dni == ""
        )

    @rx.event
    def set_postulante(self, v: str):
        self.f_postulante = v

    @rx.event
    def set_dni(self, v: str):
        self.f_dni = v[:8]

    @rx.event
    def set_pregunta(self, v: str):
        self.f_pregunta = v

    @rx.event
    def set_motivo(self, v: str):
        self.f_motivo = v

    @rx.event
    def submit_apelacion(self):
        if not self.form_valido:
            return rx.toast(
                "Completa todos los campos correctamente",
                duration=3000,
            )

        nuevo_id = max((a["id"] for a in self.apelaciones), default=0) + 1
        fecha = datetime.now().strftime("%Y-%m-%d")
        apelacion: Apelacion = {
            "id": nuevo_id,
            "postulante": self.f_postulante.strip().title(),
            "dni": self.f_dni.strip(),
            "pregunta": self.f_pregunta.strip(),
            "motivo": self.f_motivo.strip(),
            "fecha": fecha,
            "estado": "Pendiente",
        }
        self.apelaciones.append(apelacion)
        append_apelacion(apelacion)
        self.f_postulante = ""
        self.f_dni = ""
        self.f_pregunta = ""
        self.f_motivo = ""
        self.current_page = self.total_pages
        return rx.toast("Apelación registrada", duration=3000)

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
    def resolver_apelacion(self, aid: int):
        for a in self.apelaciones:
            if a["id"] == aid:
                a["estado"] = "Resuelto"
        self.apelaciones = list(self.apelaciones)
        return rx.toast("Apelación marcada como resuelta", duration=2000)

    @rx.event
    def reabrir_apelacion(self, aid: int):
        for a in self.apelaciones:
            if a["id"] == aid:
                a["estado"] = "Pendiente"
        self.apelaciones = list(self.apelaciones)
        return rx.toast("Apelación marcada como pendiente", duration=2000)
