# ============================================
# simulacion/motor.py
# ============================================

from simulacion import registro

class MotorSimulacion:
    def __init__(self, mundo):
        self.mundo = mundo
        self.paso_actual = 0
        self.registro = registro.Registro()

    def ejecutar_paso(self):
        self.paso_actual += 1
        
        # Ahora toda la lógica (movimiento, comer, reproducirse, morir)
        # ocurre dentro del método ejecutar_turno() de la clase Mundo.
        self.mundo.ejecutar_turno()
        
        # Registrar estadísticas
        self.registro.registrar_generacion(
            self.paso_actual, 
            self.mundo.presas, 
            self.mundo.depredadores
        )