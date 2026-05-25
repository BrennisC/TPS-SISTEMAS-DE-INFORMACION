import asyncio
from typing import TypedDict

import reflex as rx


class Pregunta(TypedDict):
    id: int
    area: str
    tipo: str
    enunciado: str
    alternativas: list[str]
    correcta: int


PREGUNTAS_DEMO: list[Pregunta] = [
    # =========================================================================
    # ÁREA 1: RAZONAMIENTO VERBAL (20 preguntas)
    # =========================================================================
    {
        "id": 1,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Seleccione el sinónimo de EFÍMERO:",
        "alternativas": ["Eterno", "Pasajero", "Robusto", "Constante", "Perdurable"],
        "correcta": 1,
    },
    {
        "id": 2,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Seleccione el antónimo de PRODIGIOSO:",
        "alternativas": [
            "Asombroso",
            "Portentoso",
            "Ordinario",
            "Sobresaliente",
            "Magnífico",
        ],
        "correcta": 2,
    },
    {
        "id": 3,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Identifique la relación analógica correcta: ÁRBOL : BOSQUE",
        "alternativas": [
            "Pez : Agua",
            "Abeja : Colmena",
            "Estrella : Galaxia",
            "Libro : Biblioteca",
            "Hormiga : Tierra",
        ],
        "correcta": 2,
    },
    {
        "id": 4,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": (
            "Lea el siguiente texto y responda: 'La selva amazónica es conocida como el pulmón del mundo "
            "por su capacidad de producir oxígeno y absorber CO₂.' ¿Cuál es la idea principal?"
        ),
        "alternativas": [
            "La selva es peligrosa para el hombre",
            "La Amazonía regula el clima global gracias a su rol en el intercambio gaseoso",
            "El CO₂ es perjudicial para los árboles",
            "Los pulmones funcionan como los árboles",
            "La selva produce lluvia",
        ],
        "correcta": 1,
    },
    {
        "id": 5,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál de las siguientes palabras es un hiperónimo de 'rosal', 'clavel' y 'orquídea'?",
        "alternativas": ["Planta", "Flor", "Vegetal", "Árbol", "Hierba"],
        "correcta": 1,
    },
    {
        "id": 6,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Complete la oración con el conector más adecuado: 'Estudió toda la noche; _______, aprobó el examen con nota alta.'",
        "alternativas": [
            "sin embargo",
            "aunque",
            "por consiguiente",
            "pero",
            "a pesar de",
        ],
        "correcta": 2,
    },
    {
        "id": 7,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál de las siguientes oraciones presenta un error de concordancia?",
        "alternativas": [
            "Los estudiantes llegaron temprano.",
            "La profesora explicó el tema claramente.",
            "Los niño jugaron en el parque.",
            "El perro ladró toda la noche.",
            "Ellas trajeron sus cuadernos.",
        ],
        "correcta": 2,
    },
    {
        "id": 8,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "¿Qué figura retórica se emplea en: 'Sus ojos son dos luceros brillantes'?",
        "alternativas": [
            "Hipérbole",
            "Metonimia",
            "Metáfora",
            "Antítesis",
            "Personificación",
        ],
        "correcta": 2,
    },
    {
        "id": 9,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Identifique el término EXCLUIDO por no pertenecer al mismo campo semántico:",
        "alternativas": ["Eucalipto", "Cedro", "Caoba", "Clavel", "Pino"],
        "correcta": 3,
    },
    {
        "id": 10,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": (
            "Texto: 'La contaminación del río Huallaga afecta a miles de familias de la selva peruana, "
            "quienes dependen de sus aguas para su subsistencia.' Se infiere que:"
        ),
        "alternativas": [
            "El Huallaga ya no tiene agua",
            "Las familias se dedican a la pesca y uso doméstico del río",
            "La contaminación proviene solo de las ciudades",
            "El río Huallaga está ubicado en la costa",
            "Las familias migraron por la contaminación",
        ],
        "correcta": 1,
    },
    {
        "id": 11,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Seleccione el sinónimo contextual de LATENTE en: 'El talento latente del joven fue descubierto por el maestro.'",
        "alternativas": ["Evidente", "Oculto", "Brillante", "Perdido", "Notorio"],
        "correcta": 1,
    },
    {
        "id": 12,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Analogía: MÉDICO : BISTURÍ :: CARPINTERO : ___",
        "alternativas": ["Madera", "Serrucho", "Clavo", "Martillo", "Árbol"],
        "correcta": 1,
    },
    {
        "id": 13,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el tipo de texto del siguiente fragmento: 'Por lo tanto, se concluye que el cambio climático es responsabilidad de la actividad humana'?",
        "alternativas": [
            "Narrativo",
            "Descriptivo",
            "Expositivo",
            "Argumentativo",
            "Instructivo",
        ],
        "correcta": 3,
    },
    {
        "id": 14,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Seleccione la opción que presenta el uso correcto del tilde diacrítico:",
        "alternativas": [
            "Solo quiero tomar té.",
            "El no quiso venir.",
            "Se fue sin decirme nada.",
            "Mi casa esta lejos.",
            "Tu debes estudiar más.",
        ],
        "correcta": 0,
    },
    {
        "id": 15,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "¿Qué palabra completa correctamente la analogía? HAMBRE : SACIEDAD :: IGNORANCIA : ___",
        "alternativas": ["Torpeza", "Conocimiento", "Olvido", "Duda", "Ciencia"],
        "correcta": 1,
    },
    {
        "id": 16,
        "area": "Razonamiento Verbal",
        "tipo": "Verdadero/Falso",
        "enunciado": "La paragoge es una figura que consiste en añadir una sílaba al final de una palabra.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 0,
    },
    {
        "id": 17,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "En la oración 'El estudiante que aprobó el examen recibirá una beca', la proposición subordinada es:",
        "alternativas": [
            "El estudiante",
            "que aprobó el examen",
            "recibirá una beca",
            "El estudiante recibirá",
            "una beca",
        ],
        "correcta": 1,
    },
    {
        "id": 18,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál de los siguientes enunciados usa correctamente los signos de puntuación?",
        "alternativas": [
            "María, compró pan leche y huevos.",
            "María compró: pan, leche y huevos.",
            "María compró pan, leche, y huevos.",
            "María compró pan, leche y huevos.",
            "María compró pan leche, y huevos.",
        ],
        "correcta": 3,
    },
    {
        "id": 19,
        "area": "Razonamiento Verbal",
        "tipo": "Alternativa",
        "enunciado": "Identifique el antónimo de PARCO:",
        "alternativas": ["Austero", "Pródigo", "Sobrio", "Frugal", "Moderado"],
        "correcta": 1,
    },
    {
        "id": 20,
        "area": "Razonamiento Verbal",
        "tipo": "Verdadero/Falso",
        "enunciado": "El sujeto siempre concuerda en número y persona con el verbo de la oración.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 0,
    },
    # =========================================================================
    # ÁREA 2: RAZONAMIENTO MATEMÁTICO (20 preguntas)
    # =========================================================================
    {
        "id": 21,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Continúe la secuencia: 2, 6, 18, 54, ___",
        "alternativas": ["108", "162", "216", "108", "144"],
        "correcta": 1,
    },
    {
        "id": 22,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Si todos los ingenieros son profesionales y algunos profesionales son deportistas, entonces:",
        "alternativas": [
            "Todos los ingenieros son deportistas",
            "Ningún ingeniero es deportista",
            "Algunos ingenieros pueden ser deportistas",
            "Los deportistas son ingenieros",
            "Los profesionales no son deportistas",
        ],
        "correcta": 2,
    },
    {
        "id": 23,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "En un grupo de 50 estudiantes, 30 llevan matemática y 25 llevan física. Si 10 llevan ambas, ¿cuántos no llevan ninguna?",
        "alternativas": ["5", "10", "15", "20", "25"],
        "correcta": 0,
    },
    {
        "id": 24,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "¿Cuántas diagonales tiene un octágono (polígono de 8 lados)?",
        "alternativas": ["16", "20", "24", "28", "32"],
        "correcta": 1,
    },
    {
        "id": 25,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Karen tiene S/75 más los 3/8 de su dinero. ¿Cuánto dinero tiene Karen?",
        "alternativas": ["S/. 100", "S/. 120", "S/. 105", "S/. 110", "S/. 125"],
        "correcta": 1,
    },
    {
        "id": 26,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "¿Cuántos números enteros satisfacen la inecuación: -3 < 2x + 1 ≤ 7?",
        "alternativas": ["3", "4", "5", "6", "7"],
        "correcta": 1,
    },
    {
        "id": 27,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Halle el término que sigue: 1, 1, 2, 3, 5, 8, 13, ___",
        "alternativas": ["18", "20", "21", "24", "26"],
        "correcta": 2,
    },
    {
        "id": 28,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Un reloj marca las 3:00. ¿Cuántos grados forma el ángulo entre las manecillas?",
        "alternativas": ["60°", "75°", "90°", "100°", "120°"],
        "correcta": 2,
    },
    {
        "id": 29,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Si A = {1,2,3,4,5} y B = {3,4,5,6,7}, ¿cuántos elementos tiene A ∪ B?",
        "alternativas": ["5", "6", "7", "8", "10"],
        "correcta": 2,
    },
    {
        "id": 30,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "¿Cuántos triángulos se pueden formar con 6 puntos, de los cuales 3 son colineales?",
        "alternativas": ["18", "19", "20", "16", "15"],
        "correcta": 1,
    },
    {
        "id": 31,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Pedro tiene el doble de la edad de Juan. Dentro de 5 años la suma de sus edades será 55. ¿Cuántos años tiene Pedro ahora?",
        "alternativas": ["25", "28", "30", "32", "35"],
        "correcta": 2,
    },
    {
        "id": 32,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Identifique la figura que continúa la secuencia: ○ ◻ △ ○ ◻ △ ○ ◻ ___",
        "alternativas": ["○", "◻", "△", "◇", "▭"],
        "correcta": 2,
    },
    {
        "id": 33,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Si el 40 es el 20% de un número, ¿cuál es ese número?",
        "alternativas": ["160", "180", "200", "220", "240"],
        "correcta": 2,
    },
    {
        "id": 34,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Un tren recorre 360 km en 4 horas. ¿Cuántos km recorre en 7 horas a la misma velocidad?",
        "alternativas": ["540", "600", "630", "660", "700"],
        "correcta": 2,
    },
    {
        "id": 35,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el valor de: 3³ + 2⁴ − 5²?",
        "alternativas": ["16", "18", "20", "22", "24"],
        "correcta": 1,
    },
    {
        "id": 36,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Ana, Beto y Carlos reparten S/. 240 en proporción 2:3:5. ¿Cuánto recibe Beto?",
        "alternativas": ["48", "60", "72", "84", "96"],
        "correcta": 2,
    },
    {
        "id": 37,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "¿Cuántas palabras distintas se pueden formar con las letras de LIMA?",
        "alternativas": ["12", "16", "24", "36", "48"],
        "correcta": 2,
    },
    {
        "id": 38,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "Si f(x) = 2x² − 3x + 1, halle f(3):",
        "alternativas": ["8", "9", "10", "11", "12"],
        "correcta": 2,
    },
    {
        "id": 39,
        "area": "Razonamiento Matemático",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el MCD de 84 y 120?",
        "alternativas": ["6", "12", "18", "24", "36"],
        "correcta": 1,
    },
    {
        "id": 40,
        "area": "Razonamiento Matemático",
        "tipo": "Verdadero/Falso",
        "enunciado": "El número 0 (cero) es un número natural.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 1,
    },
    # =========================================================================
    # ÁREA 3: MATEMÁTICAS – Álgebra, Aritmética, Geometría y Trigonometría (20 preguntas)
    # =========================================================================
    {
        "id": 41,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Resuelva: Si 3x + 5 = 20, ¿cuál es el valor de x?",
        "alternativas": ["3", "5", "7", "4", "6"],
        "correcta": 1,
    },
    {
        "id": 42,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Simplifique: (a² b³)² / (a b²)³",
        "alternativas": ["a/b", "a b⁰", "a b", "a⁻¹b", "ab²"],
        "correcta": 0,
    },
    {
        "id": 43,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Halle el área de un triángulo de base 10 cm y altura 6 cm:",
        "alternativas": ["30 cm²", "40 cm²", "50 cm²", "60 cm²", "70 cm²"],
        "correcta": 0,
    },
    {
        "id": 44,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el área de un círculo de radio 4 cm? (use π ≈ 3.14)",
        "alternativas": [
            "25.12 cm²",
            "37.68 cm²",
            "50.24 cm²",
            "62.80 cm²",
            "75.36 cm²",
        ],
        "correcta": 2,
    },
    {
        "id": 45,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Factorice completamente: x² − 9",
        "alternativas": [
            "(x − 3)²",
            "(x + 3)(x − 3)",
            "(x + 9)(x − 1)",
            "(x − 3)(x − 3)",
            "(x + 3)²",
        ],
        "correcta": 1,
    },
    {
        "id": 46,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "En un triángulo rectángulo, la hipotenusa mide 13 cm y un cateto 5 cm. ¿Cuánto mide el otro cateto?",
        "alternativas": ["8 cm", "10 cm", "12 cm", "11 cm", "9 cm"],
        "correcta": 2,
    },
    {
        "id": 47,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el valor de sen 30°?",
        "alternativas": ["√3/2", "1/2", "√2/2", "1", "0"],
        "correcta": 1,
    },
    {
        "id": 48,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Resuelva el sistema: 2x + y = 7 y x − y = 2. El valor de x es:",
        "alternativas": ["1", "2", "3", "4", "5"],
        "correcta": 2,
    },
    {
        "id": 49,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Halle la suma de los ángulos internos de un hexágono regular:",
        "alternativas": ["540°", "600°", "660°", "720°", "780°"],
        "correcta": 3,
    },
    {
        "id": 50,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Si log₁₀ 100 = x, entonces x vale:",
        "alternativas": ["1", "2", "3", "10", "0.5"],
        "correcta": 1,
    },
    {
        "id": 51,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "La razón entre dos números es 3:5 y su suma es 80. ¿Cuál es el mayor?",
        "alternativas": ["30", "40", "45", "50", "60"],
        "correcta": 3,
    },
    {
        "id": 52,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "¿Cuánto es el 15% de 240?",
        "alternativas": ["24", "30", "36", "42", "48"],
        "correcta": 2,
    },
    {
        "id": 53,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Simplifique: (3x² − 6x) / 3x",
        "alternativas": ["x − 2", "x + 2", "3x − 2", "x − 6", "3x"],
        "correcta": 0,
    },
    {
        "id": 54,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Un cuadrado tiene perímetro de 36 cm. ¿Cuál es su área?",
        "alternativas": ["49 cm²", "64 cm²", "81 cm²", "36 cm²", "100 cm²"],
        "correcta": 2,
    },
    {
        "id": 55,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Si tan θ = 1 y 0° < θ < 90°, entonces θ es:",
        "alternativas": ["30°", "45°", "60°", "75°", "90°"],
        "correcta": 1,
    },
    {
        "id": 56,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el volumen de un cubo de arista 5 cm?",
        "alternativas": ["75 cm³", "100 cm³", "125 cm³", "150 cm³", "175 cm³"],
        "correcta": 2,
    },
    {
        "id": 57,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "Halle la pendiente de la recta que pasa por A(1, 2) y B(3, 8):",
        "alternativas": ["2", "3", "4", "5", "6"],
        "correcta": 1,
    },
    {
        "id": 58,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "¿Cuánto es 2⁵ − 4²?",
        "alternativas": ["12", "14", "16", "18", "20"],
        "correcta": 2,
    },
    {
        "id": 59,
        "area": "Matemáticas",
        "tipo": "Alternativa",
        "enunciado": "En una progresión aritmética, el primer término es 4 y la razón es 3. ¿Cuál es el décimo término?",
        "alternativas": ["25", "27", "29", "31", "33"],
        "correcta": 3,
    },
    {
        "id": 60,
        "area": "Matemáticas",
        "tipo": "Verdadero/Falso",
        "enunciado": "El teorema de Pitágoras establece que en todo triángulo rectángulo: a² + b² = c², donde c es la hipotenusa.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 0,
    },
    # =========================================================================
    # ÁREA 4: FÍSICA, QUÍMICA Y BIOLOGÍA (10 preguntas)
    # =========================================================================
    {
        "id": 61,
        "area": "Física, Química y Biología",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el órgano principal del sistema circulatorio humano?",
        "alternativas": ["Pulmón", "Hígado", "Corazón", "Cerebro", "Riñón"],
        "correcta": 2,
    },
    {
        "id": 62,
        "area": "Física, Química y Biología",
        "tipo": "Verdadero/Falso",
        "enunciado": "La fotosíntesis se realiza únicamente durante la noche.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 1,
    },
    {
        "id": 63,
        "area": "Física, Química y Biología",
        "tipo": "Alternativa",
        "enunciado": "Un cuerpo de 5 kg se mueve a 10 m/s. ¿Cuál es su energía cinética?",
        "alternativas": ["100 J", "200 J", "250 J", "300 J", "500 J"],
        "correcta": 2,
    },
    {
        "id": 64,
        "area": "Física, Química y Biología",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el número atómico del oxígeno (O)?",
        "alternativas": ["6", "7", "8", "9", "10"],
        "correcta": 2,
    },
    {
        "id": 65,
        "area": "Física, Química y Biología",
        "tipo": "Alternativa",
        "enunciado": "La duplicación del ADN se produce en la fase:",
        "alternativas": [
            "Mitosis",
            "Meiosis",
            "Interfase (fase S)",
            "Profase",
            "Telofase",
        ],
        "correcta": 2,
    },
    {
        "id": 66,
        "area": "Física, Química y Biología",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es la unidad de medida de la fuerza en el Sistema Internacional?",
        "alternativas": ["Julio", "Pascal", "Newton", "Watt", "Coulomb"],
        "correcta": 2,
    },
    {
        "id": 67,
        "area": "Física, Química y Biología",
        "tipo": "Alternativa",
        "enunciado": "¿Qué tipo de enlace químico se forma entre Na y Cl para dar NaCl?",
        "alternativas": [
            "Covalente polar",
            "Covalente apolar",
            "Iónico",
            "Metálico",
            "Puente de hidrógeno",
        ],
        "correcta": 2,
    },
    {
        "id": 68,
        "area": "Física, Química y Biología",
        "tipo": "Alternativa",
        "enunciado": "La ley de la gravitación universal fue formulada por:",
        "alternativas": [
            "Galileo Galilei",
            "Albert Einstein",
            "Isaac Newton",
            "Nicolás Copérnico",
            "James Watt",
        ],
        "correcta": 2,
    },
    {
        "id": 69,
        "area": "Física, Química y Biología",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál de los siguientes es un ejemplo de mezcla homogénea?",
        "alternativas": [
            "Arena y agua",
            "Aceite y agua",
            "Agua salada",
            "Ensalada",
            "Tierra y piedra",
        ],
        "correcta": 2,
    },
    {
        "id": 70,
        "area": "Física, Química y Biología",
        "tipo": "Verdadero/Falso",
        "enunciado": "Los seres vivos de la selva amazónica contribuyen significativamente a la biodiversidad global.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 0,
    },
    # =========================================================================
    # ÁREA 5: HUMANIDADES – Historia Perú, Historia Universal, Geografía,
    #          Economía, Cívica, Filosofía, Literatura (30 preguntas)
    # =========================================================================
    {
        "id": 71,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿En qué año fue creada la Universidad Nacional Agraria de la Selva (UNAS)?",
        "alternativas": ["1960", "1962", "1964", "1968", "1970"],
        "correcta": 2,
    },
    {
        "id": 72,
        "area": "Humanidades",
        "tipo": "Verdadero/Falso",
        "enunciado": "Tingo María se ubica en la región Huánuco.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 0,
    },
    {
        "id": 73,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Quién fue el primer Inca del Tahuantinsuyo?",
        "alternativas": [
            "Pachacútec",
            "Túpac Inca Yupanqui",
            "Manco Cápac",
            "Huayna Cápac",
            "Atahualpa",
        ],
        "correcta": 2,
    },
    {
        "id": 74,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿En qué año proclamó la independencia el Perú?",
        "alternativas": ["1819", "1820", "1821", "1822", "1824"],
        "correcta": 2,
    },
    {
        "id": 75,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es la capital de la región Loreto?",
        "alternativas": [
            "Pucallpa",
            "Tarapoto",
            "Iquitos",
            "Puerto Maldonado",
            "Moyobamba",
        ],
        "correcta": 2,
    },
    {
        "id": 76,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál fue la primera Revolución Industrial y en qué país se inició?",
        "alternativas": [
            "Segunda Revolución, Francia",
            "Primera Revolución, Alemania",
            "Primera Revolución, Inglaterra",
            "Segunda Revolución, EE.UU.",
            "Primera Revolución, Italia",
        ],
        "correcta": 2,
    },
    {
        "id": 77,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el río más largo del Perú?",
        "alternativas": ["Huallaga", "Ucayali", "Amazonas", "Marañón", "Madre de Dios"],
        "correcta": 2,
    },
    {
        "id": 78,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "La Constitución Política del Perú actualmente vigente fue promulgada en:",
        "alternativas": ["1979", "1980", "1990", "1993", "2000"],
        "correcta": 3,
    },
    {
        "id": 79,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿En qué año terminó la Segunda Guerra Mundial?",
        "alternativas": ["1943", "1944", "1945", "1946", "1947"],
        "correcta": 2,
    },
    {
        "id": 80,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Quién escribió 'Los heraldos negros'?",
        "alternativas": [
            "José María Arguedas",
            "César Vallejo",
            "Mario Vargas Llosa",
            "Ciro Alegría",
            "Javier Heraud",
        ],
        "correcta": 1,
    },
    {
        "id": 81,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es la principal función del Banco Central de Reserva del Perú (BCRP)?",
        "alternativas": [
            "Cobrar impuestos",
            "Administrar la deuda pública",
            "Preservar la estabilidad monetaria",
            "Financiar el gasto público",
            "Regular el comercio exterior",
        ],
        "correcta": 2,
    },
    {
        "id": 82,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿En qué cultura peruana se elaboró la cerámica conocida como 'Huaco Retrato'?",
        "alternativas": ["Chavín", "Nazca", "Mochica", "Tiahuanaco", "Inca"],
        "correcta": 2,
    },
    {
        "id": 83,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "La Revolución Francesa comenzó en:",
        "alternativas": ["1776", "1789", "1793", "1800", "1815"],
        "correcta": 1,
    },
    {
        "id": 84,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuántas regiones tiene el Perú?",
        "alternativas": ["22", "24", "25", "26", "28"],
        "correcta": 1,
    },
    {
        "id": 85,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál fue el autor de 'El Principito'?",
        "alternativas": [
            "Gabriel García Márquez",
            "Pablo Neruda",
            "Antoine de Saint-Exupéry",
            "Julio Cortázar",
            "Octavio Paz",
        ],
        "correcta": 2,
    },
    {
        "id": 86,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Qué poder del Estado administra justicia en el Perú?",
        "alternativas": [
            "Poder Ejecutivo",
            "Poder Legislativo",
            "Poder Judicial",
            "Ministerio Público",
            "Defensoría del Pueblo",
        ],
        "correcta": 2,
    },
    {
        "id": 87,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el país con mayor extensión territorial de América del Sur?",
        "alternativas": ["Argentina", "Colombia", "Brasil", "Venezuela", "Perú"],
        "correcta": 2,
    },
    {
        "id": 88,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "En economía, la ley de la oferta establece que al aumentar el precio de un bien, la cantidad ofrecida:",
        "alternativas": [
            "Disminuye",
            "Permanece igual",
            "Aumenta",
            "Se vuelve negativa",
            "Se duplica",
        ],
        "correcta": 2,
    },
    {
        "id": 89,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Qué filósofo griego formuló el método socrático o mayéutica?",
        "alternativas": [
            "Platón",
            "Aristóteles",
            "Sócrates",
            "Tales de Mileto",
            "Pitágoras",
        ],
        "correcta": 2,
    },
    {
        "id": 90,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es la región natural donde se ubica Tingo María?",
        "alternativas": [
            "Costa",
            "Sierra",
            "Selva alta (Rupa Rupa)",
            "Selva baja",
            "Puna",
        ],
        "correcta": 2,
    },
    {
        "id": 91,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "La novela 'La ciudad y los perros' fue escrita por:",
        "alternativas": [
            "César Vallejo",
            "Ciro Alegría",
            "José María Arguedas",
            "Mario Vargas Llosa",
            "Alfredo Bryce",
        ],
        "correcta": 3,
    },
    {
        "id": 92,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿En qué cultura prehispánica se originaron las líneas de Nazca?",
        "alternativas": ["Inca", "Chavín", "Nazca", "Paracas", "Wari"],
        "correcta": 2,
    },
    {
        "id": 93,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el documento internacional que reconoce los Derechos Humanos?",
        "alternativas": [
            "Carta de las Naciones Unidas",
            "Tratado de Versalles",
            "Declaración Universal de Derechos Humanos",
            "Convención de Viena",
            "Pacto de Bogotá",
        ],
        "correcta": 2,
    },
    {
        "id": 94,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el lago navegable más alto del mundo y en qué países se ubica?",
        "alternativas": [
            "Lago Titicaca – Perú y Bolivia",
            "Lago Junín – Perú",
            "Lago Poopó – Bolivia",
            "Lago Nicaragua – Centroamérica",
            "Lago Baikal – Rusia",
        ],
        "correcta": 0,
    },
    {
        "id": 95,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es el nombre del primer presidente del Perú?",
        "alternativas": [
            "Simón Bolívar",
            "José de San Martín",
            "José de la Riva Agüero",
            "Agustín Gamarra",
            "Ramón Castilla",
        ],
        "correcta": 2,
    },
    {
        "id": 96,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Qué corriente filosófica sostiene que el conocimiento proviene únicamente de la experiencia sensible?",
        "alternativas": [
            "Racionalismo",
            "Idealismo",
            "Empirismo",
            "Materialismo",
            "Existencialismo",
        ],
        "correcta": 2,
    },
    {
        "id": 97,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿Cuál es la cadena montañosa más larga del mundo?",
        "alternativas": [
            "Los Alpes",
            "El Himalaya",
            "Los Andes",
            "Las Rocosas",
            "El Atlas",
        ],
        "correcta": 2,
    },
    {
        "id": 98,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "En el Perú, ¿cuántos años dura el mandato presidencial?",
        "alternativas": ["4 años", "5 años", "6 años", "7 años", "8 años"],
        "correcta": 1,
    },
    {
        "id": 99,
        "area": "Humanidades",
        "tipo": "Alternativa",
        "enunciado": "¿A qué movimiento literario pertenece el libro 'Cien años de soledad' de García Márquez?",
        "alternativas": [
            "Realismo",
            "Naturalismo",
            "Modernismo",
            "Realismo mágico",
            "Vanguardismo",
        ],
        "correcta": 3,
    },
    {
        "id": 100,
        "area": "Humanidades",
        "tipo": "Verdadero/Falso",
        "enunciado": "La Amazonía peruana representa más del 60% del territorio nacional.",
        "alternativas": ["Verdadero", "Falso"],
        "correcta": 0,
    },
]


