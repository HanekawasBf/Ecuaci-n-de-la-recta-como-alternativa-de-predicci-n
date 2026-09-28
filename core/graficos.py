"""
Construye la figura de Matplotlib con los puntos originales, la recta
ajustada y el rango proyectado. 
Regresa un objeto Figure que la capa de interfaz decide como mostrar (st.pyplot,guardar a archivo, etc.).
"""

import numpy as np
import matplotlib.pyplot as plt


def graficar_ajuste_lineal(x1, y1, x2, y2, pendiente, ordenada_origen, tabla_prediccion):
    """
    Construye el grafico Matplotlib con los puntos originales, la recta
    ajustada y los puntos proyectados (prediccion) de existir.

    Parameters
    ----------
    x1, y1, x2, y2 : float
        Coordenadas de los puntos de referencia P1 y P2.
    pendiente, ordenada_origen : float
        Parametros de la recta ajustada (m y b).
    tabla_prediccion : pandas.DataFrame
        Tabla generada por generar_tabla_prediccion, usada para definir
        el rango del eje X a graficar.

    Return
    -------
    matplotlib.figure.Figure
    """
    figura, ejes = plt.subplots(figsize=(7, 5))

    x_min = min(tabla_prediccion["x"].min(), x1)
    x_max = max(tabla_prediccion["x"].max(), x2)
    x_linea = np.linspace(x_min, x_max, 200)
    y_linea = pendiente * x_linea + ordenada_origen

    signo_ordenada = "+" if ordenada_origen >= 0 else "-"
    etiqueta_recta = (
        f"Recta ajustada: y = {pendiente:.4f}x {signo_ordenada} ({abs(ordenada_origen):.4f})"
    )

    ejes.plot(x_linea, y_linea, color="#1f77b4", linewidth=2, label=etiqueta_recta)
    ejes.scatter([x1], [y1], color="red", s=80, zorder=5, label=f"P1 ({x1}, {y1})")
    ejes.scatter([x2], [y2], color="green", s=80, zorder=5, label=f"P2 ({x2}, {y2})")

    ejes.set_title("Ajuste Lineal y Proyección de Datos", fontsize=13, fontweight="bold")
    ejes.set_xlabel("Eje X")
    ejes.set_ylabel("Eje Y")
    ejes.grid(True, linestyle="--", alpha=0.6)
    ejes.legend(loc="best")

    return figura