import csv
import os

POSTULANTES_FIELDS = [
    "id",
    "convocatoria",
    "nombres",
    "apellidos",
    "dni",
    "facultad",
    "carrera",
    "tipo_colegio",
    "costo",
    "voucher",
    "fecha",
    "puntaje",
    "estado",
]

RESULTADOS_FIELDS = [
    "id",
    "dni",
    "nombres",
    "apellidos",
    "carrera",
    "puntaje",
    "correctas",
    "condicion",
    "convocatoria",
    "fecha",
]

APELACIONES_FIELDS = [
    "id",
    "postulante",
    "dni",
    "pregunta",
    "motivo",
    "fecha",
    "estado",
]

PREGUNTAS_ERROR_FIELDS = [
    "id",
    "area",
    "enunciado",
    "indice_error",
    "total_respuestas",
]


def _ruta_postulantes(ruta: str) -> str:
    return os.path.join(os.path.dirname(__file__), "..", ruta)


def cargar_postulantes(ruta: str = "postulantes.csv") -> list[dict]:
    postulantes = []
    ruta_abs = _ruta_postulantes(ruta)
    # ↑ el with estaba adentro del if — error de indentación
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            postulantes.append(
                {
                    "id": int(row["id"]),
                    "convocatoria": row["convocatoria"],
                    "nombres": row["nombres"],
                    "apellidos": row["apellidos"],
                    "dni": row["dni"],
                    "facultad": row["facultad"],
                    "carrera": row["carrera"],
                    "tipo_colegio": row["tipo_colegio"],
                    "costo": float(row["costo"]),
                    "voucher": row["voucher"],
                    "fecha": row["fecha"],
                    "puntaje": float(row["puntaje"]) if row["puntaje"] else 0.0,
                    "estado": row["estado"],
                }
            )
    return postulantes


def cargar_resultados(ruta: str = "resultados_examen.csv") -> list[dict]:
    resultados = []
    ruta_abs = _ruta_postulantes(ruta)
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            resultados.append(
                {
                    "id": int(row["id"]),
                    "dni": row["dni"],
                    "nombres": row["nombres"],
                    "apellidos": row["apellidos"],
                    "carrera": row["carrera"],
                    "puntaje": float(row["puntaje"]) if row["puntaje"] else 0.0,
                    "correctas": int(row["correctas"]) if row["correctas"] else 0,
                    "condicion": row["condicion"],
                    "convocatoria": row.get("convocatoria", ""),
                    "fecha": row.get("fecha", ""),
                }
            )
    return resultados


def cargar_apelaciones(ruta: str = "apelaciones.csv") -> list[dict]:
    apelaciones = []
    ruta_abs = _ruta_postulantes(ruta)
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            apelaciones.append(
                {
                    "id": int(row["id"]),
                    "postulante": row["postulante"],
                    "dni": row["dni"],
                    "pregunta": row["pregunta"],
                    "motivo": row["motivo"],
                    "fecha": row["fecha"],
                    "estado": row["estado"],
                }
            )
    return apelaciones


def append_apelacion(apelacion: dict, ruta: str = "apelaciones.csv") -> None:
    ruta_abs = _ruta_postulantes(ruta)
    needs_header = not os.path.exists(ruta_abs) or os.path.getsize(ruta_abs) == 0
    with open(ruta_abs, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=APELACIONES_FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow(
            {
                "id": apelacion.get("id", ""),
                "postulante": apelacion.get("postulante", ""),
                "dni": apelacion.get("dni", ""),
                "pregunta": apelacion.get("pregunta", ""),
                "motivo": apelacion.get("motivo", ""),
                "fecha": apelacion.get("fecha", ""),
                "estado": apelacion.get("estado", ""),
            }
        )


def cargar_preguntas_error(ruta: str = "preguntas_error.csv") -> list[dict]:
    preguntas = []
    ruta_abs = _ruta_postulantes(ruta)
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            preguntas.append(
                {
                    "id": int(row["id"]),
                    "area": row["area"],
                    "enunciado": row["enunciado"],
                    "indice_error": float(row["indice_error"])
                    if row["indice_error"]
                    else 0.0,
                    "total_respuestas": int(row["total_respuestas"])
                    if row["total_respuestas"]
                    else 0,
                }
            )
    return preguntas


def append_postulante(postulante: dict, ruta: str = "postulantes.csv") -> None:
    ruta_abs = _ruta_postulantes(ruta)
    needs_header = not os.path.exists(ruta_abs) or os.path.getsize(ruta_abs) == 0
    with open(ruta_abs, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=POSTULANTES_FIELDS)
        if needs_header:
            writer.writeheader()
        writer.writerow(
            {
                "id": postulante.get("id", ""),
                "convocatoria": postulante.get("convocatoria", ""),
                "nombres": postulante.get("nombres", ""),
                "apellidos": postulante.get("apellidos", ""),
                "dni": postulante.get("dni", ""),
                "facultad": postulante.get("facultad", ""),
                "carrera": postulante.get("carrera", ""),
                "tipo_colegio": postulante.get("tipo_colegio", ""),
                "costo": postulante.get("costo", ""),
                "voucher": postulante.get("voucher", ""),
                "fecha": postulante.get("fecha", ""),
                "puntaje": postulante.get("puntaje", 0),
                "estado": postulante.get("estado", ""),
            }
        )
