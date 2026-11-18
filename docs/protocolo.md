# Protocolo experimental reproducible

**Responsable:** Jeff (R1/R4) · **Revisión:** Ana (rueda de revisión) · **Versión:** 1 · **Fecha:** 2026-11-18

## 1. Objetivo

Comparar cómo cambian el tiempo de pared, el uso de CPU y el pico de memoria al ejecutar la misma carga de tareas de forma secuencial (A) y con las estrategias alternativas (B y C), para n = 20, 40 y 80.

## 2. Preparación del entorno (antes de cada sesión)

1. Usar el mismo computador: AMD Ryzen 5 PRO 2400G, 4 núcleos físicos y 8 lógicos, Windows 10 y CPython 3.14.7.
2. Confirmar y anotar conexión a corriente y perfil de energía. Jeff confirmó conexión a corriente el 2026-11-18; volver a verificarla al empezar la corrida formal.
3. Cerrar aplicaciones no esenciales y sincronizadores; no usar el equipo durante la medición. Anotar las aplicaciones que deban permanecer abiertas.
4. Ejecutar el diagnóstico disponible y guardar su salida en `docs/entorno.md`. El script de Drive `diagnostico_entorno.py` no está en la copia de trabajo actual; no reemplazar su salida por una salida inventada.
5. Confirmar que las estrategias A, B y C estén integradas, que las pruebas de corrección pasen y que la hipótesis ya tenga un commit anterior a la medición.
6. El ejecutor prepara una lista de tareas determinista con semilla 2 por cada n y entrega la misma lista a cada estrategia. No se genera la carga dentro del intervalo cronometrado.

## 3. Procedimiento

| Paso | Acción | Comando | Evidencia |
|---|---|---|---|
| 1 | Pruebas de corrección | `py -3 -m unittest discover -s pruebas` (Windows) | Resultado de pruebas |
| 2 | Prueba de humo después de integrar el PR de Ana | `py -3 -m experimentos.ejecutar_experimento --rapido` | CSV con filas de A, B y C |
| 3 | Revisar el CSV de humo | Abrir `resultados/resultados.csv` | Encabezado y al menos una fila por estrategia |
| 4 | Experimento formal | `py -3 -m experimentos.ejecutar_experimento` | `resultados/resultados.csv` y `resultados/resultados.entorno.json` |
| 5 | (Opcional) monitoreo solicitado al instructor | Ejecutar `monitor_sistema.py` en otra terminal | Archivo de monitoreo y nota en incidentes |

El comando `py -3` se usa en este equipo porque `python` no está disponible en PATH. En plataformas donde sí lo esté, equivale a `python -m ...`.

## 4. Parámetros

- **Tamaños:** `TAMANOS = [20, 40, 80]`. Son tres niveles de carga, como mínimo exige la rúbrica. Permiten observar tendencias al duplicar n y distinguir costos pequeños, intermedios y mayores sin hacer excesivamente larga cada sesión.
- **Repeticiones:** `REPETICIONES = 10` por combinación estrategia/tamaño. Supera el mínimo de cinco de la rúbrica y permite calcular media, desviación estándar y coeficiente de variación (CV).
- **Calentamiento:** una ejecución no registrada por estrategia, con n = 20, antes de registrar resultados. Reduce el efecto de inicialización y cachés.
- **Orden:** aleatorio y reproducible con semilla 42, para reducir sesgos por deriva térmica o cambios temporales.
- **Memoria:** corrida separada con `tracemalloc`; el ejecutor la registra con repetición 0. No mezclar ese tiempo con los tiempos sin instrumentación.

## 5. Calidad y análisis de datos

- Calcular `CV = desviación estándar / media × 100 %` para cada estrategia y n.
- Si `CV ≤ 10 %`, conservar y reportar el conjunto como estable según el criterio del protocolo.
- Si `CV > 10 %`, no ocultar ni descartar corridas: revisar incidentes, reportar el CV y repetir el bloque completo en un archivo aparte (por ejemplo, `--salida resultados/repeticion_cv.csv`).
- Para señalar atípicos usar Tukey: `IQR = Q3 − Q1`; valores menores que `Q1 − 1.5 × IQR` o mayores que `Q3 + 1.5 × IQR` se reportan. Solo excluir un dato si existe una causa documentada, dejando constancia del valor y motivo.
- No interpretar `uso_cpu_pct` como potencia. Sin RAPL o vatímetro, la energía queda como “no medida”.

## 6. Registro de incidentes

| Fecha/hora | Incidente (p. ej. actualización del SO, batería o aplicación inesperada) | Corridas afectadas | Decisión |
|---|---|---|---|
| — | Sin experimento formal todavía | — | Registrar aquí cada incidente durante las corridas |
