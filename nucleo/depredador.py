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
        bioma_actual = mundo.biomas[self.posicion[0]][self.posicion[1]]
        vision_real = self.percepcion
        
        # Ajuste de biomas
        if bioma_actual == parametros.BIOMA_BOSQUE: vision_real *= 0.7 
        elif bioma_actual == parametros.BIOMA_LLANURA: vision_real *= 1.3

        # Clasificar entorno
        presas_visibles = []
        parejas_visibles = []
        
        for e in cercanos:
            dist = self.distancia(e.posicion)
            if dist <= vision_real:
                if e.tipo == "presa": presas_visibles.append(e)
                elif e.tipo == "depredador" and e != self: parejas_visibles.append(e)

        # --- TOMA DE DECISIONES ---
        
        # CAMBIO CLAVE: Umbral de reproducción mucho más alto (85%)
        # Esto evita que la población de lobos explote y mate a todos los conejos.
        modo_reproduccion = self.energia > (self.energia_maxima * 0.85)

        # 1. REPRODUCCIÓN (Solo si está muy fuerte)
        if modo_reproduccion and parejas_visibles:
            pareja = min(parejas_visibles, key=lambda x: self.distancia(x.posicion))
            
            if pareja.posicion == self.posicion:
                # 50% chance de éxito
                if random.random() < 0.5:
                    gen_hijo, e_hijo = self.reproducir_sexual_base(pareja)
                    return Depredador(self.posicion, gen_hijo, e_hijo)
            else:
                self.perseguir(mundo, pareja)
                return None

        # 2. CAZA (Prioridad estándar)
        if presas_visibles:
            presa_mas_cercana = min(presas_visibles, key=lambda x: self.distancia(x.posicion))
            self.perseguir(mundo, presa_mas_cercana)
            return None

        # 3. EXPLORACIÓN
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

    def intentar_comer(self, lista_presas_aqui):
        if not lista_presas_aqui: return False
        
        presa = random.choice(lista_presas_aqui)
        
        # CÁLCULO DE ÉXITO DE CAZA
        chance = 0.6 + (self.genoma.get("agresividad", 0.5) * 0.3)
        if presa.velocidad > self.velocidad: 
            chance -= 0.15 
        
        if random.random() < chance:
            presa.viva = False
            self.ganar_energia(parametros.ENERGIA_AL_COMER_PRESA)
            self.presas_comidas += 1
            return True
            
        return False

    def distancia(self, pos):
        return math.sqrt((self.posicion[0]-pos[0])**2 + (self.posicion[1]-pos[1])**2)