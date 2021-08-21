import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

from app import app, crime_df, barrio_geojson
from datetime import date
from dash.dependencies import Input, Output, State
from lib import femicidesmodal, nondeadlyinjuriesmodal
from lib.FeatureCard import FeatureCard

# Current date time
current_date = date.today()
current_year = current_date.year

# Cards
femicides_card = FeatureCard("Femicides", 0, 0, False, "fas fa-female fa-2x", "female", "0 0 0 11px", femicidesmodal.modal_instance).create_card()
sexualviolence_card = FeatureCard( "Violencia sexual", 0, 0, False, "fas fa-venus fa-2x", "venus", "0 0 0 11px", '').create_card()
deadlyinjury_card = FeatureCard("Lesiones fatales", 0, 0, False, "fas fa-dizzy fa-2x", "dizzy", "1px 5px", '').create_card()
nondeadlyinjury_card = FeatureCard("Lesiones no fatales", 0, 0, False, "fas fa-user-injured fa-2x", "user-injured", "0 0 0 6px", nondeadlyinjuriesmodal.modal_instance).create_card()
theftpeople_card = FeatureCard("Hurto a personas", 0, 0, False, "fas fa-mask fa-2x", "mask", "0px", '').create_card()
theftresidence_card = FeatureCard("Hurto a residencias", 0, 0, False, "fas fa-house-damage fa-2x", "house-damage", "0 0 0 2px", '').create_card()
sexharassment__card = FeatureCard("Acoso sexual", 0, 0, False, "fas fa-venus-mars fa-2x", "venus-mars", "0 0 0 2px", '').create_card()
homicide_card = FeatureCard("Homicidio", 0, 0, False, "fas fa-skull fa-2x", "skull", "0 0 0 4px", '').create_card()
personalinjury_card = FeatureCard("Lesiones personales", 0, 0, False, "fas fa-crutch fa-2x", "crutch", "0 0 0 4px", '').create_card()


@app.callback(
    Output("barplot-barrio", "figure"),
    Input("search-btn", "n_clicks"),
    State("year", "value"),
)
def get_top_ten_barrios_graph(search_btn_clicks, year):
    global current_year
    current_year = year
    cases_df = crime_df[crime_df["AÑO"] == current_year]
    cases_df["BARRIO"] = cases_df["BARRIO"].str.capitalize()
    barrio_cn = cases_df.groupby("BARRIO")["CRIMEN_ID"].count().reset_index(name="casos")
    barrio_cn = barrio_cn.sort_values(by="casos", ascending=False).head(10)
    barrio_cn = barrio_cn.sort_values(by="casos")
    bar_plot = px.bar(
        barrio_cn,
        x="casos",
        y="BARRIO",
        color='casos',
        color_continuous_scale=px.colors.sequential.Blues,
        labels={"casos": "Casos {}".format(year), "BARRIO": "Barrio"}
    )
    bar_plot.update_traces(
        marker_line_color='rgb(8,48,107)',
        marker_line_width=0.05,
        opacity=1)
    bar_plot.update_layout(
        font_family="revert",
        font_color="#5f5f5f"
    )
    return bar_plot

@app.callback(
    Output("map-plot", "figure"),
    Input("search-btn", "n_clicks"),
    State("year", "value")
)
def map_plot_cases(search_btn_clicks, year):
    global current_year
    current_year = year
    cases_df = crime_df[crime_df["AÑO"] == current_year]
    barrio_cn = cases_df.groupby("BARRIO")["CRIMEN_ID"].count().reset_index(name="casos")
    fig = px.choropleth(
        barrio_cn,
        geojson=barrio_geojson,
        color="casos",
        color_continuous_scale=px.colors.sequential.Blues,
        locations="BARRIO", featureidkey="properties.NOMBRE",
        projection="mercator",
        labels={"casos": "Casos {}".format(year)}
    )
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def bar_plot_all_years():
    cases_df = crime_df.copy()
    filtered_cases = cases_df.groupby('AÑO').size().reset_index(name="casos")
    barplot_all_years = px.bar(
        filtered_cases,
        x="AÑO",
        y="casos",
        color='casos',
        color_continuous_scale=["#97bdd4", "rgb(12, 93, 179)"],
        labels={"AÑO": "Año", "casos": "Casos"}
    )
    barplot_all_years.update_layout(
        font_family="revert",
        font_color="#5f5f5f"
    )

    barplot_all_years.update_traces(opacity=0.8)
    barplot_all_years.update_xaxes(dtick="FECHA", ticklabelmode="period")
    barplot_all_years.update_layout(paper_bgcolor="white")
    return barplot_all_years


