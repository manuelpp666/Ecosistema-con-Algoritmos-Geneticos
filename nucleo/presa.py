# ============================================
# presa.py
# Clase Presa (usa genoma completo)
# ============================================

from nucleo.entidad import Entidad
from configuracion import parametros
import math


class Presa(Entidad):
    def __init__(self, posicion, genoma):
        energia_inicial = min(parametros.ENERGIA_INICIAL_PRESA, genoma.get("energia_maxima", parametros.ENERGIA_INICIAL_PRESA))
        super().__init__(tipo="presa", energia=energia_inicial, posicion=posicion, genoma=genoma)

    def elegir_accion(self, mundo, lista_depredadores):
        if not self.viva:
            return

        dep = self.buscar_depredador_cercano(lista_depredadores)
        if dep:
            self.huir(dep)
        else:
            self.mover(mundo.tamano)

        # pastar
        self.ganar_energia(parametros.ENERGIA_HIERBA_PRESA)
        self.esta_viva()

    def buscar_depredador_cercano(self, depredadores):
        objetivo = None
        distancia_min = float("inf")
        for d in depredadores:
            if not d.viva:
                continue
            dist = self.distancia_a(d.posicion)
            if dist <= self.percepcion and dist < distancia_min:
                distancia_min = dist
                objetivo = d
        return objetivo

    def huir(self, depredador):
        dx = self.posicion[0] - depredador.posicion[0]
        dy = self.posicion[1] - depredador.posicion[1]
        distancia = math.sqrt(dx * dx + dy * dy)
        if distancia == 0:
            self.mover((parametros.TAMANO_MUNDO))
            return

        mov_x = int((dx / distancia) * self.velocidad)
        mov_y = int((dy / distancia) * self.velocidad)

        filas, cols = parametros.TAMANO_MUNDO
        nueva_f = max(0, min(filas - 1, self.posicion[0] + mov_x))
        nueva_c = max(0, min(cols - 1, self.posicion[1] + mov_y))

        self.posicion = (nueva_f, nueva_c)
        gasto = parametros.COSTO_MOVIMIENTO_BASE * (1.0 / max(0.01, self.eficiencia))
        self.energia -= gasto

    def distancia_a(self, pos):
        x1, y1 = self.posicion
        x2, y2 = pos
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def obtener_fitness(self):
        return self.pasos_sobrevividos
