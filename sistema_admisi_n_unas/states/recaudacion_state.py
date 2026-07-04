import csv
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import reflex as rx
from pydantic import BaseModel
from collections import defaultdict

# --- Modelos Pydantic para tipado de Reflex ---
class EvolucionRecaudacion(BaseModel):
    fecha: str
    monto: float

class ComparacionColegio(BaseModel):
    mes: str
    estatal: float
    privado: float

class EstadoPago(BaseModel):
    name: str
    value: int
    fill: str

class RecaudacionFacultad(BaseModel):
    facultad: str
    monto: float

class IngresoConcepto(BaseModel):
    name: str
    value: float
    fill: str

class EvolucionPagos(BaseModel):
    mes: str
    cantidad: int

class ComparacionConvocatoria(BaseModel):
    convocatoria: str
    estatal: float
    privado: float

class GaugeData(BaseModel):
    name: str
    value: float
    fill: str

class RankingCarrera(BaseModel):
    carrera: str
    monto: float

class CeldaHeatmap(BaseModel):
    dia: str
    valor: str
    opacity: str

class FilaHeatmap(BaseModel):
    hora: str
    celdas: List[CeldaHeatmap]

class FunnelData(BaseModel):
    name: str
    value: int
    fill: str

class TendenciaPromedio(BaseModel):
    mes: str
    promedio: float

class TablaEjecutiva(BaseModel):
    facultad: str
    total_recaudado: float
    pagos_validados: int
    pagos_pendientes: int
    pagos_observados: int
    porcentaje_validado: float
    variacion_mensual: float

class AlertaFinanciera(BaseModel):
    tipo: str  # rojo, amarillo, verde
    mensaje: str
    icono: str

# -----------------------------------------------

def _ruta_archivo(nombre: str) -> str:
    return os.path.join(os.path.dirname(__file__), "..", nombre)

def generar_datos_si_no_existen(ruta: str):
    if os.path.exists(ruta):
        return
    import sys
    # Import from the script we just wrote if possible, otherwise generate inline
    # To keep it safe, inline generator
    NUM_REGISTROS = 5000
    CONVOCATORIAS = ["2023-I", "2023-II", "2024-I", "2024-II", "2025-I"]
    FACULTADES_CARRERAS = {
        "Agronomía": ["Agronomía"],
        "Ing. Informática": ["Ing. Informática y Sistemas"],
        "RRNN": ["Ing. Ambiental", "Ing. Forestal", "Ing. Conser. Suelos", "Ing. RRNN"],
        "Zootecnia": ["Zootecnia"],
        "Económicas": ["Administración", "Contabilidad", "Economía"],
        "Otras": ["Ing. Mecánica", "Desarrollo Rural"]
    }
    TIPO_COLEGIO = ["Estatal", "Privado"]
    ESTADO_PAGO = ["Validado", "Pendiente", "Observado"]
    ESTADO_WEIGHTS = [0.75, 0.15, 0.10]
    CONCEPTO_PAGO = ["Inscripción", "Examen", "Matrícula", "Constancias", "Otros"]
    CONCEPTO_WEIGHTS = [0.4, 0.3, 0.2, 0.05, 0.05]
    CONCEPTO_MONTOS = {
        "Inscripción": (200, 300), "Examen": (150, 250), "Matrícula": (350, 500),
        "Constancias": (30, 80), "Otros": (50, 150)
    }

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 7, 1)
    data = []
    
    for i in range(1, NUM_REGISTROS + 1):
        facultad = random.choice(list(FACULTADES_CARRERAS.keys()))
        carrera = random.choice(FACULTADES_CARRERAS[facultad])
        fecha = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        
        if fecha.year == 2023:
            conv = "2023-I" if fecha.month <= 6 else "2023-II"
        elif fecha.year == 2024:
            conv = "2024-I" if fecha.month <= 6 else "2024-II"
        else:
            conv = "2025-I"
            
        estado = random.choices(ESTADO_PAGO, weights=ESTADO_WEIGHTS)[0]
        concepto = random.choices(CONCEPTO_PAGO, weights=CONCEPTO_WEIGHTS)[0]
        monto = round(random.uniform(*CONCEPTO_MONTOS[concepto]), 2)
        
        paso_embudo = 1
        if estado == "Validado":
            paso_embudo = random.choices([2, 3], weights=[0.4, 0.6])[0]
            if concepto == "Matrícula":
                paso_embudo = 3

        data.append({
            "id": i,
            "fecha": fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "convocatoria": conv,
            "facultad": facultad,
            "carrera": carrera,
            "tipo_colegio": random.choices(TIPO_COLEGIO, weights=[0.6, 0.4])[0],
            "estado_pago": estado,
            "concepto": concepto,
            "monto": monto,
            "paso_embudo": paso_embudo
        })
        
    data.sort(key=lambda x: x["fecha"])
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


