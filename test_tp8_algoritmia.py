import tempfile
import unittest
from pathlib import Path

from tp8_algoritmia import (
    analizar_carrera,
    a_segundos,
    construir_secuencias,
    desde_segundos,
    evaluar_intento,
    extraer_secuencias,
    guardar_puntajes,
    cargar_puntajes,
    jugar_pistas,
    ordenar_alumnos_matriz,
    ordenar_alumnos_paralelas,
    resumir_notas,
    secuencias_mas_largas,
)


class Ejercicio1Tests(unittest.TestCase):
    def test_resumen_y_ordenamientos(self):
        self.assertEqual(resumir_notas([20, 10, 30], [4, 8, 6]), {
            "aprobados": 3,
            "desaprobados": 0,
            "promedio": 6,
            "legajos_sobre_promedio": [10],
        })
        self.assertEqual(ordenar_alumnos_paralelas([20, 10], [4, 8]), [(10, 8), (20, 4)])
        self.assertEqual(ordenar_alumnos_matriz([20, 10], [4, 8]), [[10, 20], [8, 4]])


class Ejercicio2Tests(unittest.TestCase):
    def test_rechaza_unidades_duplicadas(self):
        from tp8_algoritmia import calcular_expensas
        with self.assertRaises(ValueError):
            calcular_expensas([1] * 20, [50] * 20, 100)


class Ejercicio3Tests(unittest.TestCase):
    def test_conversiones_y_ganador(self):
        self.assertEqual(a_segundos(1, 2, 3), 3723)
        self.assertEqual(desde_segundos(3723), (1, 2, 3))
        self.assertEqual(analizar_carrera([(8, 99), (2, 80), (5, 80)])["ganador"], (2, 80))


class Ejercicio4Y5Tests(unittest.TestCase):
    def test_pistas_consideran_repetidos(self):
        self.assertEqual(evaluar_intento("5739", "5678"), (1, 1))
        self.assertEqual(evaluar_intento("1122", "2211"), (0, 4))
        self.assertEqual(evaluar_intento("1122", "1111"), (2, 0))

    def test_puntajes_persisten_y_quedan_ordenados(self):
        with tempfile.TemporaryDirectory() as directorio:
            ruta = Path(directorio) / "puntajes.json"
            guardar_puntajes([
                {"alias": "Vale", "intentos": 5},
                {"alias": "Ana", "intentos": 2},
            ], ruta)
            self.assertEqual(cargar_puntajes(ruta), [
                {"alias": "Ana", "intentos": 2},
                {"alias": "Vale", "intentos": 5},
            ])

    def test_juego_con_pistas_registra_alias_y_permite_abandonar(self):
        with tempfile.TemporaryDirectory() as directorio:
            ruta = Path(directorio) / "puntajes.json"
            respuestas = iter(["5678", "5739", "Valentina"])
            leer = lambda _: next(respuestas)
            self.assertEqual(jugar_pistas("5739", leer=leer, escribir=lambda *_: None,
                                          ruta_puntajes=ruta), 2)
            self.assertEqual(cargar_puntajes(ruta), [{"alias": "Valentina", "intentos": 2}])
            self.assertEqual(jugar_pistas("1234", leer=lambda _: "-1", escribir=lambda *_: None,
                                          ruta_puntajes=ruta), 0)


class Ejercicio6Y7Tests(unittest.TestCase):
    def test_construccion_y_busqueda_de_las_mas_largas(self):
        numeros = [5, 2, 9, 6, 4, 15, 3, 19, 12, 1, 5]
        lista = construir_secuencias(numeros)
        self.assertEqual(lista, [5, 2, 9, 0, 6, 4, 0, 15, 3, 0, 19, 0, 12, 1, 5, 0])
        self.assertEqual(extraer_secuencias(lista), [[5, 2, 9], [6, 4], [15, 3], [19], [12, 1, 5]])
        self.assertEqual(secuencias_mas_largas(lista), [[5, 2, 9], [12, 1, 5]])


if __name__ == "__main__":
    unittest.main()
