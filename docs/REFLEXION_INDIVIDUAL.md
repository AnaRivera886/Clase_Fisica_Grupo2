## Reflexión individual de uso de IA — Ana (integrante C)

Durante este proyecto usé dos herramientas de IA: Claude Code, dentro de VS Code, y Claude en el chat.

**Qué me ayudó Claude Code.** En hacer la parte 5, guiar a mi equipo, explicarme, dar instrucciones, hacer los commits y leer lo que hicieron mis compañeros.

**Qué me ayudó Claude en el chat.** Lo usé para entender cómo correr los scripts del curso en PowerShell y para interpretar los errores que me salieron (rutas mal escritas, el orden de los argumentos, un módulo que no se encontraba y un problema de codificación al guardar la salida). También lo usé para organizar mi parte del informe: me dio un borrador del texto sobre resultados, atípicos, hipótesis, física y propuesta de mejora, que luego edité, y un segundo cálculo estadístico con el que comparé la salida de los scripts del curso.

**Qué verifiqué por mi cuenta.** Las cifras del informe salen de los scripts del curso, no del chat. Comparé las tablas con el cálculo independiente y coincidieron. Comprobé cada hipótesis contra el umbral que el equipo escribió en `hipotesis.md` antes de medir. Abrí los gráficos para revisar la escala log-log, las barras de error y las unidades.

**Qué tuve que corregir.** El primer borrador sugería que la estrategia C esperaba mucho tiempo porque usaba poca CPU. Al leer el protocolo vi que `time.process_time()` no cuenta el CPU de los procesos hijos, así que ese dato no sirve para concluir nada sobre C, y lo quité. También ajusté el texto a la versión de Python y al equipo que quedaron registrados en la enmienda.

**Qué aprendí.** a diferenciar lo que se midió de lo que se infiere, a decidir una hipótesis con el umbral fijado antes de medir y no con lo que "parece", y a leer un IC y la prueba de Welch para saber si una diferencia es confiable.

**Limitaciones del uso de IA.** La IA no vio el computador ni la bitácora del equipo, así que no podía saber la causa de los atípicos ni qué bloque de datos era el formal. Por eso esas partes las confirmé con mis compañeros o con los registros del repo. Las conclusiones del informe son las que puedo explicar y defender sin ayuda de la IA.