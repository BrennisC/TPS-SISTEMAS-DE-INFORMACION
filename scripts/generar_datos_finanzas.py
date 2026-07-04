import csv
import random
from datetime import datetime, timedelta
import os

# Configuraciones
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'sistema_admisi_n_unas', 'finanzas_data.csv')
NUM_REGISTROS = 5000

CONVOCATORIAS = ["2023-I", "2023-II", "2024-I", "2024-II", "2025-I"]

FACULTADES_CARRERAS = {
    "Agronomía": ["Agronomía"],
    "Ing. Informática y Sistemas": ["Ing. Informática y Sistemas"],
    "Recursos Naturales Renovables": ["Ing. Ambiental", "Ing. Forestal", "Ing. Conservación Suelos", "Ing. Recursos Naturales"],
    "Zootecnia": ["Zootecnia"],
    "Ciencias Económicas": ["Administración", "Contabilidad", "Economía"],
    "Otras Escuelas": ["Ing. Mecánica Eléctrica", "Desarrollo Rural"]
}

TIPO_COLEGIO = ["Estatal", "Privado"]
ESTADO_PAGO = ["Validado", "Pendiente", "Observado"]
ESTADO_WEIGHTS = [0.75, 0.15, 0.10]

CONCEPTO_PAGO = ["Inscripción", "Examen", "Matrícula", "Constancias", "Otros"]
CONCEPTO_WEIGHTS = [0.4, 0.3, 0.2, 0.05, 0.05]
CONCEPTO_MONTOS = {
    "Inscripción": (200, 300),
    "Examen": (150, 250),
    "Matrícula": (350, 500),
    "Constancias": (30, 80),
    "Otros": (50, 150)
}

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

def generate_data():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 7, 1)
    
    data = []
    
    for i in range(1, NUM_REGISTROS + 1):
        facultad = random.choice(list(FACULTADES_CARRERAS.keys()))
        carrera = random.choice(FACULTADES_CARRERAS[facultad])
        
        # Asignar convocatoria según fecha
        fecha = random_date(start_date, end_date)
        if fecha.year == 2023:
            convocatoria = "2023-I" if fecha.month <= 6 else "2023-II"
        elif fecha.year == 2024:
            convocatoria = "2024-I" if fecha.month <= 6 else "2024-II"
        else:
            convocatoria = "2025-I"
            
        tipo_colegio = random.choices(TIPO_COLEGIO, weights=[0.6, 0.4])[0]
        estado_pago = random.choices(ESTADO_PAGO, weights=ESTADO_WEIGHTS)[0]
        concepto = random.choices(CONCEPTO_PAGO, weights=CONCEPTO_WEIGHTS)[0]
        
        monto_min, monto_max = CONCEPTO_MONTOS[concepto]
        monto = round(random.uniform(monto_min, monto_max), 2)
        
        # Añadir algo de ruido para que la validación y embudo tengan sentido
        paso_embudo = 1
        if estado_pago == "Validado":
            paso_embudo = random.choices([2, 3], weights=[0.4, 0.6])[0] # 2 = pago validado, 3 = matricula
            if concepto == "Matrícula":
                paso_embudo = 3

        data.append({
            "id": i,
            "fecha": fecha.strftime("%Y-%m-%d %H:%M:%S"),
            "convocatoria": convocatoria,
            "facultad": facultad,
            "carrera": carrera,
            "tipo_colegio": tipo_colegio,
            "estado_pago": estado_pago,
            "concepto": concepto,
            "monto": monto,
            "paso_embudo": paso_embudo
        })
        
    # Sort by date
    data.sort(key=lambda x: x["fecha"])
    return data

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    data = generate_data()
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Generados {NUM_REGISTROS} registros en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
