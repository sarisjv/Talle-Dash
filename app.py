import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# Cargar los datos
df = pd.read_excel('Registros Tecno World.xlsx', sheet_name='Registros_2020-2022', engine='openpyxl')

# Limpieza y preparación de datos
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month
df['Semestre'] = np.where(df['Mes'] <= 6, 1, 2)
df['Trimestre'] = df['Fecha'].dt.quarter
df['Beneficio'] = df['Ingresos'] - df['Gastos']
df['Margen'] = (df['Beneficio'] / df['Ingresos']) * 100

# Crear la aplicación Dash
app = dash.Dash(__name__)
server = app.server  # Necesario para Render

# Diseño del tablero (tu layout completo aquí)
app.layout = html.Div([
    # ... (todo tu código de layout actual)
])

# Callbacks (tus callbacks actuales aquí)
@callback(
    # ... (tus callbacks actuales)
)
def update_graphs(paises, marcas, clientes, año, meses, grupo, bubble_clicks, pie_clicks):
    # ... (tu función actual)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)