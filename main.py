# ============================================
# main.py
# ============================================
from simulacion.motor import MotorSimulacion
from simulacion.visualizacion import Visualizacion
from nucleo.mundo import Mundo
from configuracion import parametros

def main():
    mundo = Mundo()
    motor = MotorSimulacion(mundo)
    vis = Visualizacion(mundo)

    pasos_totales = parametros.PASOS_POR_GENERACION * parametros.GENERACIONES
    corriendo = True
    paso = 0

    print("Iniciando simulación. Cierra la ventana gráfica para detener.")

    while corriendo and paso < pasos_totales:
        paso += 1
        motor.ejecutar_paso()
        
        # Dibujar retorna False si el usuario cierra la ventana
        corriendo = vis.dibujar()

        if len(mundo.presas) == 0 and len(mundo.depredadores) == 0:
            print("Extinción total.")
            break

    print("Fin de la simulación.")

if __name__ == "__main__":
    main()