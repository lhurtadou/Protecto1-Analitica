import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

# Lee el archivo CSV
df = pd.read_csv('DatosPS.csv')

# Convierte las columnas de fecha y hora a tipos categóricos para mejor visualización
df['Dia Semana'] = pd.Categorical(df['Dia Semana'], categories=['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'])
df['Mes'] = pd.Categorical(df['Mes'], categories=['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'])
df['Momento Dia'] = pd.Categorical(df['Momento Dia'], categories=['Madrugada', 'Mañana', 'Tarde', 'Noche'])

# Gráfico de barras (primera visualización)
fig_barras = px.bar(
    df,
    x="Dia Semana",
    y="Rented Bike Count",
    color="Momento Dia",
    barmode="group",
    facet_col="Mes",
    title="Número de bicicletas alquiladas por día de la semana, mes y momento del día",
    labels={"Rented Bike Count": "Número de bicicletas alquiladas"}
)

# Gráficos de dispersión para cada variable (segunda visualización)
figs_dispersión = {
    'Temperature(C)': px.scatter(df, x='Temperature(C)', y='Rented Bike Count', title='Número de Bicicletas Alquiladas vs. Temperatura'),
    'Humidity(%)': px.scatter(df, x='Humidity(%)', y='Rented Bike Count', title='Número de Bicicletas Alquiladas vs. Humedad'),
    'Wind speed (m/s)': px.scatter(df, x='Wind speed (m/s)', y='Rented Bike Count', title='Número de Bicicletas Alquiladas vs. Velocidad del Viento'),
    'Visibility (10m)': px.scatter(df, x='Visibility (10m)', y='Rented Bike Count', title='Número de Bicicletas Alquiladas vs. Visibilidad'),
    'Dew point temperature(C)': px.scatter(df, x='Dew point temperature(C)', y='Rented Bike Count', title='Número de Bicicletas Alquiladas vs. Punto de Rocío'),
    'Solar Radiation (MJ/m2)': px.scatter(df, x='Solar Radiation (MJ/m2)', y='Rented Bike Count', title='Número de Bicicletas Alquiladas vs. Radiación Solar'),
    'Rainfall(mm)': px.scatter(df, x='Rainfall(mm)', y='Rented Bike Count', title='Número de Bicicletas Alquiladas vs. Lluvia'),
    'Snowfall (cm)': px.scatter(df, x='Snowfall (cm)', y='Rented Bike Count', title='Número de Bicicletas Alquiladas vs. Nieve')
}

# Crear la aplicación Dash
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Estilos
label_style = {
    'font-weight': 'bold', 
    'color': '#2E8B57',
    'font-family': 'Lato, sans-serif'
}

output_style = {
    'border': '2px solid #4682B4',
    'padding': '10px',
    'font-size': '24px',
    'text-align': 'center',
    'color': '#4682B4',
    'font-weight': 'bold',
    'border-radius': '10px',
    'background-color': '#F0F8FF',
    'font-family': 'Lato, sans-serif'
}

title_style = {
    'font-weight': 'bold',
    'text-align': 'center',
    'color': '#4682B4',
    'font-family': 'Lato, sans-serif'
}

