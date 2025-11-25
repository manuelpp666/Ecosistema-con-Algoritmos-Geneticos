# ============================================
# simulacion/visualizacion.py
# ============================================
import pygame
from configuracion import parametros

# Configuración Visual
CELDA = 15  # Tamaño en pixeles de cada celda
COLOR_TIERRA = (100, 70, 40)
COLOR_HIERBA = (34, 139, 34)

class Visualizacion:
    def __init__(self, mundo):
        self.mundo = mundo
        pygame.init()
        
        cols, filas = parametros.TAMANO_MUNDO[1], parametros.TAMANO_MUNDO[0]
        self.screen = pygame.display.set_mode((cols * CELDA, filas * CELDA))
        pygame.display.set_caption("Ecosistema Genético")
        
        # Cargar imágenes si existen
        self.usar_sprites = False
        try:
            self.img_conejo = pygame.transform.scale(pygame.image.load("assets/conejo.png"), (CELDA, CELDA))
            self.img_lobo = pygame.transform.scale(pygame.image.load("assets/lobo.png"), (CELDA, CELDA))
            self.usar_sprites = True
        except:
            print("Sprites no encontrados, usando circulos.")

        self.reloj = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 14)

    def dibujar(self):
        # Manejar cierre de ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        self.screen.fill(COLOR_TIERRA)

        # Dibujar Hierba
        filas, cols = self.mundo.tamano
        for f in range(filas):
            for c in range(cols):
                nivel = self.mundo.hierba[f][c]
                if nivel > 0.1:
                    # Interpolación de color
                    color = [int(COLOR_TIERRA[i] + (COLOR_HIERBA[i]-COLOR_TIERRA[i])*nivel) for i in range(3)]
                    pygame.draw.rect(self.screen, color, (c*CELDA, f*CELDA, CELDA, CELDA))

        # Dibujar Entidades
        for entidad in self.mundo.todas_las_entidades():
            if not entidad.viva: continue
            x, y = entidad.posicion[1] * CELDA, entidad.posicion[0] * CELDA
            
            if self.usar_sprites:
                img = self.img_conejo if entidad.tipo == "presa" else self.img_lobo
                self.screen.blit(img, (x, y))
            else:
                color = (200, 200, 200) if entidad.tipo == "presa" else (200, 50, 50)
                pygame.draw.circle(self.screen, color, (x+CELDA//2, y+CELDA//2), CELDA//2 - 1)

        # Estadísticas
        info = f"Presas: {len(self.mundo.presas)} | Depredadores: {len(self.mundo.depredadores)}"
        text = self.font.render(info, True, (255, 255, 255))
        pygame.draw.rect(self.screen, (0,0,0), (0,0, self.screen.get_width(), 20))
        self.screen.blit(text, (5, 2))

        pygame.display.flip()
        self.reloj.tick(30) # 30 FPS objetivo
        return True