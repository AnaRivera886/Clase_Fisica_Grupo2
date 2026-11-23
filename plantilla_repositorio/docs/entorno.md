# Entorno experimental

## Diagnóstico disponible

No fue posible pegar la salida literal de `diagnostico_entorno.py` porque el script no está incluido en esta copia del repositorio ni en el workspace. El diagnóstico automático usado por el experimentador confirmó:

- Sistema: Windows 11
- Equipo: Acer Aspire A315-42
- Procesador: AMD Ryzen 5 3500U
- Núcleos físicos/lógicos: 4/8
- Python: CPython 3.13.0

## Condiciones del experimento

- **¿Conectado a corriente?:** confirmado antes de los bloques formales; el estado fue comunicado como conectado a corriente.
- **Aplicaciones abiertas durante el experimento:** antes de cada bloque formal se verificó que estuvieran cerrados EVE Online, MongoDB, PostgreSQL y Chrome. VS Code y el terminal pueden permanecer abiertos para ejecutar y registrar el experimento.
- **Temperatura disponible (sí/no) y plan B:** no disponible en Windows/AMD con los sensores comprobados. Plan B: reportar temperatura como no medida y mantener alimentación y calentamiento similares, registrando cualquier throttling o incidente.
- **Energía RAPL disponible (sí/no):** no disponible en Windows. Plan B: reportar energía como no medida y no inferirla a partir del porcentaje de CPU.

**Pendiente:** sustituir esta sección por la salida literal de `py -3 diagnostico_entorno.py` ejecutada en el Acer, pegada sin editar.
