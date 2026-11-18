# Hipótesis previas a la medición

**Estado:** predicciones redactadas el 9 de noviembre de 2026. Aún no están en un commit; siguiendo las reglas del curso, no iniciaremos corridas experimentales hasta guardar la hipótesis en un commit fechado. En esta sesión solo hicimos una prueba pequeña para verificar que el ejecutor corre y genera el CSV; no la usaremos como resultado experimental.

Estas predicciones corresponden a la carga del ejecutor descrita abajo, no a una equivalencia verificada con `src/linea_base.py`: ese archivo no estaba presente en el checkout disponible al preparar el documento. Antes de presentar las cifras como comparación con la línea base del proyecto, verificaremos que su función hash y sus tareas coincidan con el protocolo o ajustaremos el ejecutor antes del commit de hipótesis.

## H1: solapar esperas de E/S

**Hipótesis:** Si pasamos de E0 secuencial con un trabajador a E1 hilos o E2 asyncio con cuatro trabajadores, entonces el tiempo de pared (`t_pared_s`, s) para 32 tareas 100 % E/S, con latencia de 0.1 s, será al menos cuatro veces menor: esperamos `t_pared_s ≤ 0.8 s`, frente a `3.2 s` de espera secuencial ideal, porque mientras unas tareas esperan, los hilos o el event loop pueden avanzar otras. Este contraste cambia conjuntamente la estrategia y el número de trabajadores; mantenemos la misma lista de 32 tareas, la semilla 42, la latencia de 0.1 s y el equipo.

**Predicción numérica:** E0: `32 × 0.1 s = 3.2 s` de espera simulada; E1 y E2: `t_pared_s ≤ 0.8 s` con cuatro trabajadores. Son valores ideales de la carga de `sleep`, no resultados medidos; el tiempo observado puede incluir sobrecarga de planificación.

**La refutaría:** que, en las repeticiones, la mediana de `t_pared_s` de E1 o E2 supere `0.8 s` en esa condición, después de confirmar que se ejecutaron 32 tareas con la misma latencia y que la medición incluye las mismas fases.

## H2: procesos frente a hilos en una carga de CPU

**Hipótesis:** Si cambiamos E1 hilos por E3 procesos, entonces el tiempo de pared (`t_pared_s`, s) para 32 tareas 100 % CPU será al menos 20 % menor en E3: esperamos `t_pared_s(E3) ≤ 0.80 × t_pared_s(E1)`, porque cada hash procesa una entrada de 1024 bytes (menor que el umbral de 2048 bytes a partir del cual `hashlib` puede liberar el GIL en una llamada), y procesos distintos pueden ejecutar trabajo en núcleos diferentes; mantenemos la misma lista de tareas, semilla 42, 20 000 iteraciones de hash por tarea, equipo y 8 trabajadores (las 8 CPU lógicas que reporta este entorno).

**Predicción numérica:** la razón `t_pared_s(E3) / t_pared_s(E1)` será `≤ 0.80` (20 % o más de reducción). El entorno consultado reporta 8 CPU lógicas; confirmaremos ese dato en el equipo donde corramos el experimento. La predicción también depende de que la carga de CPU sea bastante grande para que la creación y coordinación de procesos no elimine la ganancia.

**La refutaría:** que la mediana de esa razón sea mayor que `0.80`, o que E3 tarde igual o más que E1. También revisaremos la hipótesis si el código real de la línea base procesa bloques grandes en una sola llamada de hash: algunas funciones de hash liberan el GIL con datos grandes, por lo que procesos no tienen garantizada una ventaja frente a hilos.

## Alcance de las afirmaciones físicas

`t_pared_s` mide el tiempo transcurrido y `t_cpu_s` el tiempo de CPU contabilizado; no son la misma magnitud. Mientras `time.sleep()` espera, modelamos una CPU que puede quedar ociosa, pero no medimos potencia eléctrica ni temperatura. No presentaremos potencia o temperatura como resultados medidos de este protocolo.
