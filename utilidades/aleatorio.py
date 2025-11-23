# ============================================
# aleatorio.py
# Utilidades pequeñas
# ============================================
import random

def elegir(lista):
    return random.choice(lista)

def entero(minimo, maximo):
    return random.randint(minimo, maximo)

def real(minimo, maximo):
    return random.uniform(minimo, maximo)

def evento(p):
    return random.random() < p
