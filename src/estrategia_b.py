"""
Estrategia B — Equipo 2: atender la cola con HILOS (concurrencia).

Rama del mapa de optimización: "sin esperas ociosas -> concurrencia".

Idea: en la línea base, mientras una tarea "es" duerme esperando la red
simulada (time.sleep), el procesador queda ocioso y las demás tareas esperan
en la cola. Con un grupo de hilos, varias tareas están en curso a la vez:
mientras un hilo espera, otro avanza. time.sleep libera el GIL, así que las
esperas se SOLAPAN y el tiempo de pared debería bajar sin aumentar el trabajo
total de CPU.

Tareas "cpu": en CPython el GIL deja ejecutar código Python en un solo hilo a
la vez, pero hashlib.pbkdf2_hmac es código en C que puede liberar el GIL. Por
eso NO suponemos que los hilos no aceleren la parte de CPU: lo decide la
medición (ver docs/hipotesis.md).

Misma interfaz que la línea base:
    preparar(n)       -> lista de tareas (se reutiliza la de la línea base)
    ejecutar(tareas)  -> número de tareas completadas
"""
from concurrent.futures import ThreadPoolExecutor

from src.linea_base import preparar, tarea_cpu, tarea_es  # noqa: F401  (preparar se reexporta)

# Igual al número de núcleos lógicos del equipo de medición (8). Ver docs/decisiones.md.
N_TRABAJADORES = 8


def _ejecutar_una(tarea) -> int:
    tipo, i, lat = tarea
    return (tarea_es if tipo == "es" else tarea_cpu)(i, lat)


def ejecutar(tareas) -> int:
    tareas = list(tareas)
    if not tareas:
        return 0
    with ThreadPoolExecutor(max_workers=min(N_TRABAJADORES, len(tareas))) as grupo:
        ids = list(grupo.map(_ejecutar_una, tareas))
    # Solo cuenta como completada una tarea que devolvió su propio id.
    if sorted(ids) != sorted(i for _, i, _ in tareas):
        raise RuntimeError("La estrategia B perdió o duplicó tareas")
    return len(ids)


if __name__ == "__main__":
    import time

    from src import linea_base

    for prop, nombre in ((1.0, "solo E/S"), (0.0, "solo CPU"), (0.5, "mixta")):
        t = preparar(40, prop)
        assert ejecutar(t) == linea_base.ejecutar(t)  # corrección antes de medir
        t0 = time.perf_counter(); c0 = time.process_time()
        ejecutar(t)
        tp, tc = time.perf_counter() - t0, time.process_time() - c0
        print(f"B hilos  {nombre:<9} pared = {tp:.2f} s   CPU = {tc:.2f} s   CPU/pared = {tc / tp * 100:5.1f} %")
    print("Una sola corrida: no es un experimento. Latencia de E/S simulada con time.sleep.")
