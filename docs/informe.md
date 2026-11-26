# Informe científico breve — Equipo __

**Título:** · **Integrantes:** · **Fecha:** · **Repositorio:**

## Resumen (≤ 150 palabras)
Problema, método, resultado principal con cifras y unidades, conclusión.

## 1. Introducción
Problema empresarial y pregunta de investigación. Principios físicos involucrados (con fórmulas y unidades).

## 2. Hipótesis
H1, H2... (copiadas de docs/hipotesis.md, sin modificarlas después de ver los datos).

## 3. Método
- Estrategias comparadas (descripción, no código completo).
- Variables independientes, dependientes y controladas.
- Entorno (tabla de docs/entorno.md). Instrumentos y su resolución.
- Protocolo: tamaños, repeticiones, calentamiento, orden aleatorio.

## 4. Resultados
_Redactó: Ana (R4, análisis). Datos: Acer Aspire A315-42, Windows 11, CPython 3.13.0, 2026-11-18. Análisis con `py -m experimentos.analisis_equipo2`._

**Bloque que se reporta.** El protocolo exige CV ≤ 10 %. El primer bloque formal (`resultados/resultados.csv`) no lo cumplió en 6 de 9 combinaciones y se repitió completo (`resultados/repeticion_cv.csv`), donde solo B con n = 40 queda en 10,9 %. Según D-005, se reporta la **repetición** como resultado principal y el primer bloque como complemento, sin descartar datos. Las tablas completas están en `resultados/analisis_repeticion_cv/analisis.md` y `resultados/analisis_resultados/analisis.md`.

**Tabla 1. Tiempo de pared por estrategia y n (repetición, 10 corridas por combinación).**

| Estrategia | n | t̄ [s] | DE [s] | CV [%] | IC 95 % [s] | Ū CPU [%] | tareas/s | S = t̄_A / t̄_X |
|---|---|---|---|---|---|---|---|---|
| A línea base | 20 | 0,470 | 0,025 | 5,4 | [0,452; 0,489] | 47 | 42,5 | 1,00 |
| B hilos | 20 | 0,094 | 0,009 | 9,8 | [0,087; 0,101] | 373 | 212,5 | 5,00 |
| C procesos | 20 | 0,625 | 0,061 | 9,8 | [0,582; 0,669] | 10* | 32,0 | 0,75 |
| A línea base | 40 | 0,994 | 0,030 | 3,0 | [0,973; 1,016] | 46 | 40,2 | 1,00 |
| B hilos | 40 | 0,190 | 0,021 | 10,9 | [0,175; 0,204] | 421 | 211,0 | 5,25 |
| C procesos | 40 | 0,696 | 0,042 | 6,1 | [0,666; 0,726] | 13* | 57,5 | 1,43 |
| A línea base | 80 | 2,134 | 0,021 | 1,0 | [2,120; 2,149] | 38 | 37,5 | 1,00 |
| B hilos | 80 | 0,353 | 0,011 | 3,1 | [0,345; 0,361] | 360 | 226,9 | 6,05 |
| C procesos | 80 | 0,881 | 0,024 | 2,8 | [0,864; 0,899] | 11* | 90,8 | 2,42 |

\* Subestimado: `time.process_time()` no cuenta el CPU de los procesos hijos.

**Gráfico 1: `resultados/analisis_repeticion_cv/figuras/tiempo_vs_n.png` (log–log, IC 95 %).** A y B crecen casi en proporción a n: al duplicar n, el tiempo se duplica (A: 0,47 → 0,99 → 2,13 s). Las dos rectas son casi paralelas porque B hace el mismo trabajo que A, solo que solapa las esperas, y queda unas 5 a 6 veces más abajo. C es casi plana (0,63 → 0,88 s): la domina un costo fijo de unos 0,54 s para crear los procesos con *spawn*. Por eso C es más lenta que A con n = 20 y la supera entre n = 20 y n = 40. Un ajuste lineal de las medias da ≈ 0,028 s por tarea en A y ≈ 0,004 s por tarea en B y en C.

**Gráfico 2: `resultados/analisis_repeticion_cv/figuras/comparacion_n_max.png` (n = 80).** B tarda 0,353 s frente a 2,134 s de A (S = 6,05) y C tarda 0,881 s (S = 2,42). Los IC 95 % no se solapan, así que las tres diferencias son claras con estos datos. El rendimiento de B (≈ 227 tareas/s) es unas 6 veces el de A (≈ 38 tareas/s): con la misma cola, el usuario recibe sus respuestas mucho antes.

