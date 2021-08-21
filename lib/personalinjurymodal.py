import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

modal_instance = dbc.Modal(
    [
        dbc.ModalHeader(
            html.H5("Lesiones personales", style={"font-family": "revert", "color": "#5f5f5f"}
            )
        ),
        dbc.ModalBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div([
                                html.H5("Acá va la información...",
                                        className="card-title",
                                    style={"font-family": "revert", "color": "#5f5f5f", "padding": "10px 0 0 15px"}),
                                dcc.Graph(id="bar-plot-barrios")
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
                "Cerrar", id="personalinjury-close", className="ml-auto", n_clicks=0
            )
        ),
    ],
    id="personalinjury-modal",
    size="xl",
    is_open=False,
)
