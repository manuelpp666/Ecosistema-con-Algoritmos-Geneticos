# ============================================
# nucleo/mundo.py
# ============================================
import random
import math
from configuracion import parametros
from nucleo.depredador import Depredador
from nucleo.presa import Presa
from nucleo import genetica

class Mundo:
    def __init__(self):
        self.tamano = parametros.TAMANO_MUNDO
        self.presas = []
        self.depredadores = []
        self.grid = {}
        
        # Estado Global
        self.turno_global = 0
        self.estacion = "VERANO" # VERANO / INVIERNO
        self.evento_actual = "NINGUNO" # SEQUIA, PLAGA, FRIO
        
        # Inicializar Mapas
        self.generar_biomas()
        self.generar_alimento()
        
        self.crear_poblacion_inicial()
        self.actualizar_grid()

    def generar_biomas(self):
        """Genera parches de biomas usando 'manchas' aleatorias."""
        filas, cols = self.tamano
        self.biomas = [[parametros.BIOMA_AGUA for _ in range(cols)] for _ in range(filas)]
        
        # Llenar todo de Llanura primero
        for f in range(filas):
            for c in range(cols):
                self.biomas[f][c] = parametros.BIOMA_LLANURA

        # Crear manchas de Bosque
        for _ in range(15):
            cf, cc = self.posicion_aleatoria()
            radio = random.randint(3, 8)
            for f in range(cf-radio, cf+radio):
                for c in range(cc-radio, cc+radio):
                    if 0 <= f < filas and 0 <= c < cols:
                        if random.random() < 0.7: # Ruido
                            self.biomas[f][c] = parametros.BIOMA_BOSQUE

        # Crear manchas de Roca
        for _ in range(8):
            cf, cc = self.posicion_aleatoria()
            radio = random.randint(2, 5)
            for f in range(cf-radio, cf+radio):
                for c in range(cc-radio, cc+radio):
                    if 0 <= f < filas and 0 <= c < cols:
                        self.biomas[f][c] = parametros.BIOMA_ROCA

        # Crear Ríos/Lagos (Agua)
        for _ in range(5):
            cf, cc = self.posicion_aleatoria()
            radio = random.randint(2, 6)
            for f in range(cf-radio, cf+radio):
                for c in range(cc-radio, cc+radio):
                    if 0 <= f < filas and 0 <= c < cols:
                         self.biomas[f][c] = parametros.BIOMA_AGUA

    def generar_alimento(self):
        filas, cols = self.tamano
        # Matriz de floats: cantidad de comida 0 a MAX_COMIDA_CELDA
        self.alimento = [[0.0 for _ in range(cols)] for _ in range(filas)]
        for f in range(filas):
            for c in range(cols):
                bio = self.biomas[f][c]
                if bio == parametros.BIOMA_AGUA or bio == parametros.BIOMA_ROCA:
                    self.alimento[f][c] = 0.0
                elif bio == parametros.BIOMA_BOSQUE:
                    self.alimento[f][c] = parametros.MAX_COMIDA_CELDA # Empieza lleno
                else:
                    self.alimento[f][c] = parametros.MAX_COMIDA_CELDA * 0.5

    def ciclo_climatico(self):
        # 1. Control de Estaciones
        ciclo = self.turno_global % (parametros.DURACION_ESTACION * 2)
        if ciclo < parametros.DURACION_ESTACION:
            self.estacion = "VERANO"
        else:
            self.estacion = "INVIERNO"

        # 2. Eventos Aleatorios
        self.evento_actual = "NINGUNO"
        if self.turno_global % parametros.CICLO_EVENTOS == 0 and random.random() < 0.3:
            eventos = ["SEQUIA", "PLAGA", "FRIO_EXTREMO"]
            self.evento_actual = random.choice(eventos)

    def regenerar_recursos(self):
        """Regeneración mejorada para evitar hambrunas."""
        filas, cols = self.tamano
        
        factor_estacion = 1.0 if self.estacion == "VERANO" else 0.5 # Invierno menos duro (0.5 vs 0.4)
        if self.evento_actual == "SEQUIA": factor_estacion *= 0.3 # Sequía menos mortal
        if self.evento_actual == "FRIO_EXTREMO": factor_estacion *= 0.2

        for f in range(filas):
            for c in range(cols):
                bio = self.biomas[f][c]
                if bio == parametros.BIOMA_AGUA or bio == parametros.BIOMA_ROCA:
                    continue
                
                # FÓRMULA MEJORADA:
                # Base 0.2 en lugar de 0.1
                tasa = parametros.REGENERACION_BASE * 0.2
                
                if bio == parametros.BIOMA_BOSQUE: tasa *= 2.0 # El bosque produce doble
                if bio == parametros.BIOMA_LLANURA: tasa *= 1.0
                
                if self.evento_actual == "PLAGA" and random.random() < 0.05:
                    self.alimento[f][c] = max(0, self.alimento[f][c] - 2.0)
                    continue

                crecimiento = tasa * factor_estacion
                self.alimento[f][c] = min(parametros.MAX_COMIDA_CELDA, self.alimento[f][c] + crecimiento)

    def consumir_alimento(self, pos, cantidad_deseada):
        f, c = pos
        disponible = self.alimento[f][c]
        tomar = min(disponible, cantidad_deseada)
        self.alimento[f][c] -= tomar
        return tomar

    def aplicar_penalizacion_hacinamiento(self):
        """Si hay sobrepoblación local, se desata una plaga mortal."""
        for pos, entidades in self.grid.items():
            # Filtramos solo presas para contar hacinamiento
            presas_aqui = [e for e in entidades if e.tipo == "presa"]
            
            # Si hay más de X presas en la misma casilla...
            if len(presas_aqui) > parametros.DENSIDAD_ENFERMEDAD:
                for p in presas_aqui:
                    # Probabilidad alta (30%) de daño masivo
                    if random.random() < 0.3:
                        p.energia -= 15  # Golpe duro a la salud
                        # Contagio: puede matar al instante si está débil
                        if p.energia <= 0:
                            p.viva = False

    def posicion_aleatoria(self):
        # Asegurar que no nazcan en AGUA
        while True:
            f = random.randint(0, self.tamano[0] - 1)
            c = random.randint(0, self.tamano[1] - 1)
            if self.biomas[f][c] != parametros.BIOMA_AGUA:
                return (f, c)

    def crear_poblacion_inicial(self):
        for _ in range(parametros.POBLACION_INICIAL_PRESAS):
            self.presas.append(Presa(self.posicion_aleatoria(), genetica.crear_genoma_aleatorio()))
        for _ in range(parametros.POBLACION_INICIAL_DEPREDADORES):
            self.depredadores.append(Depredador(self.posicion_aleatoria(), genetica.crear_genoma_aleatorio()))

    def actualizar_grid(self):
        self.grid = {}
        for e in self.presas + self.depredadores:
            if not e.viva: continue
            if e.posicion not in self.grid: self.grid[e.posicion] = []
            self.grid[e.posicion].append(e)

    def obtener_entidades_cercanas(self, pos, radio):
        # (Misma lógica optimizada anterior)
        entidades = []
        rango = int(radio) + 1
        f, c = pos
        for df in range(-rango, rango + 1):
            for dc in range(-rango, rango + 1):
                nf, nc = f + df, c + dc
                if (nf, nc) in self.grid:
                    entidades.extend(self.grid[(nf, nc)])
        return entidades

    def ejecutar_turno(self):
        self.turno_global += 1
        self.ciclo_climatico()
        self.regenerar_recursos()
        self.actualizar_grid()
        self.aplicar_penalizacion_hacinamiento()

        nacidos = []
        
        # Turno Presas
        for p in list(self.presas):
            vecinos = self.obtener_entidades_cercanas(p.posicion, p.percepcion)
            hijo = p.actuar(self, vecinos)
            if hijo: nacidos.append(hijo)
        
        # Turno Depredadores
        for d in list(self.depredadores):
            vecinos = self.obtener_entidades_cercanas(d.posicion, d.percepcion)
            hijo = d.actuar(self, vecinos)
            if hijo: nacidos.append(hijo)
            
            # Intentar comer
            if d.viva:
                presas_aqui = [x for x in self.grid.get(d.posicion, []) if x.tipo == "presa" and x.viva]
                d.intentar_comer(presas_aqui)

        # Añadir nacidos
        for n in nacidos:
            if n.tipo == "presa": self.presas.append(n)
            else: self.depredadores.append(n)

        # Limpiar muertos
        self.presas = [p for p in self.presas if p.viva]
        self.depredadores = [d for d in self.depredadores if d.viva]