# Experimento de concurrencia para ServiCampo Ltda.

## Problema empresarial

En ServiCampo Ltda. consultamos servicios externos de clima y precios agrícolas. La cola actual atiende las solicitudes una por una: aunque el procesador pasa parte del tiempo esperando respuestas, los usuarios pueden esperar varios segundos para recibir todos los datos. Queremos comparar estrategias de ejecución y medir su efecto en el tiempo de respuesta y en el uso de CPU, antes de recomendar un cambio.

## Situación inicial medida

La línea base prevista es la ejecución secuencial de `src/linea_base.py`, que se ejecuta con:

```powershell
python -m src.linea_base
```

**Salida real de la línea base:** pendiente de registrar. No incluimos cifras hasta ejecutar el comando en el equipo del experimento y conservar su salida completa aquí:

```text
[Pegar aquí, sin modificar, la salida obtenida de python -m src.linea_base]
```

En el checkout inicial usado para preparar este protocolo no estaba `src/linea_base.py`, así que no pudimos ejecutar la medición de referencia. Después verificamos que el lanzador `py` sí permite ejecutar Python 3.14.7 y validar el ejecutor con una prueba pequeña, pero esa prueba no reemplaza ni representa la salida de la línea base. Por eso esta sección no afirma tiempos que no hayamos observado. Antes de medir, restauraremos la línea base del equipo y registraremos su salida.

## Qué medimos

Comparamos E0 (secuencial), E1 (hilos), E2 (asyncio) y E3 (procesos), con distintas proporciones de tareas de E/S y CPU. La carga reproducible del ejecutor se describe en [docs/bitacora.md](docs/bitacora.md) y sus variables en [docs/variables.md](docs/variables.md). La hipótesis debe quedar en un commit fechado antes de iniciar las mediciones, siguiendo las reglas del curso.

`time.sleep()` **simula** una espera de red: no realiza una consulta HTTP ni representa toda la variabilidad de una red real. El resultado solo permite comparar estrategias bajo esta carga controlada.

## Ejecución del protocolo

Desde la raíz del proyecto:

```powershell
python -m src.documentar_entorno
python -m src.ejecutar_experimentos
```

En Windows, si el comando `python` no está disponible, podemos usar `py -m` con los mismos módulos.

El ejecutor prepara los mismos datos deterministas para cada estrategia, hace un calentamiento no medido, aleatoriza el orden de las estrategias dentro de cada repetición y escribe `results/resultados.csv`. Por defecto usa 30 repeticiones, 32 tareas, semilla 42, latencia simulada de 0.1 s, proporciones E/S de 0 %, 50 % y 100 %, y tantas tareas de CPU como para ejecutar 20 000 hashes por tarea. Los valores se pueden cambiar con `--help`; hay que registrar en la bitácora toda configuración no predeterminada.

Ejemplo para ejecutar solo la condición 100 % E/S con cuatro trabajadores:

```powershell
python -m src.ejecutar_experimentos --pct-es 100 --trabajadores 4
```

El CSV incluye estas columnas, en este orden: `estrategia,pct_es,n_trabajadores,n_tareas,semilla,latencia_sim_s,repeticion,t_pared_s,t_cpu_s,razon_cpu_pared_pct,tareas_por_s`. En E3, `t_cpu_s` suma el CPU del proceso principal y de los hijos; si el sistema no expone tiempos de CPU de hijos, usa como alternativa el CPU reportado por las tareas ejecutadas en ellos. El cociente CPU/pared puede superar 100 % cuando varios procesos trabajan en paralelo.

## Entorno y registro

Guardamos la información del entorno en `results/entorno.txt` con el comando anterior y documentamos las decisiones y controles en [docs/bitacora.md](docs/bitacora.md). Registramos el apoyo de IA en [docs/uso_ia.md](docs/uso_ia.md).
# Clase_Fisica_Grupo2
