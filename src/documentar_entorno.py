"""Registra información del entorno usado para los experimentos."""

import argparse
import os
import platform
import sys
from pathlib import Path
from typing import Dict, Optional


def obtener_informe(parametros: Optional[Dict[str, str]] = None) -> str:
    """Devuelve información reproducible del entorno y, si se indica, de la carga."""
    datos = [
        ("Python", sys.version.replace("\n", " ")),
        ("Ejecutable", sys.executable),
        ("Implementación", platform.python_implementation()),
        ("Sistema", platform.platform()),
        ("Procesador", platform.processor() or "No reportado"),
        ("CPU lógicas disponibles", str(os.cpu_count() or "No reportado")),
        ("Arquitectura", platform.machine() or "No reportada"),
    ]
    lineas = ["Entorno de experimentación", "=========================="]
    lineas.extend("{}: {}".format(nombre, valor) for nombre, valor in datos)
    if parametros:
        lineas.extend(["", "Configuración registrada", "========================"])
        lineas.extend(
            "{}: {}".format(nombre, valor)
            for nombre, valor in sorted(parametros.items())
        )
    return "\n".join(lineas) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--salida",
        default="results/entorno.txt",
        help="archivo donde se guardará el informe (por defecto: %(default)s)",
    )
    args = parser.parse_args()

    destino = Path(args.salida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    informe = obtener_informe()
    destino.write_text(informe, encoding="utf-8")
    print(informe, end="")
    print("Informe guardado en {}".format(destino))


if __name__ == "__main__":
    main()
