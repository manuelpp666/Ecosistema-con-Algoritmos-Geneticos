# ============================================
# registro.py
# Registro y métricas de la simulación
# ============================================

import csv
import os

class Registro:
    def __init__(self, ruta_archivo="resultados_simulacion.csv"):
        self.ruta_archivo = ruta_archivo
        self.datos = []
        if not os.path.exists(self.ruta_archivo):
            with open(self.ruta_archivo, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow([
                    "Paso",
                    "Cantidad_Presas",
                    "Cantidad_Depredadores",
                    "Vel_Presa",
                    "Vel_Depredador",
                    "Perc_Presa",
                    "Perc_Depredador",
                    "Energia_Promedio_Presas",
                    "Energia_Promedio_Depredadores"
                ])

    def registrar_generacion(self, numero, presas, depredadores):
        if presas:
            vel_p = sum(p.genoma["velocidad"] for p in presas) / len(presas)
            perc_p = sum(p.genoma["percepcion"] for p in presas) / len(presas)
            ener_p = sum(p.energia for p in presas) / len(presas)
        else:
            vel_p = perc_p = ener_p = 0

        if depredadores:
            vel_d = sum(d.genoma["velocidad"] for d in depredadores) / len(depredadores)
            perc_d = sum(d.genoma["percepcion"] for d in depredadores) / len(depredadores)
            ener_d = sum(d.energia for d in depredadores) / len(depredadores)
        else:
            vel_d = perc_d = ener_d = 0

        fila = [
            numero,
            len(presas),
            len(depredadores),
            round(vel_p, 2),
            round(vel_d, 2),
            round(perc_p, 2),
            round(perc_d, 2),
            round(ener_p, 2),
            round(ener_d, 2),
        ]
        self.datos.append(fila)
        with open(self.ruta_archivo, "a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(fila)

        print(f"Paso {numero}: Presas={len(presas)} Depredadores={len(depredadores)} VelP={vel_p:.2f} VelD={vel_d:.2f}")
