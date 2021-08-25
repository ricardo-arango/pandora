import dash_html_components as html
import dash_bootstrap_components as dbc

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink(children=[html.I(className="fas fa-tachometer-alt fa-2x"), html.H6("Dashboard")], href="/", active="exact", className="sidebar-icons"),
                dbc.NavLink(children=[html.I(className="fas fa-magic fa-2x"), html.H6("Predicciones")], href="/predictions", active="exact", className="sidebar-icons"),
                dbc.NavLink(children=[html.I(className="fas fa-tools fa-2x"), html.H6("Herramientas")], href="/tools", active="exact", className="sidebar-icons"),
                dbc.NavLink(children=[html.I(className="far fa-address-card fa-2x"), html.H6("Acerca de...")], href="/about", active="exact", className="sidebar-icons"),
                dbc.NavLink(html.Hr()),
            ],
            vertical=True,
            fill=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


