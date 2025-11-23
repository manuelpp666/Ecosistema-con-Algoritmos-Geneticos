# ============================================
# motor.py
# Controla ciclo de vida, reproducción (asex.), estadísticas básicas
# ============================================

import random
from configuracion import parametros
from nucleo.mundo import Mundo
from simulacion import registro
from nucleo import genetica
from nucleo.presa import Presa
from nucleo.depredador import Depredador


class MotorSimulacion:
    def __init__(self, mundo=None):
        self.mundo = mundo if mundo is not None else Mundo()
        self.paso_actual = 0
        self.registro = registro.Registro()

    def ejecutar_paso(self):
        self.paso_actual += 1
        self.mundo.ejecutar_turno()
        self._intentar_reproduccion_asexual()
        self.registro.registrar_generacion(self.paso_actual, self.mundo.presas, self.mundo.depredadores)

    def _intentar_reproduccion_asexual(self):
        """
        Reproducción asexual simple:
        - si la entidad tiene energía >= 60% de su max, puede reproducir clon+mutación
        - hijo aparece en una celda adyacente (si posible)
        """
        nuevas_presas = []
        nuevos_deps = []

        # Presas
        for p in list(self.mundo.presas):
            if p.energia >= 0.6 * p.energia_maxima and random.random() < 0.15:
                gen_hijo = p.reproducir_asexual()
                pos_hijo = self._posicion_vecina_aleatoria(p.posicion)
                nuevas_presas.append(Presa(pos_hijo, gen_hijo))

                # costeo energético por reproducirse
                p.energia *= 0.6

        # Depredadores
        for d in list(self.mundo.depredadores):
            if d.energia >= 0.6 * d.energia_maxima and random.random() < 0.12:
                gen_hijo = d.reproducir_asexual()
                pos_hijo = self._posicion_vecina_aleatoria(d.posicion)
                nuevos_deps.append(Depredador(pos_hijo, gen_hijo))
                d.energia *= 0.6

        self.mundo.presas.extend(nuevas_presas)
        self.mundo.depredadores.extend(nuevos_deps)

    def _posicion_vecina_aleatoria(self, posicion):
        filas, cols = self.mundo.tamano
        f, c = posicion
        candidatos = []
        for df in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if df == 0 and dc == 0:
                    continue
                nf, nc = f + df, c + dc
                if 0 <= nf < filas and 0 <= nc < cols:
                    candidatos.append((nf, nc))
        if candidatos:
            return random.choice(candidatos)
        return posicion
