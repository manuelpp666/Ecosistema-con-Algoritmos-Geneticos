# ============================================
# nucleo/mundo.py
# ============================================
import random
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
        self.turno_global = 0
        self.estacion = "VERANO"
        self.evento_actual = "NINGUNO"
        
        self.generar_biomas()
        self.generar_alimento()
        self.crear_poblacion_inicial()
        self.actualizar_grid()

    def generar_biomas(self):
        filas, cols = self.tamano
        self.biomas = [[parametros.BIOMA_LLANURA for _ in range(cols)] for _ in range(filas)]
        for _ in range(12): # Bosques
            cf, cc = self.rnd_pos()
            r = random.randint(3, 7)
            for f in range(cf-r, cf+r):
                for c in range(cc-r, cc+r):
                    if 0<=f<filas and 0<=c<cols and random.random()<0.7: self.biomas[f][c] = parametros.BIOMA_BOSQUE
        for _ in range(6): # Rocas
            cf, cc = self.rnd_pos()
            r = random.randint(2, 4)
            for f in range(cf-r, cf+r):
                for c in range(cc-r, cc+r):
                    if 0<=f<filas and 0<=c<cols: self.biomas[f][c] = parametros.BIOMA_ROCA
        for _ in range(5): # Agua
            cf, cc = self.rnd_pos()
            r = random.randint(2, 5)
            for f in range(cf-r, cf+r):
                for c in range(cc-r, cc+r):
                    if 0<=f<filas and 0<=c<cols: self.biomas[f][c] = parametros.BIOMA_AGUA

    def generar_alimento(self):
        f, c = self.tamano
        self.alimento = [[parametros.MAX_COMIDA_CELDA * 0.5 for _ in range(c)] for _ in range(f)]
        for i in range(f):
            for j in range(c):
                if self.biomas[i][j] == parametros.BIOMA_BOSQUE: self.alimento[i][j] = parametros.MAX_COMIDA_CELDA
                if self.biomas[i][j] in [parametros.BIOMA_AGUA, parametros.BIOMA_ROCA]: self.alimento[i][j] = 0

    def ciclo_climatico(self):
        self.turno_global += 1
        ciclo = self.turno_global % (parametros.DURACION_ESTACION * 2)
        self.estacion = "VERANO" if ciclo < parametros.DURACION_ESTACION else "INVIERNO"
        self.evento_actual = "NINGUNO"
        if self.turno_global % parametros.CICLO_EVENTOS == 0 and random.random() < 0.3:
            self.evento_actual = random.choice(["SEQUIA", "PLAGA", "FRIO_EXTREMO"])

    def regenerar_recursos(self):
        filas, cols = self.tamano
        factor = 1.0 if self.estacion == "VERANO" else 0.5
        if self.evento_actual == "SEQUIA": factor *= 0.3
        for f in range(filas):
            for c in range(cols):
                bio = self.biomas[f][c]
                if bio in [parametros.BIOMA_AGUA, parametros.BIOMA_ROCA]: continue
                tasa = parametros.REGENERACION_BASE * 0.2
                if bio == parametros.BIOMA_BOSQUE: tasa *= 2.0
                self.alimento[f][c] = min(parametros.MAX_COMIDA_CELDA, self.alimento[f][c] + tasa * factor)

    def consumir_alimento(self, pos, cant):
        f, c = pos
        tomar = min(self.alimento[f][c], cant)
        self.alimento[f][c] -= tomar
        return tomar

    def rnd_pos(self): return (random.randint(0, self.tamano[0]-1), random.randint(0, self.tamano[1]-1))
    def posicion_aleatoria(self):
        while True:
            f, c = self.rnd_pos()
            if self.biomas[f][c] != parametros.BIOMA_AGUA: return (f, c)

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

    def obtener_vecinos(self, pos, radio):
        ents = []
        r = int(radio) + 1
        f, c = pos
        for df in range(-r, r+1):
            for dc in range(-r, r+1):
                nf, nc = f+df, c+dc
                if (nf, nc) in self.grid: ents.extend(self.grid[(nf, nc)])
        return ents

    def ejecutar_turno(self):
        self.ciclo_climatico()
        self.regenerar_recursos()
        self.actualizar_grid()
        
        # Hacinamiento / Enfermedad
        for pos, ents in self.grid.items():
            presas = [e for e in ents if e.tipo == "presa"]
            if len(presas) > parametros.DENSIDAD_ENFERMEDAD:
                for p in presas:
                    if random.random() < 0.3: p.energia -= 15; 
                    if p.energia<=0: p.viva=False

        nacidos = []
        for p in list(self.presas):
            hijo = p.actuar(self, self.obtener_vecinos(p.posicion, p.percepcion))
            if hijo: nacidos.append(hijo)
        
        for d in list(self.depredadores):
            hijo = d.actuar(self, self.obtener_vecinos(d.posicion, d.percepcion))
            if hijo: nacidos.append(hijo)
            if d.viva:
                presas_aqui = [x for x in self.grid.get(d.posicion, []) if x.tipo == "presa" and x.viva]
                d.intentar_comer(presas_aqui)

        for n in nacidos:
            if n.tipo == "presa": self.presas.append(n)
            else: self.depredadores.append(n)

        self.presas = [p for p in self.presas if p.viva]
        self.depredadores = [d for d in self.depredadores if d.viva]