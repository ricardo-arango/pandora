import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dataloading
import seaborn as sns
from app import app
from dataloading import spunit_db, months
from datetime import date
from dash.dependencies import Input, Output, State
from lib import applicationconstants
from lib.FeatureCard import FeatureCard

voi = ['ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS',
       'ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS (CIRCUNSTANCIAS AGRAVACIÓN)',
       'ACCESO CARNAL O ACTO SEXUAL ABUSIVO CON INCAPAZ DE RESISTIR',
       'ACCESO CARNAL O ACTO SEXUAL EN PERSONA PUESTA EN INCAPACIDAD DE RESISTIR',
       'ACCESO CARNAL VIOLENTO',
       'ACCESO CARNAL VIOLENTO (CIRCUNSTANCIAS AGRAVACIÓN)',
       'ACOSO SEXUAL',
       'ACTO SEXUAL VIOLENTO',
       'ACTO SEXUAL VIOLENTO (CIRCUNSTANCIAS DE AGRAVACIÓN)',
       'ACTOS SEXUALES CON MENOR DE 14 AÑOS',
       'ACTOS SEXUALES CON MENOR DE 14 AÑOS (CIRCUNSTANCIAS DE AGRAVACIÓN)',
       'CONSTREÑIMIENTO A LA PROSTITUCIÓN',
       'DEMANDA DE EXPLOTACION SEXUAL COMERCIAL DE PERSONA MENOR DE 18 AÑOS DE EDAD',
       'ESTÍMULO A LA PROSTITUCIÓN DE MENORES',
       'FEMINICIDIO',
       'INDUCCIÓN A LA PROSTITUCIÓN',
       'LESIONES AL FETO',
       'PORNOGRAFÍA CON MENORES',
       'PROXENETISMO CON MENOR DE EDAD',
       'VIOLENCIA INTRAFAMILIAR']

sexual_violence_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("Violencia sexual", className="card-title",
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
                                html.H5("Casos relacionados con violencia sexual", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label(applicationconstants.year_label, className="labels-font labels-margin"),
                                            dcc.Dropdown(
                                                id="sex_violence_year",
                                                options=[
                                                    {"label": col, "value": col} for col in np.append([applicationconstants.all_label], dataloading.crime_df["AÑO"].unique())
                                                ],
                                                clearable=False,
                                                value=applicationconstants.all_label
                                            ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.month_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="sex_violence_month",
                                            options=months,
                                            clearable=False,
                                            value=1
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.comuna_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="sex_violence_comuna",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in dataloading.crime_df["COMUNA"].str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.barrio_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="sex_violence_barrio",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in dataloading.crime_df["BARRIO"].str.title().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.age_group_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="sex_violence_grupoetario",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in dataloading.crime_df["GRUPO_ETARIO_VICTIMA"].str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="3")
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="sex_violence_graph_table")
                            ],
                            className="sex-violence-panel"
                        )
                    ],
                    width="7"
                ),
                dbc.Col(
                    [
                        html.Div([
                            html.H5(
                                "Ubicación geográfica",
                                className="tile-title"),
                            html.Hr(),
                            dbc.Spinner(dcc.Graph(id="map-plot"), color="info")
                        ],
                            className="sex-violence-panel"
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
    Output("sex_violence_graph_table", "figure"),
    [
     Input("sex_violence_year", "value"),
     Input("sex_violence_month", "value"),
     Input("sex_violence_comuna", "value"),
     Input("sex_violence_barrio", "value"),
     Input("sex_violence_grupoetario", "value")
    ],
)
def plot_heat_map(year, month, comuna, barrio, grupo_etario):
    cases_df = pd.crosstab(
        index=dataloading.crime_df[dataloading.crime_df["TIPO_DELITO"].isin(voi)]["TIPO_DELITO"],
        columns=dataloading.crime_df[dataloading.crime_df["TIPO_DELITO"].isin(voi)]["COMUNA"],
        normalize="index") * 100
    # cases_df.loc[:, 'TIPO_DELITO'] = cases_df['TIPO_DELITO'].str.capitalize()
    # cases_df.loc[:, 'COMUNA'] = cases_df['COMUNA'].str.capitalize()

    dictionary = {
        'z': cases_df.values.tolist(),
        'x': cases_df.columns.tolist(),
        'y': cases_df.index.tolist()}

    fig = go.Figure(
        data=go.Heatmap(dictionary, colorscale="blues"),
    )
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f",
        paper_bgcolor="white"
    )
    return fig