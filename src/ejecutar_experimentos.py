"""Ejecuta y registra comparaciones reproducibles de concurrencia."""

import argparse
import asyncio
import csv
import hashlib
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

from src.documentar_entorno import obtener_informe

ESTRATEGIAS = ("E0_secuencial", "E1_hilos", "E2_asyncio", "E3_procesos")
COLUMNAS = (
    "estrategia",
    "pct_es",
    "n_trabajadores",
    "n_tareas",
    "semilla",
    "latencia_sim_s",
    "repeticion",
    "t_pared_s",
    "t_cpu_s",
    "razon_cpu_pared_pct",
    "tareas_por_s",
)
TAMANO_ENTRADA_HASH = 1024


@dataclass(frozen=True)
class Tarea:
    tipo: str
    latencia_s: float
    entrada_hash: bytes
    iteraciones_hash: int


def preparar(
    n_tareas: int,
    pct_es: int,
    semilla: int,
    latencia_sim_s: float,
    iteraciones_hash: int,
) -> List[Tarea]:
    """Construye una sola carga determinista, fuera de la región medida."""
    generador = random.Random(semilla)
    n_es = round(n_tareas * pct_es / 100)
    tipos = ["es"] * n_es + ["cpu"] * (n_tareas - n_es)
    generador.shuffle(tipos)

    tareas = []
    for tipo in tipos:
        entrada = bytes(
            generador.getrandbits(8) for _ in range(TAMANO_ENTRADA_HASH)
        )
        tareas.append(
            Tarea(
                tipo=tipo,
                latencia_s=latencia_sim_s,
                entrada_hash=entrada,
                iteraciones_hash=iteraciones_hash,
            )
        )
    return tareas


def _trabajo_cpu(tarea: Tarea) -> None:
    """Ejecuta llamadas hash pequeñas para que la carga no dependa de E/S real."""
    for _ in range(tarea.iteraciones_hash):
        hashlib.sha256(tarea.entrada_hash).digest()


def _ejecutar_tarea(tarea: Tarea) -> float:
    """Ejecuta una tarea y devuelve su CPU local para el fallback de E3."""
    inicio_cpu = time.process_time()
    if tarea.tipo == "es":
        time.sleep(tarea.latencia_s)
    else:
        _trabajo_cpu(tarea)
    return time.process_time() - inicio_cpu


async def _ejecutar_tarea_async(tarea: Tarea) -> None:
    if tarea.tipo == "es":
        await asyncio.sleep(tarea.latencia_s)
    else:
        _trabajo_cpu(tarea)


async def _ejecutar_asyncio(tareas: Iterable[Tarea], trabajadores: int) -> None:
    semaforo = asyncio.Semaphore(trabajadores)

    async def ejecutar_limitada(tarea: Tarea) -> None:
        async with semaforo:
            await _ejecutar_tarea_async(tarea)

    await asyncio.gather(*(ejecutar_limitada(tarea) for tarea in tareas))


def _cpu_hijos(segundos: Tuple[float, float, float, float, float]) -> float:
    return segundos[3] + segundos[4]


def _ejecutar_carga(estrategia: str, tareas: List[Tarea], trabajadores: int) -> float:
    """Ejecuta la carga; retorna el CPU local de tareas, para el fallback E3."""
    if estrategia == "E0_secuencial":
        for tarea in tareas:
            _ejecutar_tarea(tarea)
        return 0.0

    if estrategia == "E1_hilos":
        with ThreadPoolExecutor(max_workers=trabajadores) as pool:
            for _ in pool.map(_ejecutar_tarea, tareas):
                pass
        return 0.0

    if estrategia == "E2_asyncio":
        asyncio.run(_ejecutar_asyncio(tareas, trabajadores))
        return 0.0

    if estrategia == "E3_procesos":
        cpu_tareas_hijos = 0.0
        with ProcessPoolExecutor(max_workers=trabajadores) as pool:
            for cpu_tarea in pool.map(_ejecutar_tarea, tareas, chunksize=1):
                cpu_tareas_hijos += cpu_tarea
        return cpu_tareas_hijos

    raise ValueError("Estrategia desconocida: {}".format(estrategia))


def ejecutar(
    estrategia: str, tareas: List[Tarea], trabajadores: int
) -> Tuple[float, float]:
    """Mide tiempo de pared y CPU de la carga ya preparada."""
    reloj_hijos_antes = os.times()
    cpu_proceso_antes = time.process_time()
    pared_antes = time.perf_counter()

    cpu_tareas_hijos = _ejecutar_carga(estrategia, tareas, trabajadores)

    t_pared_s = time.perf_counter() - pared_antes
    cpu_proceso = time.process_time() - cpu_proceso_antes
    reloj_hijos_despues = os.times()
    cpu_hijos = _cpu_hijos(reloj_hijos_despues) - _cpu_hijos(reloj_hijos_antes)

    if estrategia == "E3_procesos":
        # En Windows algunos entornos no informan el tiempo agregado de los hijos.
        t_cpu_s = cpu_proceso + (
            cpu_hijos if cpu_hijos > 0 else cpu_tareas_hijos
        )
    else:
        t_cpu_s = cpu_proceso
    return t_pared_s, t_cpu_s


