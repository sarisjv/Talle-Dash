import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime

# ------------------- Cargar archivo ---------------------
# Asegúrate de que el archivo esté en la misma carpeta
df = pd.read_excel('Registros Tecno World.xlsx', engine='openpyxl')

# Preprocesamiento
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Mes'] = df['Fecha'].dt.to_period('M').astype(str)
df['Año'] = df['Fecha'].dt.year
df['Rentabilidad'] = df['Ingresos'] - df['Gastos']
df['Margen'] = df['Rentabilidad'] / df['Ingresos'].replace(0, 1)

# ------------------- App Dash --------------------------
app = dash.Dash(__name__)
server = app.server  # Necesario para Render

app.layout = html.Div([
    html.H1("Tablero Financiero TecnoWorld", style={'textAlign': 'center'}),

    # ... (todo tu layout actual igual que en Colab)
])

# ------------------- Callbacks --------------------------
# ... (todos tus callbacks actuales igual que en Colab)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