class RecaudacionState(rx.State):
    """Estado interactivo del Dashboard Ejecutivo Financiero"""
    
    # --- Filtros Globales ---
    filtro_año: str = "Todos"
    filtro_mes: str = "Todos"
    filtro_convocatoria: str = "Todos"
    
    opciones_años: List[str] = ["Todos", "2023", "2024", "2025"]
    opciones_meses: List[str] = ["Todos", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    opciones_convocatorias: List[str] = ["Todos", "2023-I", "2023-II", "2024-I", "2024-II", "2025-I"]

    # --- KPIs Principales ---
    kpi_total_recaudado: str = "0.00"
    kpi_recaudacion_estatal: str = "0.00"
    kpi_recaudacion_privada: str = "0.00"
    kpi_pagos_validados: int = 0
    kpi_pagos_pendientes: int = 0
    kpi_pagos_observados: int = 0
    
    # --- Variables para Gráficos ---
    data_evolucion_recaudacion: List[Dict[str, Any]] = []
    data_comparacion_colegio: List[Dict[str, Any]] = []
    data_estado_pagos: List[Dict[str, Any]] = []
    data_recaudacion_facultad: List[Dict[str, Any]] = []
    data_ingresos_concepto: List[Dict[str, Any]] = []
    data_evolucion_pagos: List[Dict[str, Any]] = []
    data_comparacion_convocatoria: List[Dict[str, Any]] = []
    data_meta_recaudacion: List[Dict[str, Any]] = []
    data_morosidad: List[Dict[str, Any]] = []
    data_ranking_carreras: List[Dict[str, Any]] = []
    data_heatmap: List[FilaHeatmap] = []
    data_embudo: List[Dict[str, Any]] = []
    data_tendencia_promedio: List[Dict[str, Any]] = []
    
    data_tabla_ejecutiva: List[TablaEjecutiva] = []
    alertas_financieras: List[AlertaFinanciera] = []
    
    heatmap_horas: List[str] = ["08:00", "10:00", "12:00", "14:00", "16:00"]
    heatmap_dias: List[str] = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]
    
    # Raw Data cache
    _raw_data: List[Dict[str, Any]] = []

    def set_filtro_año(self, value: str):
        self.filtro_año = value
        self._procesar_datos()

    def set_filtro_mes(self, value: str):
        self.filtro_mes = value
        self._procesar_datos()

    def set_filtro_convocatoria(self, value: str):
        self.filtro_convocatoria = value
        self._procesar_datos()

    @rx.event
    def cargar_datos_recaudacion(self):
        ruta = _ruta_archivo("finanzas_data.csv")
        generar_datos_si_no_existen(ruta)
        
        datos = []
        try:
            with open(ruta, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    datos.append({
                        "fecha": row["fecha"],
                        "convocatoria": row["convocatoria"],
                        "facultad": row["facultad"],
                        "carrera": row["carrera"],
                        "tipo_colegio": row["tipo_colegio"],
                        "estado_pago": row["estado_pago"],
                        "concepto": row["concepto"],
                        "monto": float(row["monto"]),
                        "paso_embudo": int(row["paso_embudo"])
                    })
            self._raw_data = datos
            self._procesar_datos()
        except Exception as e:
            print(f"Error cargando finanzas_data.csv: {e}")

    def _procesar_datos(self):
        if not self._raw_data:
            return
            
        # Filtrar datos
        datos = []
        for d in self._raw_data:
            # Filtro de año
            año_dt = d["fecha"][:4]
            mes_dt = d["fecha"][5:7]
            if self.filtro_año != "Todos" and año_dt != self.filtro_año:
                continue
            if self.filtro_mes != "Todos" and mes_dt != self.filtro_mes:
                continue
            if self.filtro_convocatoria != "Todos" and d["convocatoria"] != self.filtro_convocatoria:
                continue
            datos.append(d)
            
        if not datos:
            return

        # 1. KPIs
        tot = sum(d["monto"] for d in datos)
        est = sum(d["monto"] for d in datos if d["tipo_colegio"] == "Estatal")
        pri = sum(d["monto"] for d in datos if d["tipo_colegio"] == "Privado")
        self.kpi_total_recaudado = f"{tot:,.2f}"
        self.kpi_recaudacion_estatal = f"{est:,.2f}"
        self.kpi_recaudacion_privada = f"{pri:,.2f}"
        
        self.kpi_pagos_validados = sum(1 for d in datos if d["estado_pago"] == "Validado")
        self.kpi_pagos_pendientes = sum(1 for d in datos if d["estado_pago"] == "Pendiente")
        self.kpi_pagos_observados = sum(1 for d in datos if d["estado_pago"] == "Observado")
        
        # 2. Evolución de Recaudación (Líneas)
        agrup_mes = defaultdict(float)
        for d in datos:
            k = d["fecha"][:7] # YYYY-MM
            agrup_mes[k] += d["monto"]
        self.data_evolucion_recaudacion = [{"fecha": k, "monto": round(v,2)} for k, v in sorted(agrup_mes.items())]
        
        # 3. Comparación Estatal vs Privado (Área apilada)
        comp_mes = defaultdict(lambda: {"estatal": 0.0, "privado": 0.0})
        for d in datos:
            k = d["fecha"][:7]
            if d["tipo_colegio"] == "Estatal":
                comp_mes[k]["estatal"] += d["monto"]
            else:
                comp_mes[k]["privado"] += d["monto"]
        self.data_comparacion_colegio = [
            {"mes": k, "estatal": round(v["estatal"],2), "privado": round(v["privado"],2)}
            for k, v in sorted(comp_mes.items())
        ]
        
        # 4. Estado de Pagos (Dona)
        self.data_estado_pagos = [
            {"name": "Validados", "value": self.kpi_pagos_validados, "fill": "#10b981"},
            {"name": "Pendientes", "value": self.kpi_pagos_pendientes, "fill": "#f59e0b"},
            {"name": "Observados", "value": self.kpi_pagos_observados, "fill": "#ef4444"},
        ]
        
        # 5. Recaudación por Facultad (Barras H)
        facultades = defaultdict(float)
        for d in datos: facultades[d["facultad"]] += d["monto"]
        self.data_recaudacion_facultad = [
            {"facultad": k, "monto": round(v,2)} for k, v in sorted(facultades.items(), key=lambda x: x[1], reverse=True)
        ]
        
        # 6. Ingresos por concepto (Pie)
        conceptos = defaultdict(float)
        colors = {"Inscripción": "#3b82f6", "Examen": "#8b5cf6", "Matrícula": "#ec4899", "Constancias": "#14b8a6", "Otros": "#94a3b8"}
        for d in datos: conceptos[d["concepto"]] += d["monto"]
        self.data_ingresos_concepto = [
            {"name": k, "value": round(v,2), "fill": colors.get(k, "#94a3b8")} for k, v in conceptos.items()
        ]
        
        # 7. Evolución de pagos registrados (Área)
        ev_pagos = defaultdict(int)
        for d in datos: ev_pagos[d["fecha"][:7]] += 1
        self.data_evolucion_pagos = [{"mes": k, "cantidad": v} for k, v in sorted(ev_pagos.items())]
        
        # 8. Comparación por Convocatoria
        conv = defaultdict(lambda: {"estatal": 0.0, "privado": 0.0})
        for d in datos:
            if d["tipo_colegio"] == "Estatal":
                conv[d["convocatoria"]]["estatal"] += d["monto"]
            else:
                conv[d["convocatoria"]]["privado"] += d["monto"]
        self.data_comparacion_convocatoria = [
            {"convocatoria": k, "estatal": round(v["estatal"],2), "privado": round(v["privado"],2)}
            for k, v in sorted(conv.items())
        ]
        
        # 9. Meta Recaudación y Morosidad (Gauges - Half Donuts)
        meta = 3000000.0 if self.filtro_año == "Todos" else 1000000.0
        alcanzado = tot
        faltante = meta - alcanzado if meta > alcanzado else 0
        self.data_meta_recaudacion = [
            {"name": "Alcanzado", "value": round(alcanzado,2), "fill": "#10b981"},
            {"name": "Faltante", "value": round(faltante,2), "fill": "#e2e8f0"},
        ]
        
        total_pagos = len(datos)
        morosidad_val = self.kpi_pagos_pendientes + self.kpi_pagos_observados
        morosidad_ok = total_pagos - morosidad_val
        self.data_morosidad = [
            {"name": "Morosidad", "value": morosidad_val, "fill": "#f59e0b"},
            {"name": "Al día", "value": morosidad_ok, "fill": "#e2e8f0"},
        ]
        
        # 10. Ranking Carreras
        carreras = defaultdict(float)
        for d in datos: carreras[d["carrera"]] += d["monto"]
        self.data_ranking_carreras = [
            {"carrera": k, "monto": round(v,2)} for k, v in sorted(carreras.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # 11. Embudo
        p1 = len(datos)
        p2 = sum(1 for d in datos if d["paso_embudo"] >= 2)
        p3 = sum(1 for d in datos if d["paso_embudo"] == 3)
        self.data_embudo = [
            {"name": "Registrados", "value": p1, "fill": "#3b82f6"},
            {"name": "Validados", "value": p2, "fill": "#8b5cf6"},
            {"name": "Matriculados", "value": p3, "fill": "#10b981"}
        ]
        
        # 12. Tendencia Promedio
        promedios = defaultdict(lambda: {"total": 0.0, "cant": 0})
        for d in datos:
            m = d["fecha"][:7]
            promedios[m]["total"] += d["monto"]
            promedios[m]["cant"] += 1
        self.data_tendencia_promedio = [
            {"mes": k, "promedio": round(v["total"]/v["cant"],2)} for k, v in sorted(promedios.items())
        ]
        
        # 13. Tabla Ejecutiva
        tabla_dict = defaultdict(lambda: {"tot": 0.0, "val": 0, "pen": 0, "obs": 0})
        for d in datos:
            f = d["facultad"]
            tabla_dict[f]["tot"] += d["monto"]
            if d["estado_pago"] == "Validado": tabla_dict[f]["val"] += 1
            if d["estado_pago"] == "Pendiente": tabla_dict[f]["pen"] += 1
            if d["estado_pago"] == "Observado": tabla_dict[f]["obs"] += 1
        
        self.data_tabla_ejecutiva = []
        for f, v in tabla_dict.items():
            total = v["val"] + v["pen"] + v["obs"]
            pct = round((v["val"] / total * 100) if total > 0 else 0, 1)
            var = round(random.uniform(-10, 15), 1) # Variación mensual simulada
            self.data_tabla_ejecutiva.append(
                TablaEjecutiva(facultad=f, total_recaudado=round(v["tot"],2), pagos_validados=v["val"], pagos_pendientes=v["pen"], pagos_observados=v["obs"], porcentaje_validado=pct, variacion_mensual=var)
            )
        self.data_tabla_ejecutiva.sort(key=lambda x: x.total_recaudado, reverse=True)
        
        # 14. Alertas
        alertas = []
        if (morosidad_val / total_pagos) > 0.15:
            alertas.append(AlertaFinanciera(tipo="rojo", mensaje=f"El porcentaje de morosidad supera el 15% ({round(morosidad_val/total_pagos*100,1)}%)", icono="alert-triangle"))
        if self.kpi_pagos_pendientes > 100:
            alertas.append(AlertaFinanciera(tipo="amarillo", mensaje=f"Existen {self.kpi_pagos_pendientes} pagos pendientes de revisión.", icono="clock"))
        
        pct_alcanzado = alcanzado/meta
        if pct_alcanzado >= 0.9:
            alertas.append(AlertaFinanciera(tipo="verde", mensaje="La recaudación está por encima del 90% de la meta estimada.", icono="check-circle"))
        elif pct_alcanzado < 0.5:
            alertas.append(AlertaFinanciera(tipo="rojo", mensaje="Alerta de recaudación: menos del 50% de la meta alcanzada.", icono="trending-down"))
            
        fac_peor = min(self.data_tabla_ejecutiva, key=lambda x: x.variacion_mensual)
        if fac_peor.variacion_mensual < 0:
            alertas.append(AlertaFinanciera(tipo="rojo", mensaje=f"La facultad de {fac_peor.facultad} disminuyó su recaudación un {abs(fac_peor.variacion_mensual)}%.", icono="arrow-down-right"))
            
        self.alertas_financieras = alertas

        # 15. Calendario Heatmap (simulado)
        # Generar data dummy
        max_valor = 50
        datos_heat = []
        for hora in self.heatmap_horas:
            fila = FilaHeatmap(hora=hora, celdas=[])
            for dia in self.heatmap_dias:
                val = random.randint(5, 50)
                opac = round(val / max_valor, 2)
                fila.celdas.append(CeldaHeatmap(dia=dia, valor=str(val), opacity=str(opac)))
            datos_heat.append(fila)
        self.data_heatmap = datos_heat
