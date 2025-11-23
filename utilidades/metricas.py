# ============================================
# metricas.py
# Cálculo de métricas durante la simulación
# ============================================

def promedio(lista):
    """
    Devuelve el promedio de una lista numérica.
    Si la lista está vacía, devuelve 0.
    """
    if not lista:
        return 0
    return sum(lista) / len(lista)

def metricas_poblacion(entidades):
    """
    Calcula métricas básicas de un conjunto de entidades.
    Retorna un diccionario con promedios.
    """
    energias = [e.energia for e in entidades]
    velocidades = [e.genes["velocidad"] for e in entidades]
    percepciones = [e.genes["percepcion"] for e in entidades]

    return {
        "prom_energia": promedio(energias),
        "prom_velocidad": promedio(velocidades),
        "prom_percepcion": promedio(percepciones),
        "cantidad": len(entidades)
    }

def imprimir_metricas(nombre_grupo, metricas):
    """
    Imprime métricas con formato bonito.
    """
    print(f"\n--- MÉTRICAS {nombre_grupo.upper()} ---")
    print(f"Cantidad: {metricas['cantidad']}")
    print(f"Promedio energía: {metricas['prom_energia']:.2f}")
    print(f"Promedio velocidad: {metricas['prom_velocidad']:.2f}")
    print(f"Promedio percepción: {metricas['prom_percepcion']:.2f}")
