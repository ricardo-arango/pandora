import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dataloading

from lib import applicationconstants
from app import app
from dataloading import barrio_geojson
from dash.dependencies import Input, Output, State


voi = [
    'Extorsión',
    'Homicidio',
    'Homicidio culposo (en accidente de tránsito)',
    'Hurto a abigeato',
    'Hurto a automotores',
    'Hurto a entidades comerciales',
    'Hurto a entidades financieras',
    'Hurto a motocicletas',
    'Hurto a personas',
    'Hurto a piratería terrestre',
    'Hurto a residencias',
    'Incapacidad para trabajar o enfermedad',
    'Lesiones culposas',
    'Lesiones culposas (en accidente de transito)',
    'Lesiones personales',
    'Lesiones personales (circunstancias de agravación)',
    'Secuestro extorsivo'
]

view_by = [
    {"label": "Año", "value": applicationconstants.AÑO},
    {"label": "Mes", "value": applicationconstants.MES},
    {"label": "Tipo de arma", "value": applicationconstants.TIPO_ARMA},
    {"label": "Tipo de lesión", "value": applicationconstants.TIPO_LESION},
    {"label": "Género víctima", "value": applicationconstants.GENERO_VICTIMA},
    {"label": "Día semana", "value": applicationconstants.DIA_SEMANA},
    {"label": "Zona", "value": applicationconstants.ZONA},
    {"label": "Comuna", "value": applicationconstants.COMUNA},
    {"label": "Barrio", "value": applicationconstants.UNIDAD_ESPACIAL},
    {"label": "Grupo etario víctima", "value": applicationconstants.GRUPO_ETARIO_VICTIMA},
    {"label": "Estado civil víctima", "value": applicationconstants.ESTADO_CIVIL_VICTIMA}
]

yearDropdownOptions = np.append([applicationconstants.all_label], dataloading.crime_df[applicationconstants.AÑO].unique())

other_crimes_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("Otros crímenes", className="card-title",
                                    style={"font-family": "revert", "color": "#5f5f5f", "margin-left": "5px"}
                                ),
                                html.Hr()
                        ])
                    ], width=12,
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H5("Porcentaje de delitos", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label("Ver por:", className="labels-font labels-margin"),
                                            dcc.Dropdown(
                                                id="other_crimes_view_type",
                                                options=view_by,
                                                clearable=False,
                                                value=applicationconstants.AÑO
                                            ),
                                    ], width="4")
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="other_crimes_graph_table")
                            ],
                            className="heat-map-panel"
                        )
                    ],
                    width="7"
                ),
                dbc.Col(
                    [
                        html.Div([
                            html.H5("Ubicación geográfica", className="tile-title"),
                            html.Hr(),
                            dbc.Row(
                            [
                                dbc.Col([
                                    dbc.Label(applicationconstants.year_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="other_crimes_year",
                                            options=[
                                                {"label": col, "value": col} for col in yearDropdownOptions
                                            ],
                                            value=applicationconstants.all_label
                                        ),
                                ], width="4"),
                                dbc.Col([
                                    dbc.Label(applicationconstants.month_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="other_crimes_month",
                                            options=dataloading.months
                                        ),
                                ], width="4"),
                                dbc.Col([
                                    dbc.Label(applicationconstants.week_day_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="other_crimes_week_day",
                                            options=[
                                                {"label": col, "value": col} for col in dataloading.crime_df[applicationconstants.DIA_SEMANA].str.capitalize().unique()
                                            ]
                                        ),
                                ], width="4")
                            ], style={"padding": "0 16px 0 16px"}),
                            dbc.Row(
                            [
                                dbc.Col([
                                    dbc.Label(applicationconstants.crime_type_label, className="labels-font labels-margin"),
                                    dcc.Dropdown(
                                        id="other_crimes_crime_type",
                                        options=[
                                            {"label": col, "value": col} for col in
                                            voi
                                        ]
                                    ),
                                ], width="12"),

                            ], style={"padding": "0 16px 0 16px"}),
                            html.Br(), html.Br(),
                            dbc.Spinner(dcc.Graph(id="other-crimes-map-plot"), color="info")
                        ],
                            className="heat-map-panel"
                        )
                    ], width="5"
                )
            ]
        )
    ],
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)

@app.callback(
    Output("other_crimes_graph_table", "figure"),
    Input("other_crimes_view_type", "value"),
    State("other_crimes_view_type", "options")
)
def plot_heat_map(view_type, opt):
    cases_df = dataloading.crime_df.copy()
    cases_df.loc[:, applicationconstants.TIPO_DELITO] = cases_df[applicationconstants.TIPO_DELITO].str.capitalize()
    if view_type != applicationconstants.AÑO:
        cases_df.loc[:, view_type] = cases_df[view_type].str.capitalize()

    cross_df = pd.crosstab(
        index=cases_df[cases_df[applicationconstants.TIPO_DELITO].isin(voi)][applicationconstants.TIPO_DELITO],
        columns=cases_df[cases_df[applicationconstants.TIPO_DELITO].isin(voi)][view_type],
        normalize="index") * 100

    dictionary = {
        'z': cross_df.values.tolist(),
        'x': cross_df.columns.tolist(),
        'y': cross_df.index.tolist()
    }

    x_label = [x['label'] for x in opt if x['value'] == view_type]
    fig = go.Figure(
        data=go.Heatmap(
            dictionary,
            colorscale="blues",
            colorbar=dict(title='Casos'),
            hovertemplate=x_label[0] + ": %{x}<br>Tipo delito: %{y}<br>Porcentaje casos: %{z}<extra></extra>",
        ),
    )
    fig.update_xaxes(dtick=applicationconstants.FECHA, ticklabelmode="period")
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f",
        xaxis=go.layout.XAxis(tickangle=45),
        paper_bgcolor="white",
        width=990,
        height=550
    )
    return fig

@app.callback(
    Output("other-crimes-map-plot", "figure"),
    Input("other_crimes_year", "value"),
    Input("other_crimes_month", "value"),
    Input("other_crimes_week_day", "value"),
    Input("other_crimes_crime_type", "value"),
)
def map_plot(year, month, week_day, crime_type):
    cases_df = dataloading.crime_df.copy()
    if not year:
        year = 2010
    if year != applicationconstants.all_label:
        cases_df = cases_df[cases_df[applicationconstants.AÑO] == int(year)]

    cases_df.loc[:, applicationconstants.TIPO_DELITO] = cases_df[applicationconstants.TIPO_DELITO].str.capitalize()
    cases_df.loc[:, applicationconstants.DIA_SEMANA] = cases_df[applicationconstants.DIA_SEMANA].str.capitalize()
    cases_df.loc[:, applicationconstants.MES] = cases_df[applicationconstants.MES].str.capitalize()

    if month:
        cases_df = cases_df[cases_df[applicationconstants.MES_num] == month]
    if week_day:
        cases_df = cases_df[cases_df[applicationconstants.DIA_SEMANA] == week_day]
    if crime_type:
        cases_df = cases_df[cases_df[applicationconstants.TIPO_DELITO] == crime_type]

    barrio_cn = cases_df.groupby(applicationconstants.UNIDAD_ESPACIAL)[applicationconstants.CRIMEN_ID].count().reset_index(name="Casos")
    fig = px.choropleth(
        barrio_cn,
        geojson=barrio_geojson,
        color="Casos",
        color_continuous_scale=px.colors.sequential.Blues,
        locations=applicationconstants.UNIDAD_ESPACIAL, featureidkey="properties.NOMBRE",
        projection="mercator",
        labels={applicationconstants.UNIDAD_ESPACIAL: "Barrio"}
    )
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig
