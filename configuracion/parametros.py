# ============================================
# configuracion/parametros.py (MODO ETERNO)
# ============================================

# ----- Tamaño del mundo -----
# Un mundo mediano permite refugios naturales
TAMANO_MUNDO = (45, 45)

# ----- Población Inicial -----
# Pocos depredadores para empezar suave
POBLACION_INICIAL_DEPREDADORES = 12
POBLACION_INICIAL_PRESAS = 150

# ----- Biomas -----
BIOMA_AGUA = 0
BIOMA_LLANURA = 1
BIOMA_BOSQUE = 2
BIOMA_ROCA = 3

# ----- Recursos -----
MAX_COMIDA_CELDA = 15.0      # Mucha comida para conejos
REGENERACION_BASE = 3.0      # Recuperación rápida de hierba
DURACION_ESTACION = 150
CICLO_EVENTOS = 150

# ----- Genética -----
GENES_INICIALES = {
    "velocidad": (0.8, 1.5),
    "percepcion": (4.0, 9.0),
    "agresividad": (0.3, 0.9),    # Bajamos un poco la agresividad máxima
    "energia_maxima": (100.0, 300.0), # ¡Lobos con reservas gigantes!
    "eficiencia": (1.0, 1.5),
}
PROBABILIDAD_MUTACION = 0.15
INTENSIDAD_MUTACION = 0.15

# ----- Costos Metabólicos (SUPER BAJOS PARA LOBOS) -----
COSTO_EXISTENCIA = 0.05        # Casi "gratis" existir
FACTOR_GASTO_VELOCIDAD = 0.05
FACTOR_GASTO_PERCEPCION = 0.01
COSTO_MOVIMIENTO_BASE = 0.3

# ----- Ciclo de Vida -----
VIDA_MAXIMA_PRESA = 120
VIDA_MAXIMA_DEPREDADOR = 400   # Viven muchísimo tiempo
DENSIDAD_ENFERMEDAD = 5

# ----- Valores Energéticos -----
# Nacen llenos de energía
ENERGIA_INICIAL_DEPREDADOR = 200
ENERGIA_INICIAL_PRESA = 50

# Recompensas
ENERGIA_AL_COMER_PRESA = 150.0 # Comer llena el tanque
ENERGIA_AL_COMER_HIERBA = 8.0

# ----- Visualización -----
MODO_VISUAL = "pygame"
FPS = 15