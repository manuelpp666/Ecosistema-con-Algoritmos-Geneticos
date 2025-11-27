# ============================================
# nucleo/depredador.py
# ============================================
from nucleo.entidad import Entidad
from configuracion import parametros
import random
import math

class Depredador(Entidad):
    def __init__(self, posicion, genoma, energia_nacimiento=None):
        e_ini = energia_nacimiento if energia_nacimiento else parametros.ENERGIA_INICIAL_DEPREDADOR
        super().__init__("depredador", e_ini, posicion, genoma)
        self.presas_comidas = 0

    def actuar(self, mundo, cercanos):
        self.envejecer_y_metabolismo()
        if not self.viva: return None

        # --- PERCEPCIÓN ---
        bioma = mundo.biomas[self.posicion[0]][self.posicion[1]]
        vision = self.percepcion
        if bioma == parametros.BIOMA_BOSQUE: vision *= 0.7 
        elif bioma == parametros.BIOMA_LLANURA: vision *= 1.3

        presas = []
        parejas = []
        for e in cercanos:
            if self.distancia(e.posicion) <= vision:
                if e.tipo == "presa": presas.append(e)
                elif e.tipo == "depredador" and e != self: parejas.append(e)

        # --- LÓGICA DE ESTABILIDAD ---
        # Solo se reproducen si están REBOSANTES de energía (75%)
        # Esto frena la explosión demográfica de lobos.
        listo_reproducir = self.energia > (self.energia_maxima * 0.75)
        hambre = self.energia < (self.energia_maxima * 0.4)

        objetivo = None

        # 1. Prioridad: Comer si tengo hambre
        if hambre and presas:
            objetivo = min(presas, key=lambda x: self.distancia(x.posicion))
        
        # 2. Prioridad: Reproducirse si estoy muy sano
        elif listo_reproducir and parejas:
            pareja = min(parejas, key=lambda x: self.distancia(x.posicion))
            if pareja.posicion == self.posicion:
                if random.random() < 0.4: # Probabilidad moderada
                    gen_hijo, e_hijo = self.reproducir_sexual_base(pareja)
                    return Depredador(self.posicion, gen_hijo, e_hijo)
            else:
                objetivo = pareja

        # 3. Caza oportunista (si no hay nada más que hacer)
        elif presas:
            objetivo = min(presas, key=lambda x: self.distancia(x.posicion))

        # Movimiento
        if objetivo:
            self.perseguir(mundo, objetivo)
        else:
            self.mover(mundo)
        
        return None

    def perseguir(self, mundo, objetivo):
        py, px = objetivo.posicion
        my, mx = self.posicion
        vec_y, vec_x = py - my, px - mx
        dist = math.sqrt(vec_y**2 + vec_x**2)
        if dist == 0: return 
        
        pasos = max(1, int(self.velocidad))
        dest_y = int(my + (vec_y/dist) * pasos)
        dest_x = int(mx + (vec_x/dist) * pasos)
        self.mover(mundo, (dest_y, dest_x))

    def intentar_comer(self, presas_aqui):
        if not presas_aqui: return False
        
        # Elige la presa más fácil
        presa = min(presas_aqui, key=lambda p: p.velocidad)
        
        chance = 0.6 + (self.genoma.get("agresividad", 0.5) * 0.3)
        if presa.velocidad > self.velocidad: chance -= 0.15
            
        if random.random() < chance:
            presa.viva = False
            self.ganar_energia(parametros.ENERGIA_AL_COMER_PRESA)
            self.presas_comidas += 1
            return True
        return False

    def distancia(self, pos):
        return math.sqrt((self.posicion[0]-pos[0])**2 + (self.posicion[1]-pos[1])**2)