# Layout de la aplicación
app.layout = html.Div(children=[
    html.H1(children='Tablero de Bicicletas Alquiladas'),

    # Botones para cambiar entre visualizaciones
    html.Div(children=[
        html.Button('Visualización 1: Bicicletas por Día y Momento', id='btn-viz1', n_clicks=0),
        html.Button('Visualización 2: Variables Climáticas', id='btn-viz2', n_clicks=0),
        html.Button('Visualización 3: Simulación Rentabilidad', id='btn-viz3', n_clicks=0)
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'}),

    # Contenedor para los gráficos
    html.Div(id='graph-container')
])

# Callback para cambiar entre visualizaciones
@app.callback(
    Output('graph-container', 'children'),
    [Input('btn-viz1', 'n_clicks'),
     Input('btn-viz2', 'n_clicks'),
     Input('btn-viz3', 'n_clicks')]
)
def render_graph(viz1_clicks, viz2_clicks, viz3_clicks):
    if viz3_clicks > max(viz1_clicks, viz2_clicks):
        # Tercera visualización: simulación de rentabilidad
        return html.Div(
            [
                html.H1("Rentabilidad esperada Alquiler de Bicicletas", style=title_style),
                html.H6("Modifique el valor de cada una de las variables para ver el resultado de la variable de respuesta"),
                html.Div([
                    html.Div([
                        html.Label("Temperatura (°C)", style=label_style),
                        dcc.Slider(-17.8, 39.4, 5.5, value=-3, id='temperatura'),
                        html.Br(),
                        html.Label("Humedad (%)", style=label_style),
                        dcc.Slider(0, 98, 10, value=-3, id='humedad'),
                        html.Br(),
                        html.Label("Hora del día", style=label_style),
                        dcc.Slider(0, 23, 1, value=12, id='hour'),
                        html.Br(),
                        html.Label("Velocidad del viento (m/s)", style=label_style),
                        dcc.Input(id='wind_speed', type='number', value=3),
                        html.Br(),
                        html.Label("Visibilidad (10m)", style=label_style),
                        dcc.Input(id='visibility', type='number', value=10),
                        html.Br(),
                        html.Label("Temperatura del punto de rocío (°C)", style=label_style),
                        dcc.Input(id='dew_point', type='number', value=5),
                    ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),
                    html.Div([
                        html.Label("Radiación Solar (MJ/m²)", style=label_style),
                        dcc.Input(id='solar_radiation', type='number', value=0.5),
                        html.Br(),
                        html.Label("Precipitación (mm)", style=label_style),
                        dcc.Input(id='rainfall', type='number', value=0),
                        html.Br(),
                        html.Label("Nieve (cm)", style=label_style),
                        dcc.Input(id='snowfall', type='number', value=0),
                        html.Br(),
                        html.Label("Estación del año", style=label_style),
                        dcc.Dropdown(id='seasons', options=[
                            {'label': 'Primavera', 'value': 1},
                            {'label': 'Verano', 'value': 2},
                            {'label': 'Otoño', 'value': 3},
                            {'label': 'Invierno', 'value': 4},
                        ], value=1),
                        html.Br(),
                        html.Label("Día de la Semana", style=label_style),
                        dcc.Dropdown(id='dia_semana', options=[
                            {'label': 'Lunes', 'value': 1},
                            {'label': 'Martes', 'value': 2},
                            {'label': 'Miércoles', 'value': 3},
                            {'label': 'Jueves', 'value': 4},
                            {'label': 'Viernes', 'value': 5},
                            {'label': 'Sábado', 'value': 6},
                            {'label': 'Domingo', 'value': 7},
                        ], value=1),
                        html.Br(),
                        html.Label("Mes", style=label_style),
                        dcc.Dropdown(id='mes', options=[
                            {'label': 'Enero', 'value': 1},
                            {'label': 'Febrero', 'value': 2},
                            {'label': 'Marzo', 'value': 3},
                            {'label': 'Abril', 'value': 4},
                            {'label': 'Mayo', 'value': 5},
                            {'label': 'Junio', 'value': 6},
                            {'label': 'Julio', 'value': 7},
                            {'label': 'Agosto', 'value': 8},
                            {'label': 'Septiembre', 'value': 9},
                            {'label': 'Octubre', 'value': 10},
                            {'label': 'Noviembre', 'value': 11},
                            {'label': 'Diciembre', 'value': 12},
                        ], value=1),
                    ], style={'width': '45%', 'display': 'inline-block'}),
                ]),
                html.Div(id='output-container', style=output_style)
            ]
        )

    elif viz2_clicks > viz1_clicks:
        # Segunda visualización: gráficos de dispersión
        return html.Div([
            dcc.Dropdown(
                id='scatter-variable',
                options=[{'label': var, 'value': var} for var in figs_dispersión.keys()],
                value='Temperature(C)'
            ),
            dcc.Graph(id='scatter-graph')
        ])

    # Primera visualización: gráfico de barras
    return dcc.Graph(figure=fig_barras)


# Callback para actualizar el gráfico de dispersión basado en la variable seleccionada
@app.callback(
    Output('scatter-graph', 'figure'),
    [Input('scatter-variable', 'value')]
)
def update_scatter(variable):
    return figs_dispersión[variable]

# Corre la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
