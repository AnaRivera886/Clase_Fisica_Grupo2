# Análisis de resultados — Equipo 2

Fuente: `resultados/resultados.csv`. Solo corridas de tiempo (`medicion_memoria = no`); la memoria sale de la corrida separada (repetición 0). Latencia de E/S simulada con time.sleep · un solo equipo.

| Estrategia | n | reps | t̄ [s] | DE [s] | CV [%] | IC 95 % [s] | Tukey | Ū CPU [%] | tareas/s | S | pico mem [MiB] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A_linea_base | 20 | 10 | 0.502 | 0.057 | 11.4 | [0.461; 0.544] | 0 | 49 | 39.8 | 1.00 | 0.002 |
| B_hilos | 20 | 10 | 0.129 | 0.062 | 48.3 | [0.084; 0.173] | 1 | 340 | 155.3 | 3.90 | 0.063 |
| C_procesos | 20 | 10 | 0.790 | 0.261 | 33.0 | [0.604; 0.977] | 2 | 10 | 25.3 | 0.64 | 0.083 |
| A_linea_base | 40 | 10 | 1.052 | 0.114 | 10.8 | [0.971; 1.134] | 1 | 50 | 38.0 | 1.00 | 0.002 |
| B_hilos | 40 | 10 | 0.196 | 0.007 | 3.6 | [0.191; 0.201] | 2 | 453 | 203.9 | 5.36 | 0.098 |
| C_procesos | 40 | 10 | 0.875 | 0.208 | 23.7 | [0.727; 1.024] | 0 | 8 | 45.7 | 1.20 | 0.123 |
| A_linea_base | 80 | 10 | 2.172 | 0.030 | 1.4 | [2.151; 2.194] | 0 | 39 | 36.8 | 1.00 | 0.002 |
| B_hilos | 80 | 10 | 0.387 | 0.031 | 7.9 | [0.365; 0.409] | 1 | 388 | 206.9 | 5.62 | 0.167 |
| C_procesos | 80 | 10 | 1.109 | 0.424 | 38.2 | [0.806; 1.412] | 2 | 11 | 72.1 | 1.96 | 0.197 |

## Calidad de los datos (criterio del protocolo: CV ≤ 10 %)

- A_linea_base n = 20: CV = 11.4 % > 10 % → revisar incidentes y repetir el bloque según docs/protocolo.md.
- B_hilos n = 20: CV = 48.3 % > 10 % → revisar incidentes y repetir el bloque según docs/protocolo.md.
- C_procesos n = 20: CV = 33.0 % > 10 % → revisar incidentes y repetir el bloque según docs/protocolo.md.
- A_linea_base n = 40: CV = 10.8 % > 10 % → revisar incidentes y repetir el bloque según docs/protocolo.md.
- C_procesos n = 40: CV = 23.7 % > 10 % → revisar incidentes y repetir el bloque según docs/protocolo.md.
- C_procesos n = 80: CV = 38.2 % > 10 % → revisar incidentes y repetir el bloque según docs/protocolo.md.

## Contraste de hipótesis

- **H1** (criterio: t̄_A / t̄_B ≥ 1,5 con n = 80): t̄_A / t̄_B = 5.62 → **no refutada**.
- **H2** (criterio: Ū_B − Ū_A ≥ 10 puntos con n = 80): Ū_B − Ū_A = 349.6 puntos → **no refutada**.
- **H3** (criterio: t̄_B / t̄_C ≤ 1,20 con n = 80): t̄_B / t̄_C = 0.35 → **no refutada**. Comparación indirecta: el tiempo de pared no demuestra por sí solo el comportamiento del GIL.

## Gráficos e interpretación física

- `figuras/tiempo_vs_n.png` — Tiempo de pared vs. n (log–log).
- `figuras/comparacion_n_max.png` — Comparación de estrategias para n = 80.
- `figuras/uso_cpu.png` — Uso de CPU del proceso por estrategia y n.

La interpretación física de cada gráfico se redacta a mano, con los datos reales, en `docs/informe.md` (sección 4. Resultados); este archivo solo se genera.

## Límites que se deben declarar

- `time.sleep` simula la latencia de red: no representa una red real.
- En C, `uso_cpu_pct` y `pico_mem_mib` no incluyen los procesos hijos (subestimados).
- `uso_cpu_pct` no es potencia: energía **no medida** (sin RAPL ni vatímetro). E = P̄·t.
- Resultados válidos solo para este equipo y para n entre 20 y 80.
