import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

theftpeople_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Hurto a personas", className="card-title", style={"font-family": "revert", "color":"gray"}),
            dbc.Row(
                [
                    dbc.Col([
                        html.H3("6285", className="card-title", style={"font-family": "revert", "color": "#6c757d"})
                    ], width="7"),
                    dbc.Col([
                        html.Div(
                            html.I(className="fas fa-mask fa-2x", style={"color": "#0c5db3"}),
                            className="card-icon"
                    )
                    ], width="5")
                ],
            ),
            dbc.Row(
                [
                    html.Div([html.I(className="fas fa-arrow-up", style={'color': '#ce071a'}), html.Span('256', style={'color': 'red'})])
                ], style={"padding-left": "15px"}
            ),
        ]
    ),
    style={
        "width": "12rem",
        "height": "8rem",
        "margin": "5px"
    },
)