import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dataloading
from lib import applicationconstants
from app import app
from dataloading import spunit_db, barrio_geojson
from dash.dependencies import Input, Output, State


voi = ['Acceso carnal abusivo con menor de 14 años',
 'Acceso carnal abusivo con menor de 14 años (circunstancias agravación)',
 'Acceso carnal o acto sexual abusivo con persona en incapacidad de resistir',
 'Acceso carnal o acto sexual en persona puesta en incapacidad de resistir',
 'Acceso carnal violento',
 'Acceso carnal violento (circunstancias agravación)',
 'Acoso sexual',
 'Acto sexual violento',
 'Acto sexual violento (circunstancias de agravación)',
 'Actos sexuales con menor de 14 años',
 'Actos sexuales con menor de 14 años (circunstancias de agravación)',
 'Constreñimiento a la prostitución',
 'Demanda de explotacion sexual comercial de persona menor de 18 años de edad',
 'Estímulo a la prostitución de menores',
 'Feminicidio',
 'Inducción a la prostitución',
 'Lesiones al feto',
 'Pornografía con menores',
 'Proxenetismo con menor de edad',
 'Violencia intrafamiliar']

view_by = [
    {"label": "Año", "value": 'AÑO'},
    {"label": "Mes", "value": 'MES'},
    {"label": "Tipo de arma", "value": 'TIPO_ARMA'},
    {"label": "Tipo de lesión", "value": 'TIPO_LESION'},
    {"label": "Género víctima", "value": 'GENERO_VICTIMA'},
    {"label": "Día semana", "value": 'DIA_SEMANA'},
    {"label": "Zona", "value": 'ZONA'},
    {"label": "Comuna", "value": 'COMUNA'},
    {"label": "Barrio", "value": spunit_db},
    {"label": "Grupo etario víctima", "value": 'GRUPO_ETARIO_VICTIMA'},
    {"label": "Estado civil víctima", "value": 'ESTADO_CIVIL_VICTIMA'}
]

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
                                html.H5("Porcentaje de casos relacionados con violencia sexual", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label("Ver por:", className="labels-font labels-margin"),
                                            dcc.Dropdown(
                                                id="sex_violence_view_type",
                                                options=view_by,
                                                clearable=False,
                                                value="AÑO"
                                            ),
                                    ], width="4")
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="sex_violence_graph_table")
                            ],
                            className="sex-violence-panel"
                        )
                    ],
                    width="8"
                ),
                dbc.Col(
                    [
                        html.Div([
                            html.H5(
                                "Ubicación geográfica",
                                className="tile-title"),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label(applicationconstants.crime_type_label, className="labels-font labels-margin"),
                                            dcc.Dropdown(
                                                id="sex_violence_crime_type",
                                                options=[
                                                    {"label": col, "value": col} for col in
                                                    voi
                                                ]
                                            ),
                                    ], width="12")
                                ], style={"padding": "0 16px 0 16px"}),
                            dbc.Spinner(dcc.Graph(id="sexual-violence-map-plot", style={"width": "101%"}), color="info")
                        ],
                            className="sex-violence-panel"
                        )
                    ], width="4"
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
    Input("sex_violence_view_type", "value"),
    State("sex_violence_view_type", "options")
)
def plot_heat_map(view_type, opt):
    cases_df = dataloading.crime_df.copy()
    cases_df.loc[:, 'TIPO_DELITO'] = cases_df['TIPO_DELITO'].str.capitalize()
    if view_type != "AÑO":
        cases_df.loc[:, view_type] = cases_df[view_type].str.capitalize()

    cross_df = pd.crosstab(
        index=cases_df[cases_df["TIPO_DELITO"].isin(voi)]["TIPO_DELITO"],
        columns=cases_df[cases_df["TIPO_DELITO"].isin(voi)][view_type],
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
            hovertemplate=x_label[0] + ": %{x}<br>Tipo delito: %{y}<br>Porcentaje casos: %{z}<extra></extra>"
        ),
    )
    fig.update_xaxes(dtick="FECHA", ticklabelmode="period")
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f",
        xaxis=go.layout.XAxis(tickangle=45),
        paper_bgcolor="white",
    )
    return fig

@app.callback(
    Output("sexual-violence-map-plot", "figure"),
    Input("sex_violence_crime_type", "value"),
)
def map_plot(crime_type):
    print(crime_type)
    cases_df = dataloading.crime_df.copy()
    cases_df.loc[:, "TIPO_DELITO"] = cases_df["TIPO_DELITO"].str.capitalize()
    cases_df = cases_df[cases_df["TIPO_DELITO"] == crime_type]
    barrio_cn = cases_df.groupby(spunit_db)["CRIMEN_ID"].count().reset_index(name="Casos")
    fig = px.choropleth(
        barrio_cn,
        geojson=barrio_geojson,
        color="Casos",
        # color_continuous_scale=px.colors.sequential.Blues,
        color_continuous_scale=px.colors.sequential.Blues,
        locations=spunit_db, featureidkey="properties.NOMBRE",
        projection="mercator"
    )
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig