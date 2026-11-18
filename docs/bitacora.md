# Bitácora de decisiones y control experimental

En esta bitácora registramos las decisiones antes de medir y anotamos cualquier cambio de configuración. No sustituimos datos observados por valores esperados.

## Decisiones del protocolo

| Fecha | Decisión | Motivo / estado |
|---|---|---|
| 2026-11-09 | Comparamos E0 secuencial, E1 hilos, E2 asyncio y E3 procesos | Incluimos una línea base y tres estrategias alternativas |
| 2026-11-09 | Preparamos las tareas deterministas antes de iniciar cada cronómetro | Evitamos medir la preparación de los datos como parte de la ejecución |
| 2026-11-09 | Medimos el tiempo de pared con `time.perf_counter()` | Usamos un reloj monotónico de alta resolución para el tiempo transcurrido |
| 2026-11-09 | En E3 sumamos el CPU del proceso principal y los tiempos de CPU de los hijos | `time.process_time()` del proceso principal no incluye los procesos hijos |
| 2026-11-09 | Dejamos `time.sleep()` explícitamente como modelo de espera de red | La prueba no realiza solicitudes externas ni mide una red real |
| 2026-11-09 | No anotamos una salida inventada para la línea base | El checkout inicial no contenía `src/linea_base.py`; el lanzador `py` permitió ejecutar una prueba pequeña del ejecutor, no la línea base |
| 2026-11-09 | Validamos el ejecutor con una prueba técnica pequeña | Usamos 4 tareas, 3 proporciones E/S, 2 repeticiones y 2 iteraciones de hash; confirmó el formato del CSV, pero no la usamos como resultado del estudio y borramos su archivo temporal |
| 2026-11-09 | No tomamos ni conservamos resultados de estudio | La hipótesis aún debe guardarse en un commit antes de iniciar corridas experimentales |

## Registro de una serie de corridas

Completemos una fila por serie. Guardamos el comando exacto, su semilla y la salida para reproducirla.

| Fecha y hora | Commit de hipótesis | Comando / configuración | Equipo y Python | N repeticiones | Archivo de resultados | Observaciones |
|---|---|---|---|---:|---|---|
| Pendiente | Pendiente: registrar el commit anterior a medir | Pendiente | CPython 3.14.7; 8 CPU lógicas reportadas; confirmar en el equipo de corridas | 30 por defecto | `results/resultados.csv` | Sin medición de estudio registrada |

## Checklist de control de variables

Antes de cada serie, verificamos y marcamos:

- [ ] Mismo equipo y conectado a corriente.
- [ ] Cerramos aplicaciones ajenas al experimento; no iniciamos otras tareas intensivas.
- [ ] Registramos y mantenemos la misma versión e implementación de Python.
- [ ] Registramos sistema operativo, CPU y cantidad de CPU lógicas con `python -m src.documentar_entorno` (o `py -m` en Windows si hace falta).
- [ ] Usamos la misma semilla y la misma lista preparada para todas las estrategias de cada condición.
- [ ] Usamos la misma latencia de `time.sleep()` y la misma función, entrada y cantidad de iteraciones de hash.
- [ ] Hacemos un calentamiento de cada estrategia que no se incorpora al CSV.
- [ ] Aleatorizamos el orden de las estrategias en cada repetición.
- [ ] Ejecutamos 30 repeticiones por condición, o anotamos la cantidad distinta antes de medir.
- [ ] Registramos el comando completo, incluyendo los argumentos que no sean los predeterminados.
- [ ] Conservamos la salida de `python -m src.linea_base` y el CSV sin editar los valores medidos.
- [ ] Confirmamos que el commit de hipótesis se creó antes de la primera medición y que el trabajo sigue el flujo de issue, rama y PR revisado del curso.

## Plantilla para observaciones

| Fecha y hora | Condición / estrategia | Observación o desviación | Acción tomada |
|---|---|---|---|
| Pendiente | Pendiente | Pendiente | Pendiente |
