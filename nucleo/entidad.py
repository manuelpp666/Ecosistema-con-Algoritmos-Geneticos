# ============================================
# nucleo/entidad.py
# ============================================
from dataclasses import dataclass, field
import random
from configuracion import parametros
from nucleo import genetica

@dataclass
class Entidad:
    tipo: str
    energia: float
    posicion: tuple
    genoma: dict = field(default_factory=dict)

    viva: bool = True
    pasos_sobrevividos: int = 0

    @property
    def velocidad(self): return float(self.genoma.get("velocidad", 1.0))

    @property
    def percepcion(self): return float(self.genoma.get("percepcion", 1.0))

    @property
    def agresividad(self): return float(self.genoma.get("agresividad", 0.0))

    @property
    def energia_maxima(self): return float(self.genoma.get("energia_maxima", self.energia))

    @property
    def eficiencia(self): return float(self.genoma.get("eficiencia", 1.0))

    def mover(self, tamano_mundo):
        if not self.viva: return

        filas, cols = tamano_mundo
        max_despl = max(1, int(round(self.velocidad)))
        
        # Movimiento aleatorio simple si no hay objetivo
        df = random.randint(-max_despl, max_despl)
        dc = random.randint(-max_despl, max_despl)

        nueva_f = max(0, min(filas - 1, self.posicion[0] + df))
        nueva_c = max(0, min(cols - 1, self.posicion[1] + dc))

        self.posicion = (nueva_f, nueva_c)
        gasto = parametros.COSTO_MOVIMIENTO_BASE * (1.0 / max(0.01, self.eficiencia))
        self.energia -= gasto

    def esta_viva(self):
        if self.energia <= 0:
            self.viva = False
        return self.viva

    def ganar_energia(self, cantidad):
        self.energia += cantidad
        if self.energia > self.energia_maxima:
            self.energia = self.energia_maxima

    def gastar_energia(self, cantidad):
        self.energia -= cantidad
        if self.energia <= 0: self.viva = False

    def registrar_paso(self):
        if self.viva: self.pasos_sobrevividos += 1

    def reproducir_asexual(self):
        nuevo_genoma = dict(self.genoma)
        nuevo_genoma = genetica.mutar_genoma(nuevo_genoma)
        return nuevo_genoma
    
    def reproducir_sexual_genoma(self, pareja):
        """Genera un genoma hijo combinando self y pareja."""
        nuevo_genoma = genetica.cruzar_genomas(self.genoma, pareja.genoma)
        nuevo_genoma = genetica.mutar_genoma(nuevo_genoma)
        return nuevo_genoma