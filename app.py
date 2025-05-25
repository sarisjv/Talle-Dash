import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Cargar datos
try:
    df = pd.read_excel('Registros Tecno World.xlsx', engine='openpyxl')
    print("✅ Datos cargados correctamente. Registros:", len(df))
except Exception as e:
    print(f"❌ Error cargando archivo: {str(e)}")
    df = pd.DataFrame()

# Preprocesamiento
if not df.empty:
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Año'] = df['Fecha'].dt.year
    df['Mes'] = df['Fecha'].dt.month
    df['Semestre'] = df['Fecha'].dt.quarter.apply(lambda x: 1 if x <= 2 else 2)
    df['Trimestre'] = df['Fecha'].dt.quarter
    df['Beneficio'] = df['Ingresos'] - df['Gastos']
    df['Margen'] = (df['Beneficio'] / df['Ingresos']).replace([-np.inf, np.inf], 0) * 100

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Tablero de Análisis Financiero TecnoWorld", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # Fila 1: Gráficos superiores
    html.Div([
        # Gráfico 1: Líneas con slider (cumple requisito de gráfico con rango)
        html.Div([
            html.H3("Evolución Mensual de Ingresos", style={'textAlign': 'center'}),
            dcc.Graph(id='line-chart'),
            dcc.RangeSlider(
                id='month-slider',
                min=1,
                max=12,
                step=1,
                value=[1, 12],
                marks={i: str(i) for i in range(1, 13)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        
        # Gráfico 2: Barras con selector (cumple requisito de botón para cambiar propiedad)
        html.Div([
            html.H3("Beneficio por Marca", style={'textAlign': 'center'}),
            dcc.Graph(id='bar-chart'),
            html.Button('Cambiar a Vista Horizontal', id='bar-button', n_clicks=0,
                      style={'margin': '10px auto', 'display': 'block'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ], style={'margin': '20px 0'}),
    
    # Fila 2: Gráficos inferiores
    html.Div([
        # Gráfico 3: Torta con interactividad (cumple requisito de múltiples gráficos)
        html.Div([
            html.H3("Distribución de Ingresos por País", style={'textAlign': 'center'}),
            dcc.Graph(id='pie-chart'),
            dcc.RadioItems(
                id='pie-radio',
                options=[
                    {'label': 'Gráfico de Torta', 'value': 'pie'},
                    {'label': 'Gráfico de Donut', 'value': 'donut'},
                    {'label': 'Gráfico de Barras', 'value': 'bar'}
                ],
                value='pie',
                inline=True,
                style={'textAlign': 'center'}
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        
        # Gráfico 4: Dispersión con botón (cumple requisito de cambio de propiedad)
        html.Div([
            html.H3("Relación Ingresos vs. Gastos", style={'textAlign': 'center'}),
            dcc.Graph(id='scatter-chart'),
            html.Button('Cambiar Color de Fondo', id='scatter-button', n_clicks=0,
                      style={'margin': '10px auto', 'display': 'block'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Selectores globales
    html.Div([
        html.Div([
            html.Label("Seleccionar Año:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': año, 'value': año} for año in sorted(df['Año'].unique())],
                value=sorted(df['Año'].unique())[-1],
                clearable=False
            )
        ], style={'width': '24%', 'display': 'inline-block', 'margin': '10px'}),
        
        html.Div([
            html.Label("Agrupación Temporal:", style={'fontWeight': 'bold'}),
            dcc.RadioItems(
                id='time-radio',
                options=[
                    {'label': 'Mensual', 'value': 'Mes'},
                    {'label': 'Trimestral', 'value': 'Trimestre'},
                    {'label': 'Semestral', 'value': 'Semestre'}
                ],
                value='Mes',
                inline=True
            )
        ], style={'width': '24%', 'display': 'inline-block', 'margin': '10px'})
    ], style={'textAlign': 'center', 'margin': '20px 0'})
])

# Callbacks para interactividad

# Gráfico de líneas con slider
@callback(
    Output('line-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('month-slider', 'value'),
    Input('time-radio', 'value')
)
def update_line_chart(year, month_range, time_group):
    filtered_df = df[(df['Año'] == year) & 
                    (df['Mes'].between(month_range[0], month_range[1]))]
    
    if time_group == 'Mes':
        group_col = 'Mes'
    elif time_group == 'Trimestre':
        group_col = 'Trimestre'
    else:
        group_col = 'Semestre'
    
    line_data = filtered_df.groupby(group_col)['Ingresos'].sum().reset_index()
    
    fig = px.line(
        line_data, 
        x=group_col, 
        y='Ingresos',
        title=f'Ingresos {time_group.lower()} en {year} (Meses {month_range[0]}-{month_range[1]})',
        markers=True
    )
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(240,240,240,0.5)'
    )
    return fig

# Gráfico de barras con botón
@callback(
    Output('bar-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('bar-button', 'n_clicks'),
    Input('time-radio', 'value')
)
def update_bar_chart(year, n_clicks, time_group):
    filtered_df = df[df['Año'] == year]
    bar_data = filtered_df.groupby(['Marca', time_group])['Beneficio'].sum().reset_index()
    
    if n_clicks % 2 == 0:
        fig = px.bar(
            bar_data, 
            x='Marca', 
            y='Beneficio',
            color=time_group,
            title=f'Beneficio por Marca ({time_group})',
            barmode='group'
        )
    else:
        fig = px.bar(
            bar_data, 
            y='Marca', 
            x='Beneficio',
            color=time_group,
            title=f'Beneficio por Marca ({time_group})',
            orientation='h'
        )
    
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(240,240,240,0.5)'
    )
    return fig

# Gráfico circular con selector
@callback(
    Output('pie-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('pie-radio', 'value')
)
def update_pie_chart(year, chart_type):
    pie_data = df[df['Año'] == year].groupby('País')['Ingresos'].sum().reset_index()
    
    if chart_type == 'pie':
        fig = px.pie(
            pie_data,
            values='Ingresos',
            names='País',
            title='Distribución de Ingresos por País',
            hole=0
        )
    elif chart_type == 'donut':
        fig = px.pie(
            pie_data,
            values='Ingresos',
            names='País',
            title='Distribución de Ingresos por País',
            hole=0.4
        )
    else:
        fig = px.bar(
            pie_data.sort_values('Ingresos', ascending=False),
            x='País',
            y='Ingresos',
            title='Ingresos por País',
            color='País'
        )
    
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='rgba(240,240,240,0.5)'
    )
    return fig

# Gráfico de dispersión con botón
@callback(
    Output('scatter-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('scatter-button', 'n_clicks')
)
def update_scatter_chart(year, n_clicks):
    scatter_data = df[df['Año'] == year]
    
    fig = px.scatter(
        scatter_data,
        x='Ingresos',
        y='Gastos',
        color='Cliente',
        size='Beneficio',
        title='Relación Ingresos vs. Gastos',
        hover_data=['Marca', 'País']
    )
    
    if n_clicks % 2 == 0:
        fig.update_layout(plot_bgcolor='white')
    else:
        fig.update_layout(plot_bgcolor='lightgray')
    
    return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
