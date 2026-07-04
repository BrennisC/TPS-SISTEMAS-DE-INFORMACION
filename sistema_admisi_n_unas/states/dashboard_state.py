from typing import Dict, List

import reflex as rx
from annotated_types import T

# Importamos tus funciones nativas
from ..utils.csv_loader import cargar_postulantes


class DashboardState(rx.State):
    # Tab del dashboard activo: "admision" o "finanzas"
    active_dashboard_tab: str = "admision"

    # KPIs Básicos que se reflejan en las cards
    current_page: str = "Dashboard"
    mobile_menu_open: bool = False
    expanded_sidebar: list[str] = []

    total_postulantes: int = 0
    admitted_count: int = 0
    total_recaudado: float = 0.0
    total_estatal: int = 0
    total_privado: int = 0
    top_career: str = "Cargando..."
    general_avg: float = 0.0
    # Listas dinámicas para alimentar a Recharts
    chart_postulantes_vs_ingresantes: List[Dict] = []
    chart_rendimiento_areas: List[Dict] = []
    chart_evolucion_historica: List[Dict] = []
    chart_genero: List[Dict] = []
    chart_puntajes_rango: list[dict[str, int | str]] = []
    chart_promedio_convocatoria: list[dict[str, float | str]] = []
    chart_top_carreras_puntaje: list[dict[str, float | str]] = []
    paginated_postulantes: list[dict[str, str]] = []

    @rx.var
    def general_avg_percentage(self) -> float:
        # Evitar división por cero o promedios inconsistentes
        val = self.general_avg if self.general_avg <= 20.0 else 20.0
        return round((val / 20.0) * 100.0, 2)

    @rx.var
    def gauge_needle_angle(self) -> float:
        val = self.general_avg if self.general_avg <= 20.0 else 20.0
        # 0 de promedio -> 0 grados (apunta a la izquierda)
        # 20 de promedio -> 180 grados (apunta a la derecha)
        return round((val / 20.0) * 180.0, 2)

    @rx.var
    def general_avg_low(self) -> bool:
        return self.general_avg < 10.5

    @rx.var
    def general_avg_medium(self) -> bool:
        return 10.5 <= self.general_avg < 14.0

    @rx.var
    def general_avg_high(self) -> bool:
        return self.general_avg >= 14.0

    @rx.event
    def set_page(self, page: str):
        self.current_page = page

    @rx.event
    def toggle_mobile_menu(self):
        self.mobile_menu_open = not self.mobile_menu_open

    @rx.event
    def close_mobile_menu(self):
        self.mobile_menu_open = False

    @rx.event
    def toggle_sidebar_section(self, section: str):
        if section in self.expanded_sidebar:
            self.expanded_sidebar.remove(section)
        else:
            self.expanded_sidebar.append(section)

    @rx.event
    def set_dashboard_tab(self, tab: str):
        """Cambia entre el dashboard de admisión y finanzas."""
        self.active_dashboard_tab = tab
        if tab == "finanzas":
            from .recaudacion_state import RecaudacionState
            return RecaudacionState.cargar_datos_recaudacion

    @rx.event
    def cargar_datos_csv(self):
        """
        Ejecuta tu función nativa en segundo plano para no congelar el frontend
        y calcula las agrupaciones requeridas por los gráficos de Recharts.
        """
        try:
            # 1. Cargamos el archivo usando TU función nativa
            # (Por defecto busca 'postulantes.csv' usando tu ruta relativa corregida)
            lista_postulantes = cargar_postulantes()
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")
            return

        if not lista_postulantes:
            return

        # 2. Procesamiento y cálculo de métricas usando bucles limpios de Python
        total_p = len(lista_postulantes)
        ingresantes = [
            p for p in lista_postulantes if p["estado"].strip().lower() == "ingresante"
        ]
        total_ing = len(ingresantes)

        recaudado = sum(p["costo"] for p in lista_postulantes)
        estatal = sum(
            1
            for p in lista_postulantes
            if p["tipo_colegio"].strip().lower() == "estatal"
        )
        privado = total_p - estatal

        # Calcular promedios y carreras más demandadas
        conteo_carreras = {}
        suma_puntajes = 0.0
        conteo_puntajes = 0

        for p in lista_postulantes:
            carrera = p["carrera"]
            conteo_carreras[carrera] = conteo_carreras.get(carrera, 0) + 1
            if p["puntaje"] > 0:
                suma_puntajes += p["puntaje"]
                conteo_puntajes += 1

        top_c = (
            max(conteo_carreras, key=conteo_carreras.get) if conteo_carreras else "N/A"
        )
        avg_general = (suma_puntajes / conteo_puntajes) if conteo_puntajes > 0 else 0.0

        # 3. Construcción de la Estructura para el Gráfico: Postulantes vs Ingresantes
        carreras_unicas = set(p["carrera"] for p in lista_postulantes)
        mix_carreras = []
        for corr_carrera in carreras_unicas:
            post_c = sum(1 for p in lista_postulantes if p["carrera"] == corr_carrera)
            ing_c = sum(1 for p in ingresantes if p["carrera"] == corr_carrera)
            mix_carreras.append(
                {"carrera": corr_carrera, "Postulantes": post_c, "Ingresantes": ing_c}
            )

        # 4. Estructura para Rendimiento por Áreas (Agrupado por facultades del CSV)
        facultades_unicas = set(
            p["facultad"] for p in lista_postulantes if p["facultad"]
        )
        mix_areas = []
        for fac in facultades_unicas:
            puntajes_fac = [
                p["puntaje"]
                for p in lista_postulantes
                if p["facultad"] == fac and p["puntaje"] > 0
            ]
            avg_fac = (sum(puntajes_fac) / len(puntajes_fac)) if puntajes_fac else 0.0
            mix_areas.append({"area": fac, "avg_score": round(avg_fac, 2)})

        # 5. Estructura para Evolución Histórica (Agrupado por Convocatoria, ej: '2026-I')
        convocatorias_unicas = sorted(
            list(set(p["convocatoria"] for p in lista_postulantes))
        )
        mix_evolucion = []
        for conv in convocatorias_unicas:
            post_conv = sum(1 for p in lista_postulantes if p["convocatoria"] == conv)
            mix_evolucion.append({"year": conv, "Postulantes": post_conv})

        # 6. Distribución de Colegio para el Gráfico Donut/Circular
        mix_colegio = [
            {"name": "Estatal", "value": estatal, "fill": "#228B22"},
            {"name": "Privado", "value": privado, "fill": "#FFB020"},
        ]

        # 7. Distribución de puntajes por rangos
        rangos = [
            ("0-5", 0, 5),
            ("6-10", 6, 10),
            ("11-15", 11, 15),
            ("16-20", 16, 20),
        ]
        mix_rangos = []
        for etiqueta, minimo, maximo in rangos:
            cantidad = sum(
                1
                for p in lista_postulantes
                if p["puntaje"] > 0
                and minimo
                <= (p["puntaje"] / 5 if p["puntaje"] > 20 else p["puntaje"])
                <= maximo
            )
            mix_rangos.append({"rango": etiqueta, "cantidad": cantidad})

        # 8. Promedio por convocatoria
        mix_promedios_conv = []
        for conv in convocatorias_unicas:
            puntajes_conv = [
                p["puntaje"]
                for p in lista_postulantes
                if p["convocatoria"] == conv and p["puntaje"] > 0
            ]
            avg_conv = (
                (sum(puntajes_conv) / len(puntajes_conv)) if puntajes_conv else 0.0
            )
            mix_promedios_conv.append(
                {"convocatoria": conv, "avg_score": round(avg_conv, 2)}
            )

        # 9. Top carreras por puntaje promedio
        puntaje_por_carrera: dict[str, list[float]] = {}
        for p in lista_postulantes:
            if p["puntaje"] > 0:
                carrera = p["carrera"]
                puntaje_por_carrera.setdefault(carrera, []).append(p["puntaje"])
        mix_top_carreras = []
        for carrera, puntajes in puntaje_por_carrera.items():
            mix_top_carreras.append(
                {
                    "carrera": carrera,
                    "avg_score": round(sum(puntajes) / len(puntajes), 2),
                }
            )
        mix_top_carreras.sort(key=lambda item: item["avg_score"], reverse=True)
        mix_top_carreras = mix_top_carreras[:5]

        # 10. Mapear los últimos 5 alumnos para la Tabla del Dashboard
        ultimos_alumnos = []
        # Tomamos los últimos 5 agregados al CSV
        for p in lista_postulantes[-5:]:
            ultimos_alumnos.append(
                {
                    "dni": p["dni"],
                    "apellidos": p["apellidos"],
                    "nombres": p["nombres"],
                    "carrera": p["carrera"],
                    "estado": p["estado"],
                }
            )

        # 11. Guardamos los datos en el estado de Reflex
        self.total_postulantes = total_p
        self.admitted_count = total_ing
        self.total_recaudado = recaudado
        self.total_estatal = estatal
        self.total_privado = privado
        self.top_career = top_c
        self.general_avg = round(avg_general, 2)
        self.chart_postulantes_vs_ingresantes = mix_carreras
        self.chart_rendimiento_areas = mix_areas
        self.chart_evolucion_historica = mix_evolucion
        self.chart_genero = (
            mix_colegio  # Reutilizado dinámicamente como gráfico de Tipo de Colegio
        )
        self.chart_puntajes_rango = mix_rangos
        self.chart_promedio_convocatoria = mix_promedios_conv
        self.chart_top_carreras_puntaje = mix_top_carreras
        self.paginated_postulantes = ultimos_alumnos
