# Variables del experimento

En nuestro experimento comparamos la estrategia de ejecución y la composición de una misma carga. Conservamos iguales la lista de tareas, la semilla, la latencia configurada y el equipo para que esos factores no expliquen las diferencias observadas.

## Variables independientes (VI)

| Variable | Valores o definición | Unidad |
|---|---|---|
| Estrategia de ejecución | E0 secuencial, E1 hilos, E2 asyncio, E3 procesos | Categoría (sin unidad) |
| Proporción de tareas de E/S (`pct_es`) | Porcentaje de tareas de espera en la carga; el resto son tareas de CPU | % |
| Número de trabajadores (`n_trabajadores`) | Hilos, concurrencia máxima de asyncio o procesos; E0 usa 1 | trabajadores |

En E2, `n_trabajadores` representa el límite de tareas simultáneas, no el número de hilos del event loop.

## Variables dependientes (VD)

| Variable | Cómo la obtenemos | Unidad |
|---|---|---|
| Tiempo de pared (`t_pared_s`) | Diferencia de `time.perf_counter()` al ejecutar una carga | s |
| Tiempo de CPU (`t_cpu_s`) | CPU del proceso principal; en E3, añadimos el CPU de los procesos hijos | s |
| Razón CPU/pared (`razon_cpu_pared_pct`) | `100 × t_cpu_s / t_pared_s` | % |
| Rendimiento (`tareas_por_s`) | Número de tareas / tiempo de pared | tareas/s |

El tiempo de CPU agregado puede ser mayor que el tiempo de pared en E3; por ello, la razón CPU/pared puede superar el 100 %. `time.process_time()` por sí solo no incluye el CPU de procesos hijos.

## Variables controladas (VC)

| Variable controlada | Cómo la mantenemos constante | Unidad |
|---|---|---|
| Lista y cantidad de tareas | Preparamos la carga una vez por combinación de semilla y proporción, fuera de la medición, y la reutilizamos en todas las estrategias | tareas |
| Semilla (`semilla`) | Usamos el mismo valor para preparar y ordenar de manera reproducible | entero (sin unidad) |
| Latencia simulada (`latencia_sim_s`) | Usamos el mismo `time.sleep()` por tarea de E/S | s |
| Equipo | Repetimos las pruebas en el mismo equipo | No aplica |
| Versión e implementación de Python y sistema operativo | Las registramos en el informe de entorno y no las cambiamos durante la serie | versión (sin unidad) |
| Condición de ejecución | Conectamos el equipo a corriente, cerramos aplicaciones ajenas y aplicamos calentamiento, orden aleatorio y el mismo número de repeticiones | No aplica |
| Carga de CPU | Usamos la misma función hash, tamaño de entrada y cantidad de iteraciones por tarea | bytes y iteraciones |

## Mapa VI → mecanismo → VD

| VI | Mecanismo que ponemos a prueba | VD que esperamos observar |
|---|---|---|
| Estrategia | Los hilos y asyncio pueden solapar esperas; los procesos pueden ejecutar trabajo de CPU en paralelo en núcleos distintos. El resultado también depende del GIL y del costo de crear o coordinar trabajadores | `t_pared_s`, `t_cpu_s`, `razon_cpu_pared_pct`, `tareas_por_s` |
| Proporción E/S:CPU | Más esperas simuladas ofrecen más tiempo de espera que se puede solapar; más cómputo aumenta el trabajo que requiere CPU | Las cuatro VD |
| Número de trabajadores | Cambia cuántas tareas pueden esperar o ejecutarse simultáneamente; por encima de los recursos disponibles puede aumentar la contención y el costo de coordinación | Las cuatro VD |