**Gráfico 3: `resultados/analisis_repeticion_cv/figuras/uso_cpu.png`.** A queda por debajo de 100 % (38–47 %): mientras duerme esperando la red simulada, el procesador no trabaja, y ese es justamente el síntoma de ServiCampo. B llega a 360–421 %, es decir, en promedio hubo entre 3 y 4 núcleos ocupados a la vez dentro de un solo proceso. Esto solo es posible si los hilos calcularon el hash en paralelo, lo que indica que `hashlib.pbkdf2_hmac` libera el GIL. El 10–13 % de C no significa que C trabaje menos: el instrumento solo mide el proceso principal, que únicamente reparte tareas. %CPU no es potencia ni energía.

**Memoria (medido, corrida aparte con `tracemalloc`).** Pico de memoria Python con n = 80: A 0,002 MiB, B 0,167 MiB, C 0,196 MiB. Son valores muy pequeños; en C no incluyen la memoria de los procesos hijos.

**No medido:** temperatura y energía (sin sensor, sin RAPL ni vatímetro).

## 5. Discusión
_Redactó: Ana. Criterios copiados de `docs/hipotesis.md`, sin cambiarlos después de ver los datos._

| Hipótesis | Criterio (n = 80) | Primer bloque | Repetición | Resultado |
|---|---|---|---|---|
| H1 · tiempo de pared | t̄_A / t̄_B ≥ 1,5 | 5,62 | 6,05 | No refutada |
| H2 · uso de CPU | Ū_B − Ū_A ≥ 10 puntos | 349,6 | 322,8 | No refutada |
| H3 · hilos frente a procesos | t̄_B / t̄_C ≤ 1,20 | 0,35 | 0,40 | No refutada |

Las tres hipótesis se sostienen en los dos bloques, así que la conclusión no depende de qué bloque se tome como oficial.

**Explicación física.**
- **B (concurrencia).** Las tareas de E/S pasan casi todo su tiempo en `time.sleep`, que libera el GIL. Con 8 hilos, hasta 8 esperas transcurren a la vez y el tiempo muerto se solapa. Además `pbkdf2_hmac` también libera el GIL, así que las tareas de CPU corrieron en varios núcleos. Por eso B ganó en las dos partes de la carga y no solo en la E/S.
- **C (paralelismo).** Cada proceso tiene su propio intérprete y su propio GIL, así que reparte el hash entre núcleos. Pero en Windows cada proceso arranca un Python nuevo (*spawn*), y ese costo fijo (≈ 0,5 s) está dentro del tiempo medido porque el usuario también lo esperaría. Con las cargas de este experimento, ese costo no alcanza a compensarse frente a B.
- **H3 es una comparación indirecta.** El tiempo de pared no prueba por sí solo cómo se comporta el GIL. La evidencia más directa es el uso de CPU de B por encima de 100 %.

**Limitaciones y amenazas a la validez.**
- `time.sleep` es un modelo de la red: siempre dura lo programado, sin errores ni variabilidad real.
- C tiene la CPU y la memoria subestimadas porque `labmedicion` no ve a los procesos hijos.
- El primer bloque tuvo CV de hasta 48 % (B, n = 20) y 38 % (C, n = 80). La revisión retrospectiva no encontró una causa documentada ni un registro por corrida de aplicaciones abiertas o calentamiento; por tanto, no se atribuye la variabilidad a una causa específica. C/n=80/repetición 1 duró 2,263765 s y es extremo por Tukey. Se conserva, como todas las mediciones, y se reportan ambos bloques.
- El equipo de medición cambió del Lenovo al Acer antes del bloque formal (enmienda documentada en `docs/hipotesis.md` y `docs/protocolo.md`); todos los datos formales vienen del Acer y no se comparan equipos distintos.
- Los resultados valen solo para este equipo, CPython 3.13.0, carga 50 % E/S y 50 % CPU, 8 trabajadores y n entre 20 y 80.
- Energía no medida: aunque B es más rápida, usa más núcleos a la vez (más potencia instantánea), y como E = P̄·t no se puede afirmar que gaste menos energía.

## 6. Propuesta de mejora para la empresa
Recomendación cuantificada, condiciones en que es válida y riesgos.

## 7. Conclusiones

## 8. Referencias (verificables)
## Anexo: uso de IA (resumen de docs/uso_ia.md)
