# ============================================
# main.py
# Ejecutar la simulación
# ============================================

from simulacion.motor import MotorSimulacion
from simulacion.visualizacion import Visualizacion
from nucleo.mundo import Mundo
from configuracion import parametros
import matplotlib.pyplot as plt

def main():
    mundo = Mundo()
    motor = MotorSimulacion(mundo)
    vis = Visualizacion(mundo)

    pasos_totales = parametros.PASOS_POR_GENERACION * parametros.GENERACIONES

    plt.ion()
    for paso in range(1, pasos_totales + 1):
        motor.ejecutar_paso()
        vis.dibujar()

        # si la población se extingue, terminar
        if len(mundo.presas) == 0 or len(mundo.depredadores) == 0:
            print("Población extinguida. Fin de la simulación en paso", paso)
            break

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()
