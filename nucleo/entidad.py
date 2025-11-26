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
    edad: int = 0
    pasos_sobrevividos: int = 0
    turnos_sin_comer: int = 0

    @property
    def velocidad(self): return self.genoma.get("velocidad", 1.0)
    @property
    def percepcion(self): return self.genoma.get("percepcion", 1.0)
    @property
    def energia_maxima(self): return self.genoma.get("energia_maxima", 50.0)
    @property
    def eficiencia(self): return self.genoma.get("eficiencia", 1.0)

    def envejecer_y_metabolismo(self):
        """Puntos 3 y 8: Costo de vida y Muerte por edad."""
        if not self.viva: return

        self.edad += 1
        self.turnos_sin_comer += 1
        self.pasos_sobrevividos += 1

        # Muerte por Edad
        vida_max = parametros.VIDA_MAXIMA_PRESA if self.tipo == "presa" else parametros.VIDA_MAXIMA_DEPREDADOR
        # Pequeña variación genética en vida máxima
        vida_real = vida_max * (self.eficiencia) 
        if self.edad > vida_real:
            self.viva = False
            return

        # Costo Metabólico (Punto 3)
        gasto_basal = parametros.COSTO_EXISTENCIA
        gasto_cerebro = self.percepcion * parametros.FACTOR_GASTO_PERCEPCION
        gasto_musculo = self.velocidad * parametros.FACTOR_GASTO_VELOCIDAD
        
        gasto_total = (gasto_basal + gasto_cerebro + gasto_musculo) / self.eficiencia
        self.energia -= gasto_total

        if self.energia <= 0:
            self.viva = False

    def mover(self, mundo, destino_sugerido=None):
        """Punto 2: Movimiento afectado por biomas (Agua bloquea, Roca cuesta)."""
        if not self.viva: return

        filas, cols = mundo.tamano
        f_actual, c_actual = self.posicion
        
        # Determinar a dónde queremos ir
        if destino_sugerido:
             target_f, target_c = destino_sugerido
        else:
             # Movimiento aleatorio
             dist = max(1, int(self.velocidad))
             target_f = f_actual + random.randint(-dist, dist)
             target_c = c_actual + random.randint(-dist, dist)

        # Clampear límites
        target_f = max(0, min(filas - 1, target_f))
        target_c = max(0, min(cols - 1, target_c))
        
        # Verificar Terreno
        bioma_destino = mundo.biomas[target_f][target_c]
        
        if bioma_destino == parametros.BIOMA_AGUA:
            return # No se puede entrar al agua

        costo_terreno = 1.0
        if bioma_destino == parametros.BIOMA_ROCA:
            costo_terreno = 3.0 # Cuesta el triple moverse en rocas
        
        # Ejecutar movimiento
        self.posicion = (target_f, target_c)
        
        # Gasto de energía por movimiento
        gasto_mov = parametros.COSTO_MOVIMIENTO_BASE * costo_terreno * (self.velocidad / self.eficiencia)
        self.energia -= gasto_mov

    def ganar_energia(self, cantidad):
        self.energia += cantidad
        if self.energia > self.energia_maxima:
            self.energia = self.energia_maxima
        # Resetear hambre
        if cantidad > 1.0:
            self.turnos_sin_comer = 0

    def reproducir_sexual_base(self, pareja, costo_fraccion=0.3):
        """Lógica común de reproducción con costo energético."""
        costo_yo = self.energia_maxima * costo_fraccion
        costo_pareja = pareja.energia_maxima * costo_fraccion
        
        self.energia -= costo_yo
        pareja.energia -= costo_pareja
        
        energia_hijo = costo_yo + costo_pareja
        nuevo_gen = genetica.cruzar_genomas(self.genoma, pareja.genoma)
        nuevo_gen = genetica.mutar_genoma(nuevo_gen)
        
        return nuevo_gen, energia_hijo