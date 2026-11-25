"""
estadistica.py — Estadística descriptiva básica sin dependencias externas.

Funciones usadas por analizar_resultados.py y verificar_hipotesis.py.
Se implementan explícitamente para que el aprendiz pueda leer cada fórmula.
"""
from __future__ import annotations

import math
import statistics

# Valores críticos t de Student bilaterales al 95 % (gl = n - 1)
_T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
        9: 2.262, 10: 2.228, 12: 2.179, 15: 2.131, 20: 2.086, 25: 2.060, 30: 2.042,
        40: 2.021, 60: 2.000, 120: 1.980}


def t_critico_95(gl: int) -> float:
    """t crítico bilateral al 95 % (usa el gl tabulado más cercano por debajo)."""
    if gl <= 0:
        return float("nan")
    claves = [k for k in _T95 if k <= gl]
    return _T95[max(claves)] if claves else _T95[1]


def resumen(valores: list[float]) -> dict[str, float]:
    """n, media, mediana, desviación estándar muestral, CV % e IC95 % de la media."""
    n = len(valores)
    media = statistics.fmean(valores)
    s = statistics.stdev(valores) if n > 1 else 0.0
    error_estandar = s / math.sqrt(n) if n > 1 else float("nan")
    semiancho = t_critico_95(n - 1) * error_estandar if n > 1 else float("nan")
    return {
        "n": n,
        "media": media,
        "mediana": statistics.median(valores),
        "desv": s,
        "cv_pct": (s / media * 100) if media else float("nan"),
        "min": min(valores),
        "max": max(valores),
        "ic95_inf": media - semiancho,
        "ic95_sup": media + semiancho,
    }


def welch(a: list[float], b: list[float]) -> dict[str, float]:
    """Prueba t de Welch (varianzas distintas). Devuelve t, gl y si |t| > t crítico."""
    na, nb = len(a), len(b)
    va, vb = statistics.variance(a), statistics.variance(b)
    se = math.sqrt(va / na + vb / nb)
    t = (statistics.fmean(a) - statistics.fmean(b)) / se if se else float("inf")
    gl_num = (va / na + vb / nb) ** 2
    gl_den = (va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1)
    gl = gl_num / gl_den if gl_den else na + nb - 2
    tc = t_critico_95(int(gl))
    return {"t": t, "gl": gl, "t_critico": tc, "significativa": abs(t) > tc}


def tamano_efecto(a: list[float], b: list[float]) -> float:
    """d de Cohen: diferencia de medias en unidades de desviación combinada."""
    na, nb = len(a), len(b)
    sp = math.sqrt(((na - 1) * statistics.variance(a) + (nb - 1) * statistics.variance(b)) / (na + nb - 2))
    return (statistics.fmean(a) - statistics.fmean(b)) / sp if sp else float("inf")


def valores_atipicos(valores: list[float]) -> list[float]:
    """Regla de Tukey: fuera de [Q1 - 1.5·RIC, Q3 + 1.5·RIC]. Se REPORTAN, no se borran sin justificar."""
    if len(valores) < 4:
        return []
    q1, _, q3 = statistics.quantiles(valores, n=4)
    ric = q3 - q1
    return [v for v in valores if v < q1 - 1.5 * ric or v > q3 + 1.5 * ric]
