# Variables experimentales — Equipo 2

## Variables

| Tipo | Variable | Símbolo | Unidad | Valores / rango | Instrumento o forma de obtención | Justificación |
|---|---|---|---|---|---|---|
| Independiente | Estrategia | — | — | A (secuencial), B (hilos), C (según la implementación que integre Ana) | Identificador de estrategia en el CSV | Contrasta cómo cambia el rendimiento al variar la forma de ejecutar las mismas tareas. |
| Independiente | Tamaño de entrada | n | tareas | 20, 40, 80 | `linea_base.preparar(n, semilla=2)` | Permite comparar el crecimiento del costo en tres cargas distintas. |
| Dependiente | Tiempo de pared | t | s | valor medido | `time.perf_counter()` | Mide el tiempo transcurrido para completar una ejecución. |
| Dependiente | Uso de CPU del proceso | U | % | valor medido; puede superar 100 % con varios núcleos | `cpu_proceso_s / tiempo_s * 100` | Expresa tiempo de CPU consumido respecto al tiempo de pared; no es potencia eléctrica. |
| Dependiente | Pico de memoria Python | M | MiB | valor medido | `tracemalloc`, en corrida separada | Compara memoria asignada por el intérprete; no incluye toda la memoria nativa ni la del sistema. |
| Dependiente opcional | Temperatura | θ | °C | no disponible en este equipo | `herramientas.sensores`; sin sensor, no se mide | Se reporta como no medida; no se sustituye por una estimación. |
| Dependiente opcional | Energía | E | J | no disponible en este equipo | RAPL o vatímetro; ninguno disponible confirmado | No se afirma ahorro de energía a partir del porcentaje de CPU. |
| Controlada | Equipo | — | — | Lenovo 10VUS1SK00; AMD Ryzen 5 PRO 2400G, 4 núcleos físicos / 8 lógicos; Windows 10 | Diagnóstico local de Windows | Se mantendrá el mismo computador durante la comparación. |
| Controlada | Python | — | — | CPython 3.14.7 | `python --version` / `py -3 --version` | La versión puede afectar intérprete, bibliotecas y rendimiento. |
| Controlada | Alimentación y perfil | — | — | Corriente confirmada por Jeff el 2026-11-18; reconfirmar en la corrida formal. Perfil equilibrado por verificar | Verificación física y configuración de Windows | Evita cambios de frecuencia y ahorro energético entre estrategias. |
| Controlada | Programas abiertos | — | — | Por fijar antes de la corrida formal; cerrar aplicaciones no esenciales | Registro en `docs/entorno.md` | La actividad en segundo plano puede competir por CPU y memoria. |
| Controlada | Datos de entrada | — | — | Semilla 2, misma lista de tareas para A/B/C de cada n | `linea_base.preparar(n, semilla=2)` | Aísla el efecto de la estrategia y conserva la misma mezcla de tareas y latencias. |

## Mapa de dependencias

```text
Estrategia → forma de ejecutar tareas → solapamiento de esperas de E/S → tiempo de pared t
Estrategia → concurrencia de tareas CPU y E/S → CPU del proceso / tiempo de pared → uso de CPU U
Estrategia → objetos y estructuras simultáneos → asignaciones Python → pico de memoria M
n → cantidad de tareas E/S y CPU → trabajo total y recursos utilizados → t, U y M
Semilla 2 → tipo y latencia de cada tarea → carga de trabajo que recibe cada estrategia
```

La función `pbkdf2_hmac` puede liberar el GIL. Por eso no suponemos que los hilos sean incapaces de acelerar trabajo de CPU; el resultado se medirá en este equipo de 4 núcleos físicos y 8 lógicos.

## Variables no controladas y mitigación

| Variable no controlada | Efecto posible | Mitigación |
|---|---|---|
| Frecuencia dinámica, turbo y temperatura | Cambian el tiempo de CPU entre corridas | Mismo perfil de energía, equipo conectado a corriente si es posible, una corrida de calentamiento y registro de incidentes. Temperatura no disponible: no atribuir resultados a una lectura térmica inexistente. |
| Procesos del sistema operativo y tareas en segundo plano | Compiten por CPU, memoria o disco | Cerrar aplicaciones no esenciales, no usar el PC durante la medición, aleatorizar el orden y repetir si CV > 10 %. |
| Cachés y estado inicial del intérprete | Pueden modificar las primeras corridas | Una corrida de calentamiento por estrategia antes de registrar resultados. |
| Variación temporal del sistema | Produce deriva entre estrategias | Orden aleatorio reproducible con semilla 42 y diez repeticiones por combinación. |
