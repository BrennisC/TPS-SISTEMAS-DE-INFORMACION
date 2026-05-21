import reflex as rx
from typing import TypedDict


class Resultado(TypedDict):
    id: int
    nombres: str
    apellidos: str
    dni: str
    carrera: str
    puntaje: float
    correctas: int
    condicion: str
    ranking: int


RESULTADOS_DEMO: list[Resultado] = [
    {
        "id": 1,
        "nombres": "María Fernanda",
        "apellidos": "Quispe Huamán",
        "dni": "73829145",
        "carrera": "Ingeniería Forestal",
        "puntaje": 78.5,
        "correctas": 78,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 2,
        "nombres": "Carlos Andrés",
        "apellidos": "Rojas Ventura",
        "dni": "74512893",
        "carrera": "Agronomía",
        "puntaje": 82.0,
        "correctas": 82,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 3,
        "nombres": "Diana Lucía",
        "apellidos": "Mendoza Paredes",
        "dni": "72938174",
        "carrera": "Ingeniería de Sistemas e Informática",
        "puntaje": 65.0,
        "correctas": 65,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 4,
        "nombres": "Jorge Luis",
        "apellidos": "Salazar Cárdenas",
        "dni": "75829341",
        "carrera": "Administración de Empresas",
        "puntaje": 48.0,
        "correctas": 48,
        "condicion": "NO INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 5,
        "nombres": "Andrea Sofía",
        "apellidos": "Campos Lazo",
        "dni": "76123498",
        "carrera": "Medicina Veterinaria",
        "puntaje": 71.5,
        "correctas": 71,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 6,
        "nombres": "Pedro Antonio",
        "apellidos": "Vargas Ruiz",
        "dni": "77891234",
        "carrera": "Ingeniería Forestal",
        "puntaje": 92.0,
        "correctas": 92,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 7,
        "nombres": "Lucía Esther",
        "apellidos": "Flores Cabrera",
        "dni": "78123456",
        "carrera": "Agronomía",
        "puntaje": 35.0,
        "correctas": 35,
        "condicion": "NO INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 8,
        "nombres": "Ricardo Manuel",
        "apellidos": "Aguilar Soto",
        "dni": "79234567",
        "carrera": "Economía",
        "puntaje": 60.0,
        "correctas": 60,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 9,
        "nombres": "Carmen Rosa",
        "apellidos": "Diaz Pérez",
        "dni": "70345678",
        "carrera": "Enfermería",
        "puntaje": 55.0,
        "correctas": 55,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 10,
        "nombres": "Daniel Eduardo",
        "apellidos": "Gómez Lara",
        "dni": "71456789",
        "carrera": "Contabilidad",
        "puntaje": 42.0,
        "correctas": 42,
        "condicion": "NO INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 11,
        "nombres": "Valeria Nicole",
        "apellidos": "Ríos Camacho",
        "dni": "72567890",
        "carrera": "Ingeniería de Sistemas e Informática",
        "puntaje": 88.0,
        "correctas": 88,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
    {
        "id": 12,
        "nombres": "Alonso Javier",
        "apellidos": "Castro Mejía",
        "dni": "73678901",
        "carrera": "Medicina Veterinaria",
        "puntaje": 53.0,
        "correctas": 53,
        "condicion": "INGRESÓ",
        "ranking": 0,
    },
]


CARRERAS_RES: list[str] = sorted({r["carrera"] for r in RESULTADOS_DEMO})


class ResultadosState(rx.State):
    resultados: list[Resultado] = RESULTADOS_DEMO
    filter_carrera: str = "Todas"
    search_query: str = ""
    carreras: list[str] = CARRERAS_RES

    @rx.var
    def ranking_ordenado(self) -> list[Resultado]:
        result = list(self.resultados)
        if self.filter_carrera != "Todas":
            result = [r for r in result if r["carrera"] == self.filter_carrera]
        if self.search_query.strip():
            q = self.search_query.lower().strip()
            result = [
                r
                for r in result
                if q in r["nombres"].lower()
                or q in r["apellidos"].lower()
                or q in r["dni"]
            ]
        # Sort descending by puntaje
        result.sort(key=lambda r: r["puntaje"], reverse=True)
        # Re-assign ranking
        ranked: list[Resultado] = []
        for i, r in enumerate(result):
            ranked.append({**r, "ranking": i + 1})
        return ranked

    @rx.var
    def total_ingresantes(self) -> int:
        return len([r for r in self.resultados if r["condicion"] == "INGRESÓ"])

    @rx.var
    def total_no_ingresantes(self) -> int:
        return len(
            [r for r in self.resultados if r["condicion"] == "NO INGRESÓ"]
        )

    @rx.var
    def promedio_general(self) -> float:
        if not self.resultados:
            return 0.0
        return sum(r["puntaje"] for r in self.resultados) / len(self.resultados)

    @rx.var
    def puntaje_top(self) -> float:
        if not self.resultados:
            return 0.0
        return max(r["puntaje"] for r in self.resultados)

    @rx.event
    def set_filter_carrera(self, v: str):
        self.filter_carrera = v

    @rx.event
    def set_search_query(self, v: str):
        self.search_query = v

    @rx.event
    def exportar_pdf(self):
        return rx.toast(
            f"Exportando ranking de {ResultadosState.ranking_ordenado.length()} postulantes a PDF...",
            duration=3000,
        )

    @rx.event
    def exportar_excel(self):
        return rx.toast(
            f"Exportando ranking de {ResultadosState.ranking_ordenado.length()} postulantes a Excel...",
            duration=3000,
        )