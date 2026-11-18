# Registro de decisiones técnicas (ADR breve)

Cada decisión importante se registra aquí y se enlaza desde el issue o PR correspondiente.

## D-001 — Estrategias alternativas: B con hilos y C con procesos, 8 trabajadores
- **Fecha:** 2026-11-18 · **Autor(es):** Ana · **Issue/PR:** PR `feat/estrategias-b-c`
- **Contexto:** el enunciado pide al menos tres estrategias comparables (la línea base cuenta) y propone tres direcciones: hilos, asyncio y procesos. La Guía de errores frecuentes advierte que no deben ser la misma idea.
- **Opciones consideradas:** 1) B hilos + C asyncio. 2) B hilos + C procesos. 3) Implementar las tres.
- **Decisión:** B = hilos (`ThreadPoolExecutor`) y C = procesos (`ProcessPoolExecutor`), ambas con `N_TRABAJADORES = 8`. El grupo de hilos o procesos se crea dentro de `ejecutar`, así que su costo se mide.
- **Justificación (incluya evidencia o principio físico):** hilos y asyncio están en la misma rama del mapa (aprovechar esperas ociosas, concurrencia); procesos está en otra (repartir trabajo entre núcleos, paralelismo). Así comparamos concurrencia contra paralelismo. 8 = núcleos lógicos del equipo de medición (Ryzen 5 PRO 2400G, ver `docs/entorno.md`): más procesos que núcleos solo añade cambios de contexto. El costo de crear los procesos se mide porque el usuario también lo espera.
- **Consecuencias / riesgos:** C paga un costo fijo de arranque (*spawn* en Windows) que puede hacerla más lenta que A con n pequeño. `labmedicion` no cuenta el CPU ni la memoria de los procesos hijos: en C, `uso_cpu_pct` y `pico_mem_mib` salen subestimados y se reportan como tales. asyncio queda como posible estrategia D si sobra tiempo.
