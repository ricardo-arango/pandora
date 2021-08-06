import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import pandas as pd

crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",")
crime_df["GRUPO_ETARIO_VICTIMA"] = crime_df["GRUPO_ETARIO_VICTIMA"].fillna("00. Sin Información")

def femicides_plot():
    tipo_delito_fem_df = crime_df[crime_df["TIPO_DELITO"] == "FEMINICIDIO"]
    tipo_delito_fem_df["TIPO_CONDUCTA"] = tipo_delito_fem_df["TIPO_CONDUCTA"].str.capitalize()
    tipo_delito_fem_df["GENERO_VICTIMA"] = tipo_delito_fem_df["GENERO_VICTIMA"].str.capitalize()
    tipo_conducta_df = tipo_delito_fem_df.groupby(["TIPO_CONDUCTA", "GENERO_VICTIMA"]).size().reset_index(name="Casos")

    fig = px.bar(
        tipo_conducta_df,
        x="TIPO_CONDUCTA",
        y="Casos",
        color="GENERO_VICTIMA",
        labels={"GENERO_VICTIMA": "Género víctima", "TIPO_CONDUCTA": "Tipo Conducta"}
    )
    fig.update_layout(
        font_family="revert",
        font_color="#5f5f5f"
    )
    return fig

femicides_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            html.H5("Feminicidios", style={"font-family": "revert", "color": "#5f5f5f"}
            )
        ),
        dbc.ModalBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div([
                                html.H5("Delitos relacionados con Feminicidios por tipo de conducta",
                                        className="card-title",
                                    style={"font-family": "revert", "color": "#5f5f5f", "padding": "10px 0 0 15px"}),
                                dcc.Graph(id="bar-plot-barrios", figure=femicides_plot())
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
                "Cerrar", id="close", className="ml-auto", n_clicks=0
            )
        ),
    ],
    id="modal",
    size="xl",
    is_open=False,
)