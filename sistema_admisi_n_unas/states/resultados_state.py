import reflex as rx
from typing import TypedDict

from sistema_admisi_n_unas.utils.csv_loader import cargar_postulantes


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
    convocatoria: str
    fecha: str


class ResultadosState(rx.State):
    resultados: list[Resultado] = []
    filter_carrera: str = "Todas"
    search_query: str = ""
    carreras: list[str] = []
    filter_condicion: str = "Todas"
    current_page: int = 1
    page_size: int = 15

    @staticmethod
    def _normalizar_condicion(estado: str, puntaje: float) -> str:
        estado_norm = estado.strip().lower()
        if "no" in estado_norm and "ingres" in estado_norm:
            return "NO INGRESÓ"
        if "ingres" in estado_norm:
            return "INGRESÓ"
        return "INGRESÓ" if puntaje >= 51 else "NO INGRESÓ"

    @rx.event
    def cargar_resultados(self):
        try:
            datos = cargar_postulantes()
        except Exception as exc:
            print(f"Error al leer resultados desde CSV: {exc}")
            return

        if not datos:
            return

        resultados: list[Resultado] = []
        for row in datos:
            puntaje = float(row.get("puntaje", 0) or 0)
            convocatoria = row.get("convocatoria", "")
            fecha = row.get("fecha", "")
            resultados.append(
                {
                    "id": int(row.get("id", 0) or 0),
                    "nombres": row.get("nombres", ""),
                    "apellidos": row.get("apellidos", ""),
                    "dni": row.get("dni", ""),
                    "carrera": row.get("carrera", ""),
                    "puntaje": puntaje,
                    "correctas": int(round(puntaje)) if puntaje > 0 else 0,
                    "condicion": self._normalizar_condicion(
                        row.get("estado", ""), puntaje
                    ),
                    "ranking": 0,
                    "convocatoria": convocatoria,
                    "fecha": fecha,
                }
            )

        self.resultados = resultados
        self.carreras = sorted({r["carrera"] for r in resultados if r["carrera"]})

    @rx.var
    def ranking_ordenado(self) -> list[Resultado]:
        result = list(self.resultados)
        if self.filter_carrera != "Todas":
            result = [r for r in result if r["carrera"] == self.filter_carrera]
        if self.filter_condicion != "Todas":
            result = [r for r in result if r["condicion"] == self.filter_condicion]
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
    def total_pages(self) -> int:
        total = len(self.ranking_ordenado)
        if total == 0:
            return 1
        return (total + self.page_size - 1) // self.page_size

    @rx.var
    def paginated_resultados(self) -> list[Resultado]:
        page = min(max(self.current_page, 1), self.total_pages)
        start = (page - 1) * self.page_size
        end = start + self.page_size
        return self.ranking_ordenado[start:end]

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
        self.current_page = 1

    @rx.event
    def set_search_query(self, v: str):
        self.search_query = v
        self.current_page = 1

    @rx.event
    def set_filter_condicion(self, v: str):
        self.filter_condicion = v
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
    def exportar_pdf(self):
        count = len(self.ranking_ordenado)
        return rx.toast(
            f"Exportando ranking de {count} postulantes a PDF...",
            duration=3000,
        )

    @rx.event
    def exportar_excel(self):
        count = len(self.ranking_ordenado)
        return rx.toast(
            f"Exportando ranking de {count} postulantes a Excel...",
            duration=3000,
        )
