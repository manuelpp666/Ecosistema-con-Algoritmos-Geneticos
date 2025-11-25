# ============================================
# nucleo/depredador.py
# ============================================
from nucleo.entidad import Entidad
from configuracion import parametros
import math
import random

class Depredador(Entidad):
    def __init__(self, posicion, genoma):
        energia_inicial = min(parametros.ENERGIA_INICIAL_DEPREDADOR, genoma.get("energia_maxima", parametros.ENERGIA_INICIAL_DEPREDADOR))
        super().__init__(tipo="depredador", energia=energia_inicial, posicion=posicion, genoma=genoma)
        self.presas_comidas = 0

    def elegir_accion(self, mundo, entidades_cercanas):
        if not self.viva: return None

        presas = [e for e in entidades_cercanas if e.tipo == "presa"]
        parejas = [e for e in entidades_cercanas if e.tipo == "depredador" and e != self]

        objetivo = self.buscar_presa_cercana(presas)
        
        if objetivo:
            self.perseguir(objetivo)
        else:
            # Si no hay caza, intentar reproducción o moverse
            if self.energia > self.energia_maxima * 0.6:
                parejas_aqui = [d for d in parejas if d.posicion == self.posicion]
                if parejas_aqui and random.random() < 0.2:
                    pareja = random.choice(parejas_aqui)
                    self.esta_viva()
                    return self.sexo(pareja)
            
            self.mover(mundo.tamano)

        self.esta_viva()
        return None

    def sexo(self, pareja):
        costo = self.energia_maxima * 0.25
        self.energia -= costo
        pareja.energia -= costo
        nuevo_gen = self.reproducir_sexual_genoma(pareja)
        return Depredador(self.posicion, nuevo_gen)

    def buscar_presa_cercana(self, presas):
        objetivo = None
        distancia_min = float("inf")
        for p in presas:
            if not p.viva: continue
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
        distancia = math.sqrt(dx*dx + dy*dy)
        if distancia == 0: return

        mov_x = int((dx / distancia) * self.velocidad)
        mov_y = int((dy / distancia) * self.velocidad)
        
        filas, cols = parametros.TAMANO_MUNDO
        self.posicion = (max(0, min(filas-1, x+mov_x)), max(0, min(cols-1, y+mov_y)))
        
        gasto = parametros.COSTO_MOVIMIENTO_BASE * (1.0 / max(0.01, self.eficiencia))
        self.energia -= gasto

    def intentar_comer(self, presas_en_misma_casilla):
        # El motor ya filtró presas que están en mi misma casilla
        for presa in presas_en_misma_casilla:
            if presa.viva:
                presa.viva = False # Muere
                self.ganar_energia(parametros.ENERGIA_AL_COMER)
                self.presas_comidas += 1
                return True
        return False

    def distancia_a(self, pos):
        return math.sqrt((self.posicion[0]-pos[0])**2 + (self.posicion[1]-pos[1])**2)

    def obtener_fitness(self):
        return (self.presas_comidas * 5) + self.pasos_sobrevividos