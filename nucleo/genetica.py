# ============================================
# nucleo/genetica.py
# ============================================
import random
from configuracion import parametros

def limitar(valor, minimo, maximo):
    return max(min(valor, maximo), minimo)

def crear_genoma_aleatorio():
    g = {}
    for clave, (mi, ma) in parametros.GENES_INICIALES.items():
        g[clave] = random.uniform(mi, ma)
    return g

def cruzar_genomas(genoma_a, genoma_b):
    hijo = {}
    for clave in genoma_a.keys():
        pa = genoma_a[clave]
        pb = genoma_b[clave]
        hijo[clave] = (pa + pb) / 2.0
    return hijo

def mutar_genoma(genoma):
    """
    Mutación con penalización:
    Si aumentas velocidad o percepción, la eficiencia tiende a bajar.
    """
    nuevo = dict(genoma)
    prob = parametros.PROBABILIDAD_MUTACION
    intensidad = parametros.INTENSIDAD_MUTACION
    
    # Mutación normal
    for clave in nuevo.keys():
        if random.random() < prob:
            delta = random.uniform(-intensidad, intensidad)
            nuevo[clave] = nuevo[clave] * (1.0 + delta)
            
            # Limitar rangos
            mi, ma = parametros.GENES_INICIALES[clave]
            nuevo[clave] = limitar(nuevo[clave], mi, ma)

    # Lógica de Trade-off (Punto 9)
    # Si la velocidad es muy alta, baja la eficiencia (cuesta más moverse)
    if nuevo["velocidad"] > 1.3:
        nuevo["eficiencia"] *= 0.95
    if nuevo["percepcion"] > 5.0:
        nuevo["energia_maxima"] *= 0.95 # Cerebro grande consume reservas

    return nuevo