"""Soluciones de práctica para el TP 8: Ejercicios tipo Final.

Las funciones de resolución están separadas de la interacción por consola para
facilitar su prueba, lectura y reutilización.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import random
from typing import Callable, Iterable, Sequence


# Ejercicio 1 ---------------------------------------------------------------

def resumir_notas(legajos: Sequence[int], notas: Sequence[int]) -> dict:
    """Devuelve aprobados, desaprobados, promedio y legajos sobre el promedio."""
    if len(legajos) != len(notas):
        raise ValueError("Debe haber la misma cantidad de legajos y notas.")
    if not notas:
        return {"aprobados": 0, "desaprobados": 0, "promedio": None,
                "legajos_sobre_promedio": []}

    promedio = sum(notas) / len(notas)
    return {
        "aprobados": sum(nota >= 4 for nota in notas),
        "desaprobados": sum(nota < 4 for nota in notas),
        "promedio": promedio,
        "legajos_sobre_promedio": [legajo for legajo, nota in zip(legajos, notas)
                                    if nota > promedio],
    }


def ordenar_alumnos_paralelas(legajos: Sequence[int], notas: Sequence[int]) -> list[tuple[int, int]]:
    """Ordena pares (legajo, nota) por legajo sin perder la relación entre listas."""
    if len(legajos) != len(notas):
        raise ValueError("Debe haber la misma cantidad de legajos y notas.")
    return sorted(zip(legajos, notas), key=lambda alumno: alumno[0])


def ordenar_alumnos_matriz(legajos: Sequence[int], notas: Sequence[int]) -> list[list[int]]:
    """Representa los datos en dos filas y ordena las columnas por legajo."""
    if len(legajos) != len(notas):
        raise ValueError("Debe haber la misma cantidad de legajos y notas.")
    matriz = [list(legajos), list(notas)]
    for indice in range(1, len(matriz[0])):
        columna_legajo = matriz[0][indice]
        columna_nota = matriz[1][indice]
        posicion = indice - 1
        while posicion >= 0 and matriz[0][posicion] > columna_legajo:
            matriz[0][posicion + 1] = matriz[0][posicion]
            matriz[1][posicion + 1] = matriz[1][posicion]
            posicion -= 1
        matriz[0][posicion + 1] = columna_legajo
        matriz[1][posicion + 1] = columna_nota
    return matriz


# Ejercicio 2 ---------------------------------------------------------------

def calcular_expensas(unidades: Sequence[int], superficies: Sequence[float], valor_m2: float) -> dict:
    """Calcula importes, promedio y listado descendente por superficie."""
    if len(unidades) != len(superficies):
        raise ValueError("Debe haber una superficie por unidad.")
    if len(unidades) != 20:
        raise ValueError("El edificio debe tener exactamente 20 unidades.")
    if len(set(unidades)) != len(unidades):
        raise ValueError("No puede haber números de unidad duplicados.")
    if any(unidad < 1 or unidad > 20 for unidad in unidades):
        raise ValueError("Los números de unidad deben estar entre 1 y 20.")
    if any(superficie <= 0 for superficie in superficies) or valor_m2 < 0:
        raise ValueError("Las superficies deben ser positivas y el valor por m² no negativo.")

    listado = [(unidad, superficie, superficie * valor_m2)
               for unidad, superficie in zip(unidades, superficies)]
    listado.sort(key=lambda fila: fila[1], reverse=True)
    return {
        "promedio_expensas": sum(fila[2] for fila in listado) / len(listado),
        "listado": listado,
    }


# Ejercicio 3 ---------------------------------------------------------------

def a_segundos(horas: int, minutos: int, segundos: int) -> int:
    """Convierte una duración no negativa a segundos, validando minutos y segundos."""
    if horas < 0 or not 0 <= minutos < 60 or not 0 <= segundos < 60:
        raise ValueError("Use horas no negativas y minutos/segundos entre 0 y 59.")
    return horas * 3600 + minutos * 60 + segundos


def desde_segundos(total: int) -> tuple[int, int, int]:
    """Convierte segundos no negativos a (horas, minutos, segundos)."""
    if total < 0:
        raise ValueError("La duración no puede ser negativa.")
    horas, resto = divmod(total, 3600)
    minutos, segundos = divmod(resto, 60)
    return horas, minutos, segundos


def analizar_carrera(ciclistas: Sequence[tuple[int, int]]) -> dict:
    """Recibe (número, tiempo_en_segundos); conserva el primer ganador en empate."""
    if not ciclistas:
        raise ValueError("Debe participar al menos un ciclista.")
    ganador = min(ciclistas, key=lambda ciclista: ciclista[1])
    promedio = sum(tiempo for _, tiempo in ciclistas) / len(ciclistas)
    return {"ganador": ganador, "promedio_segundos": promedio}


# Ejercicio 4 ---------------------------------------------------------------

def obtener_pistas(secreto: str, intento: str) -> tuple[int, int]:
    """Devuelve (dígitos correctos, aproximados), contando duplicados correctamente."""
    if len(secreto) != 4 or len(intento) != 4 or not secreto.isdigit() or not intento.isdigit():
        raise ValueError("El secreto y el intento deben ser cadenas de cuatro dígitos.")
    correctos = sum(a == b for a, b in zip(secreto, intento))
    coincidencias = sum((Counter(secreto) & Counter(intento)).values())
    return correctos, coincidencias - correctos


def cargar_puntajes(ruta: str | Path) -> list[dict]:
    """Carga puntajes guardados; ante archivo ausente o inválido comienza vacío."""
    try:
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
        if not isinstance(datos, list):
            return []
        validos = [fila for fila in datos if isinstance(fila, dict)
                   and isinstance(fila.get("alias"), str)
                   and isinstance(fila.get("intentos"), int)
                   and fila["intentos"] >= 1]
        return sorted(validos, key=lambda fila: fila["intentos"])[:5]
    except (OSError, json.JSONDecodeError):
        return []


def guardar_puntajes(puntajes: Iterable[dict], ruta: str | Path) -> None:
    """Guarda únicamente los cinco mejores resultados, sin datos identificatorios."""
    top = sorted(puntajes, key=lambda fila: fila["intentos"])[:5]
    Path(ruta).write_text(json.dumps(top, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def registrar_puntaje(intentos: int, leer: Callable[[str], str], escribir: Callable[..., None],
                      ruta: str | Path) -> None:
    """Agrega una marca al top 5 usando alias para no almacenar documentos personales."""
    puntajes = cargar_puntajes(ruta)
    if intentos < 1 or (len(puntajes) == 5 and intentos >= puntajes[-1]["intentos"]):
        return
    alias = leer("Entraste entre las cinco mejores marcas. Elegí un alias: " ).strip()
    alias = alias[:30] or "Anónimo"
    puntajes.append({"alias": alias, "intentos": intentos})
    guardar_puntajes(puntajes, ruta)
    escribir("Marca guardada.")


def mostrar_puntajes(escribir: Callable[..., None] = print,
                     ruta: str | Path = "mejores_puntajes.json") -> None:
    """Muestra el top 5 guardado."""
    puntajes = cargar_puntajes(ruta)
    escribir("Mejores marcas:")
    if not puntajes:
        escribir("Todavía no hay marcas guardadas.")
    for posicion, fila in enumerate(puntajes, start=1):
        escribir(f"{posicion}. {fila['alias']} - {fila['intentos']} intento(s)")


def jugar_adivinanza(
    secreto: str,
    leer: Callable[[str], str] = input,
    escribir: Callable[..., None] = print,
    ruta_puntajes: str | Path = "mejores_puntajes.json",
) -> int:
    """Juega una ronda; -1 abandona. Registra la marca si se acierta."""
    if len(secreto) != 4 or not secreto.isdigit() or secreto[0] == "0":
        raise ValueError("El secreto debe ser un entero de cuatro cifras.")
    intentos = 0
    while True:
        entrada = leer("Adiviná el número de cuatro cifras (-1 para abandonar): " ).strip()
        if entrada == "-1":
            escribir("Partida abandonada.")
            return intentos
        if not entrada.isdigit() or len(entrada) != 4:
            escribir("Ingresá exactamente cuatro cifras.")
            continue

        intentos += 1
        if entrada == secreto:
            escribir(f"¡Correcto! Lo encontraste en {intentos} intento(s).")
            registrar_puntaje(intentos, leer, escribir, ruta_puntajes)
            return intentos
        escribir("El número secreto es mayor." if entrada < secreto else "El número secreto es menor.")


# Ejercicio 5 ---------------------------------------------------------------

def evaluar_intento(secreto: str, intento: str) -> tuple[int, int]:
    """Devuelve (dígitos correctos, aproximados) para el juego del ejercicio 5."""
    return obtener_pistas(secreto, intento)


def jugar_pistas(
    secreto: str,
    leer: Callable[[str], str] = input,
    escribir: Callable[..., None] = print,
    ruta_puntajes: str | Path = "mejores_puntajes.json",
) -> int:
    """Juega con pistas de dígitos; admite abandono y registra las mejores marcas."""
    if len(secreto) != 4 or not secreto.isdigit() or secreto[0] == "0":
        raise ValueError("El secreto debe ser un entero de cuatro cifras.")
    intentos = 0
    while True:
        entrada = leer("Intento de cuatro cifras (-1 para abandonar): " ).strip()
        if entrada == "-1":
            escribir("Partida abandonada.")
            return intentos
        if len(entrada) != 4 or not entrada.isdigit():
            escribir("Ingresá exactamente cuatro cifras.")
            continue
        intentos += 1
        correctos, aproximados = evaluar_intento(secreto, entrada)
        escribir(f"{correctos} correcto(s), {aproximados} aproximado(s).")
        if correctos == 4:
            escribir(f"¡Ganaste en {intentos} intento(s)!")
            registrar_puntaje(intentos, leer, escribir, ruta_puntajes)
            return intentos


# Ejercicios 6 y 7 ----------------------------------------------------------

def construir_secuencias(numeros: Sequence[int]) -> list[int]:
    """Agrupa números en orden; inserta 0 cuando una suma excedería 20 y al final."""
    if any(numero < 1 or numero > 20 for numero in numeros):
        raise ValueError("Cada número debe estar entre 1 y 20.")
    resultado: list[int] = []
    suma_actual = 0
    for numero in numeros:
        if suma_actual + numero > 20:
            resultado.append(0)
            suma_actual = 0
        resultado.append(numero)
        suma_actual += numero
    resultado.append(0)
    return resultado


def extraer_secuencias(lista: Sequence[int]) -> list[list[int]]:
    """Separa una lista delimitada por ceros e ignora secuencias vacías."""
    secuencias: list[list[int]] = []
    actual: list[int] = []
    for numero in lista:
        if numero == 0:
            if actual:
                secuencias.append(actual)
                actual = []
        else:
            actual.append(numero)
    if actual:
        secuencias.append(actual)
    return secuencias


def secuencias_mas_largas(lista: Sequence[int]) -> list[list[int]]:
    """Devuelve todas las secuencias empatadas en longitud máxima."""
    secuencias = extraer_secuencias(lista)
    if not secuencias:
        return []
    largo_maximo = max(map(len, secuencias))
    return [secuencia for secuencia in secuencias if len(secuencia) == largo_maximo]


# Interfaz de consola -------------------------------------------------------

def _leer_entero(mensaje: str, minimo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Ingresá un valor mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Ingresá un número entero válido.")


def ejercicio_1() -> None:
    legajos: list[int] = []
    notas: list[int] = []
    while True:
        legajo = _leer_entero("Legajo (-1 para finalizar): " )
        if legajo == -1:
            break
        nota = _leer_entero("Nota (1 a 10): " )
        while not 1 <= nota <= 10:
            print("La nota debe estar entre 1 y 10.")
            nota = _leer_entero("Nota (1 a 10): " )
        legajos.append(legajo)
        notas.append(nota)
    resumen = resumir_notas(legajos, notas)
    print(f"Aprobados: {resumen['aprobados']} | Desaprobados: {resumen['desaprobados']}")
    if resumen["promedio"] is None:
        print("No se cargaron alumnos.")
    else:
        print(f"Promedio: {resumen['promedio']:.2f}")
        print("Legajos sobre el promedio:", resumen["legajos_sobre_promedio"])
    print("Orden por listas paralelas:", ordenar_alumnos_paralelas(legajos, notas))
    print("Orden por matriz de dos filas:", ordenar_alumnos_matriz(legajos, notas))


def ejercicio_2() -> None:
    unidades: list[int] = []
    superficies: list[float] = []
    while len(unidades) < 20:
        unidad = _leer_entero(f"Unidad {len(unidades) + 1}/20 (1 a 20): " , minimo=1)
        if unidad > 20 or unidad in unidades:
            print("La unidad debe estar entre 1 y 20 y no repetirse.")
            continue
        try:
            superficie = float(input("Superficie en m²: " ))
            if superficie <= 0:
                raise ValueError
        except ValueError:
            print("Ingresá una superficie positiva.")
            continue
        unidades.append(unidad)
        superficies.append(superficie)
    valor_m2 = float(input("Valor fijo por m²: " ))
    resultado = calcular_expensas(unidades, superficies, valor_m2)
    print(f"Promedio de expensas: ${resultado['promedio_expensas']:.2f}")
    for unidad, superficie, importe in resultado["listado"]:
        print(f"Unidad {unidad}: {superficie:.2f} m² - ${importe:.2f}")


def ejercicio_3() -> None:
    cantidad = _leer_entero("Cantidad de ciclistas: " , minimo=1)
    ciclistas: list[tuple[int, int]] = []
    for _ in range(cantidad):
        numero = _leer_entero("Número de ciclista: " )
        horas = _leer_entero("Horas: " , minimo=0)
        minutos = _leer_entero("Minutos (0 a 59): " )
        segundos = _leer_entero("Segundos (0 a 59): " )
        try:
            tiempo = a_segundos(horas, minutos, segundos)
        except ValueError as error:
            print(error)
            return
        ciclistas.append((numero, tiempo))
    resultado = analizar_carrera(ciclistas)
    numero, tiempo = resultado["ganador"]
    record = int(input("Récord anterior en segundos: " ))
    promedio = round(resultado["promedio_segundos"])
    print(f"Ganador: {numero}, tiempo {desde_segundos(tiempo)}")
    print("Batió el récord anterior." if tiempo < record else "No superó el récord anterior.")
    print(f"Tiempo promedio: {desde_segundos(promedio)}")


def ejercicio_4() -> None:
    while True:
        secreto = str(random.randint(1000, 9999))
        jugar_adivinanza(secreto, ruta_puntajes="mejores_puntajes.json")
        mostrar_puntajes(ruta="mejores_puntajes.json")
        if input("¿Jugar otra vez? (s/n): " ).strip().lower() != "s":
            break


def ejercicio_5() -> None:
    while True:
        secreto = str(random.randint(1000, 9999))
        jugar_pistas(secreto, ruta_puntajes="mejores_puntajes.json")
        mostrar_puntajes(ruta="mejores_puntajes.json")
        if input("¿Jugar otra vez? (s/n): " ).strip().lower() != "s":
            break


def ejercicio_6_y_7() -> None:
    cantidad = _leer_entero("Cantidad de números aleatorios: " , minimo=0)
    numeros = [random.randint(1, 20) for _ in range(cantidad)]
    secuencias = construir_secuencias(numeros)
    print("Números generados:", numeros)
    print("SECUENCIAS:", secuencias)
    print("Secuencia(s) más larga(s):", secuencias_mas_largas(secuencias))


def main() -> None:
    opciones = {
        "1": ("Alumnos", ejercicio_1),
        "2": ("Expensas", ejercicio_2),
        "3": ("Carrera de ciclistas", ejercicio_3),
        "4": ("Adivinanza y mejores marcas", ejercicio_4),
        "5": ("Pistas de dígitos", ejercicio_5),
        "6": ("Secuencias y secuencia(s) más larga(s)", ejercicio_6_y_7),
        "0": ("Salir", None),
    }
    while True:
        print("\nTP 8 - Ejercicios tipo Final")
        for clave, (titulo, _) in opciones.items():
            print(f"{clave}. {titulo}")
        seleccion = input("Elegí una opción: " ).strip()
        if seleccion == "0":
            print("¡Hasta luego!")
            break
        accion = opciones.get(seleccion, (None, None))[1]
        if accion is None:
            print("Opción inválida.")
        else:
            accion()


if __name__ == "__main__":
    main()
