# Hipótesis — Equipo 2

Las predicciones se registran antes de medir. Se compararán las estrategias A y B con las mismas tareas para cada n; C se incluirá cuando su implementación esté integrada y supere las pruebas de corrección. La computadora disponible tiene 4 núcleos físicos y 8 lógicos. No suponemos que `pbkdf2_hmac` mantenga el GIL: puede liberar el GIL y permitir que los hilos ejecuten trabajo de CPU concurrentemente.

## H1 — Tiempo de pared

> **Si** sustituyo la estrategia secuencial A por la estrategia B con hilos para n = 80, **entonces** la razón entre el tiempo medio de A y el de B será al menos 1,5 (B tardará como máximo dos tercios de A), **porque** las esperas simuladas de E/S pueden solaparse y, si `pbkdf2_hmac` libera el GIL, parte del trabajo de CPU también podría ejecutarse en paralelo, **manteniendo** las mismas 80 tareas preparadas con semilla 2, el equipo, Python 3.14.7, la alimentación, los programas abiertos y el protocolo de diez repeticiones.

**La refutaríamos** si la razón entre los tiempos medios A/B para n = 80 es menor que 1,5; también quedaría refutada si B tarda más que A. El tiempo se toma de las diez corridas de tiempo, no de la corrida separada de memoria.

## H2 — Uso de CPU

> **Si** sustituyo A por B con hilos para n = 80, **entonces** el uso medio de CPU del proceso de B aumentará al menos 10 puntos porcentuales respecto de A, **porque** mientras unas tareas esperan E/S otras pueden ejecutar el hash; en este equipo de 4 núcleos físicos y 8 lógicos, la liberación del GIL por `pbkdf2_hmac` también podría permitir trabajo de CPU concurrente, **manteniendo** la misma carga y semilla 2, equipo, versión de Python, alimentación, programas abiertos y protocolo de diez repeticiones.

**La refutaríamos** si el promedio de `uso_cpu_pct` de B menos el de A es inferior a 10 puntos porcentuales. `uso_cpu_pct` es tiempo de CPU del proceso dividido por tiempo de pared; puede superar 100 % al utilizar varios núcleos y no representa potencia ni energía.

## H3 — Procesos frente a hilos y efecto del GIL

> **Si** comparo B (hilos) con C (procesos) para n = 80 con la carga mixta fija del experimento, **entonces** el tiempo medio de pared de B no superará en más de 20 % al de C (`media_B / media_C ≤ 1,20`), **porque** `hashlib.pbkdf2_hmac` puede liberar el GIL y permitir que los hilos ejecuten cómputo concurrentemente, mientras que C incurre en el costo de crear procesos, **manteniendo** la misma carga y semilla 2, ocho trabajadores, equipo, versión de Python, alimentación, programas abiertos y protocolo de diez repeticiones.

**La refutaríamos** si `media_B / media_C > 1,20`. Es una comparación indirecta: el tiempo de pared por sí solo no demuestra el comportamiento del GIL, y el costo de arranque de procesos también afecta a C. El CPU medido para C no sirve para esta comparación porque `time.process_time()` no incluye el CPU de los procesos hijos.

## Condiciones fijadas antes de medir

- **Fecha de registro:** 2026-11-18.
- **VI:** estrategia (A/B/C) y tamaño n (20, 40, 80 tareas); en H3 se compara específicamente B y C para n = 80.
- **VD para contrastar estas hipótesis:** tiempo de pared (s) y uso de CPU del proceso (%).
- **Controles:** carga mixta con proporción E/S predeterminada de 0,5, ocho trabajadores en B y C, equipo, Python, alimentación, programas abiertos, tareas generadas con semilla 2, calentamiento, orden aleatorio con semilla 42 y diez repeticiones por combinación.
- **Energía:** no se medirá con RAPL ni vatímetro; no se afirmará ahorro energético.
