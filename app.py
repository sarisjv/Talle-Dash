import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# Configuración inicial con manejo de errores
try:
    # Cargar datos (nombre de archivo sin espacios)
    df = pd.read_excel('Registros_Tecno_World.xlsx', engine='openpyxl')
    print("✅ Archivo Excel cargado correctamente")
    
    # Preprocesamiento
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df = df.dropna(subset=['Fecha'])  # Eliminar filas con fechas inválidas
    df['Año'] = df['Fecha'].dt.year
    df['Mes'] = df['Fecha'].dt.month
    df['Semestre'] = np.where(df['Mes'] <= 6, 1, 2)
    df['Trimestre'] = df['Fecha'].dt.quarter
    df['Beneficio'] = df['Ingresos'] - df['Gastos']
    df['Margen'] = np.where(
        df['Ingresos'] != 0, 
        (df['Beneficio'] / df['Ingresos']) * 100, 
        0
    )
    
except Exception as e:
    print(f"❌ Error crítico: {str(e)}")
    # Datos de ejemplo para evitar fallos
    df = pd.DataFrame({
        'Fecha': [datetime.now()],
        'Ingresos': [0],
        'Gastos': [0],
        'País': ['Ejemplo'],
        'Marca': ['Ejemplo'],
        'Cliente': ['Ejemplo']
    })

# Inicializar la app
app = dash.Dash(__name__)
server = app.server  # Essential for Render

# Layout simplificado para pruebas
app.layout = html.Div([
    html.H1("Tablero TecnoWorld - Versión Simplificada", style={'textAlign': 'center'}),
    
    html.Div([
        # Gráfico 1
        html.Div([
            dcc.Graph(
                id='grafico-prueba',
                figure=px.scatter(df, x='Ingresos', y='Gastos', title='Datos Cargados')
            )
        ], style={'width': '48%', 'display': 'inline-block'})
    ]),
    
    # Console log para debug
    html.Div(id='console-output', style={'whiteSpace': 'pre-line'})
])

# Callback básico
@callback(
    Output('console-output', 'children'),
    Input('grafico-prueba', 'id')
)
def update_console(_):
    console_msg = f"""
    Estado del Sistema:
    - Registros cargados: {len(df)}
    - Columnas disponibles: {', '.join(df.columns)}
    """
    return console_msg

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
  
