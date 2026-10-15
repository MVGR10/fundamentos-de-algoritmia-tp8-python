# Introducción a la Algoritmia - TP 8

Material de práctica en Python basado en los ejercicios tipo final de la **Guía de Trabajos Prácticos 2024** de Fundamentos de Informática / Introducción a la Algoritmia.

El objetivo de este proyecto es mostrar el planteo de soluciones modulares con funciones, validación de entradas, listas, ordenamiento, ciclos, generación aleatoria y pruebas automatizadas. Es material de práctica y portfolio; las soluciones están explicadas en el código y no reemplazan la revisión del enunciado ni el trabajo personal.

## Ejercicios incluidos

1. Alumnos: conteo y promedio de notas, legajos sobre el promedio y ordenamiento con listas paralelas o matriz de dos filas.
2. Expensas: validación de unidades únicas, cálculo del promedio y orden por superficie.
3. Carrera de ciclistas: ganador, comparación con récord y tiempo promedio.
4. Juego de adivinanza: pistas, abandono, intentos y tabla persistente de cinco mejores marcas.
5. Pistas de dígitos correctos y aproximados, contemplando dígitos repetidos.
6. Construcción de secuencias cuya suma no supera 20.
7. Búsqueda de todas las secuencias de longitud máxima.

## Uso

Requiere Python 3.10 o posterior. Desde esta carpeta:

```bash
python3 tp8_algoritmia.py
```

El menú permite ejecutar cada ejercicio. Para correr las pruebas:

```bash
python3 -m unittest -v
```

El ejercicio 4 guarda los cinco mejores resultados en `mejores_puntajes.json`. Para proteger datos personales, solicita un alias, no un número de documento.

## Nota sobre el enunciado

En el ejercicio 3 se toma como ganador al primer ciclista que haya registrado el menor tiempo si hay empate. En el ejercicio 4, abandonar con `-1` finaliza la partida y cuenta solamente los intentos válidos. En el ejercicio 6, las secuencias se forman en el orden original de los números aleatorios, insertando un cero antes de que la suma acumulada supere 20 y también al final.
