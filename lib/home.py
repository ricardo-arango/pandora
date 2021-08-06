import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import geopandas
from datetime import date
from lib import femicidescard, sexualviolencecard, genderviolencecard, deadlyinjurycard, nondeadlyinjurycard
from lib import theftpeoplecard, theftresidencecard, homicidecard, personalinjurycard


# Current date time
current_date = date.today()

# Temporal cleaning up here
crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",")
crime_df["GRUPO_ETARIO_VICTIMA"] = crime_df["GRUPO_ETARIO_VICTIMA"].fillna("00. Sin Información")
barrio_geojson = geopandas.read_file("data/barrios_bucaramanga.geojson", driver="GeoJSON")


def map_plot_cases():
    year = current_date.year
    cases_df = crime_df[crime_df["AÑO"] == year]

    barrio_cn = cases_df.groupby("BARRIO")["CRIMEN_ID"].count().reset_index(name="casos")
    fig = px.choropleth(
        barrio_cn,
        geojson=barrio_geojson,
        color="casos",
        color_continuous_scale=px.colors.sequential.Blues,
        locations="BARRIO", featureidkey="properties.NOMBRE",
        projection="mercator",
        labels={"casos": "Casos"}
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

def top_ten_barrio_cases():
    year = 2010
    cases_df = crime_df[crime_df["AÑO"] == year]
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
        labels={"casos": "Casos", "BARRIO": "Barrio"}
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
                                dbc.Button("Buscar", color="secondary", className="mr-1")
                            )
                        ], style={"padding-left": "5px"}
                    ),
                    dbc.Row(
                        [
                            dbc.Col([
                                html.Div(femicidescard.femicides_card),
                                html.Div(sexualviolencecard.sexualviolence_card),
                                html.Div(deadlyinjurycard.deadlyinjury_card)
                            ], width="auto"),
                            dbc.Col([
                                html.Div(nondeadlyinjurycard.nondeadlyinjury_card),
                                html.Div(theftpeoplecard.theftpeople_card),
                                html.Div(theftresidencecard.theftresidence_card)
                            ], width="auto"),
                            dbc.Col([
                                html.Div(genderviolencecard.genderviolence_card),
                                html.Div(homicidecard.homicide_card),
                                html.Div(personalinjurycard.personalinjury_card)
                            ], width="auto")
                        ]
                    ),
                ])], width="5"),
                dbc.Col(
                    [
                        html.Div([
                                html.H5("Casos registrados desde el 2010", className="card-title",
                                    style={"font-family": "revert", "color": "#5f5f5f", "padding": "10px 0 0 15px"}),
                                dcc.Graph(id="bar-plot-all-years", figure=bar_plot_all_years(),
                                          style={"height": "87%"})
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
                            html.H5("Top 10 de barrios con mayor cantidad de casos en {}".format(2021), className="card-title",
                                style={"font-family": "revert", "color": "#5f5f5f", "padding": "10px 0 0 15px"}),
                            dcc.Graph(id="bar-plot-barrios", figure=top_ten_barrio_cases())
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
                                style={"font-family": "revert", "color": "#5f5f5f", "padding": "10px 0 0 15px"}),

                            dcc.Graph(id="map-plot", figure=map_plot_cases())
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