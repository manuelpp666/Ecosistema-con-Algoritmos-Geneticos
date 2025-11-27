# ============================================
# nucleo/presa.py
# ============================================
from nucleo.entidad import Entidad
from configuracion import parametros
import random
import math

class Presa(Entidad):
    def __init__(self, posicion, genoma, energia_nacimiento=None):
        e_ini = energia_nacimiento if energia_nacimiento else parametros.ENERGIA_INICIAL_PRESA
        super().__init__("presa", e_ini, posicion, genoma)

    def actuar(self, mundo, cercanos):
        self.envejecer_y_metabolismo()
        if not self.viva: return None

        bioma = mundo.biomas[self.posicion[0]][self.posicion[1]]
        vision = self.percepcion
        if bioma == parametros.BIOMA_BOSQUE: vision *= 0.6 
        
        amenazas = []
        parejas = []
        for e in cercanos:
            if self.distancia(e.posicion) <= vision:
                if e.tipo == "depredador": amenazas.append(e)
                elif e.tipo == "presa" and e != self: parejas.append(e)

        # 1. SUPERVIVENCIA EXTREMA (Huir siempre si ve un lobo)
        if amenazas:
            amenaza = min(amenazas, key=lambda x: self.distancia(x.posicion))
            self.huir(mundo, amenaza)
            return None # Si huye, no hace nada más

        # 2. REPRODUCCIÓN (Prioridad si hay comida y pareja)
        # Relajamos el estrés poblacional un poco (3 vecinos) para que reboten rápido
        parejas_aqui = [p for p in parejas if p.posicion == self.posicion]
        if self.energia > self.energia_maxima * 0.5 and parejas_aqui and len(parejas) < 4:
            if random.random() < 0.3:
                pareja = random.choice(parejas_aqui)
                gen_hijo, e_hijo = self.reproducir_sexual_base(pareja)
                return Presa(self.posicion, gen_hijo, e_hijo)

        # 3. COMER
        if self.energia < self.energia_maxima * 0.9:
            cant = mundo.consumir_alimento(self.posicion, 3.0)
            if cant > 0:
                self.ganar_energia(cant * parametros.ENERGIA_AL_COMER_HIERBA)
            else:
                self.mover(mundo)
        else:
            self.mover(mundo)
            
        return None

    def huir(self, mundo, depredador):
        py, px = self.posicion
        dy, dx = depredador.posicion
        vec_y, vec_x = py - dy, px - dx
        dist = math.sqrt(vec_y**2 + vec_x**2)
        if dist == 0: vec_y, vec_x = random.choice([-1,1]), random.choice([-1,1])
        else: vec_y, vec_x = vec_y/dist, vec_x/dist
        
        pasos = max(1, int(self.velocidad))
        dest_y = int(py + vec_y * pasos)
        dest_x = int(px + vec_x * pasos)
        self.mover(mundo, (dest_y, dest_x))

    def distancia(self, pos):
        return math.sqrt((self.posicion[0]-pos[0])**2 + (self.posicion[1]-pos[1])**2)