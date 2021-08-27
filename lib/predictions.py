import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pkg_resources import safe_extra

from dataloading import months
from app import app
from dataloading import crime_df, police_df, barrio_geojson, spunit_db, spunit_js
from datetime import date
from dash.dependencies import Input, Output, State

from lib import applicationconstants
from dataloading import crime_df


predictions_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("Predicciones", className="card-title",
                                    style={"font-family": "revert", "color": "#5f5f5f", "margin-left": "5px"}
                                ),
                                html.Hr(),
                        ])
                    ], width=12,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    label="Tipo de delito",
                                    tab_id="deadly-injuries-tab",
                                    labelClassName="tabs-font",
                                    activeLabelClassName="tabs-font-selected"),
                                dbc.Tab(
                                    label="Top delitos por comuna",
                                    tab_id="sexual-violence-tab",
                                    labelClassName="tabs-font",
                                    activeLabelClassName="tabs-font-selected"),
                            ],
                            id="tabs",
                            active_tab="deadly-injuries-tab",
                        ),
                        html.Div(id="tab-content"),
                    ], width=12,
                ),
            ]
        ),
    ],
    fluid=True
)

deadly_injuries_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Predicción de lesiones fatales", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label(applicationconstants.month_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-month",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=months
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.comuna_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-comuna",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in crime_df["COMUNA"].str.title().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.barrio_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-barrio",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in crime_df["BARRIO"].str.title().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="predict-graph1", style={"height": "74%"}),
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="12"
                )
            ]
        )
    ],
    id="deadly-injuries-container",
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)

sexual_violence_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Predicción de violencia sexual", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label(applicationconstants.month_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-violence-month",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=months
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.crime_type_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-violence-delito",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in crime_df["TIPO_DELITO"].str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="3"),
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="predict-graph1", style={"height": "74%"}),
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="12"
                )
            ]
        ),
    ],
    id="sexual-violence-container",
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    if active_tab is not None:
        if active_tab == "deadly-injuries-tab":
            return deadly_injuries_container
        elif active_tab == "sexual-violence-tab":
            return sexual_violence_container
    return deadly_injuries_container