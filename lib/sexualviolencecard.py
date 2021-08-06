import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

sexualviolence_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Violencia sexual", className="card-title", style={"font-family": "revert", "color":"gray"}),
            dbc.Row(
                [
                    dbc.Col([
                        html.H3("3658", className="card-title", style={"font-family": "revert", "color": "#6c757d"})
                    ], width="7"),
                    dbc.Col([
                        html.Div(
                            html.I(className="fas fa-venus fa-2x", style={"padding-left": "11px", "color":"#0c5db3"}),
                            className="card-icon"
                        )
                    ], width="5")
                ],
            ),
            dbc.Row(
                [
                    # html.Img(src=app.get_asset_url('flecha_arriba_icon.svg'), style={"width": "15%", "padding-right":"3px"}),
                    html.Div([html.I(className="fas fa-arrow-up", style={'color': '#ce071a'}), html.Span('154', style={'color': 'red'})])
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