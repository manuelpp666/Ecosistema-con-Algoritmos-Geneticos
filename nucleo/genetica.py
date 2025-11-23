# ============================================
# genetica.py
# Operaciones de cruce y mutación sobre genomas (dict)
# ============================================
import random
from configuracion import parametros

def limitar(valor, minimo, maximo):
    return max(min(valor, maximo), minimo)


def crear_genoma_aleatorio():
    """Crea un genoma usando los rangos en parametros.GENES_INICIALES."""
    g = {}
    for clave, (mi, ma) in parametros.GENES_INICIALES.items():
        # si los rangos son enteros, usamos randrange; si float, uniform
        try:
            # si son enteros (sin decimales), la tupla puede ser ints
            if isinstance(mi, int) and isinstance(ma, int):
                g[clave] = random.randint(mi, ma)
            else:
                g[clave] = random.uniform(mi, ma)
        except Exception:
            g[clave] = random.uniform(mi, ma)
    return g


def cruzar_genomas(genoma_a, genoma_b):
    """
    Cruce simple: promedio de genes + pequeño ruido.
    Asume que ambos genomas tienen las mismas claves.
    """
    hijo = {}
    for clave in genoma_a.keys():
        pa = genoma_a[clave]
        pb = genoma_b[clave]
        mezcla = (pa + pb) / 2.0
        ruido = random.uniform(-0.05, 0.05) * mezcla  # ruido relativo pequeño
        valor = mezcla + ruido

        # limites según parametros
        mi, ma = parametros.GENES_INICIALES[clave]
        valor = limitar(valor, mi, ma)
        hijo[clave] = valor

    return hijo


def mutar_genoma(genoma, prob_mutacion=None, intensidad=None):
    """Mutación por gen: con prob_mutacion aplica un cambio relativo +- intensidad."""
    if prob_mutacion is None:
        prob_mutacion = parametros.PROBABILIDAD_MUTACION
    if intensidad is None:
        intensidad = parametros.INTENSIDAD_MUTACION

    for clave in list(genoma.keys()):
        if random.random() < prob_mutacion:
            base = genoma[clave]
            # cambio relativo (por ejemplo ±15% del valor)
            delta = base * random.uniform(-intensidad, intensidad)
            valor = base + delta
            mi, ma = parametros.GENES_INICIALES[clave]
            genoma[clave] = limitar(valor, mi, ma)

    return genoma
