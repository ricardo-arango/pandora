import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
from dataloading import crime_df

def femicides_plot():
    tipo_delito_fem_df = crime_df[crime_df["TIPO_DELITO"] == "FEMINICIDIO"]
    tipo_delito_fem_df.loc[:, "TIPO_CONDUCTA"] = tipo_delito_fem_df["TIPO_CONDUCTA"].str.capitalize()
    tipo_delito_fem_df.loc[:, "GENERO_VICTIMA"] = tipo_delito_fem_df["GENERO_VICTIMA"].str.capitalize()
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

modal_instance = dbc.Modal(
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
                                dcc.Graph(id="someid", figure=femicides_plot())
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
                "Cerrar", id="femicides-close", className="ml-auto", n_clicks=0
            )
        ),
    ],
    id="femicides-modal",
    size="xl",
    is_open=False,
)