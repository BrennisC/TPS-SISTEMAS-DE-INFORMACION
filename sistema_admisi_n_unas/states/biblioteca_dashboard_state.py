"""
Estado del Dashboard Ejecutivo de Biblioteca.
Procesa datos del CSV y genera KPIs, datos de gráficos y alertas.
"""
import csv
import os
import random
from typing import Dict, List

import reflex as rx


def _ruta_archivo(nombre: str) -> str:
    return os.path.join(os.path.dirname(__file__), "..", nombre)


def _cargar_catalogo() -> list[dict]:
    ruta = _ruta_archivo("biblioteca_data.csv")
    catalogo = []
    with open(ruta, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            catalogo.append({
                "id": int(row["id"]),
                "codigo": row["codigo"],
                "titulo": row["titulo"],
                "autor": row["autor"],
                "categoria": row["categoria"],
                "editorial": row["editorial"],
                "stock": int(row["stock"]),
                "disponibles": int(row["disponibles"]),
                "estado": row["estado"],
                "prestamos_total": int(row["prestamos_total"]),
            })
    return catalogo


# Datos de ejemplo para préstamos (generados en memoria)
CARRERAS = [
    "Agronomía", "Ing. Informática y Sistemas", "Ing. Ambiental",
    "Ing. Forestal", "Zootecnia", "Administración", "Contabilidad",
    "Economía", "Ing. Mecánica Eléctrica", "Desarrollo Rural",
    "Ing. Conservación Suelos", "Ing. Recursos Naturales",
]

FACULTADES = [
    "Fac. Agronomía", "Fac. Ing. Informática y Sistemas",
    "Fac. Recursos Naturales Renovables", "Fac. Zootecnia",
    "Fac. Ciencias Económicas", "Otras Escuelas",
]

CARRERA_FACULTAD = {
    "Agronomía": "Fac. Agronomía",
    "Ing. Informática y Sistemas": "Fac. Ing. Informática y Sistemas",
    "Ing. Ambiental": "Fac. Recursos Naturales Renovables",
    "Ing. Forestal": "Fac. Recursos Naturales Renovables",
    "Zootecnia": "Fac. Zootecnia",
    "Administración": "Fac. Ciencias Económicas",
    "Contabilidad": "Fac. Ciencias Económicas",
    "Economía": "Fac. Ciencias Económicas",
    "Ing. Mecánica Eléctrica": "Otras Escuelas",
    "Ing. Conservación Suelos": "Fac. Recursos Naturales Renovables",
    "Turismo y Hoteleria": "FACEA",
    "Ing. Recursos Naturales": "Fac. Recursos Naturales Renovables",
}

TIPOS_USUARIO = ["Estudiante", "Docente", "Administrativo"]
DIAS_SEMANA = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
HORAS = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00",
         "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00"]


def _generar_prestamos_ejemplo(catalogo: list[dict]) -> list[dict]:
    """Genera ~200 préstamos de ejemplo con datos realistas."""
    random.seed(42)  # Reproducible
    prestamos = []
    estados = ["Activo", "Devuelto", "Vencido", "Próximo a vencer"]
    meses = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06", "2026-07"]

    for i in range(1, 201):
        carrera = random.choice(CARRERAS)
        facultad = CARRERA_FACULTAD.get(carrera, "Otras Escuelas")
        libro = random.choice(catalogo)
        mes = random.choice(meses)
        dia = random.randint(1, 28)
        estado = random.choices(estados, weights=[35, 40, 15, 10])[0]
        tipo = random.choices(TIPOS_USUARIO, weights=[70, 20, 10])[0]
        dias_prestamo = random.randint(3, 21)

        prestamos.append({
            "id": i,
            "lector": f"Lector {i:03d}",
            "dni": f"7{random.randint(1000000, 9999999)}",
            "carrera": carrera,
            "facultad": facultad,
            "libro_id": libro["id"],
            "libro_titulo": libro["titulo"],
            "libro_categoria": libro["categoria"],
            "fecha_prestamo": f"{mes}-{dia:02d}",
            "dias_prestamo": dias_prestamo,
            "estado": estado,
            "tipo_usuario": tipo,
            "dias_retraso": random.randint(1, 15) if estado == "Vencido" else 0,
        })
    return prestamos


