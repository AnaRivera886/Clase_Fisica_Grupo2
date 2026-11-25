"""
energia.py — Relación entre tiempo, potencia y energía:  E = P̄ · t  (o E = ∫ P dt)

Tres modos, cada uno con su NIVEL DE EVIDENCIA declarado:

  1. --csv con columna energia_j (RAPL)      -> MEDICIÓN (modelo interno del chip, solo paquete CPU)
  2. --potencia_w X  (vatímetro externo)     -> MEDICIÓN de potencia media del equipo completo
  3. --estimar --tdp X                       -> ESTIMACIÓN de cota superior; NO es medición

Nunca convierta %CPU en vatios por regla de tres y lo presente como medido.

Uso:
    python energia.py --csv resultados.csv
    python energia.py --tiempo 12.5 --potencia_w 38       # vatímetro: 38 W medios durante 12.5 s
    python energia.py --tiempo 12.5 --estimar --tdp 15    # cota superior aproximada
"""
import argparse
import csv
from collections import defaultdict

p = argparse.ArgumentParser()
p.add_argument("--csv")
p.add_argument("--tiempo", type=float, help="s")
p.add_argument("--potencia_w", type=float, help="potencia media medida con vatímetro [W]")
p.add_argument("--estimar", action="store_true")
p.add_argument("--tdp", type=float, help="potencia de diseño térmico del procesador [W]")
a = p.parse_args()

if a.csv:
    e = defaultdict(list)
    with open(a.csv, encoding="utf-8") as f:
        for fila in csv.DictReader(l for l in f if not l.startswith("#")):
            if fila.get("energia_j"):
                e[(fila["estrategia"], int(fila["n"]))].append(float(fila["energia_j"]))
    if not e:
        print("El CSV no tiene energía RAPL. Reporte 'energía: no medida' y discuta tiempo y CPU %.")
    for (estr, n), v in sorted(e.items()):
        print(f"[MEDICIÓN RAPL] {estr:<24} n={n:<10} E media = {sum(v)/len(v):.3f} J  ({len(v)} rep.)")
elif a.tiempo and a.potencia_w:
    E = a.potencia_w * a.tiempo
    print(f"[MEDICIÓN vatímetro] E = P·t = {a.potencia_w} W × {a.tiempo} s = {E:.1f} J = {E/3600:.4f} Wh")
elif a.tiempo and a.estimar and a.tdp:
    E = a.tdp * a.tiempo
    print(f"[ESTIMACIÓN, no medición] E ≤ ~TDP·t = {a.tdp} W × {a.tiempo} s ≈ {E:.1f} J")
    print("  El TDP no es la potencia real instantánea; puede superarse brevemente (turbo) o no alcanzarse.")
    print("  Uso legítimo: orden de magnitud y comparación de escenarios, declarando la suposición.")
else:
    p.print_help()
