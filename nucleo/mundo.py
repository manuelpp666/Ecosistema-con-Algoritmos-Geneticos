# ============================================
# mundo.py
# Representa el mundo donde viven presas y depredadores
# ============================================

import random
from configuracion import parametros
from nucleo.depredador import Depredador
from nucleo.presa import Presa
from nucleo import genetica


class Mundo:
    def __init__(self):
        self.tamano = parametros.TAMANO_MUNDO
        self.presas = []
        self.depredadores = []
        self.crear_poblacion_inicial()

    def crear_poblacion_inicial(self):
        # presas
        for _ in range(parametros.POBLACION_INICIAL_PRESAS):
            pos = self.posicion_aleatoria()
            gen = genetica.crear_genoma_aleatorio()
            # Asegurar que agresividad de presa sea 0
            gen["agresividad"] = 0.0
            self.presas.append(Presa(pos, gen))

        # depredadores
        for _ in range(parametros.POBLACION_INICIAL_DEPREDADORES):
            pos = self.posicion_aleatoria()
            gen = genetica.crear_genoma_aleatorio()
            self.depredadores.append(Depredador(pos, gen))

    def posicion_aleatoria(self):
        filas, cols = self.tamano
        return (random.randint(0, filas - 1), random.randint(0, cols - 1))

    def todas_las_entidades(self):
        return list(self.presas) + list(self.depredadores)

    def ejecutar_turno(self):
        # Presas
        for presa in list(self.presas):
            presa.elegir_accion(self, self.depredadores)
            presa.registrar_paso()

        # Depredadores
        for dep in list(self.depredadores):
            dep.elegir_accion(self, self.presas)
            dep.registrar_paso()

        # Depredadores intentan comer
        for dep in list(self.depredadores):
            dep.intentar_comer(self.presas)

        # Limpiar muertos
        self.limpiar_muertos()

    def limpiar_muertos(self):
        self.presas = [p for p in self.presas if p.viva]
        self.depredadores = [d for d in self.depredadores if d.viva]

    def obtener_matriz_mundo(self):
        filas, cols = self.tamano
        matriz = [[0 for _ in range(cols)] for _ in range(filas)]
        for p in self.presas:
            f, c = p.posicion
            matriz[f][c] = 1
        for d in self.depredadores:
            f, c = d.posicion
            matriz[f][c] = 2
        return matriz
