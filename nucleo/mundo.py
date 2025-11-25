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
        
        # Grid para búsquedas rápidas: Clave=(f,c), Valor=[entidades]
        self.grid = {}
        
        # Matriz de hierba (0.0 a 1.0)
        filas, cols = self.tamano
        self.hierba = [[1.0 for _ in range(cols)] for _ in range(filas)]

        self.crear_poblacion_inicial()
        self.actualizar_grid()

    def crear_poblacion_inicial(self):
        # Presas
        for _ in range(parametros.POBLACION_INICIAL_PRESAS):
            pos = self.posicion_aleatoria()
            gen = genetica.crear_genoma_aleatorio()
            gen["agresividad"] = 0.0
            self.presas.append(Presa(pos, gen))

        # Depredadores
        for _ in range(parametros.POBLACION_INICIAL_DEPREDADORES):
            pos = self.posicion_aleatoria()
            gen = genetica.crear_genoma_aleatorio()
            self.depredadores.append(Depredador(pos, gen))

    def posicion_aleatoria(self):
        filas, cols = self.tamano
        return (random.randint(0, filas - 1), random.randint(0, cols - 1))

    def todas_las_entidades(self):
        return self.presas + self.depredadores

    def actualizar_grid(self):
        """Reconstruye el mapa espacial de entidades."""
        self.grid = {}
        for entidad in self.todas_las_entidades():
            if not entidad.viva: continue
            pos = entidad.posicion
            if pos not in self.grid:
                self.grid[pos] = []
            self.grid[pos].append(entidad)

    def obtener_entidades_en_rango(self, posicion, radio):
        """Devuelve entidades en celdas vecinas segun radio de percepcion."""
        f, c = posicion
        entidades_cercanas = []
        # Optimización: radio 1 revisa 3x3, radio 2 revisa 5x5...
        rango = int(radio) + 1 
        filas_mundo, cols_mundo = self.tamano

        for df in range(-rango, rango + 1):
            for dc in range(-rango, rango + 1):
                nf, nc = f + df, c + dc
                if 0 <= nf < filas_mundo and 0 <= nc < cols_mundo:
                    if (nf, nc) in self.grid:
                        entidades_cercanas.extend(self.grid[(nf, nc)])
        return entidades_cercanas

    def gestionar_hierba(self):
        """Crece la hierba en todo el mundo."""
        filas, cols = self.tamano
        tasa_crecimiento = 0.02 # Ajustable
        for f in range(filas):
            for c in range(cols):
                if self.hierba[f][c] < 1.0:
                    self.hierba[f][c] = min(1.0, self.hierba[f][c] + tasa_crecimiento)

    def consumir_hierba(self, posicion):
        f, c = posicion
        cantidad = self.hierba[f][c]
        consumido = 0
        if cantidad > 0.1:
            consumido = cantidad
            self.hierba[f][c] = 0.0 # Se la come toda
        return consumido

    def ejecutar_turno(self):
        self.actualizar_grid()
        self.gestionar_hierba()
        
        nacidos = []

        # Turno Presas
        for presa in list(self.presas):
            vecinos = self.obtener_entidades_en_rango(presa.posicion, presa.percepcion)
            hijo = presa.elegir_accion(self, vecinos)
            if hijo: nacidos.append(hijo)
            presa.registrar_paso()

        # Turno Depredadores
        for dep in list(self.depredadores):
            vecinos = self.obtener_entidades_en_rango(dep.posicion, dep.percepcion)
            hijo = dep.elegir_accion(self, vecinos)
            if hijo: nacidos.append(hijo)
            dep.registrar_paso()
            
            # Comer presas en la misma celda
            en_casilla = self.grid.get(dep.posicion, [])
            presas_aqui = [e for e in en_casilla if e.tipo == "presa" and e.viva]
            dep.intentar_comer(presas_aqui)

        # Añadir nacidos
        for n in nacidos:
            if n.tipo == "presa": self.presas.append(n)
            else: self.depredadores.append(n)

        self.limpiar_muertos()

    def limpiar_muertos(self):
        self.presas = [p for p in self.presas if p.viva]
        self.depredadores = [d for d in self.depredadores if d.viva]