from pydantic import BaseModel

class CeldaHeatmap(BaseModel):
    dia: str
    valor: str
    opacity: str

class FilaHeatmap(BaseModel):
    hora: str
    celdas: List[CeldaHeatmap]

def _generar_uso_horario() -> List[FilaHeatmap]:
    """Genera datos de uso por hora/día para el HeatMap estructurado por filas."""
    random.seed(123)
    datos = []
    max_valor = 40
    for hora in HORAS:
        fila = FilaHeatmap(hora=hora, celdas=[])
        for dia in DIAS_SEMANA:
            # Más uso entre 9-12 y 14-17
            h = int(hora.split(":")[0])
            base = 5
            if 9 <= h <= 12:
                base = 25
            elif 14 <= h <= 17:
                base = 20
            elif h == 8 or h == 13:
                base = 15
            valor = max(0, base + random.randint(-8, 12))
            # opacidad mínima 0.1, máxima 1.0
            opacity = round(max(0.1, min(1.0, valor / max_valor)), 2)
            fila.celdas.append(CeldaHeatmap(dia=dia, valor=str(valor), opacity=str(opacity)))
        datos.append(fila)
    return datos


class BibliotecaDashboardState(rx.State):
    """Estado completo del Dashboard Ejecutivo de Biblioteca."""

    # ─── KPIs ───────────────────────────────────────────
    total_libros: int = 0
    total_ejemplares_disponibles: int = 0
    total_lectores: int = 0
    prestamos_activos: int = 0
    prestamos_vencidos: int = 0
    devoluciones_dia: int = 0
    libros_mantenimiento: int = 0
    ocupacion_catalogo: float = 0.0
    tiempo_promedio_prestamo: float = 0.0
    indice_morosidad: float = 0.0

    # Tendencias (variación porcentual vs periodo anterior)
    tend_libros: float = 2.4
    tend_disponibles: float = -5.2
    tend_lectores: float = 8.1
    tend_activos: float = 12.3
    tend_vencidos: float = -3.7
    tend_devoluciones: float = 6.5
    tend_mantenimiento: float = 0.0
    tend_ocupacion: float = 4.2
    tend_tiempo: float = -1.8
    tend_morosidad: float = -2.1

    # ─── Datos de Gráficos ──────────────────────────────
    chart_estado_catalogo: list[dict] = []       # Dona
    chart_evolucion_prestamos: list[dict] = []   # Líneas
    chart_top_libros: list[dict] = []            # Barras horizontales
    chart_lectores_carrera: list[dict] = []      # Barras verticales
    chart_prestamos_facultad: list[dict] = []    # Barras agrupadas
    chart_material_categoria: list[dict] = []    # Barras (reemplazo treemap)
    heatmap_data: List[FilaHeatmap] = []                # HeatMap data estructurado
    chart_tiempo_comparativo: list[dict] = []    # Barras comparativas
    chart_libros_retraso: list[dict] = []        # Barras
    chart_tipo_usuario: list[dict] = []          # Pie

    # ─── Alertas ────────────────────────────────────────
    alertas: list[dict] = []

    # ─── HeatMap Grid ───────────────────────────────────
    heatmap_horas: list[str] = list(HORAS)
    heatmap_dias: list[str] = list(DIAS_SEMANA)

    @rx.event
    def cargar_dashboard_biblioteca(self):
        """Carga y procesa todos los datos del dashboard de biblioteca."""
        try:
            catalogo = _cargar_catalogo()
        except Exception as e:
            print(f"Error cargando catálogo: {e}")
            return

        prestamos = _generar_prestamos_ejemplo(catalogo)
        uso_horario = _generar_uso_horario()

        # ═══ KPIs ═══════════════════════════════════════
        self.total_libros = len(catalogo)
        self.total_ejemplares_disponibles = sum(l["disponibles"] for l in catalogo)
        self.total_lectores = len({p["dni"] for p in prestamos})
        self.prestamos_activos = sum(1 for p in prestamos if p["estado"] == "Activo")
        self.prestamos_vencidos = sum(1 for p in prestamos if p["estado"] == "Vencido")
        self.devoluciones_dia = sum(1 for p in prestamos if p["estado"] == "Devuelto" and p["fecha_prestamo"].startswith("2026-07"))
        self.libros_mantenimiento = sum(1 for l in catalogo if l["estado"] == "Mantenimiento")

        total_stock = sum(l["stock"] for l in catalogo)
        total_disponibles = sum(l["disponibles"] for l in catalogo)
        self.ocupacion_catalogo = round(((total_stock - total_disponibles) / total_stock) * 100, 1) if total_stock > 0 else 0.0

        dias_list = [p["dias_prestamo"] for p in prestamos]
        self.tiempo_promedio_prestamo = round(sum(dias_list) / len(dias_list), 1) if dias_list else 0.0

        total_prestamos = len(prestamos)
        self.indice_morosidad = round((self.prestamos_vencidos / total_prestamos) * 100, 1) if total_prestamos > 0 else 0.0

        # ═══ GRÁFICO 1: Estado del Catálogo (Dona) ═════
        disponibles = sum(1 for l in catalogo if l["estado"] == "Disponible")
        prestados = sum(1 for l in catalogo if l["estado"] == "Prestado")
        mantenimiento = sum(1 for l in catalogo if l["estado"] == "Mantenimiento")
        extraviados = sum(1 for l in catalogo if l["estado"] == "Extraviado")
        self.chart_estado_catalogo = [
            {"name": "Disponibles", "value": disponibles, "fill": "#22c55e"},
            {"name": "Prestados", "value": prestados, "fill": "#3b82f6"},
            {"name": "Mantenimiento", "value": mantenimiento, "fill": "#f59e0b"},
            {"name": "Extraviados", "value": extraviados, "fill": "#ef4444"},
        ]

        # ═══ GRÁFICO 2: Evolución Préstamos por Mes ════
        meses_count: Dict[str, int] = {}
        for p in prestamos:
            mes = p["fecha_prestamo"][:7]
            meses_count[mes] = meses_count.get(mes, 0) + 1
        self.chart_evolucion_prestamos = [
            {"mes": m, "prestamos": c} for m, c in sorted(meses_count.items())
        ]

        # ═══ GRÁFICO 3: Top 10 Libros Más Prestados ════
        libro_count: Dict[str, int] = {}
        for p in prestamos:
            libro_count[p["libro_titulo"]] = libro_count.get(p["libro_titulo"], 0) + 1
        top_libros = sorted(libro_count.items(), key=lambda x: x[1], reverse=True)[:10]
        self.chart_top_libros = [
            {"titulo": t, "prestamos": c} for t, c in top_libros
        ]

        # ═══ GRÁFICO 4: Lectores por Carrera ═══════════
        carrera_count: Dict[str, int] = {}
        for p in prestamos:
            carrera_count[p["carrera"]] = carrera_count.get(p["carrera"], 0) + 1
        self.chart_lectores_carrera = sorted(
            [{"carrera": k, "lectores": v} for k, v in carrera_count.items()],
            key=lambda x: x["lectores"], reverse=True
        )

        # ═══ GRÁFICO 5: Préstamos por Facultad ═════════
        fac_activos: Dict[str, int] = {}
        fac_vencidos: Dict[str, int] = {}
        fac_devueltos: Dict[str, int] = {}
        for p in prestamos:
            fac = p["facultad"]
            if p["estado"] == "Activo":
                fac_activos[fac] = fac_activos.get(fac, 0) + 1
            elif p["estado"] == "Vencido":
                fac_vencidos[fac] = fac_vencidos.get(fac, 0) + 1
            else:
                fac_devueltos[fac] = fac_devueltos.get(fac, 0) + 1
        all_facs = sorted(set(list(fac_activos.keys()) + list(fac_vencidos.keys()) + list(fac_devueltos.keys())))
        self.chart_prestamos_facultad = [
            {
                "facultad": f.replace("Fac. ", ""),
                "Activos": fac_activos.get(f, 0),
                "Vencidos": fac_vencidos.get(f, 0),
                "Devueltos": fac_devueltos.get(f, 0),
            }
            for f in all_facs
        ]

        # ═══ GRÁFICO 6: Material por Categoría ═════════
        cat_count: Dict[str, int] = {}
        for p in prestamos:
            cat_count[p["libro_categoria"]] = cat_count.get(p["libro_categoria"], 0) + 1
        self.chart_material_categoria = sorted(
            [{"categoria": k, "prestamos": v} for k, v in cat_count.items()],
            key=lambda x: x["prestamos"], reverse=True
        )

        # ═══ GRÁFICO 7: Uso Horario (HeatMap) ══════════
        self.heatmap_data = uso_horario

        # ═══ GRÁFICO 8: Tiempo Promedio vs Permitido ═══
        categorias_tiempo = ["Ciencias", "Informatica", "Agricultura", "Economia", "Humanidades", "Ingenieria"]
        self.chart_tiempo_comparativo = []
        random.seed(99)
        for cat in categorias_tiempo:
            cat_prestamos = [p for p in prestamos if p["libro_categoria"] == cat]
            real = round(sum(p["dias_prestamo"] for p in cat_prestamos) / max(len(cat_prestamos), 1), 1)
            self.chart_tiempo_comparativo.append({
                "categoria": cat, "real": real, "permitido": 14.0
            })

        # ═══ GRÁFICO 9: Top Libros con Mayor Retraso ═══
        retraso_count: Dict[str, int] = {}
        for p in prestamos:
            if p["dias_retraso"] > 0:
                retraso_count[p["libro_titulo"]] = retraso_count.get(p["libro_titulo"], 0) + p["dias_retraso"]
        top_retraso = sorted(retraso_count.items(), key=lambda x: x[1], reverse=True)[:10]
        self.chart_libros_retraso = [
            {"titulo": t, "dias_retraso": d} for t, d in top_retraso
        ]

        # ═══ GRÁFICO 10: Distribución por Tipo Usuario ═
        tipo_count: Dict[str, int] = {}
        for p in prestamos:
            tipo_count[p["tipo_usuario"]] = tipo_count.get(p["tipo_usuario"], 0) + 1
        colores_tipo = {"Estudiante": "#22c55e", "Docente": "#3b82f6", "Administrativo": "#f59e0b"}
        self.chart_tipo_usuario = [
            {"name": k, "value": v, "fill": colores_tipo.get(k, "#94a3b8")}
            for k, v in tipo_count.items()
        ]

        # ═══ ALERTAS ═══════════════════════════════════
        alertas = []
        if self.prestamos_vencidos > 0:
            alertas.append({
                "tipo": "critico", "icono": "triangle-alert",
                "titulo": f"{self.prestamos_vencidos} préstamos vencidos",
                "desc": "Requieren seguimiento inmediato",
            })
        proximos = sum(1 for p in prestamos if p["estado"] == "Próximo a vencer")
        if proximos > 0:
            alertas.append({
                "tipo": "advertencia", "icono": "clock",
                "titulo": f"{proximos} préstamos próximos a vencer",
                "desc": "Enviar recordatorios a los lectores",
            })
        if extraviados > 0:
            alertas.append({
                "tipo": "critico", "icono": "book-x",
                "titulo": f"{extraviados} libros extraviados",
                "desc": "Iniciar proceso de reposición",
            })
        # Alta demanda
        alta_demanda = [l for l in catalogo if l["prestamos_total"] > 60]
        if alta_demanda:
            alertas.append({
                "tipo": "advertencia", "icono": "trending-up",
                "titulo": f"{len(alta_demanda)} libros con alta demanda",
                "desc": "Considerar adquisición de más ejemplares",
            })
        # Stock crítico
        stock_critico = [l for l in catalogo if l["disponibles"] == 0 and l["estado"] != "Extraviado"]
        if stock_critico:
            alertas.append({
                "tipo": "critico", "icono": "package-x",
                "titulo": f"{len(stock_critico)} libros sin stock",
                "desc": "No hay ejemplares disponibles para préstamo",
            })
        if mantenimiento > 0:
            alertas.append({
                "tipo": "advertencia", "icono": "wrench",
                "titulo": f"{mantenimiento} libros en mantenimiento",
                "desc": "Pendientes de reparación o encuadernación",
            })
        # Normal
        if self.ocupacion_catalogo < 60:
            alertas.append({
                "tipo": "normal", "icono": "circle-check",
                "titulo": "Ocupación del catálogo normal",
                "desc": f"Nivel actual: {self.ocupacion_catalogo}%",
            })

        self.alertas = alertas
