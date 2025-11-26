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

        # Modificadores por Bioma
        bioma_actual = mundo.biomas[self.posicion[0]][self.posicion[1]]
        
        # Punto 2: En bosque, conejos se esconden (lobos los ven menos), 
        # pero aquí calculamos qué ve el conejo.
        # En Bosque, la percepción se reduce.
        vision_real = self.percepcion
        if bioma_actual == parametros.BIOMA_BOSQUE:
            vision_real *= 0.6 
        
        # Filtrar entidades visibles
        amenazas = []
        parejas = []
        for e in cercanos:
            dist = self.distancia(e.posicion)
            if dist <= vision_real:
                if e.tipo == "depredador": amenazas.append(e)
                elif e.tipo == "presa" and e != self: parejas.append(e)

        # 1. Huida (Prioridad máxima)
        if amenazas:
            amenaza = min(amenazas, key=lambda x: self.distancia(x.posicion))
            self.huir(mundo, amenaza)
            return None

        # 2. Alimentación (Comer Hierba Limitada)
        # Solo comen si tienen hambre para no agotar recursos (Punto 1)
        if self.energia < self.energia_maxima * 0.9:
            # Consumir del suelo
            cantidad = mundo.consumir_alimento(self.posicion, 3.0) # Intenta comer hasta 3
            if cantidad > 0:
                self.ganar_energia(cantidad * parametros.ENERGIA_AL_COMER_HIERBA)
            else:
                # Si no hay comida, moverse a buscar
                self.mover(mundo)
        else:
            # 3. Reproducción (Punto 6: Condicionada)
            # - Energía > 50%
            # - Ha comido recientemente (turnos_sin_comer < 10)
            # - No hay sobrepoblación local
            vecinos_aqui = [p for p in parejas if p.posicion == self.posicion]
            
            condicion_repro = (
                self.energia > self.energia_maxima * 0.5 and 
                self.turnos_sin_comer < 15 and
                len(vecinos_aqui) < 3 # Evita explosión local
            )

            if condicion_repro and vecinos_aqui and random.random() < 0.2:
                pareja = random.choice(vecinos_aqui)
                gen_hijo, e_hijo = self.reproducir_sexual_base(pareja)
                return Presa(self.posicion, gen_hijo, e_hijo)
            
            self.mover(mundo)
        
        return None

    def huir(self, mundo, depredador):
        # Lógica de huida inversa
        py, px = self.posicion
        dy, dx = depredador.posicion
        vec_y, vec_x = py - dy, px - dx
        
        dist = math.sqrt(vec_y**2 + vec_x**2)
        if dist == 0: vec_y, vec_x = random.choice([-1,1]), random.choice([-1,1])
        else: vec_y, vec_x = vec_y/dist, vec_x/dist
        
        # Intentar moverse en dirección opuesta
        pasos = max(1, int(self.velocidad))
        dest_y = int(py + vec_y * pasos)
        dest_x = int(px + vec_x * pasos)
        
        self.mover(mundo, (dest_y, dest_x))

    def distancia(self, pos):
        return math.sqrt((self.posicion[0]-pos[0])**2 + (self.posicion[1]-pos[1])**2)