# Ajuste de Recta y Prediccion Interactiva

Aplicacion web hecha con **Streamlit** que recibe un archivo `.csv` con dos puntos
P1(x1, y1) y P2(x2, y2), calcula la recta que pasa por ellos, la grafica y genera
una tabla de interpolacion y prediccion.

- **Alumno:** Ortega Plaza Diego
- **Matricula:** 2403230009
- **Asignatura:** Ciencia de Datos

## Que hace

1. Carga un `.csv` con exactamente dos puntos y lo valida (pandas).
2. Calcula la pendiente y la ordenada al origen:
   - `m = (y2 - y1) / (x2 - x1)`
   - `b = y1 - m * x1`
3. Grafica los puntos y la recta ajustada (matplotlib).
4. Genera una tabla con los valores interpolados (entre x1 y x2) y los valores
   predichos para x > x2 (numpy). La cantidad de puntos futuros se elige con un slider.

## Instalacion y uso

```bash
# 1. Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate         

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicacion
streamlit run app.py
```

## Formato del archivo .csv

Dos filas con las columnas `x` e `y`:

```csv
x,y
1.0,3.0
8.0,14.0
```

## Librerias utilizadas

- `streamlit`: interfaz web y carga del archivo
- `pandas`: lectura, validacion y tabla de resultados
- `numpy`: calculo vectorizado de los valores proyectados
- `matplotlib`: grafica de la recta y los puntos
