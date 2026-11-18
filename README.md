# Equipo 2 — Concurrencia y procesamiento de tareas

> Proyecto: *Laboratorio colaborativo de rendimiento y eficiencia computacional desde la física aplicada*
> Física Aplicada al Desarrollo de Software · SENA · ADSO · 7.º trimestre

## 1. Problema empresarial
**Empresa (caso simulado):** ServiCampo Ltda., plataforma que consulta servicios externos de clima y precios agrícolas

La cola de solicitudes se atiende una por una. Los usuarios esperan varios segundos aunque el servidor reporta la CPU casi ociosa.

## 2. Situación inicial medible
src/linea_base.py ejecuta secuencialmente tareas de E/S (espera) y de CPU (hash).

| Medición preliminar (Clase 3) | Valor | Unidad |
|---|---|---|
| n utilizado | 40 por condición | tareas |
| Tiempo de pared (1 corrida por condición) | Solo E/S: 1.71; solo CPU: 0.37 | s |
| Equipo y fecha | Lenovo 10VUS1SK00 · Ryzen 5 PRO 2400G · 2026-11-18 | — |

Salida literal de `py -3 -m src.linea_base` (el programa hace una corrida de n = 40 para cada condición):

```text
Could not find platform independent libraries <prefix>
solo E/S  pared = 1.71 s   CPU = 0.00 s   CPU/pared =   0.0 %
solo CPU  pared = 0.37 s   CPU = 0.36 s   CPU/pared =  97.1 %
```

## 3. Pregunta de investigación
_¿Cómo cambia el tiempo de pared (s), el uso de CPU (%) y el pico de memoria (MiB) al cambiar la estrategia A/B/C y n = 20, 40, 80 tareas, manteniendo el equipo, Python, los datos de semilla 2, la alimentación y los programas abiertos?_

## 4. Hipótesis
Ver [docs/hipotesis.md](docs/hipotesis.md).

## 5. Estrategias
| Id | Estrategia | Idea principal | Efecto físico esperado | Responsable |
|---|---|---|---|---|
| A | Línea base secuencial | Atiende las tareas una por una | Referencia sin solapamiento de esperas | Julian |
| B | Con hilos (`src/estrategia_b.py`, `ThreadPoolExecutor`, 8 hilos) · rama *sin esperas ociosas → concurrencia* | Varias tareas en curso a la vez: mientras un hilo duerme esperando la red simulada, otro avanza. `time.sleep` libera el GIL, así que las esperas se solapan | Menor tiempo de pared sin más trabajo total: el tiempo de E/S pasa de ≈ Σ latencias a ≈ Σ latencias / 8. Si `pbkdf2_hmac` libera el GIL, el hash también corre en varios núcleos y `uso_cpu_pct` puede superar 100 % | Ana |
| C | Con procesos (`src/estrategia_c.py`, `ProcessPoolExecutor`, 8 procesos) · rama *repartir trabajo → multinúcleo* | Cada proceso tiene su propio intérprete y su propio GIL: el trabajo de CPU se reparte entre núcleos (paralelismo) y las esperas también se solapan | Menor tiempo de pared solo si el trabajo de CPU supera el costo fijo de crear procesos (*spawn* en Windows) y serializar datos; con n pequeño puede ser más lento que A. Más núcleos activos implican más potencia instantánea, así que más rápido no significa menos energía (E = P̄·t) | Ana |

**Concurrencia vs. paralelismo.** B es concurrencia: aprovecha el tiempo en que la CPU estaba ociosa esperando, incluso con un solo núcleo. C es paralelismo: ejecuta trabajo de CPU en el mismo instante en núcleos distintos. Por eso están en ramas distintas del mapa de optimización y no son dos versiones de la misma idea.

**El GIL.** En CPython un proceso ejecuta bytecode Python en un solo hilo a la vez. `time.sleep` y algunas funciones en C (como `hashlib.pbkdf2_hmac`) lo liberan mientras trabajan. Una prueba informal (una corrida, en otro PC, n = 40 solo CPU) mostró B con una razón CPU/pared de ≈ 365 %, señal de que el hash sí corrió en varios hilos a la vez. **No es un resultado del experimento:** lo decide la medición formal en el equipo de Jeff.

**Límites de medición de C.** `labmedicion` mide `cpu_proceso_s` con `time.process_time()`, que solo cuenta el proceso principal, y `tracemalloc` no ve la memoria de los hijos. En C, `uso_cpu_pct` y `pico_mem_mib` quedan **subestimados** y así deben reportarse.

**Corrección.** B y C usan `preparar(n)` de la línea base (la preparación no se mide) y `ejecutar(tareas)` devuelve el número de tareas completadas; además verifican que cada tarea devolvió su propio id. `experimentos/ejecutar_experimento.py` compara cada estrategia con la línea base antes de medir.

## 6. Cómo reproducir
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt                          # opcional: psutil, matplotlib
python -m src.linea_base                                 # situación inicial
python -m unittest discover -s pruebas                   # corrección
python -m experimentos.ejecutar_experimento              # experimento formal -> resultados/resultados.csv
python ruta/a/analizar_resultados.py resultados/resultados.csv
```
En este Windows, `python` no está en PATH; usar `py -3 -m ...` como equivalente.

## 7. Integrantes y roles
| Rol | Integrante | Responsabilidad principal |
|---|---|---|
| R1 — Coordinación y protocolo experimental | Jeff | Mantiene el protocolo, controla variables y coordina issues y planeación. |
| R2 — Desarrollo de estrategia base | Julian | Comprende y documenta la línea base y verifica la corrección. |
| R3 — Estrategias alternativas y optimización | Ana | Implementa las estrategias alternativas y justifica los cambios esperados. |
| R4 — Automatización de mediciones y análisis | Jeff (entorno y ejecución); Ana (análisis y gráficos) | Automatiza/ejecuta mediciones, documenta el entorno y analiza resultados. |

Los roles son flexibles: **todos** participan en la comprensión física y en el código.

## 8. Documentación
- [Variables](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md)
- [Decisiones técnicas](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

## 9. Resultados y conclusiones (Clase 5)
_Resumen de máximo 5 líneas con cifras, unidades e intervalo de confianza._
# Clase_Fisica_Grupo2
