"""
analizar_resultados.py — Resumen estadístico y gráficos de un CSV del laboratorio.

Entrada: CSV con columnas estrategia, n, tiempo_s, medicion_memoria, pico_mem_mib, ...
        (formato producido por labmedicion.py de la Clase 4)
Salida:  <nombre>_resumen.csv   media, mediana, desviación, CV %, IC95 % por estrategia y n
        <nombre>_tiempo_vs_n.png  (si matplotlib está instalado)
        <nombre>_barras.png       comparación con barras de error (IC95 %)

Uso:
    python analizar_resultados.py resultados_demo.csv
    python analizar_resultados.py ../../06_Material_Complementario/Datos_Ejemplo/resultados_simulados_equipo7.csv
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

from estadistica import resumen, valores_atipicos

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


def cargar(ruta: Path):
    tiempos, memoria, simulado = defaultdict(list), defaultdict(list), False
    with ruta.open(encoding="utf-8") as f:
        filas = [l for l in f if not l.startswith("#")]  # admite comentarios de cabecera
    for fila in csv.DictReader(filas):
        clave = (fila["estrategia"], int(fila["n"]))
        if "SIMULADO" in (fila.get("observacion", "") + fila.get("equipo", "")).upper():
            simulado = True
        if fila.get("medicion_memoria", "no") == "si":
            if fila.get("pico_mem_mib"):
                memoria[clave].append(float(fila["pico_mem_mib"]))
        else:
            tiempos[clave].append(float(fila["tiempo_s"]))
    return tiempos, memoria, simulado


def main(ruta: Path) -> None:
    tiempos, memoria, simulado = cargar(ruta)
    if not tiempos:
        sys.exit("No se encontraron corridas de tiempo en el archivo.")
    salida = ruta.with_name(ruta.stem + "_resumen.csv")
    tabla = []
    for (estr, n), vals in sorted(tiempos.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        r = resumen(vals)
        mem = memoria.get((estr, n))
        tabla.append({
            "estrategia": estr, "n": n, "repeticiones": r["n"],
            "media_s": f"{r['media']:.6f}", "mediana_s": f"{r['mediana']:.6f}",
            "desv_s": f"{r['desv']:.6f}", "cv_pct": f"{r['cv_pct']:.1f}",
            "ic95_inf_s": f"{r['ic95_inf']:.6f}", "ic95_sup_s": f"{r['ic95_sup']:.6f}",
            "pico_mem_mib": f"{sum(mem) / len(mem):.3f}" if mem else "",
            "atipicos": len(valores_atipicos(vals)),
        })
    with salida.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(tabla[0]))
        w.writeheader()
        w.writerows(tabla)

    print(f"{'estrategia':<24}{'n':>10}{'media (s)':>12}{'CV %':>7}{'IC95 % (s)':>26}{'pico MiB':>10}")
    for t in tabla:
        print(f"{t['estrategia']:<24}{t['n']:>10}{float(t['media_s']):>12.5f}{t['cv_pct']:>7}"
              f"   [{float(t['ic95_inf_s']):.5f}, {float(t['ic95_sup_s']):.5f}]{t['pico_mem_mib']:>10}")
    print(f"\nResumen: {salida}")
    alertas = [t for t in tabla if float(t["cv_pct"]) > 10]
    if alertas:
        print(f"ATENCIÓN: {len(alertas)} combinaciones con CV > 10 %: revise ruido o repeticiones.")

    if plt is None:
        print("matplotlib no instalado: se omiten los gráficos (pip install matplotlib).")
        return
    etiqueta = "  [DATOS SIMULADOS]" if simulado else ""
    estrategias = sorted({t["estrategia"] for t in tabla})

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for e in estrategias:
        fs = [t for t in tabla if t["estrategia"] == e]
        ns = [t["n"] for t in fs]
        med = [float(t["media_s"]) for t in fs]
        err = [float(t["media_s"]) - float(t["ic95_inf_s"]) for t in fs]
        ax.errorbar(ns, med, yerr=err, marker="o", capsize=3, label=e)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Tamaño de entrada n [elementos]")
    ax.set_ylabel("Tiempo de ejecución medio [s]")
    ax.set_title("Tiempo vs. tamaño de entrada (media ± IC95 %)" + etiqueta)
    ax.grid(True, which="both", alpha=.3); ax.legend()
    fig.tight_layout(); fig.savefig(ruta.with_name(ruta.stem + "_tiempo_vs_n.png"), dpi=150)

    n_max = max(t["n"] for t in tabla)
    fs = [t for t in tabla if t["n"] == n_max]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    medias = [float(t["media_s"]) for t in fs]
    errs = [float(t["media_s"]) - float(t["ic95_inf_s"]) for t in fs]
    ax.bar([t["estrategia"] for t in fs], medias, yerr=errs, capsize=5, color="#4C78A8")
    ax.set_ylabel("Tiempo de ejecución medio [s]")
    ax.set_title(f"Comparación de estrategias, n = {n_max:,}".replace(",", ".") + etiqueta)
    ax.grid(axis="y", alpha=.3)
    fig.tight_layout(); fig.savefig(ruta.with_name(ruta.stem + "_barras.png"), dpi=150)
    print("Gráficos PNG guardados junto al CSV.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python analizar_resultados.py <archivo.csv>")
    main(Path(sys.argv[1]))
