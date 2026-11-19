# Línea base secuencial

La línea base representa la situación inicial del caso ServiCampo: atender una
cola de tareas de una en una. Es la referencia para comparar las estrategias
con hilos y procesos.

## Funciones e interfaz

- `preparar(n, proporcion_es=0.5, semilla=2)` crea y devuelve una lista de
  `n` tareas con formato `(tipo, id_tarea, latencia)`. `tipo` es `"es"` para
  una tarea de entrada/salida o `"cpu"` para una tarea de cálculo. La semilla
  fija el generador aleatorio, por lo que las mismas entradas producen la
  misma lista. La preparación ocurre antes de medir la ejecución.
- `ejecutar(tareas) -> int` recorre la lista secuencialmente y devuelve la
  cantidad de tareas completadas. Esta misma firma debe conservarse en las
  estrategias A, B y C.

La firma común del experimento es:

```python
preparar(n) -> tareas       # preparación; no se incluye en el cronómetro
ejecutar(tareas) -> int     # ejecución; sí se mide
```

En las tareas `"es"`, `tarea_es` llama `time.sleep(latencia)`. La latencia
simulada se elige entre 0,02 y 0,06 segundos. Durante esa espera el hilo queda
bloqueado y la CPU puede atender otro trabajo; no se está consultando una red
real. En las tareas `"cpu"`, `tarea_cpu` ejecuta
`hashlib.pbkdf2_hmac("sha256", ...)` con 20 000 iteraciones, trabajo de
cómputo.

## Cómo ejecutarla

Desde la raíz del repositorio:

```powershell
py -3 -m src.linea_base
```

El bloque `__main__` prepara 40 tareas para cada condición (solo E/S y solo
CPU), mide el tiempo de pared con `time.perf_counter()` y el tiempo de CPU del
proceso con `time.process_time()`, y muestra ambos y su razón porcentual.
`py -3` es la forma usada en este equipo Windows; en otro entorno puede
ejecutarse con `python -m src.linea_base`.

## Límite de interpretación

El tiempo de pared incluye tanto el trabajo como las esperas observadas por el
usuario; el tiempo de CPU cuenta el tiempo de procesador consumido por el
proceso. Por eso una tarea con `time.sleep` puede aumentar el tiempo de pared
sin aumentar de forma similar el tiempo de CPU. La carga de E/S es una
simulación, no representa latencia ni comportamiento de un servicio externo
real. El porcentaje CPU/pared no es potencia eléctrica; sin medir energía no
se puede concluir que una estrategia ahorre energía.
