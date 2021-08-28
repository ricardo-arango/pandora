import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import numpy as np
import plotly.express as px
import dataloading

from dataloading import spunit_db
from app import app
from dash.dependencies import Input, Output
from lib import applicationconstants
from dataloading import months
allYears = applicationconstants.all_label
yearDropdownOptions = np.append([allYears], dataloading.crime_df["AÑO"].unique())


modal_instance = dbc.Modal(
    [
        dbc.ModalHeader(
            html.H5("Violencia Domestica", style={"font-family": "revert", "color": "#5f5f5f"})
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
                                                dbc.Label(applicationconstants.year_label,
                                                          className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="domesticviolence-year",
                                                    options=[
                                                        {"label": col, "value": col} for col in yearDropdownOptions
                                                    ],
                                                    value=allYears,
                                                    clearable=False
                                                ),
                                            ], width="3"),
                                            dbc.Col([
                                                dbc.Label(applicationconstants.week_day_label,
                                                          className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="domesticviolence-diasemana",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=[
                                                        {"label": col, "value": col} for col in
                                                        dataloading.crime_df["DIA_SEMANA"].str.capitalize().unique()
                                                    ],
                                                ),
                                            ], width="3"),
                                            dbc.Col([
                                                dbc.Label(applicationconstants.month_label,
                                                          className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="domesticviolence-meses",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=months,
                                                ),
                                            ], width="3"),
                                            dbc.Col([
                                                dbc.Label(applicationconstants.age_group_label,
                                                          className="labels-font labels-margin"),
                                                dcc.Dropdown(
                                                    id="domesticviolence-grupoetario",
                                                    placeholder=applicationconstants.dropdown_placeholder,
                                                    options=[
                                                        {"label": col, "value": col} for col in
                                                        dataloading.crime_df["GRUPO_ETARIO_VICTIMA"].str.capitalize().unique()
                                                    ]
                                                ),
                                            ], width="3")
                                        ], style={"padding": "0 16px 0 16px"}),
                                    dcc.Graph(id="domesticviolencegraph"),
                                    html.Div(
                                        dbc.Checklist(
                                            id="domesticviolence-diasemana-toggle",
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
                                    "width": "100%",
                                    "height": "100%"
                                }
                            )
                        ], width="12"
                    )
                ]
            ),
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Cerrar", id="domesticviolence-close", className="ml-auto", n_clicks=0
            )
        ),
    ],
    id="domesticviolence-modal",
    size="xl",
    is_open=False,
)

@app.callback(
    Output("domesticviolencegraph", "figure"),
    [
     Input("domesticviolence-year", "value"),
     Input("domesticviolence-diasemana", "value"),
     Input("domesticviolence-meses", "value"),
     Input("domesticviolence-grupoetario", "value"),
     Input("domesticviolence-diasemana-toggle", "value")
    ]
)
def generate_graphic(year, week_day, month, grupo_etario, show_by_week_day):
    cases_df = dataloading.crime_df[dataloading.crime_df["TIPO_DELITO"] == "VIOLENCIA INTRAFAMILIAR"]
    if not year:
        year = 2010

    if year != allYears:
        cases_df = cases_df[cases_df["AÑO"] == int(year)]

    cases_df.loc[:, spunit_db] = cases_df[spunit_db].str.title()
    cases_df.loc[:, 'DIA_SEMANA'] = cases_df['DIA_SEMANA'].str.capitalize()
    cases_df.loc[:, 'TIPO_DELITO'] = cases_df['TIPO_DELITO'].str.capitalize()
    cases_df.loc[:, 'TIPO_CONDUCTA'] = cases_df['TIPO_CONDUCTA'].str.capitalize()
    cases_df.loc[:, 'TIPO_LESION'] = cases_df['TIPO_LESION'].str.capitalize()
    cases_df.loc[:, 'GRUPO_ETARIO_VICTIMA'] = cases_df['GRUPO_ETARIO_VICTIMA'].str.capitalize()
    cases_df.loc[:, 'MES'] = cases_df['MES'].str.capitalize()
    if month:
        cases_df = cases_df[cases_df["MES_num"] == month]
    if week_day:
        cases_df = cases_df[cases_df["DIA_SEMANA"] == week_day]
    if grupo_etario:
        cases_df = cases_df[cases_df["GRUPO_ETARIO_VICTIMA"] == grupo_etario]

    # This if means the "Mostrar por día de la semana" toggle is off
    if len(show_by_week_day) == 1:
        injury_type_df = cases_df.groupby([spunit_db]).size().reset_index(name="Casos")
        fig = px.bar(
            injury_type_df,
            x=spunit_db,
            y="Casos",
            color=spunit_db,
            color_continuous_scale=["#97bdd4", "rgb(12, 93, 179)"],
            labels={spunit_db: "Barrios"},
            height=800
        )
    else:
        injury_type_df = cases_df.groupby(["DIA_SEMANA", "TIPO_DELITO"]).size().reset_index(name="Casos")
        fig = px.bar(
            injury_type_df.sort_values(by="Casos", ascending=False),
            x="DIA_SEMANA",
            y="Casos",
            color="TIPO_DELITO",
            color_continuous_scale=["#97bdd4", "rgb(12, 93, 179)"],
            labels={"DIA_SEMANA": "Día de la semana", "TIPO_DELITO": "Tipo Delito"},
            height=800
        )
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f"
    )
    fig.update_traces(opacity=0.8)
    fig.update_layout(paper_bgcolor="white")
    return fig