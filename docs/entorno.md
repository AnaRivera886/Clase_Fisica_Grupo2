# Entorno experimental

## Diagnóstico disponible

El script `diagnostico_entorno.py` de la carpeta Scripts del Drive no está en esta copia de trabajo, así que todavía no puedo pegar su salida ni afirmar que esta sea su ejecución. Como comprobación local, ejecuté `py -3 -c "from herramientas.labmedicion import describir_entorno; import json; print(json.dumps(describir_entorno(), indent=2, ensure_ascii=False))"` desde `plantilla_repositorio/` el **2026-11-18 10:46:32**:

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

- **Equipo de medición confirmado:** Acer Aspire A315-42.
- **Sistema/Python:** Windows 11 · CPython 3.13.0 (`py -3`); `py -3.14` no está instalado. Esta configuración reemplaza el registro inicial del Lenovo/Windows 10/CPython 3.14.7.
- **¿Conectado a corriente?:** Jeff lo confirmó antes del intento piloto el 2026-11-18. Volver a verificarlo antes de la corrida formal; Windows no devolvió una lectura de batería en la consulta disponible.
- **Aplicaciones abiertas en la sesión de documentación (snapshot 2026-11-18 10:48:35):** Chrome, VS Code, Word y EVE Online; también se observaron procesos de MongoDB y PostgreSQL. Este snapshot no es el estado de una corrida formal. Antes del experimento se cerrarán las aplicaciones no esenciales y se registrará cualquier aplicación que deba permanecer abierta.
- **Temperatura:** no disponible. Plan B: reportarla como **no medida**, no estimarla; mantener iguales las condiciones de alimentación y calentamiento, y anotar cualquier señal de throttling o incidente.
- **RAPL:** no disponible en Windows; **energía no medida**. El porcentaje de CPU no se usará como sustituto de energía.
- **Experimento formal:** pendiente; volver a confirmar la alimentación, las aplicaciones cerradas y registrar el perfil de energía antes de ejecutar.

## Intento de corrida del 2026-11-18

El usuario confirmó conexión a corriente y cierre de EVE Online, MongoDB, PostgreSQL y Chrome antes de ejecutar el comando. El usuario confirmó después Acer Aspire A315-42 como el equipo correcto; la configuración actual del entorno queda actualizada a Windows 11 y CPython 3.13.0. `py -3.14` no está instalado.

Los archivos del primer bloque se conservan solo en la copia local como `resultados/ensayo_no_formal_acer.csv` y `resultados/ensayo_no_formal_acer.entorno.json`; no se incluyen en el PR como resultados formales porque precedieron a la enmienda. El CSV tuvo 99 registros (90 de tiempo y 9 de memoria); el CV de B superó 10 % para n = 20, 40 y 80. Se hará un bloque formal nuevo y se repetirá si corresponde según el CV.

## Salida solicitada pendiente

El archivo `diagnostico_entorno.py` del Drive no fue proporcionado y no aparece en el workspace. Pegar aquí, sin editar, su salida cuando esté disponible y se ejecute en el equipo de medición; el JSON automático anterior no sustituye esa salida.
