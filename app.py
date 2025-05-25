import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# ------------------- Cargar archivo ---------------------
# Asegúrate de subir el archivo a Render y cambiar esta ruta si es necesario
try:
    df = pd.read_excel('Registros_Tecno_World.xlsx', engine='openpyxl')
    print("✅ Archivo cargado correctamente")
except Exception as e:
    print(f"❌ Error cargando archivo: {e}")
    # Datos de ejemplo si falla la carga
    df = pd.DataFrame({
        'Fecha': pd.date_range(start='2020-01-01', periods=24, freq='M'),
        'Ingresos': np.random.randint(1000, 5000, 24),
        'Gastos': np.random.randint(500, 3000, 24),
        'Marca': np.random.choice(['Samsung', 'Apple', 'Xiaomi'], 24),
        'Cliente': np.random.choice(['Minorista', 'Mayorista'], 24),
        'País': np.random.choice(['España', 'México', 'Colombia'], 24)
    })

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
    html.H1("Tablero Financiero TecnoWorld", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
    
    # Fila 1: Gráficos superiores
    html.Div([
        # Gráfico 1: Líneas con selector temporal
        html.Div([
            html.H3("Comportamiento mensual de la rentabilidad", 
                   style={'textAlign': 'center', 'color': '#3498db'}),
            dcc.Graph(id='grafico-linea-rentabilidad'),
            html.Div([
                html.Label("Agregación temporal:", style={'marginRight': '10px'}),
                dcc.RadioItems(
                    id='aggregation-radio',
                    options=[
                        {'label': 'Mensual', 'value': 'M'},
                        {'label': 'Semestral', 'value': 'S'},
                        {'label': 'Anual', 'value': 'Y'}
                    ],
                    value='M',
                    inline=True,
                    style={'display': 'inline-block'}
                )
            ], style={'textAlign': 'center', 'marginTop': '10px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '15px', 
                 'boxShadow': '0 0 5px rgba(0,0,0,0.1)', 'margin': '5px'}),
        
        # Gráfico 2: Barras por marca
        html.Div([
            html.H3("Ingreso total por marca", 
                   style={'textAlign': 'center', 'color': '#e74c3c'}),
            dcc.Graph(id='grafico-barras-ingresos-marca'),
            html.Button("Cambiar a horizontal", id='orientacion-boton', n_clicks=0,
                      style={'margin': '10px auto', 'display': 'block', 
                             'padding': '8px 15px', 'background': '#3498db', 
                             'color': 'white', 'border': 'none', 'borderRadius': '4px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '15px', 
                 'boxShadow': '0 0 5px rgba(0,0,0,0.1)', 'margin': '5px'})
    ], style={'marginBottom': '20px'}),
    
    # Fila 2: Gráficos inferiores
    html.Div([
        # Gráfico 3: Líneas por cliente
        html.Div([
            html.H3("Beneficios por mes y cliente", 
                   style={'textAlign': 'center', 'color': '#2ecc71'}),
            dcc.Graph(id='grafico-linea-beneficio-cliente'),
            html.Div([
                html.Label("Seleccionar Cliente:", style={'marginRight': '10px'}),
                dcc.Dropdown(
                    id='cliente-dropdown',
                    options=[{'label': c, 'value': c} for c in df['Cliente'].unique()],
                    value=df['Cliente'].unique()[0],
                    clearable=False,
                    style={'width': '200px', 'display': 'inline-block'}
                )
            ], style={'textAlign': 'center', 'marginTop': '10px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '15px', 
                 'boxShadow': '0 0 5px rgba(0,0,0,0.1)', 'margin': '5px'}),
        
        # Gráfico 4: Torta con controles
        html.Div([
            html.H3("Distribución porcentual de beneficios por país", 
                   style={'textAlign': 'center', 'color': '#f39c12'}),
            dcc.Graph(id='grafico-torta-pais'),
            html.Div([
                html.Label("Opacidad:", style={'marginRight': '10px'}),
                dcc.Slider(
                    id='slider-opacidad', 
                    min=0, 
                    max=1, 
                    step=0.1, 
                    value=1,
                    marks={i/10: str(i/10) for i in range(0, 11)},
                    tooltip={'placement': 'bottom'}
                ),
                html.Button("Cambiar a gráfico de barras", id='tipo-grafico-boton', n_clicks=0,
                          style={'margin': '10px auto', 'display': 'block', 
                                 'padding': '8px 15px', 'background': '#3498db', 
                                 'color': 'white', 'border': 'none', 'borderRadius': '4px'})
            ], style={'textAlign': 'center'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '15px', 
                 'boxShadow': '0 0 5px rgba(0,0,0,0.1)', 'margin': '5px'})
    ]),
    
    # Gráfico 5: Scatter con botón (oculto inicialmente)
    html.Div([
        html.H3("Relación Ingresos vs Gastos", 
               style={'textAlign': 'center', 'color': '#9b59b6'}),
        dcc.Graph(id='grafico-scatter'),
        html.Button("Cambiar fondo", id='boton-fondo', n_clicks=0,
                  style={'margin': '10px auto', 'display': 'block', 
                         'padding': '8px 15px', 'background': '#3498db', 
                         'color': 'white', 'border': 'none', 'borderRadius': '4px'})
    ], id='scatter-container', style={'display': 'none', 'padding': '15px', 
                                    'boxShadow': '0 0 5px rgba(0,0,0,0.1)', 'margin': '20px auto', 'width': '80%'})
])

# ------------------- Callbacks --------------------------

@app.callback(
    Output('grafico-linea-rentabilidad', 'figure'),
    Input('aggregation-radio', 'value')
)
def actualizar_rentabilidad(agg):
    df_temp = df.copy()
    if agg == 'M':
        df_temp['Periodo'] = df_temp['Fecha'].dt.to_period('M').astype(str)
    elif agg == 'S':
        df_temp['Periodo'] = df_temp['Fecha'].dt.to_period('6M').astype(str)
    elif agg == 'Y':
        df_temp['Periodo'] = df_temp['Fecha'].dt.year.astype(str)
    df_agg = df_temp.groupby('Periodo')['Rentabilidad'].sum().reset_index()
    fig = px.line(df_agg, x='Periodo', y='Rentabilidad', title='Rentabilidad Total',
                 labels={'Rentabilidad': 'Rentabilidad ($)', 'Periodo': 'Periodo'})
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(240,240,240,0.5)'
    )
    return fig

@app.callback(
    Output('grafico-barras-ingresos-marca', 'figure'),
    Input('aggregation-radio', 'value'),
    Input('orientacion-boton', 'n_clicks')
)
def actualizar_ingresos_marca(agg, n_clicks):
    df_agg = df.groupby('Marca')['Ingresos'].sum().reset_index()
    
    if n_clicks % 2 == 0:
        fig = px.bar(df_agg, x='Marca', y='Ingresos', title='Ingresos Totales por Marca',
                    labels={'Ingresos': 'Ingresos ($)', 'Marca': 'Marca'})
    else:
        fig = px.bar(df_agg, y='Marca', x='Ingresos', title='Ingresos Totales por Marca',
                    labels={'Ingresos': 'Ingresos ($)', 'Marca': 'Marca'},
                    orientation='h')
    
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(240,240,240,0.5)'
    )
    return fig

@app.callback(
    Output('grafico-linea-beneficio-cliente', 'figure'),
    Input('aggregation-radio', 'value'),
    Input('cliente-dropdown', 'value')
)
def actualizar_beneficios_cliente(agg, cliente):
    df_temp = df[df['Cliente'] == cliente].copy()
    if agg == 'M':
        df_temp['Periodo'] = df_temp['Fecha'].dt.to_period('M').astype(str)
    elif agg == 'S':
        df_temp['Periodo'] = df_temp['Fecha'].dt.to_period('6M').astype(str)
    elif agg == 'Y':
        df_temp['Periodo'] = df_temp['Fecha'].dt.year.astype(str)
    df_agg = df_temp.groupby('Periodo')['Rentabilidad'].sum().reset_index()
    fig = px.line(df_agg, x='Periodo', y='Rentabilidad', 
                 title=f'Beneficios para {cliente}',
                 labels={'Rentabilidad': 'Rentabilidad ($)', 'Periodo': 'Periodo'})
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(240,240,240,0.5)'
    )
    return fig

@app.callback(
    Output('grafico-torta-pais', 'figure'),
    Input('aggregation-radio', 'value'),
    Input('slider-opacidad', 'value'),
    Input('tipo-grafico-boton', 'n_clicks')
)
def actualizar_torta_pais(agg, opacidad, n_clicks):
    df_agg = df.groupby('País')['Rentabilidad'].sum().reset_index()
    
    if n_clicks % 2 == 0:
        fig = px.pie(df_agg, values='Rentabilidad', names='País',
                    title='Distribución de Beneficios por País',
                    opacity=opacidad)
    else:
        fig = px.bar(df_agg.sort_values('Rentabilidad', ascending=False), 
                    x='País', y='Rentabilidad',
                    title='Distribución de Beneficios por País',
                    color='País',
                    labels={'Rentabilidad': 'Rentabilidad ($)', 'País': 'País'})
    
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(240,240,240,0.5)'
    )
    return fig

@app.callback(
    Output('grafico-scatter', 'figure'),
    Input('boton-fondo', 'n_clicks')
)
def cambiar_fondo(n):
    fig = px.scatter(df, x='Ingresos', y='Gastos', color='Cliente',
                    title='Ingresos vs Gastos',
                    labels={'Ingresos': 'Ingresos ($)', 'Gastos': 'Gastos ($)'},
                    hover_data=['Marca', 'País'])
    if n % 2 == 1:
        fig.update_layout(plot_bgcolor='lightgray')
    else:
        fig.update_layout(plot_bgcolor='white')
    return fig

@app.callback(
    Output('scatter-container', 'style'),
    Input('tipo-grafico-boton', 'n_clicks')
)
def toggle_scatter(n_clicks):
    if n_clicks % 2 == 1:
        return {'display': 'block', 'padding': '15px', 
               'boxShadow': '0 0 5px rgba(0,0,0,0.1)', 
               'margin': '20px auto', 'width': '80%'}
    else:
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
  
