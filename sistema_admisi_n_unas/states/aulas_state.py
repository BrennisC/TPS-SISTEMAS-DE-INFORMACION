import reflex as rx
from typing import List, Dict, Any
from ..utils.csv_loader import cargar_postulantes


class AulasState(rx.State):
    """Estado para el módulo de asignación de aulas"""
    
    # Configuración
    aulas_por_piso: int = 5
    capacidad_por_aula: int = 30
    
    # Datos procesados
    aulas_agrupadas: list[dict[str, Any]] = []
    
    # Estadísticas
    total_postulantes: int = 0
    total_aulas: int = 0
    promedio_utilizacion: str = "0%"
    
    @rx.event
    def set_aulas_por_piso(self, value: str):
        """Actualiza el número de aulas por piso"""
        try:
            self.aulas_por_piso = int(value)
        except ValueError:
            self.aulas_por_piso = 5
    
    @rx.event
    def set_capacidad_por_aula(self, value: str):
        """Actualiza la capacidad por aula"""
        try:
            self.capacidad_por_aula = int(value)
        except ValueError:
            self.capacidad_por_aula = 30
    
    @rx.event
    def generar_asignaciones(self):
        """Genera la asignación automática de aulas"""
        try:
            postulantes = cargar_postulantes()
        except Exception as e:
            print(f"Error al cargar postulantes: {e}")
            return
        
        if not postulantes:
            return
        
        self.total_postulantes = len(postulantes)
        
        # Agrupar postulantes por carrera
        postulantes_por_carrera: Dict[str, List[Dict]] = {}
        for post in postulantes:
            carrera = post.get("carrera", "N/A").strip()
            if carrera not in postulantes_por_carrera:
                postulantes_por_carrera[carrera] = []
            postulantes_por_carrera[carrera].append(post)
        
        # Generar aulas
        aulas_agrupadas = []
        total_aulas = 0
        total_utilizacion = 0
        
        for carrera, postulantes_carrera in postulantes_por_carrera.items():
            cantidad = len(postulantes_carrera)
            aulas_necesarias = (cantidad + self.capacidad_por_aula - 1) // self.capacidad_por_aula
            
            aulas_carrera = []
            postulantes_restantes = cantidad
            
            for i in range(aulas_necesarias):
                postulantes_en_aula = min(postulantes_restantes, self.capacidad_por_aula)
                porcentaje_utilizacion = (postulantes_en_aula / self.capacidad_por_aula) * 100
                
                piso = (i // self.aulas_por_piso) + 1
                numero_aula_en_piso = (i % self.aulas_por_piso) + 1
                
                aulas_carrera.append({
                    "numero_aula": f"{piso}-{numero_aula_en_piso}",
                    "cantidad_postulantes": postulantes_en_aula,
                    "capacidad": self.capacidad_por_aula,
                    "porcentaje_utilizacion": round(porcentaje_utilizacion, 1),
                })
                
                total_utilizacion += porcentaje_utilizacion
                postulantes_restantes -= postulantes_en_aula
                total_aulas += 1
            
            aulas_agrupadas.append({
                "carrera": carrera,
                "aulas": aulas_carrera,
            })
        
        self.aulas_agrupadas = aulas_agrupadas
        self.total_aulas = total_aulas
        
        if total_aulas > 0:
            self.promedio_utilizacion = f"{round(total_utilizacion / total_aulas, 1)}%"
