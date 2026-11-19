# Entorno experimental

## Diagnóstico disponible

El script `diagnostico_entorno.py` de la carpeta Scripts del Drive no está en esta copia de trabajo, así que todavía no puedo pegar su salida ni afirmar que esta sea su ejecución. Como comprobación local anterior, ejecuté `py -3 -c "from herramientas.labmedicion import describir_entorno; import json; print(json.dumps(describir_entorno(), indent=2, ensure_ascii=False))"` desde `plantilla_repositorio/` el **2026-11-18 10:46:32**:

```json
{
  "fecha": "2026-11-18T10:46:32",
  "sistema": "Windows 10",
  "maquina": "AMD64",
  "procesador": "AMD64 Family 23 Model 17 Stepping 0, AuthenticAMD",
  "nucleos_logicos": 8,
  "python": "3.14.7",
  "implementacion": "CPython",
  "psutil": null,
  "sensores_disponibles": {
    "frecuencia": false,
    "temperatura": false,
    "energia_rapl": false,
    "psutil": false
  }
}
```

La comprobación de sensores de `herramientas.sensores` informó que temperatura y RAPL no están disponibles. Esta salida local **no sustituye** la del script solicitado del Drive.

## Condiciones para el experimento

- **Equipo:** Lenovo 10VUS1SK00; AMD Ryzen 5 PRO 2400G, 4 núcleos físicos y 8 lógicos.
- **Sistema/Python:** Windows 10 · CPython 3.14.7.
- **¿Conectado a corriente?:** Sí, confirmado por Jeff el 2026-11-18. Windows no devolvió una lectura de batería en la consulta disponible, así que la confirmación no proviene de un sensor; volver a verificar al iniciar el experimento formal.
- **Aplicaciones abiertas en la sesión de documentación (snapshot 2026-11-18 10:48:35):** Chrome, VS Code, Word y EVE Online; también se observaron procesos de MongoDB y PostgreSQL. Este snapshot no es el estado de una corrida formal. Antes del experimento se cerrarán las aplicaciones no esenciales y se registrará cualquier aplicación que deba permanecer abierta.
- **Temperatura:** no disponible. Plan B: reportarla como **no medida**, no estimarla; mantener iguales las condiciones de alimentación y calentamiento, y anotar cualquier señal de throttling o incidente.
- **RAPL:** no disponible en Windows; **energía no medida**. El porcentaje de CPU no se usará como sustituto de energía.
- **Experimento formal:** pendiente; volver a confirmar la alimentación y anotar qué aplicaciones quedan abiertas en la fecha de ejecución.

## Salida solicitada pendiente

Pegar aquí, sin editar, la salida de `diagnostico_entorno.py` cuando se copie desde el Drive y se ejecute en el equipo de medición.
