# Análisis de resultados — Equipo 2

Fuente: `resultados/repeticion_cv.csv`. Solo corridas de tiempo (`medicion_memoria = no`); la memoria sale de la corrida separada (repetición 0). Latencia de E/S simulada con time.sleep · un solo equipo.

| Estrategia | n | reps | t̄ [s] | DE [s] | CV [%] | IC 95 % [s] | Tukey | Ū CPU [%] | tareas/s | S | pico mem [MiB] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A_linea_base | 20 | 10 | 0.470 | 0.025 | 5.4 | [0.452; 0.489] | 1 | 47 | 42.5 | 1.00 | 0.002 |
| B_hilos | 20 | 10 | 0.094 | 0.009 | 9.8 | [0.087; 0.101] | 0 | 373 | 212.5 | 5.00 | 0.063 |
| C_procesos | 20 | 10 | 0.625 | 0.061 | 9.8 | [0.582; 0.669] | 0 | 10 | 32.0 | 0.75 | 0.081 |
| A_linea_base | 40 | 10 | 0.994 | 0.030 | 3.0 | [0.973; 1.016] | 0 | 46 | 40.2 | 1.00 | 0.002 |
| B_hilos | 40 | 10 | 0.190 | 0.021 | 10.9 | [0.175; 0.204] | 0 | 421 | 211.0 | 5.25 | 0.098 |
| C_procesos | 40 | 10 | 0.696 | 0.042 | 6.1 | [0.666; 0.726] | 0 | 13 | 57.5 | 1.43 | 0.122 |
| A_linea_base | 80 | 10 | 2.134 | 0.021 | 1.0 | [2.120; 2.149] | 0 | 38 | 37.5 | 1.00 | 0.002 |
| B_hilos | 80 | 10 | 0.353 | 0.011 | 3.1 | [0.345; 0.361] | 0 | 360 | 226.9 | 6.05 | 0.167 |
| C_procesos | 80 | 10 | 0.881 | 0.024 | 2.8 | [0.864; 0.899] | 0 | 11 | 90.8 | 2.42 | 0.196 |

## Calidad de los datos (criterio del protocolo: CV ≤ 10 %)

- B_hilos n = 40: CV = 10.9 % > 10 % → revisar incidentes y repetir el bloque según docs/protocolo.md.

## Contraste de hipótesis

- **H1** (criterio: t̄_A / t̄_B ≥ 1,5 con n = 80): t̄_A / t̄_B = 6.05 → **no refutada**.
- **H2** (criterio: Ū_B − Ū_A ≥ 10 puntos con n = 80): Ū_B − Ū_A = 322.8 puntos → **no refutada**.
- **H3** (criterio: t̄_B / t̄_C ≤ 1,20 con n = 80): t̄_B / t̄_C = 0.40 → **no refutada**. Comparación indirecta: el tiempo de pared no demuestra por sí solo el comportamiento del GIL.

## Gráficos e interpretación física

Las figuras existentes en `figuras/` se conservan. No se regeneraron en esta ejecución porque `matplotlib` no está instalado en el entorno; la interpretación está en `docs/informe.md` (sección 4).


## Límites que se deben declarar

- `time.sleep` simula la latencia de red: no representa una red real.
- En C, `uso_cpu_pct` y `pico_mem_mib` no incluyen los procesos hijos (subestimados).
- `uso_cpu_pct` no es potencia: energía **no medida** (sin RAPL ni vatímetro). E = P̄·t.
- Resultados válidos solo para este equipo y para n entre 20 y 80.
