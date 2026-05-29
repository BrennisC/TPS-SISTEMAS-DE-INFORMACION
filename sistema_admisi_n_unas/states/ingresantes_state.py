from typing import Dict, List
import reflex as rx
from ..utils.csv_loader import cargar_postulantes


class IngresantesState(rx.State):
    """Estado para el dashboard de ingresantes"""
    
    # Datos procesados
    ingresantes_por_convocatoria: list[dict] = []
    ingresantes_por_carrera: list[dict] = []
    ingresantes_por_colegio: list[dict] = []
    ingresantes_por_año: list[dict] = []
    
    # Estadísticas
    total_ingresantes: int = 0
    año_mayor_ingreso: str = ""
    carrera_mas_ingresantes: str = ""
    
    @rx.event
    def cargar_datos_ingresantes(self):
        """Carga y procesa datos de ingresantes desde CSV"""
        try:
            postulantes = cargar_postulantes()
        except Exception as e:
            print(f"Error al cargar postulantes: {e}")
            return
        
        if not postulantes:
            return
        
        # Filtrar solo ingresantes (estado = "ingresante" o similar)
        ingresantes = [
            p for p in postulantes 
            if p.get("estado", "").strip().lower() in ["ingresante", "ingresantes"]
        ]
        
        self.total_ingresantes = len(ingresantes)
        
        # 1. Ingresantes por convocatoria (examen)
        conv_dict = {}
        for ing in ingresantes:
            conv = ing.get("convocatoria", "N/A").strip()
            conv_dict[conv] = conv_dict.get(conv, 0) + 1
        
        # Ordenar convocatorias por año y período
        self.ingresantes_por_convocatoria = sorted(
            [{"convocatoria": k, "cantidad": v} for k, v in conv_dict.items()],
            key=lambda x: (x["convocatoria"].split("-")[0] if "-" in x["convocatoria"] else x["convocatoria"], 
                          x["convocatoria"].split("-")[1] if "-" in x["convocatoria"] else "")
        )
        
        # 2. Ingresantes por carrera
        carrera_dict = {}
        for ing in ingresantes:
            carrera = ing.get("carrera", "N/A").strip()
            carrera_dict[carrera] = carrera_dict.get(carrera, 0) + 1
        
        self.ingresantes_por_carrera = sorted(
            [{"carrera": k, "cantidad": v} for k, v in carrera_dict.items()],
            key=lambda x: x["cantidad"],
            reverse=True
        )
        
        # Obtener carrera con más ingresantes
        if self.ingresantes_por_carrera:
            self.carrera_mas_ingresantes = self.ingresantes_por_carrera[0]["carrera"]
        
        # 3. Ingresantes por tipo de colegio
        colegio_dict = {}
        for ing in ingresantes:
            tipo = ing.get("tipo_colegio", "N/A").strip()
            if tipo.lower() == "estatal":
                tipo = "Estatal"
            elif tipo.lower() == "privado":
                tipo = "Privado"
            colegio_dict[tipo] = colegio_dict.get(tipo, 0) + 1
        
        self.ingresantes_por_colegio = [
            {
                "tipo": k,
                "cantidad": v,
                "fill": "#3b82f6" if k == "Estatal" else "#10b981" if k == "Privado" else "#9ca3af",
            }
            for k, v in colegio_dict.items()
        ]
        
        # 4. Ingresantes por año
        año_dict = {}
        for ing in ingresantes:
            conv = ing.get("convocatoria", "N/A").strip()
            # Extraer año de convocatoria (ej: "2023-I" -> "2023")
            año = conv.split("-")[0] if "-" in conv else "N/A"
            año_dict[año] = año_dict.get(año, 0) + 1
        
        self.ingresantes_por_año = sorted(
            [{"año": k, "cantidad": v} for k, v in año_dict.items()],
            key=lambda x: x["año"]
        )
        
        # Obtener año con mayor ingreso
        if self.ingresantes_por_año:
            max_año = max(self.ingresantes_por_año, key=lambda x: x["cantidad"])
            self.año_mayor_ingreso = f"{max_año['año']} ({max_año['cantidad']})"