home_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("Dashboard", className="card-title",
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
                dbc.Col([html.Div([
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.FormGroup(
                                    [
                                        dbc.Label("Año:", html_for="year", width=2, className="labels-font"),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="year",
                                                options=[
                                                    {"label": "2010", "value": 2010},
                                                    {"label": "2011", "value": 2011},
                                                    {"label": "2012", "value": 2012},
                                                    {"label": "2013", "value": 2013},
                                                    {"label": "2014", "value": 2014},
                                                    {"label": "2015", "value": 2015},
                                                    {"label": "2016", "value": 2016},
                                                    {"label": "2017", "value": 2017},
                                                    {"label": "2018", "value": 2018},
                                                    {"label": "2019", "value": 2019},
                                                    {"label": "2020", "value": 2020},
                                                    {"label": "2021", "value": 2021}
                                                ],
                                                clearable=False,
                                                placeholder="Año...",
                                                value=current_date.year
                                            ),
                                            width=10,
                                        ),
                                    ],
                                    row=True,
                                )
                            ),
                            dbc.Col(
                                dbc.FormGroup(
                                    [
                                        dbc.Label("Mes:", html_for="month", width=2, className="labels-font"),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="month",
                                                options=[
                                                    {"label": "Enero", "value": 1},
                                                    {"label": "Febrero", "value": 2},
                                                    {"label": "Marzo", "value": 3},
                                                    {"label": "Abril", "value": 4},
                                                    {"label": "Mayo", "value": 5},
                                                    {"label": "Junio", "value": 6},
                                                    {"label": "Julio", "value": 7},
                                                    {"label": "Agosto", "value": 8},
                                                    {"label": "Septiembre", "value": 9},
                                                    {"label": "Octubre", "value": 10},
                                                    {"label": "Noviembre", "value": 11},
                                                    {"label": "Diciembre", "value": 12, "disabled": True}
                                                ],
                                                clearable=False,
                                                placeholder="Mes...",
                                                value=current_date.month
                                            ),
                                            width=10,
                                        ),
                                    ],
                                    row=True,
                                )
                            ),
                            dbc.Col(
                                dbc.Button("Buscar", color="secondary", className="mr-1", id="search-btn", n_clicks=0)
                            )
                        ], style={"padding-left": "5px"}
                    ),
                    dbc.Row(
                        [
                            dbc.Col([
                                html.Div(femicides_card, id="femicides-div"),
                                html.Div(sexualviolence_card, id="sexualviolence-div"),
                                html.Div(deadlyinjury_card, id="deadlyinjury-div")
                            ], width="auto"),
                            dbc.Col([
                                html.Div(nondeadlyinjury_card, id="nondeadlyinjury-div"),
                                html.Div(theftpeople_card, id="theftpeople-div"),
                                html.Div(theftresidence_card, id="theftresidence-div")
                            ], width="auto"),
                            dbc.Col([
                                html.Div(sexharassment__card, id="sexharassment-div"),
                                html.Div(homicide_card, id="homicide-div"),
                                html.Div(personalinjury_card, id="personalinjury-div")
                            ], width="auto")
                        ]
                    ),
                ])], width="5"),
                dbc.Col(
                    [
                        html.Div([
                                html.H5("Casos registrados desde el 2010", className="tile-title"),
                                dcc.Graph(id="bar-plot-all-years", figure=bar_plot_all_years(), style={"height": "87%"})
                                ],
                            style={
                                "border": "1px solid lightgrey",
                                "width": "100.8%",
                                "height": "100%",
                                "margin": "-4px",
                                "background": "white",
                                "border-radius": "10px"
                            }
                        )
                    ],
                    width="7"
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div([
                            html.H5(
                                "Top 10 de barrios con mayor cantidad de casos por año",
                                className="tile-title"
                            ),
                            dcc.Graph(id="barplot-barrio")
                        ],
                        style={
                            "border": "1px solid lightgrey",
                            "width": "100%",
                            "height": "100%",
                            "margin": "5px",
                            "padding-right": "5px",
                            "background": "white",
                            "border-radius": "10px"
                        }
                        )
                    ], width="7"
                ),
                dbc.Col(
                    [
                        html.Br(),
                        html.Div([
                            html.H5([
                                "Ubicación geográfica ",
                                html.I(className="fas fa-location-arrow", style={"color": "#5f5f5f"})],
                                className="tile-title"),
                            dcc.Graph(id="map-plot")
                        ],
                        style={
                            "border": "1px solid lightgrey",
                            "width": "100%",
                            "height": "100%",
                            "margin": "5px",
                            "padding-right": "5px",
                            "background": "white",
                            "border-radius": "10px"
                        }
                        )
                    ], width="5"
                )
            ]
        ),
    ],
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)

