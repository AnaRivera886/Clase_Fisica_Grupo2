# Registro de uso de IA

## 2026-11-09

- **Herramienta:** asistente de IA integrado al entorno de desarrollo.
- **Qué pedimos:** pedimos apoyo para redactar el README, la tabla de variables, las hipótesis, la bitácora y el ejecutor reproducible de estrategias secuencial, hilos, asyncio y procesos; también para documentar el entorno.
- **Qué verificamos:** comprobamos que el checkout inicial no contenía archivos del proyecto ni commits; Git indicó que la rama `main` no tenía commits y que el remoto no tenía una rama disponible. El lanzador `py` permitió ejecutar CPython 3.14.7. Una prueba pequeña del ejecutor generó 24 filas con las cuatro estrategias, tres proporciones E/S y dos repeticiones; confirmamos que el encabezado coincide con las 11 columnas solicitadas. El sistema reportó AMD Ryzen 5 PRO 2400G con Radeon Vega Graphics y 8 CPU lógicas.
- **Qué no verificamos:** no ejecutamos `src.linea_base`, no realizamos ni conservamos la serie de 30 repeticiones por condición y no comparamos las hipótesis con resultados. La prueba pequeña solo comprobó que el código corre; no la tratamos como medición del estudio. La hipótesis aún debe quedar en un commit anterior a cualquier corrida experimental, conforme al curso.
- **Revisión del equipo:** antes de entregar, compararemos el ejecutor con la línea base real, confirmaremos el número de trabajadores en el equipo de corridas, completaremos las mediciones y gestionaremos el cambio mediante issue, rama y PR revisado por otro integrante.
