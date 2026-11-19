"""
Estrategia C — Equipo 2: repartir la cola entre PROCESOS (paralelismo).

Rama del mapa de optimización: "repartir trabajo -> multinúcleo" (distinta de
B, que solo aprovecha las esperas).

Idea: cada proceso tiene su propio intérprete y su propio GIL, así que las
tareas "cpu" (pbkdf2_hmac) pueden ejecutarse al mismo tiempo en núcleos
distintos. Las esperas "es" también se solapan, porque cada proceso duerme
por su cuenta.

Costo: crear procesos (en Windows se usa "spawn": cada hijo arranca un
intérprete nuevo) y enviar tareas y resultados serializados con pickle. Ese
costo está DENTRO del tiempo medido, porque el usuario también lo espera; C
solo vale la pena cuando el trabajo de CPU es mayor que ese costo fijo.

Limitaciones de medición que hay que declarar en el informe:
  * labmedicion mide cpu_proceso_s con time.process_time(), que solo cuenta el
    proceso principal: el CPU de los hijos NO aparece y uso_cpu_pct de C sale
    subestimado.
  * tracemalloc tampoco ve la memoria de los procesos hijos.

Misma interfaz que la línea base:
    preparar(n)       -> lista de tareas (se reutiliza la de la línea base)
    ejecutar(tareas)  -> número de tareas completadas
"""
from concurrent.futures import ProcessPoolExecutor

from src.linea_base import preparar, tarea_cpu, tarea_es  # noqa: F401  (preparar se reexporta)

# Igual al número de núcleos lógicos del equipo de medición (8). Ver docs/decisiones.md.
N_TRABAJADORES = 8


def _ejecutar_una(tarea) -> int:
    # Función de nivel de módulo: pickle debe poder enviarla a los procesos hijos.
    tipo, i, lat = tarea
    return (tarea_es if tipo == "es" else tarea_cpu)(i, lat)


def ejecutar(tareas) -> int:
    tareas = list(tareas)
    if not tareas:
        return 0
    with ProcessPoolExecutor(max_workers=min(N_TRABAJADORES, len(tareas))) as grupo:
        ids = list(grupo.map(_ejecutar_una, tareas))
    # Solo cuenta como completada una tarea que devolvió su propio id.
    if sorted(ids) != sorted(i for _, i, _ in tareas):
        raise RuntimeError("La estrategia C perdió o duplicó tareas")
    return len(ids)


if __name__ == "__main__":  # obligatorio en Windows para usar procesos
    import time

    from src import linea_base

    for prop, nombre in ((1.0, "solo E/S"), (0.0, "solo CPU"), (0.5, "mixta")):
        t = preparar(40, prop)
        assert ejecutar(t) == linea_base.ejecutar(t)  # corrección antes de medir
        t0 = time.perf_counter(); c0 = time.process_time()
        ejecutar(t)
        tp, tc = time.perf_counter() - t0, time.process_time() - c0
        print(f"C procesos {nombre:<9} pared = {tp:.2f} s   CPU (solo proceso principal) = {tc:.2f} s")
    print("Una sola corrida: no es un experimento. Latencia de E/S simulada con time.sleep.")
