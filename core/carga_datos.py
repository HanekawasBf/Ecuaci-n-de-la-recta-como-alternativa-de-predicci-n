"""
Modulo de carga y validacion de datos.

Contiene la logica responsable de leer el archivo .csv de entrada y
validar que cumpla con el formato esperado (dos puntos, columnas 'x' e 'y').
Recibe un objeto tipo archivo y regresa un
DataFrame o lanza una excepcion, para poder reutilizarse o probarse
de forma independiente de la interfaz web.
"""

import pandas as pd


class ArchivoPuntosInvalido(Exception):
    """Excepcion lanzada cuando el .csv de entrada no cumple el formato esperado."""


def cargar_puntos(archivo_csv):
    """
    Lee y valida un archivo .csv que debe contener exactamente dos registros
    con las columnas 'x' e 'y'.

    Parameters
    ----------
    archivo_csv : str, Path o file-like object
        Ruta o archivo .csv a leer (compatible con st.file_uploader).

    Return
    -------
    pandas.DataFrame
        DataFrame ordenado por 'x' con exactamente dos filas (P1 y P2).

    Raises
    ------
    ArchivoPuntosInvalido
        Si faltan columnas, si no hay exactamente dos puntos, o si
        x1 es igual a x2 (recta indefinida).
    """
    dataframe_puntos = pd.read_csv(archivo_csv)
    dataframe_puntos.columns = [columna.strip().lower() for columna in dataframe_puntos.columns]

    if not {"x", "y"}.issubset(dataframe_puntos.columns):
        raise ArchivoPuntosInvalido("El archivo .csv debe contener las columnas 'x' e 'y'.")

    if len(dataframe_puntos) != 2:
        raise ArchivoPuntosInvalido("El archivo .csv debe contener únicamente dos puntos (P1 y P2).")

    dataframe_puntos = dataframe_puntos.sort_values(by="x").reset_index(drop=True)

    if dataframe_puntos.loc[0, "x"] == dataframe_puntos.loc[1, "x"]:
        raise ArchivoPuntosInvalido("Los valores de 'x' de P1 y P2 no pueden ser iguales.")

    return dataframe_puntos