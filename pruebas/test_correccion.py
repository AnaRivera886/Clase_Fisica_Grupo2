"""
Pruebas de corrección (R2). Ejecutar:  python -m unittest discover -s pruebas
Una estrategia más rápida pero incorrecta NO es una mejora.
"""
import unittest

from src import estrategia_b, estrategia_c, linea_base

ESTRATEGIAS = (
    ("estrategia_b", estrategia_b),
    ("estrategia_c", estrategia_c),
)
CASOS = tuple((n, proporcion_es) for n in (0, 1, 4, 9) for proporcion_es in (0.0, 0.5, 1.0))


class TestCorreccion(unittest.TestCase):
    def test_estrategias_coinciden_con_linea_base(self):
        for nombre, estrategia in ESTRATEGIAS:
            for n, proporcion_es in CASOS:
                with self.subTest(estrategia=nombre, n=n, proporcion_es=proporcion_es):
                    tareas = linea_base.preparar(n, proporcion_es=proporcion_es)
                    esperado = linea_base.ejecutar(tareas)
                    obtenido = estrategia.ejecutar(tareas)

                    self.assertEqual(esperado, len(tareas))
                    self.assertEqual(obtenido, esperado)
                    self.assertEqual(obtenido, len(tareas))


if __name__ == "__main__":
    unittest.main()
