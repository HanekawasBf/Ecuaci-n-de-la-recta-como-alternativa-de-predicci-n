"""
Modulo de calculo analitico del modelo lineal.

Contiene unicamente logica matematica (numpy/pandas): calculo de la
pendiente y ordenada al origen a partir de dos puntos, y generacion de
la tabla de interpolacion/prediccion.
"""

import numpy as np
import pandas as pd


def calcular_pendiente_y_ordenada(x1, y1, x2, y2):
    """
    Calcula analiticamente la pendiente (m) y la ordenada al origen (b)
    de la recta que pasa por los puntos P1(x1, y1) y P2(x2, y2).

    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    Return
    -------
    tuple(float, float)
        Pendiente (m) y ordenada al origen (b).
    """
    pendiente = (y2 - y1) / (x2 - x1)
    ordenada_origen = y1 - pendiente * x1
    return pendiente, ordenada_origen


def generar_tabla_prediccion(x1, x2, pendiente, ordenada_origen, puntos_futuros):
    """
    Genera un DataFrame con los valores interpolados dentro del intervalo
    [x1, x2] y los valores extrapolados (prediccion) para x > x2.

    Parameters
    ----------
    x1, x2 : float
        Valores de x de los puntos de referencia P1 y P2.
    pendiente, ordenada_origen : float
        Parametros de la recta ajustada (m y b).
    puntos_futuros : int
        Cantidad de valores enteros posteriores a x2 a proyectar.

    Return
    -------
    pandas.DataFrame
        Tabla con columnas 'x', 'y_proyectado' y 'Tipo'.
    """

    """
    Se Genera el rango de enteros entre x1 y x2 (interpolacion).
    np.floor(x1) y np.ceil(x2) redondean hacia afuera para no perder
    ningun punto del intervalo si x1 o x2 llegan como decimales.
    +1 al final porque np.arange no incluye el limite superior.
    """
    valores_x_interpolados = np.arange(int(np.floor(x1)), int(np.ceil(x2)) + 1)
    valores_x_extrapolados = np.arange(
        int(np.ceil(x2)) + 1, int(np.ceil(x2)) + 1 + puntos_futuros
    )

    # Se unen ambos rangos en un solo arreglo para procesarlos juntos
    valores_x_totales = np.concatenate([valores_x_interpolados, valores_x_extrapolados])

    # Se calcula y = m*x + b para TODOS los valores de x a la vez (vectorizado, sin for)
    valores_y_proyectados = pendiente * valores_x_totales + ordenada_origen

    """
    Se etiqueta cada fila segun si esta dentro del rango original (interpolacion)
    o fuera de el (prediccion/extrapolacion)
    """
    etiquetas_tipo = (
        ["Interpolación"] * len(valores_x_interpolados)
        + ["Predicción (Extrapolación)"] * len(valores_x_extrapolados)
    )

    tabla_resultado = pd.DataFrame(
        {
            "x": valores_x_totales,
            "y_proyectado": np.round(valores_y_proyectados, 4),
            "Tipo": etiquetas_tipo,
        }
    )
    return tabla_resultado