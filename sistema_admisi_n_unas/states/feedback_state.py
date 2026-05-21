import reflex as rx
from typing import TypedDict


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

    @rx.event
    def set_filter_estado(self, v: str):
        self.filter_estado = v

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