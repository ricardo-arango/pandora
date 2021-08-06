import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

deadlyinjury_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Lesiones fatales", className="card-title", style={"font-family": "revert", "color":"gray"}),
            dbc.Row(
                [
                    dbc.Col([
                        html.H3("1504", className="card-title", style={"font-family": "revert", "color": "#6c757d"})
                    ], width="7"),
                    dbc.Col([
                        html.Div(
                            html.I(className="fas fa-dizzy fa-2x", style={"padding": "1px 5px", "color": "#0c5db3"}),
                            className="card-icon"
                        )
                    ], width="5")
                ],
            ),
            dbc.Row(
                [
                    html.Div([html.I(className="fas fa-arrow-up", style={'color': '#ce071a'}), html.Span('59', style={'color': 'red'})])
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