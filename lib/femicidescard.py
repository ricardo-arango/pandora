import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from lib import femicidesmodal
from app import app

femicides_card = dbc.Card(
    dbc.CardBody(
    [
        html.H6("Feminicidios", className="card-title", style={"font-family": "revert", "color":"gray"}),
        dbc.Row(
            [
                dbc.Col([
                    html.H3("5", className="card-title", style={"font-family": "revert", "color": "#6c757d"})
                ], width="7"),
                dbc.Col([
                    html.Div(
                        html.I(className="fas fa-female fa-2x", style={"padding-left": "11px", "color": "#0c5db3"}, title="Ver más..."),
                        className="card-icon", id="icon-div", n_clicks=0
                    )
                ], width="5")
            ],
        ),
        dbc.Row(
            [
                # html.Img(src=app.get_asset_url('flecha_arriba_icon.svg'), style={"width": "15%", "padding-right":"3px"}),
                html.Div([
                    html.I(className="fas fa-arrow-up", style={'color': '#ce071a'}),
                    html.Span('2', style={'color': 'red'}),
                    html.Span(' desde el mes pasado.', className="card-font")
                ])
            ], style={"padding-left": "15px"}
        ),
        femicidesmodal.femicides_modal
    ]),
    style={
        "width": "12rem",
        "height": "8rem",
        "margin": "5px"
    },
)


@app.callback(
    Output("modal", "is_open"),
    [Input("icon-div", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open