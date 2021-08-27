import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dataloading

from app import app
from dataloading import police_df, barrio_geojson, spunit_db, spunit_js, months
from datetime import date
from dash.dependencies import Input, Output, State
from lib import applicationconstants
from lib.FeatureCard import FeatureCard

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
                                html.H5("Casos relacionados conviolencia sexual", className="tile-title"),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label(applicationconstants.year_label, html_for="year", width=2, className="labels-font"),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="year",
                                                options=[
                                                    {"label": col, "value": col} for col in np.append([applicationconstants.all_label], dataloading.crime_df["AÑO"].unique())
                                                ],
                                                clearable=False,
                                                value=applicationconstants.all_label
                                            ),
                                            width=10,
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.month_label, html_for="month", width=2, className="labels-font"),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="month",
                                                options=months,
                                                clearable=False,
                                                value=2
                                            ),
                                            width=10,
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.comuna_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="comuna",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in dataloading.crime_df["COMUNA"].str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.barrio_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="barrio",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in dataloading.crime_df["BARRIO"].str.title().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.age_group_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="grupoetario",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in dataloading.crime_df["GRUPO_ETARIO_VICTIMA"].str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="2")
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="bar-plot-all-years", style={"height": "74%"}),
                                html.Div(
                                    dbc.Checklist(
                                        id="diasemana-toggle",
                                        value=[0],
                                        switch=True,
                                        options=[
                                            {"label": applicationconstants.show_week_day_label, "value": 1}
                                        ],
                                        className="toggle-font"
                                    ),
                                    style={"padding-left": "16px", "margin": "-27px 0"}
                                ),
                            ],
                            className="panel-st-2"
                        )
                    ],
                    width="12"
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