import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dataloading

from app import app
from dash.dependencies import Input, Output
from lib import applicationconstants

allYears = applicationconstants.all_label
yearDropdownOptions = np.append([allYears], dataloading.crime_df[applicationconstants.AÑO].unique())

modal_instance = dbc.Modal(
    [
        dbc.ModalHeader(
            html.H5("Feminicidios", style={"font-family": "revert", "color": "#5f5f5f"})
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
                                                    id="femicides-year",
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
                                                    id="femicides-diasemana",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=[
                                                        {"label": col, "value": col} for col in dataloading.crime_df[applicationconstants.DIA_SEMANA].str.capitalize().unique()
                                                    ],
                                                ),
                                            ], width="3"),
                                            dbc.Col([
                                                dbc.Label(applicationconstants.month_label, className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="femicides-meses",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=dataloading.months,
                                                ),
                                            ], width="3"),
                                            dbc.Col([
                                                dbc.Label(applicationconstants.age_group_label, className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="femicides-grupoetario",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=[
                                                        {"label": col, "value": col} for col in dataloading.crime_df[applicationconstants.GRUPO_ETARIO_VICTIMA].str.capitalize().unique()
                                                    ]
                                                ),
                                            ], width="3")
                                        ], style={"padding": "0 16px 0 16px"}),
                                    dcc.Graph(id="femgraph"),
                                    html.Div(
                                        dbc.Checklist(
                                            id="femicides-diasemana-toggle",
                                            value=[0],
                                            switch=True,
                                            options=[
                                                {"label": applicationconstants.show_week_day_label, "value": 1}
                                            ],
                                            className="toggle-font"
                                        ),
                                        style={"padding-left": "16px", "margin": "25px 0"}
                                    ),
                                ],
                                 style={
                                     "height": "600px"
                                 }
                            )
                        ], width="12"
                    )
                ]
            ),
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Cerrar", id="femicides-close", className="ml-auto", n_clicks=0
            )
        ),
    ],
    id="femicides-modal",
    size="xl",
    is_open=False,
)


@app.callback(
    Output("femgraph", "figure"),
    [
     Input("femicides-year", "value"),
     Input("femicides-diasemana", "value"),
     Input("femicides-meses", "value"),
     Input("femicides-grupoetario", "value"),
     Input("femicides-diasemana-toggle", "value")
    ]
)
def generate_graphic(year, week_day, month, grupo_etario, show_by_week_day):
    cases_df = dataloading.crime_df[dataloading.crime_df[applicationconstants.TIPO_DELITO] == "FEMINICIDIO"]
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
    cases_df.loc[:, applicationconstants.MES] = cases_df[applicationconstants.MES].str.capitalize()
    if month:
        cases_df = cases_df[cases_df[applicationconstants.MES_num] == month]
    if week_day:
        cases_df = cases_df[cases_df[applicationconstants.DIA_SEMANA] == week_day]
    if grupo_etario:
        cases_df = cases_df[cases_df[applicationconstants.GRUPO_ETARIO_VICTIMA] == grupo_etario]

    # This if means the "Mostrar por día de la semana" toggle is off
    if len(show_by_week_day) == 1:
        femicides_df = cases_df.groupby([applicationconstants.UNIDAD_ESPACIAL]).size().reset_index(name="Casos")
        femicides_df = femicides_df.sort_values(by="Casos", ascending=False)
        fig = px.bar(
            femicides_df,
            x=applicationconstants.UNIDAD_ESPACIAL,
            y="Casos",
            color='Casos',
            color_continuous_scale=px.colors.sequential.Blues,
            labels={applicationconstants.UNIDAD_ESPACIAL: "Barrio"},
            height=500
        )
    else:
        femicides_df = cases_df.groupby([applicationconstants.DIA_SEMANA, applicationconstants.TIPO_DELITO]).size().reset_index(name="Casos")
        fig = px.bar(
            femicides_df.sort_values(by="Casos", ascending=False),
            x=applicationconstants.DIA_SEMANA,
            y="Casos",
            color='Casos',
            color_continuous_scale=px.colors.sequential.Blues,
            labels={applicationconstants.DIA_SEMANA: "Día de la semana", applicationconstants.TIPO_CONDUCTA: "Tipo Conducta", applicationconstants.TIPO_DELITO: "Tipo Delito"},
            height=500
        )
    fig.update_traces(
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0.2,
        opacity=0.8)
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f",
        xaxis=go.layout.XAxis(tickangle=45)
    )
    return fig