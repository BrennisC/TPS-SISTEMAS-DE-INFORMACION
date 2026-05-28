from typing import Dict, List
import reflex as rx
from ..utils.csv_loader import cargar_postulantes


class RecaudacionState(rx.State):
    """Estado para el dashboard de recaudación"""
    
    # Datos procesados
    recaudacion_por_convocatoria: list[dict] = []
    recaudacion_por_colegio: list[dict] = []
    recaudacion_por_carrera: list[dict] = []
    recaudacion_por_año: list[dict] = []
    
    # Estadísticas
    total_recaudado: float = 0.0
    promedio_por_postulante: float = 0.0
    recaudacion_estatal: float = 0.0
    recaudacion_privada: float = 0.0
    
    @rx.event
    def cargar_datos_recaudacion(self):
        """Carga y procesa datos de recaudación desde CSV"""
        try:
            postulantes = cargar_postulantes()
        except Exception as e:
            print(f"Error al cargar postulantes: {e}")
            return
        
        if not postulantes:
            return
        
        # 1. Recaudación total
        total = sum(p["costo"] for p in postulantes)
        self.total_recaudado = round(total, 2)
        
        # 2. Promedio por postulante
        if postulantes:
            self.promedio_por_postulante = round(total / len(postulantes), 2)
        
        # 3. Recaudación por tipo de colegio
        estatal_total = sum(
            p["costo"] for p in postulantes 
            if p["tipo_colegio"].strip().lower() == "estatal"
        )
        privada_total = sum(
            p["costo"] for p in postulantes 
            if p["tipo_colegio"].strip().lower() == "privado"
        )
        self.recaudacion_estatal = round(estatal_total, 2)
        self.recaudacion_privada = round(privada_total, 2)
        
        # 4. Recaudación por convocatoria (examen)
        convocatorias: Dict[str, float] = {}
        convocatorias_conteo: Dict[str, int] = {}
        for p in postulantes:
            conv = p.get("convocatoria", "Sin información")
            convocatorias[conv] = convocatorias.get(conv, 0) + p["costo"]
            convocatorias_conteo[conv] = convocatorias_conteo.get(conv, 0) + 1
        
        recaudacion_conv = []
        for conv in sorted(convocatorias.keys(), reverse=True):
            recaudacion_conv.append({
                "convocatoria": conv,
                "monto": round(convocatorias[conv], 2),
                "cantidad": convocatorias_conteo[conv],
                "promedio": round(convocatorias[conv] / convocatorias_conteo[conv], 2),
            })
        self.recaudacion_por_convocatoria = recaudacion_conv
        
        # 5. Recaudación por tipo de colegio (para gráfico)
        recaudacion_colegio = [
            {
                "tipo": "Estatal",
                "monto": round(estatal_total, 2),
                "fill": "#0066CC"
            },
            {
                "tipo": "Privado",
                "monto": round(privada_total, 2),
                "fill": "#FF9500"
            }
        ]
        self.recaudacion_por_colegio = recaudacion_colegio
        
        # 6. Recaudación por carrera (top 10)
        carreras: Dict[str, float] = {}
        for p in postulantes:
            carrera = p.get("carrera", "Sin información")
            carreras[carrera] = carreras.get(carrera, 0) + p["costo"]
        
        recaudacion_carrera = sorted(
            [
                {"carrera": k, "monto": round(v, 2)}
                for k, v in carreras.items()
            ],
            key=lambda x: x["monto"],
            reverse=True
        )[:10]
        self.recaudacion_por_carrera = recaudacion_carrera
        
        # 7. Recaudación por año
        años: Dict[str, float] = {}
        for p in postulantes:
            conv = p.get("convocatoria", "Sin información")
            if conv != "Sin información":
                año = conv.split("-")[0]  # Extrae el año de "2024-I"
                años[año] = años.get(año, 0) + p["costo"]
        
        recaudacion_año = sorted(
            [
                {"año": k, "monto": round(v, 2)}
                for k, v in años.items()
            ],
            key=lambda x: x["año"]
        )
        self.recaudacion_por_año = recaudacion_año
