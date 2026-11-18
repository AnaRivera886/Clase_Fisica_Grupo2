"""
Línea base — Equipo 2: Concurrencia y procesamiento de tareas.

Situación inicial: el servicio de la empresa atiende una cola de tareas de
UNA EN UNA (secuencial). Hay dos tipos de tarea:
  * "es"  (entrada/salida): consultar un servicio externo. El procesador casi
          no trabaja: ESPERA la respuesta (simulado con time.sleep).
  * "cpu" (cómputo): calcular una huella criptográfica. El procesador trabaja
          todo el tiempo.

preparar(n) -> lista de n tareas mezcladas (proporción configurable)
ejecutar(tareas) -> número de tareas completadas
"""
import hashlib
import random
import time

LATENCIA_S = (0.02, 0.06)     # latencia simulada de la red/servicio externo
ITERACIONES_HASH = 20_000      # trabajo de CPU por tarea "cpu"


def tarea_es(id_tarea: int, latencia: float) -> int:
    time.sleep(latencia)       # el hilo queda bloqueado esperando; la CPU queda libre
    return id_tarea


def tarea_cpu(id_tarea: int, _: float) -> int:
    hashlib.pbkdf2_hmac("sha256", str(id_tarea).encode(), b"sena-adso", ITERACIONES_HASH)
    return id_tarea


def preparar(n: int, proporcion_es: float = 0.5, semilla: int = 2):
    rng = random.Random(semilla)
    return [("es" if rng.random() < proporcion_es else "cpu", i, rng.uniform(*LATENCIA_S)) for i in range(n)]


def ejecutar(tareas) -> int:
    completadas = 0
    for tipo, i, lat in tareas:
        (tarea_es if tipo == "es" else tarea_cpu)(i, lat)
        completadas += 1
    return completadas


if __name__ == "__main__":
    for prop, nombre in ((1.0, "solo E/S"), (0.0, "solo CPU")):
        t = preparar(40, prop)
        t0 = time.perf_counter(); c0 = time.process_time()
        ejecutar(t)
        tp, tc = time.perf_counter() - t0, time.process_time() - c0
        print(f"{nombre:<9} pared = {tp:.2f} s   CPU = {tc:.2f} s   CPU/pared = {tc / tp * 100:5.1f} %")
