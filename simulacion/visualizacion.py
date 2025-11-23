# ============================================
# visualizacion.py
# Visualización 2D con matplotlib y sprites
# ============================================
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from configuracion import parametros


class Visualizacion:
    def __init__(self, mundo):
        self.mundo = mundo
        self.filas, self.columnas = parametros.TAMANO_MUNDO

        # intenta cargar sprites (si no están, matplotlib fallará)
        try:
            self.img_conejo = mpimg.imread("assets/conejo.png")
            self.img_lobo = mpimg.imread("assets/lobo.png")
        except Exception:
            self.img_conejo = None
            self.img_lobo = None

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.set_xlim(0, self.columnas)
        self.ax.set_ylim(0, self.filas)
        self.ax.set_aspect("equal")
        self.ax.set_title("Ecosistema - Genoma completo")

    def dibujar(self):
        self.ax.clear()
        self.ax.set_xlim(0, self.columnas)
        self.ax.set_ylim(0, self.filas)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_aspect("equal")

        # dibujar presas
        for presa in self.mundo.presas:
            f, c = presa.posicion
            # extent = (x0, x1, y0, y1) con x=columnas (c), y=filas (f)
            if self.img_conejo is not None:
                self.ax.imshow(self.img_conejo, extent=(c, c + 1, f, f + 1), zorder=2)
            else:
                self.ax.scatter(c + 0.5, f + 0.5, s=80, marker='o', color='green', zorder=2)

            # barra de energia (normalizada)
            nivel = presa.energia / max(1.0, presa.energia_maxima)
            nivel = max(0.0, min(1.0, nivel))
            ancho = 0.8 * nivel
            fondo = Rectangle((c + 0.1, f + 0.95), 0.8, 0.08, color=(0.4, 0.4, 0.4), zorder=3)
            barra = Rectangle((c + 0.1, f + 0.95), ancho, 0.08, color=(0, 1, 0), zorder=4)
            self.ax.add_patch(fondo); self.ax.add_patch(barra)

        # dibujar depredadores
        for d in self.mundo.depredadores:
            f, c = d.posicion
            if self.img_lobo is not None:
                self.ax.imshow(self.img_lobo, extent=(c, c + 1, f, f + 1), zorder=2)
            else:
                self.ax.scatter(c + 0.5, f + 0.5, s=100, marker='s', color='red', zorder=2)

            nivel = d.energia / max(1.0, d.energia_maxima)
            nivel = max(0.0, min(1.0, nivel))
            ancho = 0.8 * nivel
            fondo = Rectangle((c + 0.1, f + 0.95), 0.8, 0.08, color=(0.4, 0.4, 0.4), zorder=3)
            barra = Rectangle((c + 0.1, f + 0.95), ancho, 0.08, color=(1, 0, 0), zorder=4)
            self.ax.add_patch(fondo); self.ax.add_patch(barra)

        plt.pause(1.0 / parametros.FPS)
