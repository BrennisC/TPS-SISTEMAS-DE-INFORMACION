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
