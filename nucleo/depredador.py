# ============================================
# depredador.py
# Clase Depredador (usa genoma completo)
# ============================================

from nucleo.entidad import Entidad
from configuracion import parametros
import math


class Depredador(Entidad):
    def __init__(self, posicion, genoma):
        energia_inicial = min(parametros.ENERGIA_INICIAL_DEPREDADOR, genoma.get("energia_maxima", parametros.ENERGIA_INICIAL_DEPREDADOR))
        super().__init__(tipo="depredador", energia=energia_inicial, posicion=posicion, genoma=genoma)
        self.presas_comidas = 0

    def elegir_accion(self, mundo, lista_presas):
        if not self.viva:
            return

        objetivo = self.buscar_presa_cercana(lista_presas)
        if objetivo:
            self.perseguir(objetivo)
        else:
            self.mover(mundo.tamano)

        self.esta_viva()

    def buscar_presa_cercana(self, presas):
        objetivo = None
        distancia_min = float("inf")
        for p in presas:
            if not p.viva:
                continue
            dist = self.distancia_a(p.posicion)
            if dist <= self.percepcion and dist < distancia_min:
                distancia_min = dist
                objetivo = p
        return objetivo

    def perseguir(self, presa):
        px, py = presa.posicion
        x, y = self.posicion
        dx = px - x
        dy = py - y
        distancia = math.sqrt(dx * dx + dy * dy)
        if distancia == 0:
            return
        mov_x = int((dx / distancia) * self.velocidad)
        mov_y = int((dy / distancia) * self.velocidad)
        filas, cols = parametros.TAMANO_MUNDO
        nueva_f = max(0, min(filas - 1, x + mov_x))
        nueva_c = max(0, min(cols - 1, y + mov_y))
        self.posicion = (nueva_f, nueva_c)
        gasto = parametros.COSTO_MOVIMIENTO_BASE * (1.0 / max(0.01, self.eficiencia))
        self.energia -= gasto

    def intentar_comer(self, presas):
        for presa in presas:
            if presa.viva and presa.posicion == self.posicion:
                presa.viva = False
                self.ganar_energia(parametros.ENERGIA_AL_COMER)
                self.presas_comidas += 1
                return True
        return False

    def distancia_a(self, pos):
        x1, y1 = self.posicion
        x2, y2 = pos
        import math
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def obtener_fitness(self):
        return (self.presas_comidas * 5) + self.pasos_sobrevividos