def _calentar(trabajadores: int, latencia_sim_s: float) -> None:
    tareas = [
        Tarea("es", min(latencia_sim_s, 0.01), b"x" * TAMANO_ENTRADA_HASH, 1),
        Tarea("cpu", 0.0, b"x" * TAMANO_ENTRADA_HASH, 10),
    ]
    for estrategia in ESTRATEGIAS:
        ejecutar(estrategia, tareas, trabajadores)


def _guardar_entorno(parametros: dict) -> None:
    destino = Path("results/entorno.txt")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(
        obtener_informe({nombre: str(valor) for nombre, valor in parametros.items()}),
        encoding="utf-8",
    )


def ejecutar_experimentos(args: argparse.Namespace) -> Path:
    trabajadores = (
        args.trabajadores
        if args.trabajadores is not None
        else os.cpu_count() or 1
    )
    if trabajadores < 1:
        raise ValueError("El número de trabajadores debe ser al menos 1.")
    if args.n_tareas < 1 or args.repeticiones < 1:
        raise ValueError("Las tareas y repeticiones deben ser al menos 1.")
    if args.iteraciones_hash < 1:
        raise ValueError("Las iteraciones de hash deben ser al menos 1.")
    if args.latencia_sim_s < 0:
        raise ValueError("La latencia simulada no puede ser negativa.")
    if any(pct < 0 or pct > 100 for pct in args.pct_es):
        raise ValueError("Cada porcentaje E/S debe estar entre 0 y 100.")

    parametros = {
        "estrategias": ", ".join(ESTRATEGIAS),
        "proporciones_es_pct": ", ".join(str(pct) for pct in args.pct_es),
        "n_trabajadores": trabajadores,
        "n_tareas": args.n_tareas,
        "semilla": args.semilla,
        "latencia_sim_s": args.latencia_sim_s,
        "repeticiones": args.repeticiones,
        "iteraciones_hash_por_tarea": args.iteraciones_hash,
        "tamano_entrada_hash_bytes": TAMANO_ENTRADA_HASH,
    }
    _guardar_entorno(parametros)

    # La preparación es previa al calentamiento y a todas las mediciones.
    cargas = {
        pct: preparar(
            args.n_tareas,
            pct,
            args.semilla,
            args.latencia_sim_s,
            args.iteraciones_hash,
        )
        for pct in args.pct_es
    }
    _calentar(trabajadores, args.latencia_sim_s)

    destino = Path(args.salida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        for pct_es, tareas in cargas.items():
            for repeticion in range(1, args.repeticiones + 1):
                orden = list(ESTRATEGIAS)
                random.Random(args.semilla + repeticion + pct_es).shuffle(orden)
                for estrategia in orden:
                    n_trabajadores = (
                        1 if estrategia == "E0_secuencial" else trabajadores
                    )
                    t_pared_s, t_cpu_s = ejecutar(
                        estrategia, tareas, n_trabajadores
                    )
                    escritor.writerow(
                        {
                            "estrategia": estrategia,
                            "pct_es": pct_es,
                            "n_trabajadores": n_trabajadores,
                            "n_tareas": len(tareas),
                            "semilla": args.semilla,
                            "latencia_sim_s": args.latencia_sim_s,
                            "repeticion": repeticion,
                            "t_pared_s": "{:.9f}".format(t_pared_s),
                            "t_cpu_s": "{:.9f}".format(t_cpu_s),
                            "razon_cpu_pared_pct": "{:.6f}".format(
                                100 * t_cpu_s / t_pared_s
                            ),
                            "tareas_por_s": "{:.6f}".format(
                                len(tareas) / t_pared_s
                            ),
                        }
                    )
    return destino


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-tareas", type=int, default=32)
    parser.add_argument("--pct-es", type=int, nargs="+", default=[0, 50, 100])
    parser.add_argument("--trabajadores", type=int, default=None)
    parser.add_argument("--semilla", type=int, default=42)
    parser.add_argument("--latencia-sim-s", type=float, default=0.1)
    parser.add_argument("--repeticiones", type=int, default=30)
    parser.add_argument("--iteraciones-hash", type=int, default=20000)
    parser.add_argument("--salida", default="results/resultados.csv")
    args = parser.parse_args()

    destino = ejecutar_experimentos(args)
    print("Resultados guardados en {}".format(destino))


if __name__ == "__main__":
    main()