class ExamenState(rx.State):
    preguntas: list[Pregunta] = PREGUNTAS_DEMO
    respuestas: dict[int, int] = {}
    indice_actual: int = 0
    tiempo_restante: int = 180 * 60
    examen_iniciado: bool = False
    examen_finalizado: bool = False
    timer_activo: bool = False
    puntaje: int = 0
    correctas: int = 0
    condicion: str = ""

    @rx.var
    def total_preguntas(self) -> int:
        return len(self.preguntas)

    @rx.var
    def respondidas(self) -> int:
        return len(self.respuestas)

    @rx.var
    def progreso(self) -> float:
        if len(self.preguntas) == 0:
            return 0.0
        return (len(self.respuestas) / len(self.preguntas)) * 100.0

    @rx.var
    def pregunta_actual(self) -> Pregunta:
        if 0 <= self.indice_actual < len(self.preguntas):
            return self.preguntas[self.indice_actual]
        return self.preguntas[0]

    @rx.var
    def respuesta_actual(self) -> int:
        return self.respuestas.get(self.indice_actual, -1)

    @rx.var
    def tiempo_formateado(self) -> str:
        h = self.tiempo_restante // 3600
        m = (self.tiempo_restante % 3600) // 60
        s = self.tiempo_restante % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @rx.var
    def tiempo_critico(self) -> bool:
        return self.tiempo_restante <= 600 and self.tiempo_restante > 0

    @rx.event
    def iniciar_examen(self):
        self.examen_iniciado = True
        self.examen_finalizado = False
        self.respuestas = {}
        self.indice_actual = 0
        self.tiempo_restante = 180 * 60
        self.puntaje = 0
        self.correctas = 0
        self.condicion = ""
        self.timer_activo = True
        return ExamenState.tick_timer

    @rx.event(background=True)
    async def tick_timer(self):
        while True:
            await asyncio.sleep(1)
            async with self:
                if not self.timer_activo or self.examen_finalizado:
                    return
                if self.tiempo_restante <= 0:
                    self.timer_activo = False
                    self._calcular_resultado()
                    return
                self.tiempo_restante -= 1

    @rx.event
    def seleccionar_respuesta(self, idx: int):
        self.respuestas[self.indice_actual] = idx

    @rx.event
    def ir_pregunta(self, idx: int):
        if 0 <= idx < len(self.preguntas):
            self.indice_actual = idx

    @rx.event
    def siguiente(self):
        if self.indice_actual < len(self.preguntas) - 1:
            self.indice_actual += 1

    @rx.event
    def anterior(self):
        if self.indice_actual > 0:
            self.indice_actual -= 1

    def _calcular_resultado(self):
        correctas = 0
        for i, p in enumerate(self.preguntas):
            if self.respuestas.get(i, -1) == p["correcta"]:
                correctas += 1
        # Exact calculation: 1 point per correct answer
        # Condición: INGRESÓ if correctas > 51
        self.correctas = correctas
        self.puntaje = correctas
        self.condicion = "INGRESÓ" if self.correctas > 51 else "NO INGRESÓ"
        self.examen_finalizado = True
        self.timer_activo = False

    @rx.event
    def finalizar_examen(self):
        self._calcular_resultado()
        return rx.toast(
            f"Examen finalizado. {self.correctas}/{len(self.preguntas)} correctas",
            duration=3000,
        )

    @rx.event
    def reiniciar(self):
        self.examen_iniciado = False
        self.examen_finalizado = False
        self.respuestas = {}
        self.indice_actual = 0
        self.tiempo_restante = 180 * 60
        self.puntaje = 0
        self.correctas = 0
        self.condicion = ""
        self.timer_activo = False
