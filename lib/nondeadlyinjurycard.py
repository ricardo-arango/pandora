import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

nondeadlyinjury_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Lesiones no fatales", className="card-title", style={"font-family": "revert", "color":"gray"}),
            dbc.Row(
                [
                    dbc.Col([
                        html.H3("635", className="card-title", style={"font-family": "revert", "color": "#6c757d"})
                    ], width="7"),
                    dbc.Col([
                        html.Div(
                            html.I(className="fas fa-user-injured fa-2x", style={"padding-left": "6px", "color":"#0c5db3"}),
                             className="card-icon"
                        )
                    ], width="5")
                ],
            ),
            dbc.Row(
                [
                    # html.Img(src=app.get_asset_url('flecha_abajo_icon.svg'), style={"width": "15%", "padding-right":"3px"}),
                    html.Div([html.I(className="fas fa-arrow-down", style={'color': '#52cc52'}), html.Span('145', style={'color': '#52cc52'})])
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