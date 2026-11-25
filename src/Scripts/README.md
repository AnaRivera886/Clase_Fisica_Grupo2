# Scripts · Clase 5 — Análisis, verificación y sustentación

Requisitos: Python 3.10+. Opcional: matplotlib para gráficos.

| Script | Qué hace | Uso |
|---|---|---|
| `estadistica.py` | Media, mediana, s, CV, IC 95 % (t de Student), Welch, d de Cohen, atípicos (Tukey). Fórmulas legibles | módulo |
| `analizar_resultados.py` | Resumen por estrategia y n (`*_resumen.csv`) + gráficos tiempo vs n (log–log) y barras con IC | `python analizar_resultados.py resultados.csv` |
| `verificar_hipotesis.py` | Contraste entre dos estrategias para un n: aceleración, Welch, d de Cohen, solapamiento de IC | `python verificar_hipotesis.py resultados.csv A B 1000000` |
| `energia.py` | E = P̄·t con nivel de evidencia declarado (RAPL, vatímetro, estimación) | `python energia.py --csv resultados.csv` |
| `modelo_termico.py` | **SIMULACIÓN** del modelo térmico de primer orden (τ = R·C) | `python modelo_termico.py --R 2 --C 15` |

Datos para practicar (SIMULADOS): `../../06_Material_Complementario/Datos_Ejemplo/`.

**Recuerde:** significativo no es lo mismo que importante; los IC solapados indican falta de evidencia, no igualdad;
la extrapolación fuera del rango medido es una suposición.
