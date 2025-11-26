# ============================================
# simulacion/visualizacion.py
# ============================================
import pygame
from configuracion import parametros

CELDA = 12 # Celda un poco más chica para mapa grande

# Colores Biomas
C_AGUA = (50, 50, 200)
C_LLANURA = (154, 205, 50)
C_BOSQUE = (34, 139, 34)
C_ROCA = (120, 120, 120)

class Visualizacion:
    def __init__(self, mundo):
        self.mundo = mundo
        pygame.init()
        
        cols, filas = parametros.TAMANO_MUNDO[1], parametros.TAMANO_MUNDO[0]
        self.alto_hud = 60
        self.screen = pygame.display.set_mode((cols * CELDA, filas * CELDA + self.alto_hud))
        pygame.display.set_caption("EcoGen Complex")
        
        # Cargar assets
        self.usar_sprites = False
        try:
            raw_conejo = pygame.image.load("assets/conejo.png")
            raw_lobo = pygame.image.load("assets/lobo.png")
            self.img_conejo = pygame.transform.scale(raw_conejo, (CELDA, CELDA))
            self.img_lobo = pygame.transform.scale(raw_lobo, (CELDA, CELDA))
            self.usar_sprites = True
        except: pass

        self.reloj = pygame.time.Clock()
        self.font = pygame.font.SysFont("Consolas", 14)
        self.font_big = pygame.font.SysFont("Arial", 24, bold=True)
        self.pausado = False
        self.fps_actual = parametros.FPS

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: self.pausado = not self.pausado
                elif event.key == pygame.K_RIGHT: self.fps_actual += 5
                elif event.key == pygame.K_LEFT: self.fps_actual = max(1, self.fps_actual - 5)
        return True

    def dibujar(self, paso):
        # Dibujar Fondo (Biomas + Comida)
        filas, cols = self.mundo.tamano
        for f in range(filas):
            for c in range(cols):
                bio = self.mundo.biomas[f][c]
                comida = self.mundo.alimento[f][c]
                
                color_base = C_LLANURA
                if bio == parametros.BIOMA_AGUA: color_base = C_AGUA
                elif bio == parametros.BIOMA_BOSQUE: color_base = C_BOSQUE
                elif bio == parametros.BIOMA_ROCA: color_base = C_ROCA
                
                # Oscurecer si hay poca comida (solo en tierra)
                if bio != parametros.BIOMA_AGUA and bio != parametros.BIOMA_ROCA:
                    factor = 0.5 + (0.5 * (comida / parametros.MAX_COMIDA_CELDA))
                    color_final = (int(color_base[0]*factor), int(color_base[1]*factor), int(color_base[2]*factor))
                else:
                    color_final = color_base

                pygame.draw.rect(self.screen, color_final, (c*CELDA, f*CELDA, CELDA, CELDA))

        # Dibujar Entidades
        for e in self.mundo.presas + self.mundo.depredadores:
            if not e.viva: continue
            x, y = e.posicion[1] * CELDA, e.posicion[0] * CELDA
            if self.usar_sprites:
                img = self.img_conejo if e.tipo == "presa" else self.img_lobo
                self.screen.blit(img, (x, y))
            else:
                c = (200,200,200) if e.tipo == "presa" else (200,50,50)
                pygame.draw.circle(self.screen, c, (x+CELDA//2, y+CELDA//2), CELDA//2-1)

        # HUD
        pygame.draw.rect(self.screen, (20,20,20), (0, filas*CELDA, self.screen.get_width(), self.alto_hud))
        
        info1 = f"Población: Presas {len(self.mundo.presas)} | Lobos {len(self.mundo.depredadores)} | FPS: {self.fps_actual}"
        info2 = f"Estación: {self.mundo.estacion} | Evento: {self.mundo.evento_actual} | Paso: {paso}"
        
        t1 = self.font.render(info1, True, (255,255,255))
        t2 = self.font.render(info2, True, (255,200,100) if self.mundo.evento_actual != "NINGUNO" else (200,200,200))
        
        self.screen.blit(t1, (10, filas*CELDA + 5))
        self.screen.blit(t2, (10, filas*CELDA + 25))

        if self.pausado:
            tp = self.font_big.render("PAUSA", True, (255,0,0))
            self.screen.blit(tp, (self.screen.get_width()//2 - 40, filas*CELDA + 15))

        pygame.display.flip()
        self.reloj.tick(self.fps_actual)