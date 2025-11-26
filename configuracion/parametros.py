# ============================================
# configuracion/parametros.py (ESTABILIDAD TOTAL)
# ============================================

# ----- Tamaño del mundo -----
TAMANO_MUNDO = (40, 40) # Tamaño medio para dar respiro

# ----- Población -----
POBLACION_INICIAL_DEPREDADORES = 12  # Pocos para empezar suave
POBLACION_INICIAL_PRESAS = 150       

# ----- Biomas -----
BIOMA_AGUA = 0
BIOMA_LLANURA = 1
BIOMA_BOSQUE = 2
BIOMA_ROCA = 3

# ----- Recursos -----
MAX_COMIDA_CELDA = 15.0      # Comida abundante para conejos
REGENERACION_BASE = 3.0
DURACION_ESTACION = 100
CICLO_EVENTOS = 100

# ----- Genética -----
GENES_INICIALES = {
    "velocidad": (0.8, 1.5),
    "percepcion": (4.0, 9.0),     # Buena visión
    "agresividad": (0.3, 1.0),
    "energia_maxima": (100.0, 200.0), # ¡Tanques de energía gigantes!
    "eficiencia": (0.9, 1.3),
}
PROBABILIDAD_MUTACION = 0.15
INTENSIDAD_MUTACION = 0.15

# ----- Costos Metabólicos (Muy bajos) -----
# Vivir es barato, morir de hambre es difícil
COSTO_EXISTENCIA = 0.1         
FACTOR_GASTO_VELOCIDAD = 0.1   
FACTOR_GASTO_PERCEPCION = 0.02  
COSTO_MOVIMIENTO_BASE = 0.4    

# ----- Ciclo de Vida -----
VIDA_MAXIMA_PRESA = 120
VIDA_MAXIMA_DEPREDADOR = 300   # ¡Viven 300 turnos! Sobreviven crisis.
DENSIDAD_ENFERMEDAD = 3        # Control estricto de conejos (si se juntan 3, enferman)

# ----- Valores Energéticos -----
ENERGIA_INICIAL_DEPREDADOR = 150 
ENERGIA_INICIAL_PRESA = 60

# Recompensas
ENERGIA_AL_COMER_PRESA = 150.0  # Comer 1 conejo llena la barra entera
ENERGIA_AL_COMER_HIERBA = 10.0

# ----- Visualización -----
MODO_VISUAL = "pygame"
FPS = 15