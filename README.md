# Equipo 2 — Concurrencia y procesamiento de tareas

> Proyecto: *Laboratorio colaborativo de rendimiento y eficiencia computacional desde la física aplicada*
> Física Aplicada al Desarrollo de Software · SENA · ADSO · 7.º trimestre

## 1. Problema empresarial
**Empresa (caso simulado):** ServiCampo Ltda., plataforma que consulta servicios externos de clima y precios agrícolas

La cola de solicitudes se atiende una por una. Los usuarios esperan varios segundos aunque el servidor reporta la CPU casi ociosa.

## 2. Situación inicial medible
src/linea_base.py ejecuta secuencialmente tareas de E/S (espera) y de CPU (hash).

| Medición preliminar (Clase 3) | Valor | Unidad |
|---|---|---|
| n utilizado | 40 por condición | tareas |
| Tiempo de pared (1 corrida por condición) | Solo E/S: 1.71; solo CPU: 0.37 | s |
| Equipo y fecha | Lenovo 10VUS1SK00 · Ryzen 5 PRO 2400G · 2026-11-18 | — |

Salida literal de `py -3 -m src.linea_base` (el programa hace una corrida de n = 40 para cada condición):

```text
Could not find platform independent libraries <prefix>
solo E/S  pared = 1.71 s   CPU = 0.00 s   CPU/pared =   0.0 %
solo CPU  pared = 0.37 s   CPU = 0.36 s   CPU/pared =  97.1 %
```

## 3. Pregunta de investigación
_¿Cómo cambia el tiempo de pared (s), el uso de CPU (%) y el pico de memoria (MiB) al cambiar la estrategia A/B/C y n = 20, 40, 80 tareas, manteniendo el equipo, Python, los datos de semilla 2, la alimentación y los programas abiertos?_

## 4. Hipótesis
Ver [docs/hipotesis.md](docs/hipotesis.md).

## 5. Estrategias
| Id | Estrategia | Idea principal | Efecto físico esperado | Responsable |
|---|---|---|---|---|
| A | Línea base secuencial | Atiende las tareas una por una | Referencia sin solapamiento de esperas | Julian |
| B | Con hilos | Solapa tareas mientras otras esperan E/S; el trabajo CPU también se medirá sin asumir que el GIL lo impide | Puede reducir tiempo de pared y elevar el uso de CPU | Ana |
| C | Por confirmar en el PR de Ana | Pendiente de documentar al revisar su implementación | Pendiente de justificar | Ana |

## 6. Cómo reproducir
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt                          # opcional: psutil, matplotlib
python -m src.linea_base                                 # situación inicial
python -m unittest discover -s pruebas                   # corrección
python -m experimentos.ejecutar_experimento              # experimento formal -> resultados/resultados.csv
python ruta/a/analizar_resultados.py resultados/resultados.csv
```
En este Windows, `python` no está en PATH; usar `py -3 -m ...` como equivalente.

## 7. Integrantes y roles
| Rol | Integrante | Responsabilidad principal |
|---|---|---|
| R1 — Coordinación y protocolo experimental | Jeff | Mantiene el protocolo, controla variables y coordina issues y planeación. |
| R2 — Desarrollo de estrategia base | Julian | Comprende y documenta la línea base y verifica la corrección. |
| R3 — Estrategias alternativas y optimización | Ana | Implementa las estrategias alternativas y justifica los cambios esperados. |
| R4 — Automatización de mediciones y análisis | Jeff (entorno y ejecución); Ana (análisis y gráficos) | Automatiza/ejecuta mediciones, documenta el entorno y analiza resultados. |

Los roles son flexibles: **todos** participan en la comprensión física y en el código.

## 8. Documentación
- [Variables](docs/variables.md) · [Protocolo](docs/protocolo.md) · [Entorno](docs/entorno.md)
- [Decisiones técnicas](docs/decisiones.md) · [Uso de IA](docs/uso_ia.md) · [Informe](docs/informe.md)

## 9. Resultados y conclusiones (Clase 5)
_Resumen de máximo 5 líneas con cifras, unidades e intervalo de confianza._
