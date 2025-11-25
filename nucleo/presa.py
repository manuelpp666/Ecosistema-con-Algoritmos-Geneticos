# ============================================
# nucleo/presa.py
# ============================================
from nucleo.entidad import Entidad
from configuracion import parametros
import math
import random

class Presa(Entidad):
    def __init__(self, posicion, genoma):
        energia_inicial = min(parametros.ENERGIA_INICIAL_PRESA, genoma.get("energia_maxima", parametros.ENERGIA_INICIAL_PRESA))
        super().__init__(tipo="presa", energia=energia_inicial, posicion=posicion, genoma=genoma)

    def elegir_accion(self, mundo, entidades_cercanas):
        if not self.viva: return None

        # Filtrar listas
        depredadores = [e for e in entidades_cercanas if e.tipo == "depredador"]
        parejas = [e for e in entidades_cercanas if e.tipo == "presa" and e != self]

        # 1. Huir
        dep = self.buscar_depredador_cercano(depredadores)
        if dep:
            self.huir(dep)
        else:
            # 2. Comer y Reproducirse
            hierba = mundo.consumir_hierba(self.posicion)
            self.ganar_energia(parametros.ENERGIA_HIERBA_PRESA * hierba)

            # Reproducción Sexual si hay energía y pareja en la MISMA celda
            if self.energia > self.energia_maxima * 0.6:
                parejas_aqui = [p for p in parejas if p.posicion == self.posicion]
                if parejas_aqui and random.random() < 0.3:
                    pareja = random.choice(parejas_aqui)
                    return self.sexo(pareja)

            # Movimiento normal
            self.mover(mundo.tamano)

        self.esta_viva()
        return None

    def sexo(self, pareja):
        costo = self.energia_maxima * 0.25
        self.energia -= costo
        pareja.energia -= costo
        nuevo_gen = self.reproducir_sexual_genoma(pareja)
        return Presa(self.posicion, nuevo_gen)

    def buscar_depredador_cercano(self, depredadores):
        objetivo = None
        distancia_min = float("inf")
        for d in depredadores:
            if not d.viva: continue
            dist = self.distancia_a(d.posicion)
            if dist <= self.percepcion and dist < distancia_min:
                distancia_min = dist
                objetivo = d
        return objetivo

    def huir(self, depredador):
        dx = self.posicion[0] - depredador.posicion[0]
        dy = self.posicion[1] - depredador.posicion[1]
        distancia = math.sqrt(dx*dx + dy*dy)
        if distancia == 0: 
            self.mover(parametros.TAMANO_MUNDO)
            return

        mov_x = int((dx / distancia) * self.velocidad)
        mov_y = int((dy / distancia) * self.velocidad)
        
        f, c = self.posicion
        filas, cols = parametros.TAMANO_MUNDO
        nf = max(0, min(filas - 1, f + mov_x))
        nc = max(0, min(cols - 1, c + mov_y))
        
        self.posicion = (nf, nc)
        gasto = parametros.COSTO_MOVIMIENTO_BASE * (1.0 / max(0.01, self.eficiencia))
        self.energia -= gasto

    def distancia_a(self, pos):
        return math.sqrt((self.posicion[0]-pos[0])**2 + (self.posicion[1]-pos[1])**2)

    def obtener_fitness(self):
        return self.pasos_sobrevividos