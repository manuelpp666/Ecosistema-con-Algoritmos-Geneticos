# ============================================
# simulacion/visualizacion.py
# ============================================
import pygame
import random
from configuracion import parametros

CELDA = 14  # Tamaño perfecto para sprites bonitos y mapa visible

# Paleta de colores profesional y viva
C_AGUA = (25, 90, 170)
C_LLANURA = (170, 215, 100)
C_BOSQUE = (15, 100, 45)
C_ROCA = (85, 85, 85)
C_TIERRA_MUERTA = (120, 90, 60)

class Visualizacion:
    def __init__(self, mundo):
        self.mundo = mundo
        pygame.init()
        pygame.display.set_caption("EcoGen Complex - Evolución Natural")

        filas, cols = parametros.TAMANO_MUNDO
        self.alto_hud = 80
        self.ancho = cols * CELDA
        self.alto = filas * CELDA + self.alto_hud

        self.screen = pygame.display.set_mode((self.ancho, self.alto))
        self.reloj = pygame.time.Clock()

        # Fuentes
        self.font = pygame.font.SysFont("Consolas", 15)
        self.font_big = pygame.font.SysFont("Arial Black", 32)
        self.font_small = pygame.font.SysFont("Arial", 13)

        # Cargar sprites (tus archivos)
        self.sprites_rabbit = self.cargar_sprites("assets/rabbit.png", 4)
        self.sprites_dog = self.cargar_sprites("assets/dog.png", 4)

        self.usar_animacion = self.sprites_rabbit is not None and self.sprites_dog is not None

        # Fallback si no hay sprites con 4 direcciones
        if not self.usar_animacion:
            try:
                self.img_rabbit = pygame.transform.scale(pygame.image.load("assets/rabbit.png").convert_alpha(), (CELDA, CELDA))
                self.img_dog = pygame.transform.scale(pygame.image.load("assets/dog.png").convert_alpha(), (CELDA, CELDA))
                self.usar_sprites = True
            except:
                self.usar_sprites = False
        else:
            self.usar_sprites = False

        self.pausado = False
        self.fps_objetivo = parametros.FPS
        self.paso_global = 0

    def cargar_sprites(self, ruta, frames):
        """Intenta cargar un sprite sheet horizontal con N frames"""
        try:
            sheet = pygame.image.load(ruta).convert_alpha()
            w, h = sheet.get_size()
            if w < h * frames:  # probablemente no es un sheet horizontal
                return None
            frame_ancho = w // frames
            lista = []
            for i in range(frames):
                frame = sheet.subsurface(pygame.Rect(i * frame_ancho, 0, frame_ancho, h))
                frame = pygame.transform.scale(frame, (CELDA, CELDA))
                lista.append(frame)
            return lista
        except Exception as e:
            print(f"No se pudo cargar {ruta} como animación: {e}")
            return None

    def manejar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pausado = not self.pausado
                elif event.key == pygame.K_RIGHT:
                    self.fps_objetivo = min(300, self.fps_objetivo + 10)
                elif event.key == pygame.K_LEFT:
                    self.fps_objetivo = max(1, self.fps_objetivo - 10)
                elif event.key == pygame.K_r:
                    self.paso_global = 0  # reiniciar contador visual
        return True

    def dibujar(self, paso):
        self.paso_global = paso
        filas, cols = self.mundo.tamano

        # === FONDO: BIOMAS + COMIDA VISUAL ===
        for f in range(filas):
            for c in range(cols):
                bio = self.mundo.biomas[f][c]
                comida = self.mundo.alimento[f][c]
                max_comida = parametros.MAX_COMIDA_CELDA

                # Color base del bioma
                if bio == parametros.BIOMA_AGUA:
                    color = C_AGUA
                elif bio == parametros.BIOMA_ROCA:
                    color = C_ROCA
                elif bio == parametros.BIOMA_BOSQUE:
                    color = C_BOSQUE
                else:
                    color = C_LLANURA

                # Efecto de fertilidad/comida (solo en tierra)
                if bio not in [parametros.BIOMA_AGUA, parametros.BIOMA_ROCA]:
                    factor = comida / max_comida
                    if factor < 0.2:
                        color = C_TIERRA_MUERTA
                    else:
                        color = (
                            int(color[0] * (0.7 + 0.4 * factor)),
                            int(color[1] * (0.8 + 0.3 * factor)),
                            int(color[2] * (0.7 + 0.4 * factor)),
                        )

                pygame.draw.rect(self.screen, color, (c * CELDA, f * CELDA, CELDA, CELDA))

        # === ENTIDADES ===
        for entidad in self.mundo.presas + self.mundo.depredadores:
            if not entidad.viva:
                continue

            x = entidad.posicion[1] * CELDA
            y = entidad.posicion[0] * CELDA

            # Determinar frame de animación y dirección
            moviendose = hasattr(entidad, 'velocidad') and entidad.velocidad > 0
            frame_idx = (paso // 10) % 4 if moviendose else 0

            # Dirección (si el objeto guarda última dirección)
            if hasattr(entidad, 'ultima_direccion') and entidad.ultima_direccion != (0, 0):
                dx, dy = entidad.ultima_direccion
                if abs(dx) > abs(dy):
                    dir_idx = 1 if dx > 0 else 3
                else:
                    dir_idx = 0 if dy < 0 else 2
            else:
                dir_idx = 1  # mirando a la derecha por defecto

            # Dibujar sprite
            if self.usar_animacion:
                imgs = self.sprites_rabbit if entidad.tipo == "presa" else self.sprites_dog
                img = imgs[dir_idx] if len(imgs) > dir_idx else imgs[0]
                if moviendose and frame_idx > 0:
                    img = imgs[frame_idx % len(imgs)]
                self.screen.blit(img, (x, y))
            elif self.usar_sprites:
                img = self.img_rabbit if entidad.tipo == "presa" else self.img_dog
                self.screen.blit(img, (x, y))
            else:
                # Círculos bonitos con borde de energía
                centro = (x + CELDA//2, y + CELDA//2)
                radio = CELDA//2 - 2
                color_base = (255, 240, 200) if entidad.tipo == "presa" else (220, 80, 80)
                pygame.draw.circle(self.screen, color_base, centro, radio)

                # Borde de energía
                energia_por = entidad.energia / entidad.energia_max
                if energia_por > 0.6:
                    color_energia = (100, 255, 100)
                elif energia_por > 0.3:
                    color_energia = (255, 200, 50)
                else:
                    color_energia = (255, 50, 50)
                pygame.draw.circle(self.screen, color_energia, centro, radio, 3)

        # === EFECTOS CLIMÁTICOS ===
        overlay = pygame.Surface((self.ancho, filas * CELDA), pygame.SRCALPHA)

        if self.mundo.estacion == "INVIERNO":
            overlay.fill((220, 240, 255, 25))
            for _ in range(6):
                sx = random.randint(0, self.ancho)
                sy = random.randint(0, filas * CELDA // 2)
                pygame.draw.circle(overlay, (255, 255, 255, 200), (sx, sy), random.randint(1, 3))

        elif self.mundo.evento_actual == "SEQUIA":
            overlay.fill((220, 150, 60, 30))

        elif self.mundo.evento_actual == "PLAGA":
            for _ in range(20):
                px = random.randint(0, self.ancho)
                py = random.randint(0, filas * CELDA)
                pygame.draw.circle(overlay, (150, 255, 100, 120), (px, py), random.randint(5, 12))

        elif self.mundo.evento_actual == "FRIO_EXTREMO":
            overlay.fill((180, 200, 255, 40))

        self.screen.blit(overlay, (0, 0))

        # === HUD PROFESIONAL ===
        hud_y = filas * CELDA
        pygame.draw.rect(self.screen, (10, 15, 35), (0, hud_y, self.ancho, self.alto_hud))
        pygame.draw.line(self.screen, (80, 180, 255), (0, hud_y), (self.ancho, hud_y), 4)

        presas = len([p for p in self.mundo.presas if p.viva])
        depredadores = len([d for d in self.mundo.depredadores if d.viva])
        total = presas + depredadores
        ratio = depredadores / presas if presas > 0 else 0

        textos = [
            f"Paso: {paso:,}   |   FPS: {int(self.reloj.get_fps())} / {self.fps_objetivo}",
            f"Presas: {presas:,}     Depredadores: {depredadores:,}     Ratio D/P: {ratio:.3f}",
            f"Estación: {self.mundo.estacion}     Evento actual: {self.mundo.evento_actual}",
        ]

        for i, texto in enumerate(textos):
            color = (100, 220, 255) if i == 0 else (180, 255, 180) if i == 1 else (255, 180, 100) if self.mundo.evento_actual != "NINGUNO" else (200, 200, 220)
            surf = self.font.render(texto, True, color)
            self.screen.blit(surf, (15, hud_y + 10 + i * 20))

        

        # PAUSA grande y bonita
        if self.pausado:
            s = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.screen.blit(s, (0, 0))
            txt = self.font_big.render("||  PAUSADO  ||", True, (255, 50, 50))
            self.screen.blit(txt, (self.ancho//2 - txt.get_width()//2, self.alto//2 - 30))

        pygame.display.flip()
        self.reloj.tick(self.fps_objetivo)