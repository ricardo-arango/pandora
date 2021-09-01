import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import numpy as np
import plotly.express as px
import dataloading
import plotly.graph_objects as go

from app import app
from dash.dependencies import Input, Output
from lib import applicationconstants

allYears = applicationconstants.all_label
yearDropdownOptions = np.append([allYears], dataloading.crime_df[applicationconstants.AÑO].unique())


modal_instance = dbc.Modal(
    [
        dbc.ModalHeader(
            html.H5("Violencia sexual", style={"font-family": "revert", "color": "#5f5f5f"})
        ),
        dbc.ModalBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col([
                                                dbc.Label(applicationconstants.year_label, className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="sexviolence-year",
                                                    options=[
                                                        {"label": col, "value": col} for col in yearDropdownOptions
                                                    ],
                                                    value=allYears,
                                                    clearable=False
                                                ),
                                            ], width="3"),
                                            dbc.Col([
                                                dbc.Label(applicationconstants.week_day_label, className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="sexviolence-diasemana",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=[
                                                        {"label": col, "value": col} for col in dataloading.crime_df[applicationconstants.DIA_SEMANA].str.capitalize().unique()
                                                    ],
                                                ),
                                            ], width="3"),
                                            dbc.Col([
                                                dbc.Label(applicationconstants.barrio_label, className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="sexviolence-barrio",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=[
                                                        {"label": col, "value": col} for col in dataloading.crime_df[applicationconstants.UNIDAD_ESPACIAL].str.title().unique()
                                                    ],
                                                ),
                                            ], width="3"),
                                            dbc.Col([
                                                dbc.Label(applicationconstants.age_group_label, className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="sexviolence-grupoetario",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=[
                                                        {"label": col, "value": col} for col in dataloading.crime_df[applicationconstants.GRUPO_ETARIO_VICTIMA].str.capitalize().unique()
                                                    ]
                                                ),
                                            ], width="3")
                                        ], style={"padding": "0 16px 0 16px"}),
                                    dcc.Graph(id="sexviolence-graph"),
                                    html.Div(
                                        dbc.Checklist(
                                            id="sexviolence-diasemana-toggle",
                                            value=[0],
                                            switch=True,
                                            options=[
                                                {"label": applicationconstants.show_week_day_label, "value": 1}
                                            ],
                                            className="toggle-font"
                                        ),
                                        style={"padding-left": "16px", "margin": "-20px 0"}
                                    ),
                                ],
                                style={
                                    "height": "850px"
                                }
                            )
                        ],
                        width="12"
                    )
                ]
            ),
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Cerrar", id="sexviolence-close", className="ml-auto", n_clicks=0
            )
        ),
    ],
    id="sexviolence-modal",
    size="xl",
    is_open=False
)


@app.callback(
    Output("sexviolence-graph", "figure"),
    [
     Input("sexviolence-year", "value"),
     Input("sexviolence-diasemana", "value"),
     Input("sexviolence-barrio", "value"),
     Input("sexviolence-grupoetario", "value"),
     Input("sexviolence-diasemana-toggle", "value")
    ]
)
def generate_graphic(year, week_day, barrio, grupo_etario, show_by_week_day):
    cases_df = dataloading.crime_df[dataloading.crime_df[applicationconstants.TIPO_LESION] == "VIOLENCIA SEXUAL"]
    if not year:
        year = 2010

    if year != allYears:
        cases_df = cases_df[cases_df[applicationconstants.AÑO] == int(year)]

    cases_df.loc[:, applicationconstants.UNIDAD_ESPACIAL] = cases_df[applicationconstants.UNIDAD_ESPACIAL].str.title()
    cases_df.loc[:, applicationconstants.DIA_SEMANA] = cases_df[applicationconstants.DIA_SEMANA].str.capitalize()
    cases_df.loc[:, applicationconstants.TIPO_DELITO] = cases_df[applicationconstants.TIPO_DELITO].str.capitalize()
    cases_df.loc[:, applicationconstants.TIPO_CONDUCTA] = cases_df[applicationconstants.TIPO_CONDUCTA].str.capitalize()
    cases_df.loc[:, applicationconstants.TIPO_LESION] = cases_df[applicationconstants.TIPO_LESION].str.capitalize()
    cases_df.loc[:, applicationconstants.GRUPO_ETARIO_VICTIMA] = cases_df[applicationconstants.GRUPO_ETARIO_VICTIMA].str.capitalize()
    if barrio:
        cases_df = cases_df[cases_df[applicationconstants.UNIDAD_ESPACIAL] == barrio]
    if week_day:
        cases_df = cases_df[cases_df[applicationconstants.DIA_SEMANA] == week_day]
    if grupo_etario:
        cases_df = cases_df[cases_df[applicationconstants.GRUPO_ETARIO_VICTIMA] == grupo_etario]

    # This if means the "Mostrar por día de la semana" toggle is off
    if len(show_by_week_day) == 1:
        injury_type_df = cases_df.groupby([applicationconstants.TIPO_DELITO, applicationconstants.TIPO_CONDUCTA]).size().reset_index(name="Casos")
        injury_type_df = injury_type_df.sort_values(by="Casos", ascending=False)
        fig = px.bar(
            injury_type_df,
            x=applicationconstants.TIPO_DELITO,
            y="Casos",
            color=applicationconstants.TIPO_CONDUCTA,
            color_continuous_scale=["#97bdd4", "rgb(12, 93, 179)"],
            labels={applicationconstants.TIPO_CONDUCTA: "Tipo Conducta", applicationconstants.TIPO_DELITO: "Tipo Delito"},
            height=800
        )
    else:
        injury_type_df = cases_df.groupby([applicationconstants.DIA_SEMANA, applicationconstants.TIPO_DELITO, applicationconstants.TIPO_CONDUCTA]).size().reset_index(name="Casos")
        fig = px.bar(
            injury_type_df.sort_values(by="Casos", ascending=False),
            x=applicationconstants.DIA_SEMANA,
            y="Casos",
            color=applicationconstants.TIPO_CONDUCTA,
            color_continuous_scale=["#97bdd4", "rgb(12, 93, 179)"],
            labels={applicationconstants.DIA_SEMANA: "Día de la semana", applicationconstants.TIPO_CONDUCTA: "Tipo Conducta", applicationconstants.TIPO_DELITO: "Tipo Delito"},
            height=800
        )
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f",
        xaxis=go.layout.XAxis(tickangle=45),
        paper_bgcolor="white"
    )
    fig.update_traces(opacity=0.8)
    return fig