# @app.callback(
#     [
#         Output("number-cases-count", "children"),
#         Output("number-cases-arrow", "className"),
#         Output("number-cases-diff", "children"),
#         Output("number-cases-diff", "className"),
#     ],
#     [
#         Input("year", "value"),
#         Input("month", "value"),
#         Input("search-btn", "n_clicks")
#      ],
# )
# def refresh_dashboard_by_date(year, month, search_clicks):
#     number_cases_count = 5
#     number_cases_arrow_class = "fas fa-arrow-up card_arrow_up"
#     number_cases_diff_number = 2
#     number_cases_diff_class = "card_arrow_up"
#     if search_clicks > 0:
#         number_cases_count = 2
#         number_cases_arrow_class = "fas fa-arrow-down card_arrow_down"
#         number_cases_diff_number = 3
#         number_cases_diff_class = "card_arrow_down"
#     return number_cases_count, number_cases_arrow_class, number_cases_diff_number, number_cases_diff_class


@app.callback(
    [
        Output("femicides-div", "children"),
        Output("sexualviolence-div", "children"),
        Output("deadlyinjury-div", "children"),
        Output("nondeadlyinjury-div", "children"),
        Output("theftpeople-div", "children"),
        Output("theftresidence-div", "children"),
        Output("sexharassment-div", "children"),
        Output("homicide-div", "children"),
        Output("personalinjury-div", "children")
    ],
    [
        Input("search-btn", "n_clicks")
    ],
    [
        State("year", "value"),
        State("month", "value"),
     ],
)
def refresh_dashboard_by_date(search_clicks, year, month):
    global current_year
    current_year = year
    cases_df = crime_df[(crime_df["AÑO"] == current_year) & (crime_df["MES_num"] == month)]
    cases_before_df = pd.DataFrame()
    if month == 1:
        month_before = 12
        year_before = year - 1
    else:
        month_before = month - 1
        year_before = current_year

    if year_before >= 2010:
        cases_before_df = crime_df[(crime_df["AÑO"] == year_before) & (crime_df["MES_num"] == month_before)]

    femicides_count, femicides_diff, femicides_increased = get_card_info(cases_df, cases_before_df, "TIPO_DELITO", "FEMINICIDIO")
    nondeadly_count, nondeadly_diff, nondeadly_increase = get_card_info(cases_df, cases_before_df, "TIPO_LESION", "LESIONES NO FATALES")
    p_injuries_count, p_injuries_diff, p_injuries_increase = get_card_info(cases_df, cases_before_df, "TIPO_DELITO", "LESIONES PERSONALES")
    h_residence_count, h_residence_diff, h_residence_increase = get_card_info(cases_df, cases_before_df, "TIPO_DELITO", "HURTO A RESIDENCIAS")
    sexualviolence_count, sexualviolence_diff, sexualviolence_increase = get_card_info(cases_df, cases_before_df, "TIPO_LESION", "VIOLENCIA SEXUAL")
    deadly_count, deadly_diff, deadly_increase = get_card_info(cases_df, cases_before_df, "TIPO_LESION", "LESIONES FATALES")
    h_personas_count, h_personas_diff, h_personas_increase = get_card_info(cases_df, cases_before_df, "TIPO_DELITO", "HURTO A PERSONAS")
    homicide_count, homicide_diff, homicide_increase = get_card_info(cases_df, cases_before_df, "TIPO_DELITO", "HOMICIDIO")
    sexharassment_count, sexharassment_diff, sexharassment_increase = get_card_info(cases_df, cases_before_df, "TIPO_DELITO", "ACOSO SEXUAL")
    if search_clicks > 0:
        f = FeatureCard("Femicides", femicides_count, femicides_diff, femicides_increased, "fas fa-female fa-2x", "female", "0 0 0 11px", femicidesmodal.modal_instance).create_card(),
        vs = FeatureCard("Violencia sexual", sexualviolence_count, sexualviolence_diff, sexualviolence_increase, "fas fa-venus fa-2x", "venus", "0 0 0 11px", '').create_card(),
        lf = FeatureCard("Lesiones fatales", deadly_count, deadly_diff, deadly_increase, "fas fa-dizzy fa-2x", "dizzy", "1px 5px", '').create_card(),
        lnf = FeatureCard("Lesiones no fatales", nondeadly_count, nondeadly_diff, nondeadly_increase, "fas fa-user-injured fa-2x", "user-injured", "0 0 0 6px", nondeadlyinjuriesmodal.modal_instance).create_card(),
        hp = FeatureCard("Hurto a personas",  h_personas_count, h_personas_diff, h_personas_increase, "fas fa-mask fa-2x", "mask", "0px", '').create_card(),
        hr = FeatureCard("Hurto a residencias", h_residence_count, h_residence_diff, h_residence_increase, "fas fa-house-damage fa-2x", "house-damage", "0 0 0 2px", '').create_card(),
        vg = FeatureCard("Acoso sexual", sexharassment_count, sexharassment_diff, sexharassment_increase, "fas fa-venus-mars fa-2x", "venus-mars", "0 0 0 2px", '').create_card(),
        h = FeatureCard("Homicidio", homicide_count, homicide_diff, homicide_increase, "fas fa-skull fa-2x", "skull", "0 0 0 4px", '').create_card(),
        lp = FeatureCard("Lesiones personales", p_injuries_count, p_injuries_diff, p_injuries_increase, "fas fa-crutch fa-2x", "crutch", "0 0 0 4px", '').create_card(),
        return f, vs, lf, lnf, hp, hr, vg, h, lp
    return femicides_card, sexualviolence_card, deadlyinjury_card, nondeadlyinjury_card, theftpeople_card, \
           theftresidence_card, sexharassment__card, homicide_card, personalinjury_card


def get_card_info(cases_df, cases_before_df, column, value):
    count = len(cases_df[cases_df[column] == value])
    diff = count
    increased = True
    if not cases_before_df.empty:
        last_count = len(cases_before_df[cases_before_df[column] == value])
        diff = count - last_count
        increased = diff > 0
    else:
        diff = 0
        increased = False
    if diff < 0:
        diff = diff * (-1)
    return count, diff, increased
