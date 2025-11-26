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

    paso = 0
    corriendo = True

    print("=== ECOSYSTEM COMPLEX ===")
    print("Controles: [ESPACIO] Pausa, [FLECHAS] Velocidad")

    while corriendo:
        corriendo = vis.manejar_eventos()
        
        if not vis.pausado:
            motor.ejecutar_paso()
            paso += 1
            
            # Chequeo de seguridad anti-crash
            if len(mundo.presas) == 0 and len(mundo.depredadores) == 0:
                print("Mundo vacío.")
                vis.pausado = True

        vis.dibujar(paso)

if __name__ == "__main__":
    main()