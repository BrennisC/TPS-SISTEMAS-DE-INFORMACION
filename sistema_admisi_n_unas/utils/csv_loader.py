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

PAGOS_FIELDS = [
    "id",
    "postulante_id",
    "dni",
    "postulante",
    "convocatoria",
    "concepto",
    "tipo_pago",
    "monto",
    "voucher",
    "fecha_pago",
    "estado_pago",
    "observacion",
]

BIBLIOTECA_FIELDS = [
    "id",
    "codigo",
    "titulo",
    "autor",
    "categoria",
    "editorial",
    "stock",
    "disponibles",
    "estado",
    "prestamos_total",
]

PRESTAMOS_FIELDS = [
    "id",
    "dni_lector",
    "lector",
    "libro_codigo",
    "libro",
    "fecha_prestamo",
    "fecha_devolucion",
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


def _ensure_csv(ruta_abs: str, fieldnames: list[str]) -> None:
    if os.path.exists(ruta_abs) and os.path.getsize(ruta_abs) > 0:
        return
    with open(ruta_abs, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()


def cargar_pagos(ruta: str = "pagos.csv") -> list[dict]:
    ruta_abs = _ruta_postulantes(ruta)
    _ensure_csv(ruta_abs, PAGOS_FIELDS)
    pagos = []
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            pagos.append(
                {
                    "id": int(row["id"]),
                    "postulante_id": int(row.get("postulante_id") or 0),
                    "dni": row.get("dni", ""),
                    "postulante": row.get("postulante", ""),
                    "convocatoria": row.get("convocatoria", ""),
                    "concepto": row.get("concepto", "Derecho de admision"),
                    "tipo_pago": row.get("tipo_pago", ""),
                    "monto": float(row.get("monto") or 0),
                    "voucher": row.get("voucher", ""),
                    "fecha_pago": row.get("fecha_pago", ""),
                    "estado_pago": row.get("estado_pago", "Pendiente"),
                    "observacion": row.get("observacion", ""),
                }
            )
    return pagos


def guardar_pagos(pagos: list[dict], ruta: str = "pagos.csv") -> None:
    ruta_abs = _ruta_postulantes(ruta)
    with open(ruta_abs, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PAGOS_FIELDS)
        writer.writeheader()
        for pago in pagos:
            writer.writerow({field: pago.get(field, "") for field in PAGOS_FIELDS})


def cargar_libros(ruta: str = "biblioteca_data.csv") -> list[dict]:
    ruta_abs = _ruta_postulantes(ruta)
    _ensure_csv(ruta_abs, BIBLIOTECA_FIELDS)
    libros = []
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            libros.append(
                {
                    "id": int(row["id"]),
                    "codigo": row.get("codigo", ""),
                    "titulo": row.get("titulo", ""),
                    "autor": row.get("autor", ""),
                    "categoria": row.get("categoria", ""),
                    "editorial": row.get("editorial", ""),
                    "stock": int(row.get("stock") or 0),
                    "disponibles": int(row.get("disponibles") or 0),
                    "estado": row.get("estado", "Disponible"),
                    "prestamos_total": int(row.get("prestamos_total") or 0),
                }
            )
    return libros


def guardar_libros(libros: list[dict], ruta: str = "biblioteca_data.csv") -> None:
    ruta_abs = _ruta_postulantes(ruta)
    with open(ruta_abs, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=BIBLIOTECA_FIELDS)
        writer.writeheader()
        for libro in libros:
            writer.writerow({field: libro.get(field, "") for field in BIBLIOTECA_FIELDS})


def cargar_prestamos(ruta: str = "prestamos.csv") -> list[dict]:
    ruta_abs = _ruta_postulantes(ruta)
    _ensure_csv(ruta_abs, PRESTAMOS_FIELDS)
    prestamos = []
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            prestamos.append(
                {
                    "id": int(row["id"]),
                    "dni_lector": row.get("dni_lector", ""),
                    "lector": row.get("lector", ""),
                    "libro_codigo": row.get("libro_codigo", ""),
                    "libro": row.get("libro", ""),
                    "fecha_prestamo": row.get("fecha_prestamo", ""),
                    "fecha_devolucion": row.get("fecha_devolucion", ""),
                    "estado": row.get("estado", "Prestado"),
                }
            )
    return prestamos


def guardar_prestamos(prestamos: list[dict], ruta: str = "prestamos.csv") -> None:
    ruta_abs = _ruta_postulantes(ruta)
    with open(ruta_abs, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PRESTAMOS_FIELDS)
        writer.writeheader()
        for prestamo in prestamos:
            writer.writerow({field: prestamo.get(field, "") for field in PRESTAMOS_FIELDS})


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


def cargar_estado_pagos(ruta: str = "pagos.csv") -> dict:
    """Devuelve dict {(dni, convocatoria): estado_pago} solo para pagos de admision."""
    lookup: dict[tuple, str] = {}
    ruta_abs = _ruta_postulantes(ruta)
    if not os.path.exists(ruta_abs):
        return lookup
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            concepto = row.get("concepto", "").strip().lower()
            if "admision" not in concepto:
                continue
            dni = row.get("dni", "").strip()
            conv = row.get("convocatoria", "").strip()
            estado = row.get("estado_pago", "Pendiente").strip()
            if dni and conv:
                lookup[(dni, conv)] = estado
    return lookup


def cargar_pagos_validados(ruta: str = "pagos.csv") -> list[dict]:
    """Carga pagos validados con datos de postulante para reportes de recaudacion."""
    pagos = []
    ruta_abs = _ruta_postulantes(ruta)
    if not os.path.exists(ruta_abs):
        return pagos
    with open(ruta_abs, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            if row.get("estado_pago", "").strip() != "Validado":
                continue
            pagos.append({
                "id": int(row["id"]),
                "postulante_id": int(row.get("postulante_id") or 0),
                "dni": row.get("dni", ""),
                "postulante": row.get("postulante", ""),
                "convocatoria": row.get("convocatoria", ""),
                "concepto": row.get("concepto", "Derecho de admision"),
                "tipo_pago": row.get("tipo_pago", ""),
                "monto": float(row.get("monto") or 0),
                "voucher": row.get("voucher", ""),
                "fecha_pago": row.get("fecha_pago", ""),
                "estado_pago": "Validado",
                "observacion": row.get("observacion", ""),
            })
    return pagos


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
