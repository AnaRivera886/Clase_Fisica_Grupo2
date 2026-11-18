"""
analisis_equipo2.py — Estadística y gráficos del experimento del Equipo 2 (Clase 5).

Responsable: Ana (R3 + mitad de R4: análisis estadístico y gráficos).

Lee el CSV que escribe herramientas/labmedicion.py y, por estrategia y n:
  * usa SOLO las corridas de tiempo (medicion_memoria = "no"); la corrida de
    memoria (repetición 0, con tracemalloc) infla el tiempo y se analiza aparte;
  * calcula media, desviación estándar muestral, CV, IC 95 % (t de Student),
    atípicos por la regla de Tukey, aceleración S = t_A / t_X (mismo n) y
    rendimiento n / t [tareas/s];
  * contrasta H1 y H2 con los criterios escritos en docs/hipotesis.md.

Uso (desde la raíz del repositorio):
    python -m experimentos.analisis_equipo2 resultados/resultados.csv

Escribe resultados/resumen.csv, resultados/analisis.md y, si matplotlib está
instalado, tres gráficos en resultados/figuras/. Sin RAPL ni vatímetro no se
concluye nada sobre energía (E = P̄·t requiere medir la potencia P).
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

BASE = "A_linea_base"
NOTA = "Latencia de E/S simulada con time.sleep · un solo equipo"

# Valores críticos t de Student, dos colas, 95 %, por grados de libertad (tabla estándar).
_T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
        9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
        16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 25: 2.060, 30: 2.042,
        40: 2.021, 60: 2.000, 120: 1.980}


def t95(gl: int) -> float:
    if gl in _T95:
        return _T95[gl]
    if gl > 120:
        return 1.960
    return _T95[max(k for k in _T95 if k < gl)]  # fila inferior: valor más conservador


def num(x: str) -> float | None:
    return float(x) if x not in ("", None) else None


def leer(ruta: Path) -> list[dict]:
    with ruta.open(newline="", encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    if not filas:
        raise SystemExit(f"{ruta} no tiene filas")
    for r in filas:
        r["n"] = int(r["n"])
        r["repeticion"] = int(r["repeticion"])
        for c in ("tiempo_s", "cpu_proceso_s", "uso_cpu_pct", "pico_mem_mib", "rss_mib"):
            r[c] = num(r[c])
    return filas


def tukey(valores: list[float]) -> int:
    if len(valores) < 4:
        return 0
    q1, _, q3 = statistics.quantiles(valores, n=4, method="inclusive")
    iqr = q3 - q1
    return sum(v < q1 - 1.5 * iqr or v > q3 + 1.5 * iqr for v in valores)


def resumir(filas: list[dict]) -> list[dict]:
    tiempo, memoria = defaultdict(list), defaultdict(list)
    for r in filas:
        (memoria if r["medicion_memoria"] == "si" else tiempo)[(r["estrategia"], r["n"])].append(r)

    resumen = []
    for (est, n), rs in sorted(tiempo.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        t = [r["tiempo_s"] for r in rs]
        k = len(t)
        media = statistics.fmean(t)
        de = statistics.stdev(t) if k > 1 else 0.0
        semi = t95(k - 1) * de / math.sqrt(k) if k > 1 else float("nan")
        mem = [r["pico_mem_mib"] for r in memoria.get((est, n), []) if r["pico_mem_mib"] is not None]
        resumen.append({
            "estrategia": est, "n": n, "repeticiones": k,
            "t_media_s": media, "t_de_s": de, "t_cv_pct": 100 * de / media if media else float("nan"),
            "t_ic95_inf_s": media - semi, "t_ic95_sup_s": media + semi,
            "t_mediana_s": statistics.median(t), "atipicos_tukey": tukey(t),
            "uso_cpu_media_pct": statistics.fmean(r["uso_cpu_pct"] for r in rs),
            "tareas_por_s": n / media if media else float("nan"),
            "pico_mem_mib": statistics.fmean(mem) if mem else float("nan"),
        })
    base = {f["n"]: f["t_media_s"] for f in resumen if f["estrategia"] == BASE}
    for f in resumen:
        f["aceleracion_S"] = base[f["n"]] / f["t_media_s"] if f["n"] in base else float("nan")
    return resumen


def guardar_csv(resumen: list[dict], ruta: Path) -> None:
    with ruta.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(resumen[0]))
        w.writeheader()
        for fila in resumen:
            w.writerow({k: f"{v:.6g}" if isinstance(v, float) else v for k, v in fila.items()})


def graficar(resumen: list[dict], carpeta: Path) -> list[tuple[str, str]]:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker
    except ImportError:
        print("matplotlib no está instalado: se omiten los gráficos (pip install matplotlib)")
        return []
    carpeta.mkdir(parents=True, exist_ok=True)
    estrategias = sorted({f["estrategia"] for f in resumen})
    tamanos = sorted({f["n"] for f in resumen})
    n_max = tamanos[-1]
    err = lambda f: 0.0 if math.isnan(f["t_ic95_sup_s"]) else f["t_ic95_sup_s"] - f["t_media_s"]
    hechas = []

    def pie(fig):
        fig.text(0.99, 0.01, NOTA, ha="right", va="bottom", fontsize=7, color="0.4")
        fig.tight_layout(rect=(0, 0.03, 1, 1))

    # 1) Tiempo vs n en escala log–log con IC 95 %.
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for est in estrategias:
        pts = [f for f in resumen if f["estrategia"] == est]
        ax.errorbar([f["n"] for f in pts], [f["t_media_s"] for f in pts],
                    yerr=[err(f) for f in pts], marker="o", capsize=3, label=est)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks(tamanos, [str(n) for n in tamanos])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Tamaño de la cola n [tareas]")
    ax.set_ylabel("Tiempo de pared medio t [s]")
    ax.set_title("Tiempo de pared vs. n (log–log, barras: IC 95 %)")
    ax.legend(fontsize=8); pie(fig)
    fig.savefig(carpeta / "tiempo_vs_n.png", dpi=150); plt.close(fig)
    hechas.append(("figuras/tiempo_vs_n.png", "Tiempo de pared vs. n (log–log)"))

    # 2) Comparación de estrategias para el n mayor.
    fila = [f for f in resumen if f["n"] == n_max]
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.bar([f["estrategia"] for f in fila], [f["t_media_s"] for f in fila],
           yerr=[err(f) for f in fila], capsize=4, color=["#4C72B0", "#DD8452", "#55A868", "#C44E52"][:len(fila)])
    for i, f in enumerate(fila):
        ax.annotate(f"S = {f['aceleracion_S']:.2f}", (i, f["t_media_s"] + err(f)), ha="center",
                    xytext=(0, 4), textcoords="offset points", fontsize=8)
    ax.margins(y=0.12)
    ax.set_ylabel("Tiempo de pared medio t [s]")
    ax.set_title(f"Comparación de estrategias para n = {n_max} (IC 95 %)")
    pie(fig)
    fig.savefig(carpeta / "comparacion_n_max.png", dpi=150); plt.close(fig)
    hechas.append(("figuras/comparacion_n_max.png", f"Comparación de estrategias para n = {n_max}"))

    # 3) Uso de CPU del proceso por estrategia y n.
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ancho = 0.8 / len(estrategias)
    for i, est in enumerate(estrategias):
        pts = [f for f in resumen if f["estrategia"] == est]
        ax.bar([tamanos.index(f["n"]) + (i - (len(estrategias) - 1) / 2) * ancho for f in pts],
               [f["uso_cpu_media_pct"] for f in pts], ancho, label=est)
    ax.axhline(100, color="0.5", lw=0.8, ls="--")
    ax.set_xticks(range(len(tamanos)), [f"n = {n}" for n in tamanos])
    ax.set_ylabel("Uso de CPU del proceso U = t_CPU / t · 100 [%]")
    ax.set_title("Uso de CPU por estrategia (>100 % = varios núcleos; C no cuenta los hijos)")
    ax.legend(fontsize=8); pie(fig)
    fig.savefig(carpeta / "uso_cpu.png", dpi=150); plt.close(fig)
    hechas.append(("figuras/uso_cpu.png", "Uso de CPU del proceso por estrategia y n"))
    return hechas


def contrastar(resumen: list[dict]) -> list[str]:
    """Criterios copiados de docs/hipotesis.md (no se ajustan después de ver datos)."""
    por = {(f["estrategia"], f["n"]): f for f in resumen}
    a, b = por.get((BASE, 80)), por.get(("B_hilos", 80))
    if not (a and b):
        return ["- H1/H2: faltan datos de A_linea_base o B_hilos con n = 80; no se pueden contrastar."]
    s = a["t_media_s"] / b["t_media_s"]
    du = b["uso_cpu_media_pct"] - a["uso_cpu_media_pct"]
    return [
        f"- **H1** (criterio: t̄_A / t̄_B ≥ 1,5 con n = 80): t̄_A / t̄_B = {s:.2f} → "
        + ("**no refutada**." if s >= 1.5 else "**refutada**."),
        f"- **H2** (criterio: Ū_B − Ū_A ≥ 10 puntos con n = 80): Ū_B − Ū_A = {du:.1f} puntos → "
        + ("**no refutada**." if du >= 10 else "**refutada**."),
    ]


def main(argv=None) -> None:
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")  # consolas de Windows sin UTF-8
    p = argparse.ArgumentParser(description="Análisis del experimento del Equipo 2")
    p.add_argument("csv", nargs="?", default="resultados/resultados.csv")
    p.add_argument("--salida", default="resultados")
    a = p.parse_args(argv)
    ruta, salida = Path(a.csv), Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)

    resumen = resumir(leer(ruta))
    guardar_csv(resumen, salida / "resumen.csv")
    figuras = graficar(resumen, salida / "figuras")

    enc = "| Estrategia | n | reps | t̄ [s] | DE [s] | CV [%] | IC 95 % [s] | Tukey | Ū CPU [%] | tareas/s | S | pico mem [MiB] |"
    lineas = [f"# Análisis de resultados — Equipo 2", "",
              f"Fuente: `{ruta.as_posix()}`. Solo corridas de tiempo (`medicion_memoria = no`); "
              "la memoria sale de la corrida separada (repetición 0). " + NOTA + ".", "",
              enc, "|" + "---|" * 12]
    for f in resumen:
        lineas.append(
            f"| {f['estrategia']} | {f['n']} | {f['repeticiones']} | {f['t_media_s']:.3f} | {f['t_de_s']:.3f} "
            f"| {f['t_cv_pct']:.1f} | [{f['t_ic95_inf_s']:.3f}; {f['t_ic95_sup_s']:.3f}] | {f['atipicos_tukey']} "
            f"| {f['uso_cpu_media_pct']:.0f} | {f['tareas_por_s']:.1f} | {f['aceleracion_S']:.2f} | {f['pico_mem_mib']:.3f} |")
    inestables = [f for f in resumen if f["t_cv_pct"] > 10]
    lineas += ["", "## Calidad de los datos (criterio del protocolo: CV ≤ 10 %)", ""]
    lineas += [f"- {f['estrategia']} n = {f['n']}: CV = {f['t_cv_pct']:.1f} % > 10 % → revisar incidentes "
               "y repetir el bloque según docs/protocolo.md." for f in inestables] or ["- Todas las combinaciones cumplen CV ≤ 10 %."]
    lineas += ["", "## Contraste de hipótesis", ""] + contrastar(resumen)
    lineas += ["", "## Gráficos e interpretación física", ""]
    for ruta_fig, titulo in figuras:
        lineas.append(f"- `{ruta_fig}` — {titulo}. _Interpretación física: redactar con los datos reales._")
    lineas += ["", "## Límites que se deben declarar", "",
               "- `time.sleep` simula la latencia de red: no representa una red real.",
               "- En C, `uso_cpu_pct` y `pico_mem_mib` no incluyen los procesos hijos (subestimados).",
               "- `uso_cpu_pct` no es potencia: energía **no medida** (sin RAPL ni vatímetro). E = P̄·t.",
               "- Resultados válidos solo para este equipo y para n entre 20 y 80."]
    (salida / "analisis.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    print(f"{'estrategia':<14}{'n':>4}{'t [s]':>9}{'+-IC95':>8}{'CV%':>7}{'U%':>6}{'tareas/s':>10}{'S':>7}")
    for f in resumen:
        e = f["t_ic95_sup_s"] - f["t_media_s"]
        print(f"{f['estrategia']:<14}{f['n']:>4}{f['t_media_s']:>9.3f}{e:>8.3f}{f['t_cv_pct']:>7.1f}"
              f"{f['uso_cpu_media_pct']:>6.0f}{f['tareas_por_s']:>10.1f}{f['aceleracion_S']:>7.2f}")
    texto = "\n".join(contrastar(resumen))
    for viejo, nuevo in (("t̄", "t"), ("Ū", "U"), ("**", ""), ("≥", ">="), ("−", "-"), ("→", "->")):
        texto = texto.replace(viejo, nuevo)
    print(texto)
    print(f"Escrito: {salida / 'resumen.csv'}, {salida / 'analisis.md'}"
          + (f" y {len(figuras)} figuras en {salida / 'figuras'}" if figuras else ""))


if __name__ == "__main__":
    main()
