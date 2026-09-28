"""
Alumno: Ortega Plaza Diego
Matricula: 2403230009
Asignatura: Ciencia de Datos
Fecha: 27/09/2026

Interfaz web (Streamlit) de la aplicacion. Este archivo NO contiene
logica de calculo ni de graficacion: unicamente los
componentes visuales y delega el procesamiento al `core`
(carga_datos, modelo_lineal, graficos).
"""

import streamlit as st

from core.carga_datos import cargar_puntos, ArchivoPuntosInvalido
from core.modelo_lineal import calcular_pendiente_y_ordenada, generar_tabla_prediccion
from core.graficos import graficar_ajuste_lineal


def configurar_pagina():
    """Define el titulo y layout general."""
    st.set_page_config(
        page_title="Ajuste de Recta y Predicción Interactiva",
        layout="wide",
    )


def mostrar_encabezado():
    """Muestra el titulo principal"""
    st.title("Ajuste de Recta y Predicción Interactiva")
    st.caption("Ciencia de Datos")
    st.divider()


def mostrar_barra_lateral():
    """
    Renderiza los controles de entrada en la barra lateral.

    Return
    -------
    tuple(UploadedFile or None, int)
        Archivo .csv cargado por el usuario y la cantidad de puntos de
        prediccion futura seleccionada mediante el slider.
    """
    st.sidebar.header("Configuración de Entrada")
    archivo_subido = st.sidebar.file_uploader(
        "Cargar archivo .csv con 2 puntos", type=["csv"]
    )
    puntos_futuros = st.sidebar.slider(
        "Puntos de predicción futura (x > x2):", min_value=1, max_value=15, value=5
    )
    return archivo_subido, puntos_futuros


def mostrar_parametros_analiticos(pendiente, ordenada_origen):
    """Muestra los valores calculados de m, b y la ecuacion de la recta."""
    st.subheader("Parámetros Analíticos Calculados")
    columna_m, columna_b, columna_ecuacion = st.columns(3)

    columna_m.metric("Pendiente (m)", f"{pendiente:.4f}")
    columna_b.metric("Ordenada al origen (b)", f"{ordenada_origen:.4f}")

    signo_ordenada = "+" if ordenada_origen >= 0 else "-"
    columna_ecuacion.markdown("Ecuación de la recta")
    columna_ecuacion.markdown(
        f"### y = {pendiente:.2f}x {signo_ordenada} {abs(ordenada_origen):.2f}"
    )
    st.divider()


def mostrar_grafica_y_tabla(figura, tabla_prediccion):
    """Muestra en dos columnas la grafica de Matplotlib y la tabla resultante."""
    columna_grafica, columna_tabla = st.columns(2)

    with columna_grafica:
        st.subheader("Visualización Gráfica")
        st.pyplot(figura)

    with columna_tabla:
        st.subheader("Tabla de Interpolación y Predicción")
        st.dataframe(tabla_prediccion, use_container_width=True)


def main():
    """Funcion principal que orquesta la ejecucion de la aplicacion."""
    configurar_pagina()
    mostrar_encabezado()

    archivo_subido, puntos_futuros = mostrar_barra_lateral()

    if archivo_subido is None:
        st.info("Carga un archivo .csv con dos puntos (columnas 'x' e 'y') para comenzar.")
        return

    try:
        dataframe_puntos = cargar_puntos(archivo_subido)
    except ArchivoPuntosInvalido as error:
        st.error(str(error))
        return

    x1, y1 = dataframe_puntos.loc[0, "x"], dataframe_puntos.loc[0, "y"]
    x2, y2 = dataframe_puntos.loc[1, "x"], dataframe_puntos.loc[1, "y"]

    pendiente, ordenada_origen = calcular_pendiente_y_ordenada(x1, y1, x2, y2)
    mostrar_parametros_analiticos(pendiente, ordenada_origen)

    tabla_prediccion = generar_tabla_prediccion(x1, x2, pendiente, ordenada_origen, puntos_futuros)
    figura = graficar_ajuste_lineal(x1, y1, x2, y2, pendiente, ordenada_origen, tabla_prediccion)

    mostrar_grafica_y_tabla(figura, tabla_prediccion)


if __name__ == "__main__":
    main()