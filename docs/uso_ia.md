# Bitácora de uso de inteligencia artificial

La IA es una herramienta de apoyo permitida. Cada uso relevante se registra. **Usted es responsable de
verificar todo lo que la IA produce y de poder explicarlo sin ella.**

| # | Fecha | Integrante | Herramienta | Propósito (investigar, depurar, alternativas...) | Consulta (resumen) | ¿Qué se usó de la respuesta? | ¿Cómo se verificó? | Errores o suposiciones detectadas en la respuesta |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-18 | Jeff | Copilot SDK en VS Code | Completar el protocolo y preparar mediciones reproducibles | Pedí documentar variables, hipótesis, protocolo y entorno para comparar A/B/C, sin inventar salidas ni resultados | Usé dos hipótesis falsables, parámetros del protocolo, el diagnóstico local disponible y la salida literal de la línea base; Jeff confirmó conexión a corriente, pero aún falta la salida de Drive, las aplicaciones para la corrida formal y las mediciones A/B/C | Contrasté el equipo con Windows; ejecuté `herramientas.sensores`, `labmedicion.describir_entorno`, `py -3 -m src.linea_base` y `py -3 -m unittest discover -s pruebas` (1 prueba pasó); revisé el ejecutor de la plantilla antes de ejecutar; consulté ramas/issues/PR del repositorio corregido | `python` no está en PATH; `py -3` inicia Python 3.14.7 pero muestra el aviso `Could not find platform independent libraries <prefix>`. La línea base imprime dos condiciones separadas (E/S y CPU), no una carga mixta única. `diagnostico_entorno.py` no está disponible en la copia. El repo GitHub corregido no tiene ramas, issues ni PR; las herramientas disponibles solo permiten lectura, por lo que no se afirmó haber publicado el branch ni creado issue/PR. |

## Reflexión individual (Clase 5, una por integrante)
- **Nombre:** Jeff
- ¿En qué le ayudó la IA y en qué lo confundió?
- Un error o afirmación sin evidencia que detectó en la IA y cómo lo comprobó:
- ¿Qué parte del proyecto puede explicar completamente sin ayuda?
