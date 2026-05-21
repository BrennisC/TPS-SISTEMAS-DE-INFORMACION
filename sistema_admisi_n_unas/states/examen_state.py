import reflex as rx
import asyncio
from typing import TypedDict


class Pregunta(TypedDict):
    id: int
    area: str
    tipo: str
    enunciado: str
    alternativas: list[str]
    correcta: int


PREGUNTAS_DEMO: list[Pregunta] = [
    {
        "id": 1,
        "area": "Matemática",
        "tipo": "Alternativa",
        "enunciado": "Si 3x + 5 = 20, ¿cuál es el valor de x?",
        "alternativas": ["3", "5", "7", "15"],
        "correcta": 1,
    },
    {
        "id": 2,
        "area": "Matemática",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el área de un círculo de radio 4?",
        "alternativas": ["8π", "12π", "16π", "32π"],
        "correcta": 2,
    },
    {
        "id": 3,
        "area": "Comunicación",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el sinónimo de 'efímero'?",
        "alternativas": ["Eterno", "Pasajero", "Robusto", "Constante"],
        "correcta": 1,
    },
    {
        "id": 4,
        "area": "Comunicación",
        "tipo": "Verdadero/Falso",
        "enunciado": "El sujeto siempre concuerda en número y persona con el verbo.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 0,
    },
    {
        "id": 5,
        "area": "Ciencias Naturales",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el órgano principal del sistema circulatorio?",
        "alternativas": ["Pulmón", "Hígado", "Corazón", "Cerebro"],
        "correcta": 2,
    },
    {
        "id": 6,
        "area": "Ciencias Naturales",
        "tipo": "Verdadero/Falso",
        "enunciado": "La fotosíntesis se realiza únicamente durante la noche.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 1,
    },
    {
        "id": 7,
        "area": "Cultura General",
        "tipo": "Alternativa",
        "enunciado": "¿En qué año se fundó la UNAS?",
        "alternativas": ["1962", "1964", "1970", "1980"],
        "correcta": 0,
    },
    {
        "id": 8,
        "area": "Cultura General",
        "tipo": "Verdadero/Falso",
        "enunciado": "Tingo María se ubica en la región Huánuco.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 0,
    },
    {
        "id": 9,
        "area": "Psicotécnico",
        "tipo": "Alternativa",
        "enunciado": "Continúa la secuencia: 2, 4, 8, 16, ...",
        "alternativas": ["18", "24", "32", "20"],
        "correcta": 2,
    },
    {
        "id": 10,
        "area": "Psicotécnico",
        "tipo": "Alternativa",
        "enunciado": "Si todos los gatos son felinos y algunos felinos son salvajes, entonces:",
        "alternativas": [
            "Todos los gatos son salvajes",
            "Ningún gato es salvaje",
            "Algunos gatos pueden ser salvajes",
            "Los felinos son gatos",
        ],
        "correcta": 2,
    },
]


class ExamenState(rx.State):
    preguntas: list[Pregunta] = PREGUNTAS_DEMO
    respuestas: dict[int, int] = {}
    indice_actual: int = 0
    tiempo_restante: int = 180 * 60
    examen_iniciado: bool = False
    examen_finalizado: bool = False
    timer_activo: bool = False
    puntaje: int = 0
    correctas: int = 0
    condicion: str = ""

    @rx.var
    def total_preguntas(self) -> int:
        return len(self.preguntas)

    @rx.var
    def respondidas(self) -> int:
        return len(self.respuestas)

    @rx.var
    def progreso(self) -> float:
        if len(self.preguntas) == 0:
            return 0.0
        return (len(self.respuestas) / len(self.preguntas)) * 100.0

    @rx.var
    def pregunta_actual(self) -> Pregunta:
        if 0 <= self.indice_actual < len(self.preguntas):
            return self.preguntas[self.indice_actual]
        return self.preguntas[0]

    @rx.var
    def respuesta_actual(self) -> int:
        return self.respuestas.get(self.indice_actual, -1)

    @rx.var
    def tiempo_formateado(self) -> str:
        h = self.tiempo_restante // 3600
        m = (self.tiempo_restante % 3600) // 60
        s = self.tiempo_restante % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @rx.var
    def tiempo_critico(self) -> bool:
        return self.tiempo_restante <= 600 and self.tiempo_restante > 0

    @rx.event
    def iniciar_examen(self):
        self.examen_iniciado = True
        self.examen_finalizado = False
        self.respuestas = {}
        self.indice_actual = 0
        self.tiempo_restante = 180 * 60
        self.puntaje = 0
        self.correctas = 0
        self.condicion = ""
        self.timer_activo = True
        return ExamenState.tick_timer

    @rx.event(background=True)
    async def tick_timer(self):
        while True:
            await asyncio.sleep(1)
            async with self:
                if not self.timer_activo or self.examen_finalizado:
                    return
                if self.tiempo_restante <= 0:
                    self.timer_activo = False
                    self._calcular_resultado()
                    return
                self.tiempo_restante -= 1

    @rx.event
    def seleccionar_respuesta(self, idx: int):
        self.respuestas[self.indice_actual] = idx

    @rx.event
    def ir_pregunta(self, idx: int):
        if 0 <= idx < len(self.preguntas):
            self.indice_actual = idx

    @rx.event
    def siguiente(self):
        if self.indice_actual < len(self.preguntas) - 1:
            self.indice_actual += 1

    @rx.event
    def anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1

    def _calcular_resultado(self):
        correctas = 0
        for i, p in enumerate(self.preguntas):
            if self.respuestas.get(i, -1) == p["correcta"]:
                correctas += 1
        # Exact calculation: 1 point per correct answer
        # Condición: INGRESÓ if correctas > 51
        self.correctas = correctas
        self.puntaje = correctas
        self.condicion = "INGRESÓ" if self.correctas > 51 else "NO INGRESÓ"
        self.examen_finalizado = True
        self.timer_activo = False

    @rx.event
    def finalizar_examen(self):
        self._calcular_resultado()
        return rx.toast(
            f"Examen finalizado. {self.correctas}/{len(self.preguntas)} correctas",
            duration=3000,
        )

    @rx.event
    def reiniciar(self):
        self.examen_iniciado = False
        self.examen_finalizado = False
        self.respuestas = {}
        self.indice_actual = 0
        self.tiempo_restante = 180 * 60
        self.puntaje = 0
        self.correctas = 0
        self.condicion = ""
        self.timer_activo = False