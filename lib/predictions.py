import dash_html_components as html
import dash_bootstrap_components as dbc
from dataloading import crime_df

predictions_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("Predicciones", className="card-title panel-title"),
                                html.Hr()
                        ])
                    ], width=12,
                ),
            ]
        ),
    ],
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)

