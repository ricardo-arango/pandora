import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

personalinjury_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Lesiones personales", className="card-title", style={"font-family": "revert", "color":"gray"}),
            dbc.Row(
                [
                    dbc.Col([
                        html.H3("7005", className="card-title", style={"font-family": "revert", "color": "#6c757d"})
                    ], width="7"),
                    dbc.Col([
                        html.Div(
                            html.I(className="fas fa-crutch fa-2x", style={"padding-left": "4px", "color": "#0c5db3"}),
                             className="card-icon")
                    ], width="5")
                ],
            ),
            dbc.Row(
                [
                    html.Div([html.I(className="fas fa-arrow-down", style={'color': '#52cc52'}), html.Span('314', style={'color': '#52cc52'})])
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