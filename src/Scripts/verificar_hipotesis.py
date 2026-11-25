"""
verificar_hipotesis.py — Contraste de hipótesis entre dos estrategias para un n dado.

Responde con evidencia: ¿la estrategia B es realmente más rápida que A,
o la diferencia observada cabe dentro de la variabilidad entre ejecuciones?

Criterios reportados:
  * Diferencia de medias y diferencia relativa (%)
  * Aceleración (speedup) = media_A / media_B
  * Prueba t de Welch al 95 % (no asume varianzas iguales)
  * Tamaño del efecto d de Cohen
  * Solapamiento de intervalos de confianza

Uso:
    python verificar_hipotesis.py resultados.csv A_lista_intermedia B_generador 1000000
"""
import csv
import sys

from estadistica import resumen, tamano_efecto, welch

if len(sys.argv) != 5:
    sys.exit("Uso: python verificar_hipotesis.py <csv> <estrategia_A> <estrategia_B> <n>")
ruta, ea, eb, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])

datos = {ea: [], eb: []}
with open(ruta, encoding="utf-8") as f:
    for fila in csv.DictReader(l for l in f if not l.startswith("#")):
        if fila["estrategia"] in datos and int(fila["n"]) == n and fila.get("medicion_memoria", "no") != "si":
            datos[fila["estrategia"]].append(float(fila["tiempo_s"]))

a, b = datos[ea], datos[eb]
if len(a) < 3 or len(b) < 3:
    sys.exit(f"Se necesitan al menos 3 repeticiones por estrategia (hay {len(a)} y {len(b)}).")

ra, rb = resumen(a), resumen(b)
w = welch(a, b)
d = tamano_efecto(a, b)
solapan = not (ra["ic95_sup"] < rb["ic95_inf"] or rb["ic95_sup"] < ra["ic95_inf"])

print(f"n = {n}   (A = {ea} · B = {eb})")
for nombre, r in ((ea, ra), (eb, rb)):
    print(f"  {nombre:<24} media = {r['media']:.6f} s   CV = {r['cv_pct']:.1f} %   "
          f"IC95 = [{r['ic95_inf']:.6f}, {r['ic95_sup']:.6f}]  ({r['n']} rep.)")
dif = ra["media"] - rb["media"]
print(f"\nDiferencia A - B      = {dif:.6f} s  ({dif / ra['media'] * 100:+.1f} % respecto a A)")
print(f"Aceleración A/B       = {ra['media'] / rb['media']:.2f}x")
print(f"t de Welch            = {w['t']:.2f}  (gl ≈ {w['gl']:.1f}, t crítico 95 % = {w['t_critico']:.3f})")
print(f"d de Cohen            = {d:.2f}")
print(f"Intervalos solapados  = {'sí' if solapan else 'no'}")
print("\nLectura:")
if w["significativa"] and not solapan:
    print("  La diferencia es estadísticamente consistente: es poco probable que se deba al ruido.")
elif w["significativa"]:
    print("  Diferencia significativa, pero los IC se solapan: reporte con cautela y aumente repeticiones.")
else:
    print("  NO hay evidencia suficiente de diferencia: la hipótesis no se confirma con estos datos.")
print("  Recuerde: significativo no es lo mismo que importante. ¿Cuántos segundos/julios ahorra en producción?")
