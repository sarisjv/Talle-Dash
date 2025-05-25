import dash
from dash import dcc, html, Input, Output, callback  # Añadí callback aquí
import plotly.express as px
import pandas as pd
from datetime import datetime

# Cargar archivo (verifica la ruta)
try:
    df = pd.read_excel('Registros Tecno World.xlsx', engine='openpyxl')
    print("✅ Archivo cargado correctamente. Filas:", len(df))
except Exception as e:
    print("❌ Error cargando el archivo:", str(e))
    df = pd.DataFrame()  # DataFrame vacío para evitar errores

# Preprocesamiento (con validación)
if not df.empty:
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Mes'] = df['Fecha'].dt.to_period('M').astype(str)
    df['Año'] = df['Fecha'].dt.year
    df['Rentabilidad'] = df['Ingresos'] - df['Gastos']
    df['Margen'] = df['Rentabilidad'] / df['Ingresos'].replace(0, 1)
    print("✅ Datos preprocesados")
else:
    print("❌ No hay datos para preprocesar")

app = dash.Dash(__name__)
server = app.server

# Layout (simplificado para prueba)
app.layout = html.Div([
    html.H1("Tablero Financiero TecnoWorld", style={'textAlign': 'center'}),
    
    # Gráfico de prueba mínimo
    dcc.Graph(
        id='grafico-prueba',
        figure=px.scatter(df, x='Ingresos', y='Gastos', title='Prueba Inicial')
        if not df.empty else {}
    ),
    
    # Tus componentes originales...
    # (Añádelos gradualmente después de verificar que esto funciona)
])

# Callback de prueba
@callback(
    Output('grafico-prueba', 'figure'),
    Input('grafico-prueba', 'id')
)
def update_graph(_):
    if not df.empty:
        return px.scatter(df, x='Ingresos', y='Gastos', color='Cliente', title='Datos Cargados')
    return {}

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
