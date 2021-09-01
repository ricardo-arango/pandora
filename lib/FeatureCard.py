import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app


class FeatureCard:
    icon_id = ''

    def __init__(self, title, number_of_cases, cases_diff, increased, icon, icon_id, icon_padding, modal):
        self.title = title
        self.number_of_cases = number_of_cases
        self.cases_diff = cases_diff
        self.modal = modal
        self.icon = icon
        self.increased = increased
        self.icon_padding = icon_padding
        self.icon_id = icon_id
        FeatureCard.icon_id = icon_id
        if increased:
            self.arrow = "fas fa-arrow-up card_arrow_up"
            self.diff_class = "card_arrow_up"
        else:
            self.arrow = "fas fa-arrow-down card_arrow_down"
            self.diff_class = "card_arrow_down"

    def update_card(self, number_of_cases):
        self.number_of_cases = number_of_cases

    def create_card(self):
        card = dbc.Card(
            dbc.CardBody(
                [
                    html.H6(self.title, className="card-title", style={"font-family": "revert", "color": "gray"}),
                    dbc.Row(
                        [
                            dbc.Col([
                                html.H3(
                                    self.number_of_cases,
                                    className="card-title",
                                    style={"font-family": "revert", "color": "#6c757d"},
                                    id="number-cases-count")
                            ], width="7"),
                            dbc.Col([
                                dbc.Tooltip(
                                    "Ver más...",
                                    target=self.icon_id,
                                    placement="right"
                                ),
                                html.Div(
                                    html.I(
                                        className=self.icon,
                                        style={"padding": self.icon_padding, "color": "#0c5db3"},
                                        title="Ver más..."),
                                    className="card-icon", n_clicks=0,
                                    id=self.icon_id
                                )
                            ], width="5")
                        ],
                    ),
                    dbc.Row(
                        [
                            html.Div([
                                html.I(className=self.arrow),
                                html.Span(self.cases_diff, className=self.diff_class),
                                html.Span(' al mes pasado.', className="card-font")
                            ])
                        ], style={"padding-left": "15px"}
                    ),
                    self.modal
                ]
            ),
            style={
                "width": "12rem",
                "height": "8rem",
                "margin": "5px"
            }
        )
        return card


@app.callback(
    Output("femicides-modal", "is_open"),
    [
        Input("female", "n_clicks"),
        Input("femicides-close", "n_clicks")
    ],
    [State("femicides-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_femicides_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open

@app.callback(
    Output("nondeadlyinjuries-modal", "is_open"),
    [
        Input("user-injured", "n_clicks"),
        Input("nondeadlyinjuries-close", "n_clicks")
    ],
    State("nondeadlyinjuries-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_nondeadlyinjuries_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open

@app.callback(
    Output("domesticviolence-modal", "is_open"),
    [
        Input("house-user", "n_clicks"),
        Input("domesticviolence-close", "n_clicks")
    ],
    [State("domesticviolence-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_sexharassment_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open

@app.callback(
    Output("deadlyinjuries-modal", "is_open"),
    [
        Input("dizzy", "n_clicks"),
        Input("deadlyinjuries-close", "n_clicks")
    ],
    State("deadlyinjuries-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_deadlyinjuries_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open

@app.callback(
    Output("homicide-modal", "is_open"),
    [
        Input("skull", "n_clicks"),
        Input("homicide-close", "n_clicks")
    ],
    [State("homicide-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_homicide_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open

@app.callback(
    Output("personalinjury-modal", "is_open"),
    [
        Input("crutch", "n_clicks"),
        Input("personalinjury-close", "n_clicks")
    ],
    State("personalinjury-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_personalinjury_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open

@app.callback(
    Output("sexviolence-modal", "is_open"),
    [
        Input("venus", "n_clicks"),
        Input("sexviolence-close", "n_clicks")
    ],
    [State("sexviolence-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_sexviolence_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open

@app.callback(
    Output("theftpeople-modal", "is_open"),
    [
        Input("mask", "n_clicks"),
        Input("theftpeople-close", "n_clicks")
    ],
    State("theftpeople-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_theftpeople_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open

@app.callback(
    Output("theftresidence-modal", "is_open"),
    [
        Input("house-damage", "n_clicks"),
        Input("theftresidence-close", "n_clicks")
    ],
    [State("theftresidence-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_theftresidence_modal(n1, n2, is_open):
    if n1 > 0 or n2 > 0:
        return not is_open
    return is_open
