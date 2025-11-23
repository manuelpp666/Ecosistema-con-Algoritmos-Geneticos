# ============================================
# parametros.py
# Configuración general del ecosistema (genoma completo)
# ============================================

# ----- Tamaño del mundo (filas, columnas) -----
TAMANO_MUNDO = (30, 30)  # filas, columnas

# ----- Población inicial -----
POBLACION_INICIAL_DEPREDADORES = 15
POBLACION_INICIAL_PRESAS = 35

# ----- Parámetros genéticos (rangos por gen) -----
# Cada entrada: (min, max)
GENES_INICIALES = {
    "velocidad": (0.5, 2.0),        # celdas por turno (float)
    "percepcion": (2.0, 8.0),       # radio de detección (float)
    "agresividad": (0.0, 1.0),      # factor (0..1) para comportamiento agresivo
    "energia_maxima": (20.0, 60.0), # capacidad energética
    "eficiencia": (0.5, 1.5),       # mayor -> menos gasto relativo
}

# ----- Mutación -----
PROBABILIDAD_MUTACION = 0.10
INTENSIDAD_MUTACION = 0.15  # fracción relativa del valor (ej. 0.15 = ±15%)

# ----- Ciclo evolutivo -----
GENERACIONES = 40
PASOS_POR_GENERACION = 150

# ----- Energía y supervivencia (valores base; cada individuo tendrá su energia_maxima) -----
ENERGIA_INICIAL_DEPREDADOR = 40
ENERGIA_INICIAL_PRESA = 30

COSTO_MOVIMIENTO_BASE = 1.0        # coste base por movimiento (se escala por eficiencia)
ENERGIA_AL_COMER = 25.0            # energia que gana un depredador al comerse una presa
ENERGIA_HIERBA_PRESA = 3.0         # energia que obtiene una presa por turno (pastar)

# ----- Visualización -----
MODO_VISUAL = "matplotlib"   # "matplotlib" o "texto"
FPS = 6                      # frames por segundo de la visualización
