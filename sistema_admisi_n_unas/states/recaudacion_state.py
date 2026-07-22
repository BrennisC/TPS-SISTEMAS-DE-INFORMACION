from typing import Dict
import reflex as rx
from ..utils.csv_loader import cargar_pagos_validados, cargar_postulantes


class RecaudacionState(rx.State):
    recaudacion_por_convocatoria: list[dict] = []
    recaudacion_por_colegio: list[dict] = []
    recaudacion_por_carrera: list[dict] = []
    recaudacion_por_año: list[dict] = []

    total_recaudado: float = 0.0
    promedio_por_postulante: float = 0.0
    recaudacion_estatal: float = 0.0
    recaudacion_privada: float = 0.0

    @rx.event
    def cargar_datos_recaudacion(self):
        try:
            pagos_validados = cargar_pagos_validados()
            postulantes = cargar_postulantes()
        except Exception as e:
            print(f"Error al cargar datos de recaudación: {e}")
            return

        if not pagos_validados:
            return

        postulantes_por_id: Dict[int, dict] = {}
        for p in postulantes:
            postulantes_por_id[p["id"]] = p

        total = sum(pago["monto"] for pago in pagos_validados)
        self.total_recaudado = round(total, 2)

        if pagos_validados:
            self.promedio_por_postulante = round(total / len(pagos_validados), 2)

        estatal_total = 0.0
        privada_total = 0.0
        for pago in pagos_validados:
            post = postulantes_por_id.get(pago["postulante_id"])
            if post and post["tipo_colegio"].strip().lower() == "estatal":
                estatal_total += pago["monto"]
            elif post and post["tipo_colegio"].strip().lower() == "privado":
                privada_total += pago["monto"]
        self.recaudacion_estatal = round(estatal_total, 2)
        self.recaudacion_privada = round(privada_total, 2)

        convocatorias: Dict[str, float] = {}
        convocatorias_conteo: Dict[str, int] = {}
        for pago in pagos_validados:
            conv = pago.get("convocatoria", "Sin información")
            convocatorias[conv] = convocatorias.get(conv, 0) + pago["monto"]
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

        recaudacion_colegio = [
            {"tipo": "Estatal", "monto": round(estatal_total, 2), "fill": "#0066CC"},
            {"tipo": "Privado", "monto": round(privada_total, 2), "fill": "#FF9500"},
        ]
        self.recaudacion_por_colegio = recaudacion_colegio

        carreras: Dict[str, float] = {}
        for pago in pagos_validados:
            post = postulantes_por_id.get(pago["postulante_id"])
            carrera = post.get("carrera", "Sin información") if post else "Sin información"
            carreras[carrera] = carreras.get(carrera, 0) + pago["monto"]

        recaudacion_carrera = sorted(
            [{"carrera": k, "monto": round(v, 2)} for k, v in carreras.items()],
            key=lambda x: x["monto"],
            reverse=True,
        )[:10]
        self.recaudacion_por_carrera = recaudacion_carrera

        años: Dict[str, float] = {}
        for pago in pagos_validados:
            conv = pago.get("convocatoria", "Sin información")
            if conv != "Sin información" and "-" in conv:
                año = conv.split("-")[0]
                años[año] = años.get(año, 0) + pago["monto"]

        recaudacion_año = sorted(
            [{"año": k, "monto": round(v, 2)} for k, v in años.items()],
            key=lambda x: x["año"],
        )
        self.recaudacion_por_año = recaudacion_año
