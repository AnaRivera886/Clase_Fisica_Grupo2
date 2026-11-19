# Registro de decisiones técnicas (ADR breve)

Cada decisión importante se registra aquí y se enlaza desde el issue o PR correspondiente.

## D-001 — Estrategias alternativas: B con hilos y C con procesos, 8 trabajadores
- **Fecha:** 2026-11-18 · **Autor(es):** Ana · **Issue/PR:** PR `feat/estrategias-b-c`
- **Contexto:** el enunciado pide al menos tres estrategias comparables (la línea base cuenta) y propone tres direcciones: hilos, asyncio y procesos. La Guía de errores frecuentes advierte que no deben ser la misma idea.
- **Opciones consideradas:** 1) B hilos + C asyncio. 2) B hilos + C procesos. 3) Implementar las tres.
- **Decisión:** B = hilos (`ThreadPoolExecutor`) y C = procesos (`ProcessPoolExecutor`), ambas con `N_TRABAJADORES = 8`. El grupo de hilos o procesos se crea dentro de `ejecutar`, así que su costo se mide.
- **Justificación (incluya evidencia o principio físico):** hilos y asyncio están en la misma rama del mapa (aprovechar esperas ociosas, concurrencia); procesos está en otra (repartir trabajo entre núcleos, paralelismo). Así comparamos concurrencia contra paralelismo. 8 = núcleos lógicos del equipo de medición (Ryzen 5 PRO 2400G, ver `docs/entorno.md`): más procesos que núcleos solo añade cambios de contexto. El costo de crear los procesos se mide porque el usuario también lo espera.
- **Consecuencias / riesgos:** C paga un costo fijo de arranque (*spawn* en Windows) que puede hacerla más lenta que A con n pequeño. `labmedicion` no cuenta el CPU ni la memoria de los procesos hijos: en C, `uso_cpu_pct` y `pico_mem_mib` salen subestimados y se reportan como tales. asyncio queda como posible estrategia D si sobra tiempo.

## D-002 — Verificación de que no se omitan tareas
- **Fecha:** 2026-11-18 · **Autor:** Julian · **Issue/PR:** R2, relacionado con PR #1
- **Contexto:** `ejecutar(tareas)` devuelve solo un entero. Comparar ese entero con la línea base puede pasar aunque una implementación omita una tarea y cuente otra más de una vez.
- **Opciones consideradas:** 1) Cambiar la interfaz para devolver los identificadores procesados. 2) Mantener el entero y verificar dentro de cada estrategia los identificadores devueltos por cada trabajador. 3) Confiar únicamente en comparar los conteos.
- **Decisión:** Mantener `ejecutar(tareas) -> int`; cada estrategia comprueba que la lista de identificadores devuelta coincide, incluyendo duplicados, con los identificadores de entrada. Las pruebas comparan el resultado con la línea base y comprueban además que el conteo sea igual a `len(tareas)`.
- **Justificación:** La comprobación de identificadores detecta tareas omitidas o duplicadas sin romper la interfaz usada por el ejecutor del experimento. Los casos con n = 0, n = 1 y proporciones 0, 0,5 y 1 cubren entradas vacías, pequeñas y las dos clases de tarea.
- **Consecuencias / riesgos:** Se conserva una API sencilla, pero la verificación depende de que cada tarea devuelva su propio identificador; no prueba por sí sola que el cálculo interno de una tarea sea correcto.

## D-003 — Variables independientes y controles del experimento
- **Fecha:** 2026-11-18 · **Autor:** Jeff · **Issue/PR:** R1/R4, PR #1
- **Contexto:** El experimento debe atribuir los cambios observados a factores definidos, evitando multiplicar las condiciones y confundir el efecto de la estrategia con otras decisiones de configuración.
- **Opciones consideradas:** Tratar como factores experimentales la estrategia, el tamaño `n`, la proporción E/S y el número de trabajadores; o variar estrategia y `n` y mantener fija la carga mixta y la configuración de trabajadores.
- **Decisión:** Las variables independientes son la estrategia (A/B/C) y el tamaño `n` (20, 40, 80). La proporción E/S queda fija en su valor predeterminado (0,5), y B/C mantienen ocho trabajadores.
- **Justificación:** Estrategia y `n` responden directamente a la pregunta de investigación y sus efectos se observan en las mediciones de pared, CPU y memoria. Variar también la proporción E/S mezclaría el efecto del tipo de carga con el de la estrategia; variar trabajadores añadiría otro factor y muchas combinaciones, además de apartarse de la comparación prevista con ocho trabajadores. Mantener ambas constantes permite una comparación reproducible dentro del tiempo disponible.
- **Consecuencias / riesgos:** Las conclusiones aplican a una carga mixta 50/50 y ocho trabajadores; no permiten afirmar cómo cambiarían los resultados con otras proporciones o tamaños de grupo.

## D-004 — Rama principal del repositorio
- **Fecha:** 2026-11-18 · **Autor:** Jeff · **Issue/PR:** R1, PR #1
- **Contexto:** PR #1 tiene como base `main`, mientras que la referencia local `origin/HEAD` apuntaba inicialmente a `jefferson`; las ramas no estaban en el mismo commit.
- **Opciones consideradas:** Tratar `jefferson` como rama principal por la referencia local; cambiar la base del PR; o usar la rama predeterminada que anuncia GitHub.
- **Decisión:** Usar `main` como rama principal: GitHub informa `default_branch = main` y el HEAD remoto apunta a `refs/heads/main`. Se actualizó la referencia local `origin/HEAD`; PR #1 conserva `main` como base.
- **Justificación:** La configuración del repositorio remoto es la fuente de verdad para la rama predeterminada. Al verificar, `main` estaba un commit por delante de `jefferson`.
- **Consecuencias / riesgos:** `jefferson` no se considera rama principal; cualquier cambio exclusivo de esa rama debe integrarse mediante PR antes de asumirse presente en `main`.
